import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { mkdtemp, readFile, rm, writeFile, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createMemoryStore } from "./memory_store.mjs";
import { acceptIntake, handleRequest, retryNotifications } from "../../supabase/functions/site-contact-intake/handler.mjs";
import { RECIPIENT, SUBJECT, buildNotice, createMailer } from "../../supabase/functions/site-contact-intake/notice.mjs";
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

function mailOk() {
  const sent = [];
  return {
    sent,
    async send(message) {
      sent.push(message);
    },
  };
}

async function accept(store, input, extra = {}) {
  const mail = extra.mail || mailOk();
  const result = await acceptIntake(input, {
    now: Date.now(),
    ip: extra.ip || "203.0.113.10",
    pepper: "test-pepper",
    mailer: extra.mailer || mail.send,
    store,
    suppressLead: extra.suppressLead === true,
  });
  return { result, mail };
}

test("saved inquiry is notified once and counted once", async () => {
  const store = createMemoryStore();
  const { result, mail } = await accept(store, payload(1, { body: "要点です。" }));
  assert.equal(result.status, 200);
  assert.equal(result.body.stored, true);
  assert.equal(result.body.notified, true);
  assert.equal(result.body.notification, "sent");
  assert.equal(result.body.lead_event, true);
  assert.equal(result.body.duplicate, false);
  assert.equal(result.body.test, false);
  assert.equal(mail.sent.length, 1);
  assert.equal(mail.sent[0].to, RECIPIENT);
  assert.equal(mail.sent[0].subject, SUBJECT);
  assert.equal(mail.sent[0].text.includes("Bcc:"), false);
  assert.equal(mail.sent[0].text.includes("山田太郎"), true);
  assert.equal(mail.sent[0].text.includes("taro@example.com"), true);
  assert.equal(mail.sent[0].text.includes("要点です。"), true);
  assert.equal(JSON.stringify(result.body).includes("taro@example.com"), false);
  assert.equal(JSON.stringify(result.body).includes("山田太郎"), false);
  assert.equal(store.rows.length, 1);
  assert.equal(store.rows[0].notification_status, "sent");
  assert.equal(shouldCountLead(result.body), true);
  assert.equal(store.rows[0].email, "taro@example.com");
});

test("notice text is fixed and cannot add a header", () => {
  const text = buildNotice({
    id: "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
    created_at: "2026-11-07T00:00:00.000Z",
    service: "決まっていない",
    name: "山田太郎",
    email: "taro@example.com",
    body: "要点です。",
  }).text;
  assert.equal(text, [
    "星心会ウェブサイトの相談フォームから新しい問い合わせです。",
    "このメールは受付通知です。送信者への自動返信ではありません。",
    "",
    "受付番号: aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
    "受付時刻: 2026-11-07T00:00:00.000Z",
    "相談したい事業: 決まっていない",
    "お名前: 山田太郎",
    "メールアドレス: taro@example.com",
    "",
    "内容:",
    "要点です。",
    "",
    "返信は、上のメールアドレスへ直接お願いします。",
  ].join("\n"));
  assert.throws(() => buildNotice({
    id: "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
    created_at: "2026-11-07T00:00:00.000Z",
    service: "決まっていない",
    name: "山田\r\nBcc: evil@example.com",
    email: "taro@example.com",
    body: "要点です。",
  }), /header_rejected/);
});

test("persisted inquiry stays retryable when notification fails and is not counted twice", async () => {
  const store = createMemoryStore();
  let calls = 0;
  const mailer = async (message) => {
    calls += 1;
    if (calls === 1) {
      const error = new Error("mail_http_502");
      error.code = "mail_http_502";
      throw error;
    }
    assert.equal(message.to, RECIPIENT);
  };
  const first = await accept(store, payload(2), { mailer });
  assert.equal(first.result.body.stored, true);
  assert.equal(first.result.body.notified, false);
  assert.equal(first.result.body.notification, "failed");
  assert.equal(first.result.body.lead_event, true);
  assert.equal(shouldCountLead(first.result.body), true);
  assert.equal(store.rows[0].notification_status, "failed");
  assert.equal(store.rows[0].notification_error, "mail_http_502");
  const retry = await retryNotifications({ mailer, store });
  assert.equal(retry.status, 200);
  assert.equal(retry.body.lead_event, false);
  assert.equal(retry.body.results[0].lead_event, false);
  assert.equal(retry.body.results[0].notification, "sent");
  assert.equal(shouldCountLead(retry.body), false);
  assert.equal(store.rows[0].notification_status, "sent");
  assert.equal(calls, 2);
  assert.equal(store.rows.length, 1);
});

test("persistence failure stores nothing and sends nothing", async () => {
  const store = createMemoryStore();
  store.transaction = async () => {
    const error = new Error("down");
    error.code = "persist";
    throw error;
  };
  const mail = mailOk();
  const { result } = await accept(store, payload(3), { mail });
  assert.equal(result.status, 500);
  assert.equal(result.body.stored, false);
  assert.equal(result.body.lead_event, false);
  assert.equal(result.body.code, "persist");
  assert.equal(mail.sent.length, 0);
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
    const { result, mail } = await accept(store, input);
    assert.equal(result.body.stored, false);
    assert.equal(result.body.lead_event, false);
    assert.equal(shouldCountLead(result.body), false);
    assert.equal(mail.sent.length, 0);
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
  assert.equal(first.mail.sent.length + replay.mail.sent.length + duplicate.mail.sent.length, 1);
});

test("rate limits hold for one address, one mailbox, and the whole site", async () => {
  const store = createMemoryStore();
  for (let i = 0; i < 5; i++) {
    const { result } = await accept(store, payload(20 + i, { email: `p${i}@example.com`, body: "ip " + i }), { ip: "203.0.113.20" });
    assert.equal(result.status, 200, result.body.code);
  }
  const blocked = await accept(store, payload(30, { email: "fresh@example.com", body: "ip blocked" }), { ip: "203.0.113.20" });
  assert.equal(blocked.result.status, 429);
  assert.equal(blocked.result.body.lead_event, false);
  assert.equal(blocked.mail.sent.length, 0);
  const otherIp = await accept(store, payload(31, { email: "other@example.com", body: "other ip" }), { ip: "203.0.113.21" });
  assert.equal(otherIp.result.status, 200);

  for (let i = 0; i < 5; i++) {
    const { result } = await accept(store, payload(40 + i, { email: "same@example.com", body: "box " + i }), { ip: "198.51.100." + i });
    assert.equal(result.status, 200);
  }
  const box = await accept(store, payload(49, { email: "same@example.com", body: "box last" }), { ip: "198.51.100.99" });
  assert.equal(box.result.status, 429);
  assert.equal(shouldCountLead(box.result.body), false);

  const globalStore = createMemoryStore();
  for (let i = 0; i < 30; i++) {
    const { result } = await accept(globalStore, payload(100 + i, { email: `g${i}@example.com`, body: "all " + i }), { ip: "192.0.2." + i });
    assert.equal(result.status, 200);
  }
  const globalBlock = await accept(globalStore, payload(140, { email: "g-extra@example.com", body: "all extra" }), { ip: "192.0.2.200" });
  assert.equal(globalBlock.result.status, 429);
  assert.equal(globalBlock.result.body.stored, false);
});

test("parallel requests cannot pass the address limit", async () => {
  const store = createMemoryStore();
  const results = await Promise.all(Array.from({ length: 8 }, (_, i) =>
    accept(store, payload(60 + i, { email: `c${i}@example.com`, body: "conc " + i }), { ip: "203.0.113.40" })));
  const saved = results.filter((item) => item.result.body.stored);
  const limited = results.filter((item) => item.result.status === 429);
  assert.equal(saved.length, 5);
  assert.equal(limited.length, 3);
  assert.equal(saved.filter((item) => item.result.body.lead_event).length, 5);
  assert.equal(store.rows.length, 5);
});

test("client-supplied address fields do not reset the server rate bucket", async () => {
  const store = createMemoryStore();
  const env = {
    CONTACT_INTAKE_ENABLED: "1",
    CONTACT_MAIL_TRANSPORT: "https-json",
    CONTACT_MAIL_URL: "https://mail.example.test/send",
    CONTACT_MAIL_TOKEN: "test-token",
    CONTACT_MAIL_FROM: "sender@example.com",
    CONTACT_IP_PEPPER: "pepper",
  };
  const seen = [];
  const fetchImpl = async (url, init) => {
    seen.push({ url, body: JSON.parse(init.body), authorization: init.headers.authorization });
    return { ok: true, status: 200 };
  };
  async function post(n, headers, extra = {}) {
    const input = payload(70 + n, { email: `h${n}@example.com`, body: "hdr " + n, ip: "1.2.3.4", ip_hash: "nope", suppressLead: true, test: true, ...extra });
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
  assert.equal(seen.length, 5);
  assert.equal(seen[0].body.to, RECIPIENT);
  assert.equal(seen[0].body.from, "sender@example.com");
  assert.equal(seen[0].body.subject, SUBJECT);
  assert.equal(Object.keys(seen[0].body).sort().join(), "from,subject,text,to");
  assert.equal(seen[0].body.text.includes("taro@example.com"), false);
  assert.equal(seen[0].body.text.includes("h0@example.com"), true);
  assert.equal(JSON.stringify(body).includes("test-token"), false);
});

test("unconfigured transport, bad origin, and mock mode do not count", async () => {
  const store = createMemoryStore();
  let called = false;
  const off = await handleRequest(new Request("https://example.test/", {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://psr-seishinkai.org" },
    body: JSON.stringify(payload(80)),
  }), { env: {}, fetch: async () => { called = true; return { ok: true }; }, store });
  assert.equal(off.status, 503);
  assert.equal((await off.json()).lead_event, false);
  assert.equal(called, false);
  assert.equal(store.rows.length, 0);

  const evil = await handleRequest(new Request("https://example.test/", {
    method: "POST",
    headers: { "content-type": "application/json", origin: "https://evil.example" },
    body: JSON.stringify(payload(81)),
  }), {
    env: { CONTACT_INTAKE_ENABLED: "1", CONTACT_MAIL_TRANSPORT: "https-json", CONTACT_MAIL_URL: "https://mail.example.test/send", CONTACT_MAIL_TOKEN: "t", CONTACT_MAIL_FROM: "sender@example.com" },
    fetch: async () => { called = true; return { ok: true }; },
    store,
  });
  assert.equal(evil.status, 403);
  assert.equal(called, false);

  const mocked = await accept(store, payload(82), { suppressLead: true });
  assert.equal(mocked.result.body.stored, true);
  assert.equal(mocked.result.body.test, true);
  assert.equal(mocked.result.body.lead_event, false);
  assert.equal(shouldCountLead(mocked.result.body), false);
  assert.equal((await retryNotifications({ mailer: async () => { throw new Error("should not send"); }, store })).body.results.length, 0);
  assert.equal(createMailer({ CONTACT_INTAKE_ENABLED: "1" }, async () => ({ ok: true })), null);
  assert.equal(createMailer({ CONTACT_INTAKE_ENABLED: "1", CONTACT_MAIL_TRANSPORT: "https-json", CONTACT_MAIL_URL: "https://mail.example.test/send", CONTACT_MAIL_TOKEN: "t", CONTACT_MAIL_FROM: "bad\nfrom@example.com" }, async () => ({ ok: true })), null);
});

test("public page keeps the form disabled and does not treat form_submit as a lead", () => {
  const html = readFileSync(path.join(root, "contact/index.html"), "utf8");
  const config = readFileSync(path.join(root, "assets/contact-config.js"), "utf8");
  const browser = readFileSync(path.join(root, "assets/contact-intake.mjs"), "utf8");
  assert.equal(html.includes('href="#line"'), false);
  assert.equal(html.includes('id="line"'), true);
  assert.equal(html.includes('id="contact-intake"'), true);
  assert.equal(html.includes('type="submit" disabled'), true);
  assert.equal(html.includes("supabase.co"), false);
  assert.equal(html.includes("gtag('event', 'form_submit'"), false);
  assert.equal(html.includes("contact-intake-submit"), true);
  assert.equal(html.includes("送信は停止しています"), true);
  assert.match(config, /enabled:\s*false/);
  assert.match(config, /endpoint:\s*""/);
  assert.equal(browser.includes("contact_inquiry_accepted"), true);
  assert.equal(browser.includes("form_submit"), false);
  assert.equal(browser.includes(RECIPIENT), false);
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
  assert.equal(generated.includes("type=\"submit\" disabled"), true);
  assert.equal(generated.includes("contact-intake-submit"), true);
  assert.equal(generated.includes("contact-config.js"), true);
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
