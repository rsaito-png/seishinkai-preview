-- Website contact intake. Project zvrardoyxocmqhvyddnf (database region ap-northeast-1).
-- Private schema. Not added to the Data API exposed schemas.
-- anon and authenticated have no table privileges. RLS is forced and has no policies.
-- The public functions below are the only authenticated entry. Each one checks
-- auth.users.email for the owner account. That email is the Auth identity,
-- not user_metadata and not staff role.

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
  lane text not null check (lane in ('normal', 'sales')),
  review text not null check (review in ('clear', 'needs-review', 'restored')),
  sales_reason text,
  read_at timestamptz,
  restored_at timestamptz,
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

create or replace function site_contact.is_owner()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from auth.users
    where id = auth.uid()
      and lower(email) = 'rsaito@psr-seishinkai.org'
  );
$$;

revoke all on function site_contact.is_owner() from public, anon;
grant execute on function site_contact.is_owner() to authenticated;

create or replace function site_contact.rows_for(p_lane text)
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not site_contact.is_owner() then
    raise exception 'forbidden' using errcode = '42501';
  end if;
  if p_lane is not null and p_lane not in ('normal', 'sales') then
    raise exception 'bad lane' using errcode = '22023';
  end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object(
      'id', id,
      'created_at', created_at,
      'service', service,
      'name', name,
      'email', email,
      'body', body,
      'lane', lane,
      'review', review,
      'sales_reason', sales_reason,
      'read_at', read_at,
      'restored_at', restored_at
    ) order by created_at desc)
    from site_contact.inquiries
    where test = false
      and (p_lane is null or lane = p_lane)
  ), '[]'::jsonb);
end $$;

revoke all on function site_contact.rows_for(text) from public, anon;
grant execute on function site_contact.rows_for(text) to authenticated;

create or replace function site_contact.unread_count()
returns integer
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not site_contact.is_owner() then
    raise exception 'forbidden' using errcode = '42501';
  end if;
  return (
    select count(*)::integer from site_contact.inquiries
    where test = false and lane = 'normal' and read_at is null
  );
end $$;

revoke all on function site_contact.unread_count() from public, anon;
grant execute on function site_contact.unread_count() to authenticated;

create or replace function site_contact.mark_read(p_id uuid)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare row_json jsonb;
begin
  if not site_contact.is_owner() then
    raise exception 'forbidden' using errcode = '42501';
  end if;
  update site_contact.inquiries
    set read_at = coalesce(read_at, now())
    where id = p_id and test = false
    returning jsonb_build_object('id', id, 'lane', lane, 'read_at', read_at) into row_json;
  return row_json;
end $$;

revoke all on function site_contact.mark_read(uuid) from public, anon;
grant execute on function site_contact.mark_read(uuid) to authenticated;

create or replace function site_contact.restore(p_id uuid)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare row_json jsonb;
begin
  if not site_contact.is_owner() then
    raise exception 'forbidden' using errcode = '42501';
  end if;
  update site_contact.inquiries
    set lane = 'normal',
        review = case when lane = 'sales' then 'restored' else review end,
        restored_at = case when lane = 'sales' then now() else restored_at end
    where id = p_id and test = false
    returning jsonb_build_object('id', id, 'lane', lane, 'review', review, 'read_at', read_at, 'sales_reason', sales_reason) into row_json;
  return row_json;
end $$;

revoke all on function site_contact.restore(uuid) from public, anon;
grant execute on function site_contact.restore(uuid) to authenticated;

grant usage on schema site_contact to authenticated;
revoke all on table site_contact.inquiries from public, anon, authenticated;
revoke all on table site_contact.rate_buckets from public, anon, authenticated;

-- Owner check: auth.uid() matched to auth.users.email, not user_metadata and not staff role.
-- Tables stay in site_contact with RLS forced and no policies, and API roles have no table grants.
-- Private functions are security definer and refuse every caller who is not the owner.
-- Public wrappers are security invoker. They do not bypass RLS themselves.
-- anon cannot execute them. A signed-in staff JWT can call them and still receives forbidden.
create or replace function public.site_contact_is_owner()
returns boolean
language sql
stable
security invoker
set search_path = ''
as $$ select site_contact.is_owner() $$;

create or replace function public.site_contact_inbox(p_lane text)
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $$ select site_contact.rows_for(p_lane) $$;

create or replace function public.site_contact_unread_count()
returns integer
language sql
stable
security invoker
set search_path = ''
as $$ select site_contact.unread_count() $$;

create or replace function public.site_contact_mark_read(p_id uuid)
returns jsonb
language sql
volatile
security invoker
set search_path = ''
as $$ select site_contact.mark_read(p_id) $$;

create or replace function public.site_contact_restore(p_id uuid)
returns jsonb
language sql
volatile
security invoker
set search_path = ''
as $$ select site_contact.restore(p_id) $$;

revoke all on function public.site_contact_is_owner() from public, anon;
revoke all on function public.site_contact_inbox(text) from public, anon;
revoke all on function public.site_contact_unread_count() from public, anon;
revoke all on function public.site_contact_mark_read(uuid) from public, anon;
revoke all on function public.site_contact_restore(uuid) from public, anon;

grant execute on function public.site_contact_is_owner() to authenticated;
grant execute on function public.site_contact_inbox(text) to authenticated;
grant execute on function public.site_contact_unread_count() to authenticated;
grant execute on function public.site_contact_mark_read(uuid) to authenticated;
grant execute on function public.site_contact_restore(uuid) to authenticated;
