import assert from "node:assert/strict";
import test from "node:test";
import { classifyInquiry, markRead, restoreInquiry, unreadCount } from "../../supabase/functions/site-contact-intake/classify.mjs";
import { acceptIntake } from "../../supabase/functions/site-contact-intake/handler.mjs";
import { shouldCountLead } from "../../supabase/functions/site-contact-intake/shared.mjs";
import { createMemoryStore } from "./memory_store.mjs";

function row(partial) {
  return {
    id: partial.id,
    lane: "normal",
    review: "clear",
    sales_reason: null,
    read_at: null,
    test: false,
    ...partial,
  };
}

test("clear sales pitch is quarantined and is not an unread lead", async () => {
  const text = "株式会社サンプルの営業です。SEO対策のご提案をさせてください。資料を送付させていただきます。";
  const screen = classifyInquiry({ service: "決まっていない", name: "営業担当", body: text });
  assert.equal(screen.lane, "sales");
  assert.match(screen.sales_reason, /営業/);
  const store = createMemoryStore();
  const result = await acceptIntake({
    service: "決まっていない",
    name: "営業担当",
    email: "sales@example.com",
    body: text,
    idempotency_key: "00000000-0000-4000-8000-0000000000a1",
    opened_at: Date.now() - 10_000,
    company_url: "",
  }, { now: Date.now(), INTAKE_DEPLOY_ENABLED: true, store, suppressLead: false });
  assert.equal(result.body.stored, true);
  assert.equal(result.body.lead_event, false);
  assert.equal(shouldCountLead(result.body), false);
  assert.equal(store.rows[0].lane, "sales");
  assert.equal(unreadCount(store.rows), 0);
});

test("welfare referral and collaboration stay in the normal inbox", () => {
  const samples = [
    "病院の相談員です。障害のある方をご紹介したいです。連携をお願いします。",
    "株式会社あさひ福祉会です。就労の空きと見学について相談したいです。",
    "ハローワークから、水晶玉の利用についてご紹介いただきました。",
  ];
  for (const body of samples) {
    const screen = classifyInquiry({ service: "決まっていない", name: "相談員", body });
    assert.equal(screen.lane, "normal", body);
    assert.equal(screen.review === "clear" || screen.review === "needs-review", true, body);
  }
});

test("ambiguous company wording stays visible and is not quarantined", () => {
  const screen = classifyInquiry({
    service: "決まっていない",
    name: "佐藤",
    body: "株式会社リーフの者です。ご提案があるので、一度お時間をいただけますか。",
  });
  assert.equal(screen.lane, "normal");
  assert.equal(screen.review, "needs-review");
  assert.match(screen.sales_reason, /通常の受信に残しました/);
});

test("restore returns a pitch to the unread normal inbox and strangers cannot do it", () => {
  const rows = [row({ id: "s1", lane: "sales", sales_reason: "業者の営業と判断しました：営業の連絡・提案" })];
  assert.throws(() => restoreInquiry(rows, { owner: false }, "s1"), /forbidden/);
  assert.throws(() => markRead(rows, null, "s1"), /forbidden/);
  assert.equal(unreadCount(rows), 0);
  const restored = restoreInquiry(rows, { owner: true }, "s1");
  assert.equal(restored.lane, "normal");
  assert.equal(restored.review, "restored");
  assert.equal(restored.sales_reason.includes("営業"), true);
  assert.equal(unreadCount(rows), 1);
  markRead(rows, { owner: true }, "s1");
  assert.equal(unreadCount(rows), 0);
  const again = restoreInquiry(rows, { owner: true }, "s1");
  assert.equal(again.review, "restored");
  assert.equal(unreadCount(rows), 0);
});

test("concurrent restores leave one normal unread row", async () => {
  const rows = [row({ id: "s2", lane: "sales", sales_reason: "業者の営業と判断しました：売り込み・テレアポ" })];
  let chain = Promise.resolve();
  function locked(fn) {
    const run = chain.then(fn, fn);
    chain = run.then(() => {}, () => {});
    return run;
  }
  const results = await Promise.all([0, 1, 2].map(() => locked(() => restoreInquiry(rows, { owner: true }, "s2"))));
  assert.equal(results.every((item) => item.lane === "normal"), true);
  assert.equal(rows.length, 1);
  assert.equal(unreadCount(rows), 1);
});
