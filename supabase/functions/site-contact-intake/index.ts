// Public contact intake. verify_jwt stays false: visitors have no Supabase user.
// Validation, the honeypot, dwell time, and database rate limits are the controls.
// Nothing is emailed. The owner reads saved rows in the portal.

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
      getByIdempotency() {
        return Promise.resolve(null);
      },
      getByDedupe() {
        return Promise.resolve(null);
      },
    };

Deno.serve((req) => handleRequest(req, {
  env: { CONTACT_IP_PEPPER: Deno.env.get("CONTACT_IP_PEPPER") ?? "" },
  fetch: globalThis.fetch,
  store,
}));
