// In-memory store used by local tests. Production uses pg_store.mjs.
// A thrown error rolls the transaction back, including rate increments.

export function createMemoryStore() {
  const rows = [];
  const buckets = new Map();
  let chain = Promise.resolve();

  function lock(fn) {
    const run = chain.then(fn, fn);
    chain = run.then(() => {}, () => {});
    return run;
  }

  function api() {
    return {
      async lock() {},
      async findByIdempotency(key) {
        return rows.find((row) => row.idempotency_key === key) || null;
      },
      async findByDedupe(key) {
        return rows.find((row) => row.dedupe_key === key) || null;
      },
      async consumeRate(items) {
        for (const item of items) {
          if ((buckets.get(item.bucket) || 0) >= item.limit) return false;
        }
        for (const item of items) buckets.set(item.bucket, (buckets.get(item.bucket) || 0) + 1);
        return true;
      },
      async insert(row) {
        if (rows.some((item) => item.idempotency_key === row.idempotency_key)) {
          const error = new Error("idempotency");
          error.code = "idempotency";
          throw error;
        }
        if (rows.some((item) => item.dedupe_key === row.dedupe_key)) {
          const error = new Error("dedupe");
          error.code = "dedupe";
          throw error;
        }
        const saved = {
          ...row,
          id: crypto.randomUUID(),
          created_at: new Date().toISOString(),
          notification_attempts: 0,
          notification_error: null,
          notified_at: null,
        };
        rows.push(saved);
        return saved;
      },
    };
  }

  return {
    rows,
    buckets,
    transaction(fn) {
      return lock(async () => {
        const snapRows = rows.map((row) => ({ ...row }));
        const snapBuckets = new Map(buckets);
        try {
          return await fn(api());
        } catch (error) {
          rows.splice(0, rows.length, ...snapRows);
          buckets.clear();
          for (const [key, value] of snapBuckets) buckets.set(key, value);
          throw error;
        }
      });
    },
    async mark(id, patch) {
      const row = rows.find((item) => item.id === id);
      if (!row) return null;
      row.notification_status = patch.notification_status;
      row.notification_error = patch.notification_error ?? null;
      row.notification_attempts += 1;
      if (patch.notification_status === "sent") row.notified_at = new Date().toISOString();
      return row;
    },
    async listRetryable(limit) {
      return rows
        .filter((row) => row.test !== true && (row.notification_status === "pending" || row.notification_status === "failed") && row.notification_attempts < 8)
        .slice(0, limit);
    },
    async getByIdempotency(key) {
      return rows.find((row) => row.idempotency_key === key) || null;
    },
    async getByDedupe(key) {
      return rows.find((row) => row.dedupe_key === key) || null;
    },
  };
}
