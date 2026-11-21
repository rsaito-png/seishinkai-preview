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
      const values = {
        idempotency_key: row.idempotency_key,
        dedupe_key: row.dedupe_key,
        service: row.service,
        name: row.name,
        email: row.email,
        body: row.body,
        email_hash: row.email_hash,
        content_hash: row.content_hash,
        ip_hash: row.ip_hash,
        lane: row.lane,
        review: row.review,
        sales_reason: row.sales_reason,
        lead_eligible: row.lead_eligible,
        test: row.test,
      };
      const attr = {
        utm_source: row.utm_source ?? null,
        utm_medium: row.utm_medium ?? null,
        utm_campaign: row.utm_campaign ?? null,
        referrer_host: row.referrer_host ?? null,
        landing_path: row.landing_path ?? null,
        submit_path: row.submit_path ?? null,
      };
      const write = async (withAttr) => {
        if (withAttr) {
          const rows = await sql`
            insert into site_contact.inquiries (
              idempotency_key, dedupe_key, service, name, email, body,
              email_hash, content_hash, ip_hash, lane, review, sales_reason, lead_eligible, test,
              utm_source, utm_medium, utm_campaign, referrer_host, landing_path, submit_path
            ) values (
              ${values.idempotency_key}, ${values.dedupe_key}, ${values.service}, ${values.name}, ${values.email}, ${values.body},
              ${values.email_hash}, ${values.content_hash}, ${values.ip_hash}, ${values.lane}, ${values.review}, ${values.sales_reason}, ${values.lead_eligible}, ${values.test},
              ${attr.utm_source}, ${attr.utm_medium}, ${attr.utm_campaign}, ${attr.referrer_host}, ${attr.landing_path}, ${attr.submit_path}
            ) returning *`;
          return rows[0];
        }
        const rows = await sql`
          insert into site_contact.inquiries (
            idempotency_key, dedupe_key, service, name, email, body,
            email_hash, content_hash, ip_hash, lane, review, sales_reason, lead_eligible, test
          ) values (
            ${values.idempotency_key}, ${values.dedupe_key}, ${values.service}, ${values.name}, ${values.email}, ${values.body},
            ${values.email_hash}, ${values.content_hash}, ${values.ip_hash}, ${values.lane}, ${values.review}, ${values.sales_reason}, ${values.lead_eligible}, ${values.test}
          ) returning *`;
        return rows[0];
      };
      try {
        await sql`savepoint inquiry_attr`;
        try {
          const saved = await write(true);
          await sql`release savepoint inquiry_attr`;
          return saved;
        } catch (error) {
          if (!error || error.code !== "42703") throw error;
          await sql`rollback to savepoint inquiry_attr`;
          return await write(false);
        }
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
