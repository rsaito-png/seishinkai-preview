// Browser-safe rules for the public contact form.
// No recipient address and no secrets in this file: the page imports it.

export const SERVICES = [
  "決まっていない",
  "環境調整支援　水晶玉",
  "しちりんの会",
  "B型事業所　次世代労働研究所　RYDEEN",
  "自立支援寮　梁山泊",
  "生活介護事業所　茶夢",
  "訪問支援　金斗雲",
  "児発・放デイ　レオ",
  "ペアレントトレーニング",
  "発達検査",
  "雇用定着サポート",
  "ストレスチェック",
  "エージェントコンサル",
  "ストレスチェック実施者養成研修",
  "研修",
];

export const LIMITS = {
  name: 80,
  email: 254,
  body: 2000,
  json: 8000,
  minDwellMs: 2000,
  maxAgeMs: 24 * 60 * 60 * 1000,
  ipPerHour: 5,
  emailPerDay: 5,
  globalPerHour: 30,
  maxNotifyAttempts: 8,
};

const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function shouldCountLead(res) {
  return !!(
    res &&
    res.ok === true &&
    res.stored === true &&
    res.lead_event === true &&
    res.duplicate !== true &&
    res.test !== true &&
    res.notification !== "mocked"
  );
}

function controls(value) {
  return /[\u0000-\u001F\u007F]/.test(value);
}

export function validateIntake(input) {
  const errors = {};
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, errors: { form: "invalid" }, spam: false };
  }
  const honeypot = input.company_url;
  if (honeypot != null && String(honeypot) !== "") {
    return { ok: false, errors: { form: "rejected" }, spam: true };
  }
  const service = typeof input.service === "string" ? input.service : "";
  if (!SERVICES.includes(service)) errors.service = "invalid";

  const name = typeof input.name === "string" ? input.name.trim() : "";
  if (!name) errors.name = "required";
  else if (name.length > LIMITS.name || controls(name)) errors.name = "invalid";

  const emailRaw = typeof input.email === "string" ? input.email.trim().toLowerCase() : "";
  if (!emailRaw) errors.email = "required";
  else if (emailRaw.length > LIMITS.email || controls(emailRaw) || !EMAIL.test(emailRaw)) errors.email = "invalid";

  const body = typeof input.body === "string" ? input.body.replace(/\u0000/g, "").trim() : "";
  if (!body) errors.body = "required";
  else if (body.length > LIMITS.body) errors.body = "invalid";

  const key = typeof input.idempotency_key === "string" ? input.idempotency_key.trim().toLowerCase() : "";
  if (!UUID_V4.test(key)) errors.idempotency_key = "invalid";

  const opened = Number(input.opened_at);
  if (!Number.isFinite(opened)) errors.opened_at = "invalid";

  return {
    ok: Object.keys(errors).length === 0,
    errors,
    spam: false,
    value: { service, name, email: emailRaw, body, idempotency_key: key, opened_at: opened },
  };
}

export function dwellError(openedAt, now) {
  const dwell = now - openedAt;
  if (dwell < LIMITS.minDwellMs || dwell > LIMITS.maxAgeMs) return "timing";
  return "";
}

export function jstStamp(ms, withHour) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    hourCycle: "h23",
  }).formatToParts(new Date(ms));
  const get = (type) => parts.find((p) => p.type === type).value;
  const day = `${get("year")}-${get("month")}-${get("day")}`;
  return withHour ? `${day}T${get("hour")}` : day;
}

export async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function clientIp(headers) {
  const xff = String(headers.get("x-forwarded-for") || "");
  const parts = xff.split(",").map((s) => s.trim()).filter(Boolean);
  if (parts.length) return parts[parts.length - 1].slice(0, 80);
  const real = String(headers.get("x-real-ip") || "").trim();
  return (real || "unknown").slice(0, 80);
}

export function publicResult(status, body) {
  return { status, body };
}
