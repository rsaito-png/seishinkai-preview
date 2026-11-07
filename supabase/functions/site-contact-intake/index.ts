// Public contact intake. verify_jwt stays false: visitors have no Supabase user.
// CONTACT_INTAKE_ENABLED must be the exact string "true" or this process does not
// open a database connection and every POST returns 503 without storing anything.

import postgres from "npm:postgres@3.4.5";
import { handleRequest, intakeEnabled } from "./handler.mjs";
import { createPgStore } from "./pg_store.mjs";

let sql = null;

function openStore() {
  if (!intakeEnabled({ CONTACT_INTAKE_ENABLED: Deno.env.get("CONTACT_INTAKE_ENABLED") ?? "" })) return null;
  if (!sql) {
    const dbUrl = Deno.env.get("SUPABASE_DB_URL") ?? "";
    if (!dbUrl) return null;
    sql = postgres(dbUrl, { max: 1, prepare: false });
  }
  return createPgStore(sql);
}

Deno.serve((req) => {
  const enabled = intakeEnabled({ CONTACT_INTAKE_ENABLED: Deno.env.get("CONTACT_INTAKE_ENABLED") ?? "" });
  return handleRequest(req, {
    env: {
      CONTACT_INTAKE_ENABLED: enabled ? "true" : "",
      CONTACT_IP_PEPPER: enabled ? (Deno.env.get("CONTACT_IP_PEPPER") ?? "") : "",
    },
    fetch: globalThis.fetch,
    store: enabled ? openStore() : null,
  });
});
