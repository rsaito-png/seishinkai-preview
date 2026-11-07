// Public contact intake. verify_jwt must stay false: visitors have no Supabase user.
// JWT verification is not the spam control. Validation, the honeypot, dwell time,
// and database rate limits are. CORS only restricts browsers.
//
// No mail is sent unless CONTACT_INTAKE_ENABLED=1 and an https-json transport is set.
// Until then every POST returns not_configured and writes nothing.

import postgres from "npm:postgres@3.4.5";
import { handleRequest } from "./handler.mjs";
import { createPgStore } from "./pg_store.mjs";

const dbUrl = Deno.env.get("SUPABASE_DB_URL") ?? "";
const sql = dbUrl ? postgres(dbUrl, { max: 1, prepare: false }) : null;
const store = sql
  ? createPgStore(sql)
  : {
      transaction() {
        const error = new Error("persist");
        error.code = "persist";
        throw error;
      },
      mark() {
        return Promise.resolve(null);
      },
      listRetryable() {
        return Promise.resolve([]);
      },
      getByIdempotency() {
        return Promise.resolve(null);
      },
      getByDedupe() {
        return Promise.resolve(null);
      },
    };

const env = {
  CONTACT_INTAKE_ENABLED: Deno.env.get("CONTACT_INTAKE_ENABLED") ?? "",
  CONTACT_MAIL_TRANSPORT: Deno.env.get("CONTACT_MAIL_TRANSPORT") ?? "",
  CONTACT_MAIL_URL: Deno.env.get("CONTACT_MAIL_URL") ?? "",
  CONTACT_MAIL_TOKEN: Deno.env.get("CONTACT_MAIL_TOKEN") ?? "",
  CONTACT_MAIL_FROM: Deno.env.get("CONTACT_MAIL_FROM") ?? "",
  CONTACT_RETRY_SECRET: Deno.env.get("CONTACT_RETRY_SECRET") ?? "",
  CONTACT_IP_PEPPER: Deno.env.get("CONTACT_IP_PEPPER") ?? "",
};

Deno.serve((req) => handleRequest(req, { env, fetch: globalThis.fetch, store }));
