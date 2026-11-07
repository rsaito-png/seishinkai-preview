-- Private intake store for https://psr-seishinkai.org/contact/
-- Apply on project zvrardoyxocmqhvyddnf only after review.
-- Schema site_contact is not added to the Data API exposed schemas.
-- No privileges are granted to anon or authenticated. RLS is on and has no policies.
-- The edge function connects with SUPABASE_DB_URL (postgres), not the public API.

create schema if not exists site_contact;

revoke all on schema site_contact from public;
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'anon') then
    execute 'revoke all on schema site_contact from anon';
  end if;
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    execute 'revoke all on schema site_contact from authenticated';
  end if;
end $$;

create table if not exists site_contact.inquiries (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  idempotency_key text not null,
  dedupe_key text not null,
  service text not null,
  name text not null,
  email text not null,
  body text not null,
  email_hash text not null,
  content_hash text not null,
  ip_hash text not null,
  notification_status text not null default 'pending' check (notification_status in ('pending', 'sent', 'failed')),
  notification_attempts integer not null default 0 check (notification_attempts >= 0),
  notification_error text,
  notified_at timestamptz,
  lead_eligible boolean not null,
  test boolean not null default false,
  constraint inquiries_idem_uq unique (idempotency_key),
  constraint inquiries_dedupe_uq unique (dedupe_key),
  constraint inquiries_name_len check (char_length(name) between 1 and 80),
  constraint inquiries_email_len check (char_length(email) between 3 and 254),
  constraint inquiries_body_len check (char_length(body) between 1 and 2000)
);

create table if not exists site_contact.rate_buckets (
  bucket text primary key,
  hits integer not null check (hits >= 0),
  updated_at timestamptz not null default now()
);

alter table site_contact.inquiries enable row level security;
alter table site_contact.rate_buckets enable row level security;
alter table site_contact.inquiries force row level security;
alter table site_contact.rate_buckets force row level security;

revoke all on site_contact.inquiries from public;
revoke all on site_contact.rate_buckets from public;
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'anon') then
    execute 'revoke all on site_contact.inquiries from anon';
    execute 'revoke all on site_contact.rate_buckets from anon';
  end if;
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    execute 'revoke all on site_contact.inquiries from authenticated';
    execute 'revoke all on site_contact.rate_buckets from authenticated';
  end if;
end $$;

comment on table site_contact.inquiries is
  'Website contact intake. No public read. notification_status is independent of lead_eligible.';
