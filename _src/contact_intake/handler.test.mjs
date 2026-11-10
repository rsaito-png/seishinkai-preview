import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { mkdtemp, readFile, rm, writeFile, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createMemoryStore } from "./memory_store.mjs";
import { acceptIntake, handleRequest } from "../../supabase/functions/site-contact-intake/handler.mjs";
import { SERVICES, shouldCountLead } from "../../supabase/functions/site-contact-intake/shared.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

function key(n) {
  return `00000000-0000-4000-8000-${n.toString(16).padStart(12, "0")}`;
}

function payload(n, extra = {}) {
  return {
    service: "決まっていない",
    name: "山田太郎",
    email: extra.email || "taro@example.com",
    body: extra.body || "要点です。" + n,
    idempotency_key: extra.idempotency_key || key(n),
    opened_at: Date.now() - 10_000,
    company_url: "",
    ...extra,
  };
}

async function accept(store, input, extra = {}) {
  const result = await acceptIntake(input, {
    now: Date.now(),
    INTAKE_DEPLOY_ENABLED: true,
    store,
    suppressLead: extra.suppressLead === true,
  });
  return { result };
}

test("saved inquiry is counted once and is not emailed", async () => {
  const store = createMemoryStore();
  const { result } = await accept(store, payload(1, { body: "見学したいです。家族の相談です。" }));
  assert.equal(result.status, 200);
  assert.equal(result.body.stored, true);
  assert.equal(result.body.lead_event, true);
  assert.equal(result.body.duplicate, false);
  assert.equal(result.body.notified, undefined);
  assert.equal(JSON.stringify(result.body).includes("taro@example.com"), false);
  assert.equal(JSON.stringify(result.body).includes("山田太郎"), false);
  assert.equal(store.rows.length, 1);
  assert.equal(store.rows[0].lane, "normal");
  assert.equal(shouldCountLead(result.body), true);
});

test("persistence failure stores nothing and sends nothing", async () => {
  const store = createMemoryStore();
  store.transaction = async () => {
    const error = new Error("down");
    error.code = "persist";
    throw error;
  };
  const { result } = await accept(store, payload(3));
  assert.equal(result.status, 500);
  assert.equal(result.body.stored, false);
  assert.equal(result.body.lead_event, false);
  assert.equal(result.body.code, "persist");
  assert.equal(shouldCountLead(result.body), false);
});

test("validation, injection, honeypot, and timing do not store or count", async () => {
  const store = createMemoryStore();
  const cases = [
    payload(4, { name: "" }),
    payload(5, { email: "not-an-email" }),
    payload(6, { name: "山田\r\nBcc: evil@example.com" }),
    payload(7, { body: "あ".repeat(2001) }),
    payload(8, { service: "存在しない事業" }),
    payload(9, { company_url: "https://spam.example" }),
    payload(10, { opened_at: Date.now() }),
    payload(11, { idempotency_key: "not-a-uuid" }),
  ];
  for (const input of cases) {
    const { result } = await accept(store, input);
    assert.equal(result.body.stored, false);
    assert.equal(result.body.lead_event, false);
    assert.equal(shouldCountLead(result.body), false);
  }
  assert.equal(store.rows.length, 0);
});

test("same idempotency key or same content does not create another lead or email", async () => {
  const store = createMemoryStore();
  const first = await accept(store, payload(12, { body: "同じ内容" }));
  const replay = await accept(store, payload(12, { body: "同じ内容" }));
  const duplicate = await accept(store, payload(13, { body: "同じ内容", email: "taro@example.com" }));
  assert.equal(first.result.body.lead_event, true);
  assert.equal(replay.result.body.duplicate, true);
  assert.equal(replay.result.body.lead_event, false);
  assert.equal(duplicate.result.body.duplicate, true);
  assert.equal(duplicate.result.body.lead_event, false);
  assert.equal(shouldCountLead(replay.result.body), false);
  assert.equal(shouldCountLead(duplicate.result.body), false);
  assert.equal(store.rows.length, 1);
});

test("rate limits hold for one mailbox and the whole site, not a forwarded IP", async () => {
  const store = createMemoryStore();
  for (let i = 0; i < 5; i++) {
    const { result } = await accept(store, payload(40 + i, { email: "same@example.com", body: "box " + i }));
    assert.equal(result.status, 200);
  }
  const box = await accept(store, payload(49, { email: "same@example.com", body: "box last" }));
  assert.equal(box.result.status, 429);
  assert.equal(shouldCountLead(box.result.body), false);

  const globalStore = createMemoryStore();
  for (let i = 0; i < 30; i++) {
    const { result } = await accept(globalStore, payload(100 + i, { email: `g${i}@example.com`, body: "all " + i }));
    assert.equal(result.status, 200);
  }
  const globalBlock = await accept(globalStore, payload(140, { email: "g-extra@example.com", body: "all extra" }));
  assert.equal(globalBlock.result.status, 429);
  assert.equal(globalBlock.result.body.stored, false);
});

test("parallel requests cannot pass the mailbox limit", async () => {
  const store = createMemoryStore();
  const results = await Promise.all(Array.from({ length: 8 }, (_, i) =>
    accept(store, payload(60 + i, { email: "same-parallel@example.com", body: "conc " + i }))));
  const saved = results.filter((item) => item.result.body.stored);
  const limited = results.filter((item) => item.result.status === 429);
  assert.equal(saved.length, 5);
  assert.equal(limited.length, 3);
  assert.equal(saved.filter((item) => item.result.body.lead_event).length, 5);
  assert.equal(store.rows.length, 5);
});

test("forwarded IP headers do not reset the mailbox limit", async () => {
  const store = createMemoryStore();
  const env = { INTAKE_DEPLOY_ENABLED: true };
  const seen = [];
  const fetchImpl = async (url) => {
    seen.push(String(url));
    return { ok: true, status: 200 };
  };
  async function post(n, headers, extra = {}) {
    const input = payload(70 + n, { email: "one@example.com", body: "hdr " + n, ip: "1.2.3.4", ip_hash: "nope", suppressLead: true, test: true, ...extra });
    return handleRequest(new Request("https://psr-seishinkai.org/functions/v1/site-contact-intake", {
      method: "POST",
      headers: { "content-type": "application/json", origin: "https://psr-seishinkai.org", ...headers },
      body: JSON.stringify(input),
    }), { env, fetch: fetchImpl, store });
  }
  for (let i = 0; i < 5; i++) {
    const response = await post(i, { "x-forwarded-for": "1.1.1.1, 203.0.113.50", "x-client-ip": "8.8.8." + i });
    assert.equal(response.status, 200);
    assert.equal((await response.clone().json()).lead_event, true);
  }
  const blocked = await post(5, { "x-forwarded-for": "9.9.9.9, 203.0.113.50", "x-client-ip": "4.4.4.4" });
  assert.equal(blocked.status, 429);
  const body = await blocked.json();
  assert.equal(body.lead_event, false);
  assert.equal(body.stored, false);
  assert.equal(seen.length, 0);
  assert.equal(JSON.stringify(body).includes("@"), false);
});

test("disabled intake returns 503 and does not store, classify, or count", async () => {
  const store = createMemoryStore();
  let used = false;
  store.transaction = async () => { used = true; throw new Error("store called"); };
  const sales = payload(90, { body: "株式会社サンプルの営業です。SEO対策のご提案をさせてください。資料を送付させていただきます。" });
  for (const flag of [undefined, "", "false", "1", "TRUE", "True", " true"]) {
    const env = {};
    if (flag !== undefined) env.CONTACT_INTAKE_ENABLED = flag;
    const response = await handleRequest(new Request("https://psr-seishinkai.org/functions/v1/site-contact-intake", {
      method: "POST",
      headers: { "content-type": "application/json", "x-forwarded-for": "203.0.113.10" },
      body: JSON.stringify(sales),
    }), { env, fetch: async () => { throw new Error("fetch"); }, store });
    const body = await response.json();
    assert.equal(response.status, 503, String(flag));
    assert.equal(body.code, "not_configured");
    assert.equal(body.stored, false);
    assert.equal(body.lead_event, false);
    assert.equal(shouldCountLead(body), false);
  }
  assert.equal(used, false);
  assert.equal(store.rows.length, 0);
});

test("deploy switch opens invalid requests and emergency false stays closed", async () => {
  const store = createMemoryStore();
  let used = false;
  const original = store.transaction.bind(store);
  store.transaction = async (...args) => {
    used = true;
    return original(...args);
  };
  const invalid = payload(91, { email: "not-an-email" });
  const opened = await handleRequest(new Request("https://psr-seishinkai.org/functions/v1/site-contact-intake", {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://psr-seishinkai.org" },
    body: JSON.stringify(invalid),
  }), { env: { INTAKE_DEPLOY_ENABLED: true, CONTACT_INTAKE_ENABLED: "TRUE" }, fetch: async () => { throw new Error("fetch"); }, store });
  const openedBody = await opened.json();
  assert.equal(opened.status, 400);
  assert.equal(openedBody.stored, false);
  assert.equal(openedBody.lead_event, false);
  assert.equal(used, false);

  for (const env of [
    { INTAKE_DEPLOY_ENABLED: true, CONTACT_INTAKE_ENABLED: "false" },
    { INTAKE_DEPLOY_ENABLED: false, CONTACT_INTAKE_ENABLED: "true" },
    { INTAKE_DEPLOY_ENABLED: "true", CONTACT_INTAKE_ENABLED: "true" },
  ]) {
    const response = await handleRequest(new Request("https://psr-seishinkai.org/functions/v1/site-contact-intake", {
      method: "POST",
      headers: { "content-type": "application/json", origin: "https://psr-seishinkai.org" },
      body: JSON.stringify(payload(92)),
    }), { env, fetch: async () => { throw new Error("fetch"); }, store });
    const body = await response.json();
    assert.equal(response.status, 503);
    assert.equal(body.code, "not_configured");
    assert.equal(body.stored, false);
  }
  assert.equal(store.rows.length, 0);
});

test("missing store, bad origin, and mock mode do not count", async () => {
  let called = false;
  const off = await handleRequest(new Request("https://example.test/", {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://psr-seishinkai.org" },
    body: JSON.stringify(payload(80)),
  }), { env: {}, fetch: async () => { called = true; return { ok: true }; }, store: null });
  assert.equal(off.status, 503);
  assert.equal((await off.json()).lead_event, false);
  assert.equal(called, false);

  const store = createMemoryStore();
  const evil = await handleRequest(new Request("https://example.test/", {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://evil.example" },
    body: JSON.stringify(payload(81)),
  }), { env: { INTAKE_DEPLOY_ENABLED: true }, fetch: async () => { called = true; return { ok: true }; }, store });
  assert.equal(evil.status, 403);
  assert.equal(called, false);
  assert.equal(store.rows.length, 0);

  const mocked = await accept(store, payload(82), { suppressLead: true });
  assert.equal(mocked.result.body.stored, true);
  assert.equal(mocked.result.body.test, true);
  assert.equal(mocked.result.body.lead_event, false);
  assert.equal(shouldCountLead(mocked.result.body), false);
});

test("public inbox wrappers are invoker and private owner checks stay definer", () => {
  const sql = readFileSync(path.join(root, "supabase/functions/site-contact-intake/schema.sql"), "utf8");
  const publicFns = sql.split(/create or replace function public\./).slice(1);
  assert.equal(publicFns.length, 5);
  for (const fn of publicFns) {
    assert.match(fn, /security invoker/);
    assert.equal(/security definer/.test(fn.split(/create or replace function /)[0]), false);
  }
  assert.match(sql, /function site_contact\.is_owner\(\)[\s\S]*security definer/);
  assert.match(sql, /revoke all on table site_contact\.inquiries from public, anon, authenticated/);
});

test("public page keeps the form disabled and does not treat form_submit as a lead", () => {
  const html = readFileSync(path.join(root, "contact/index.html"), "utf8");
  const config = readFileSync(path.join(root, "assets/contact-config.js"), "utf8");
  const browser = readFileSync(path.join(root, "assets/contact-intake.mjs"), "utf8");
  assert.equal(html.includes('href="#line"'), false);
  assert.equal(html.includes('id="line"'), true);
  assert.equal(html.includes("https://line.me/R/ti/p/@279qxcql"), true);
  assert.equal(html.includes("@279qxcql"), true);
  assert.equal(html.includes("星心会 公式LINE"), true);
  assert.equal(html.includes("確認できるまで掲載していません"), false);
  assert.equal(html.includes("公式LINEのURLは公開していません"), false);
  assert.equal(html.includes('id="contact-intake"'), true);
  assert.equal(html.includes('type="submit" disabled'), true);
  assert.equal(html.includes("supabase.co"), false);
  assert.equal(html.includes("gtag('event', 'form_submit'"), false);
  assert.equal(html.includes("contact-intake-submit"), true);
  assert.equal(html.includes("送信は停止しています"), true);
  assert.equal(html.includes("東京のデータベースに保存します"), true);
  assert.equal(html.includes("国外で行われる可能性があります"), true);
  assert.equal(html.includes("通知メールや自動返信はありません"), true);
  assert.equal(html.includes("国内で処理"), false);
  assert.equal(html.includes("自動返信します"), false);
  assert.match(config, /enabled:\s*true/);
  assert.match(config, /endpoint:\s*"https:\/\/zvrardoyxocmqhvyddnf\.supabase\.co\/functions\/v1\/site-contact-intake"/);
  assert.equal(browser.includes("contact_inquiry_accepted"), true);
  assert.match(browser, /gtag\("event", "contact_inquiry_accepted", globalThis\.inquiryAcceptedParams\(location\.pathname\)\)/);
  assert.equal(html.includes("要確認：受付日・時間"), false);
  assert.equal(browser.includes("form_submit"), false);
  assert.equal(browser.includes("メールでお知らせ"), false);
  assert.equal(browser.includes("通知メールは送りません"), true);
  assert.equal(browser.includes("国外で行われる可能性があります"), true);
  assert.equal(browser.includes("国内で処理"), false);
  const options = [...html.matchAll(/<option>([^<]*)<\/option>/g)].map((m) => m[1]);
  assert.deepEqual(options, SERVICES);
});

test("content rebuild preserves a hand-edited contact page and can still generate a safe one", async () => {
  const dir = await mkdtemp(path.join(tmpdir(), "contact-build-"));
  const preserved = path.join(dir, "contact");
  await mkdir(preserved);
  const marker = "<!doctype html><title>HAND</title><p>hand-edited-contact</p>";
  await writeFile(path.join(preserved, "index.html"), marker);
  await runBuild(dir);
  assert.equal(await readFile(path.join(preserved, "index.html"), "utf8"), marker);
  await rm(preserved, { recursive: true });
  await runBuild(dir);
  const generated = await readFile(path.join(preserved, "index.html"), "utf8");
  assert.equal(generated.includes("hand-edited-contact"), false);
  assert.equal(generated.includes('id="contact-intake"'), true);
  assert.equal(generated.includes('href="#line"'), false);
  assert.equal(generated.includes("https://line.me/R/ti/p/@279qxcql"), true);
  assert.equal(generated.includes("@279qxcql"), true);
  assert.equal(generated.includes("星心会 公式LINE"), true);
  assert.equal(generated.includes("確認できるまで掲載していません"), false);
  assert.equal(generated.includes("公式LINEのURLは公開していません"), false);
  assert.equal(generated.includes("type=\"submit\" disabled"), true);
  assert.equal(generated.includes("contact-intake-submit"), true);
  assert.equal(generated.includes("contact-config.js"), true);
  assert.equal(generated.includes("通知メールや自動返信はありません"), true);
  assert.equal(generated.includes("国内で処理"), false);
  assert.equal(generated.includes("要確認：受付日・時間"), false);
  await rm(dir, { recursive: true });
});

function runBuild(out) {
  return new Promise((resolve, reject) => {
    const child = spawn("python3", ["_src/build.py"], {
      cwd: root,
      env: { ...process.env, OUT: out, CONTENT: path.join(root, "content") },
    });
    let err = "";
    child.stderr.on("data", (chunk) => { err += chunk; });
    child.on("close", (code) => code === 0 ? resolve() : reject(new Error(err || "build exit " + code)));
  });
}
