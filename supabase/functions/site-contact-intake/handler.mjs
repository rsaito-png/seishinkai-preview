import {
  LIMITS,
  clientIp,
  dwellError,
  jstStamp,
  publicResult,
  sha256Hex,
  validateIntake,
} from "./shared.mjs";
import { classifyInquiry } from "./classify.mjs";

const ALLOWED_ORIGINS = new Set([
  "https://psr-seishinkai.org",
  "https://www.psr-seishinkai.org",
]);

function empty(extra) {
  return {
    ok: false,
    stored: false,
    duplicate: false,
    notified: false,
    notification: "none",
    lead_event: false,
    test: false,
    ...extra,
  };
}

function view(row, extra) {
  return {
    ok: true,
    stored: true,
    duplicate: extra.duplicate === true,
    lead_event: extra.lead_event === true,
    test: row.test === true,
    reference: String(row.id).slice(0, 8),
  };
}

async function hashes(value, ip, pepper, now) {
  const emailHash = await sha256Hex(value.email);
  const contentHash = await sha256Hex(value.body);
  const ipHash = await sha256Hex(String(pepper || "site-contact-v1") + "\n" + ip);
  const day = jstStamp(now, false);
  const hour = jstStamp(now, true);
  return {
    emailHash,
    contentHash,
    ipHash,
    dedupe_key: emailHash + ":" + contentHash + ":" + day,
    rate: [
      { bucket: "ip:" + ipHash + ":" + hour, limit: LIMITS.ipPerHour },
      { bucket: "em:" + emailHash + ":" + day, limit: LIMITS.emailPerDay },
      { bucket: "all:" + hour, limit: LIMITS.globalPerHour },
    ],
  };
}

export async function acceptIntake(input, ctx) {
  if (!ctx.store) return publicResult(503, empty({ code: "not_configured" }));
  const validated = validateIntake(input);
  if (!validated.ok) {
    return publicResult(400, empty({ code: validated.spam ? "rejected" : "invalid", fields: validated.spam ? undefined : validated.errors }));
  }
  const value = validated.value;
  const timing = dwellError(value.opened_at, ctx.now);
  if (timing) return publicResult(400, empty({ code: "rejected" }));

  const ip = ctx.ip || "unknown";
  const hashed = await hashes(value, ip, ctx.pepper, ctx.now);
  let outcome;
  try {
    outcome = await ctx.store.transaction(async (tx) => {
      if (tx.lock) await tx.lock();
      const replay = await tx.findByIdempotency(value.idempotency_key);
      if (replay) return { kind: "replay", row: replay };
      const duplicate = await tx.findByDedupe(hashed.dedupe_key);
      if (duplicate) return { kind: "duplicate", row: duplicate };
      const allowed = await tx.consumeRate(hashed.rate);
      if (!allowed) return { kind: "limited" };
      const screen = classifyInquiry(value);
      const row = await tx.insert({
        idempotency_key: value.idempotency_key,
        dedupe_key: hashed.dedupe_key,
        service: value.service,
        name: value.name,
        email: value.email,
        body: value.body,
        email_hash: hashed.emailHash,
        content_hash: hashed.contentHash,
        ip_hash: hashed.ipHash,
        lane: screen.lane,
        review: screen.review,
        sales_reason: screen.sales_reason,
        read_at: null,
        lead_eligible: ctx.suppressLead !== true && screen.lane === "normal",
        test: ctx.suppressLead === true,
      });
      return { kind: "created", row };
    });
  } catch (error) {
    if (error && error.code === "idempotency") {
      const replay = await ctx.store.getByIdempotency(value.idempotency_key);
      if (replay) return publicResult(200, view(replay, { duplicate: true, lead_event: false }));
    }
    if (error && error.code === "dedupe") {
      const duplicate = await ctx.store.getByDedupe(hashed.dedupe_key);
      if (duplicate) return publicResult(200, view(duplicate, { duplicate: true, lead_event: false }));
    }
    return publicResult(500, empty({ code: "persist" }));
  }

  if (outcome.kind === "replay" || outcome.kind === "duplicate") {
    return publicResult(200, view(outcome.row, { duplicate: true, lead_event: false }));
  }
  if (outcome.kind === "limited") return publicResult(429, empty({ code: "rate_limited" }));

  const saved = outcome.row;
  return publicResult(200, view(saved, { duplicate: false, lead_event: saved.lead_eligible === true && saved.test !== true }));
}

export async function handleRequest(req, deps) {
  const origin = req.headers.get("origin");
  const headers = new Headers({
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
  });
  if (origin && ALLOWED_ORIGINS.has(origin)) {
    headers.set("access-control-allow-origin", origin);
    headers.set("vary", "Origin");
    headers.set("access-control-allow-methods", "POST, OPTIONS");
    headers.set("access-control-allow-headers", "content-type");
  }
  const send = (result) => new Response(JSON.stringify(result.body), { status: result.status, headers });

  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (req.method !== "POST") return send(publicResult(405, empty({ code: "method" })));
  if (origin && !ALLOWED_ORIGINS.has(origin)) return send(publicResult(403, empty({ code: "origin" })));

  const declared = Number(req.headers.get("content-length") || 0);
  if (declared > LIMITS.json) return send(publicResult(413, empty({ code: "too_large" })));
  const text = await req.text();
  if (text.length > LIMITS.json) return send(publicResult(413, empty({ code: "too_large" })));
  let input;
  try {
    input = JSON.parse(text);
  } catch {
    return send(publicResult(400, empty({ code: "invalid_json" })));
  }
  if (input && typeof input === "object") {
    delete input.suppressLead;
    delete input.lead_event;
    delete input.test;
    delete input.ip;
    delete input.ip_hash;
  }
  const result = await acceptIntake(input, {
    now: Date.now(),
    ip: clientIp(req.headers),
    pepper: deps.env.CONTACT_IP_PEPPER || "",
    store: deps.store,
    suppressLead: false,
  });
  return send(result);
}
