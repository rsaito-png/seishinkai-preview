// Public contact intake. verify_jwt stays false: visitors have no Supabase user.
// Intake opens only when deploy_switch.mjs sets INTAKE_DEPLOY_ENABLED to exactly true.
// CONTACT_INTAKE_ENABLED "false" stops intake without a new deploy and does not open a database.

import postgres from "npm:postgres@3.4.5";
import { INTAKE_DEPLOY_ENABLED } from "./deploy_switch.mjs";
import { handleRequest, intakeEnabled } from "./handler.mjs";
import { createPgStore } from "./pg_store.mjs";

let sql = null;

function runtimeEnv() {
  return {
    CONTACT_INTAKE_ENABLED: Deno.env.get("CONTACT_INTAKE_ENABLED") ?? "",
    INTAKE_DEPLOY_ENABLED,
  };
}

function openStore() {
  if (!intakeEnabled(runtimeEnv())) return null;
  if (!sql) {
    const dbUrl = Deno.env.get("SUPABASE_DB_URL") ?? "";
    if (!dbUrl) return null;
    sql = postgres(dbUrl, { max: 1, prepare: false });
  }
  return createPgStore(sql);
}

Deno.serve((req) => {
  const env = runtimeEnv();
  const enabled = intakeEnabled(env);
  return handleRequest(req, {
    env: {
      CONTACT_INTAKE_ENABLED: env.CONTACT_INTAKE_ENABLED,
      INTAKE_DEPLOY_ENABLED: env.INTAKE_DEPLOY_ENABLED,
      CONTACT_IP_PEPPER: enabled ? (Deno.env.get("CONTACT_IP_PEPPER") ?? "") : "",
    },
    fetch: globalThis.fetch,
    store: enabled ? openStore() : null,
  });
});
