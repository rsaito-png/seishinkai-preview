// Direct Postgres access for the private site_contact schema.
// The Data API does not expose this schema. Caller must pass a postgres.js client
// opened with the function's SUPABASE_DB_URL.

function mapUnique(error) {
  if (!error || error.code !== "23505") throw error;
  const name = String(error.constraint_name || error.constraint || "");
  const wrapped = new Error("conflict");
  if (name.includes("idem")) wrapped.code = "idempotency";
  else if (name.includes("dedupe")) wrapped.code = "dedupe";
  else wrapped.code = "persist";
  throw wrapped;
}

function txApi(sql) {
  return {
    async lock() {
      await sql`select pg_advisory_xact_lock(814201)`;
    },
    async findByIdempotency(key) {
      const rows = await sql`select * from site_contact.inquiries where idempotency_key = ${key} limit 1`;
      return rows[0] || null;
    },
    async findByDedupe(key) {
      const rows = await sql`select * from site_contact.inquiries where dedupe_key = ${key} limit 1`;
      return rows[0] || null;
    },
    async consumeRate(items) {
      await sql`select pg_advisory_xact_lock(814201)`;
      for (const item of items) {
        const rows = await sql`select hits from site_contact.rate_buckets where bucket = ${item.bucket}`;
        if ((rows[0]?.hits || 0) >= item.limit) return false;
      }
      for (const item of items) {
        await sql`
          insert into site_contact.rate_buckets as b (bucket, hits)
          values (${item.bucket}, 1)
          on conflict (bucket) do update
            set hits = b.hits + 1, updated_at = now()`;
      }
      return true;
    },
    async insert(row) {
      try {
        const rows = await sql`
          insert into site_contact.inquiries (
            idempotency_key, dedupe_key, service, name, email, body,
            email_hash, content_hash, ip_hash, notification_status, lead_eligible, test
          ) values (
            ${row.idempotency_key}, ${row.dedupe_key}, ${row.service}, ${row.name}, ${row.email}, ${row.body},
            ${row.email_hash}, ${row.content_hash}, ${row.ip_hash}, 'pending', ${row.lead_eligible}, ${row.test}
          ) returning *`;
        return rows[0];
      } catch (error) {
        mapUnique(error);
      }
    },
  };
}

export function createPgStore(sql) {
  return {
    transaction(fn) {
      return sql.begin(async (tx) => fn(txApi(tx)));
    },
    async mark(id, patch) {
      const status = patch.notification_status;
      const error = patch.notification_error ?? null;
      const rows = await sql`
        update site_contact.inquiries
        set notification_status = ${status},
            notification_error = ${error},
            notification_attempts = notification_attempts + 1,
            notified_at = case when ${status} = 'sent' then now() else notified_at end
        where id = ${id}
        returning *`;
      return rows[0] || null;
    },
    async listRetryable(limit) {
      return sql`
        select * from site_contact.inquiries
        where test = false
          and notification_status in ('pending', 'failed')
          and notification_attempts < 8
        order by created_at
        limit ${limit}`;
    },
    async getByIdempotency(key) {
      const rows = await sql`select * from site_contact.inquiries where idempotency_key = ${key} limit 1`;
      return rows[0] || null;
    },
    async getByDedupe(key) {
      const rows = await sql`select * from site_contact.inquiries where dedupe_key = ${key} limit 1`;
      return rows[0] || null;
    },
  };
}
