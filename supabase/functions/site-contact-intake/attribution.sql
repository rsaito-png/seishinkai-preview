-- Add first-touch attribution columns to site_contact.inquiries.
-- Safe to run more than once. Does not change table privileges or RLS.
-- The intake function inserts these columns and, if they are missing, saves the inquiry without them.

alter table site_contact.inquiries
  add column if not exists utm_source text,
  add column if not exists utm_medium text,
  add column if not exists utm_campaign text,
  add column if not exists referrer_host text,
  add column if not exists landing_path text,
  add column if not exists submit_path text;

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
      'restored_at', restored_at,
      'utm_source', utm_source,
      'utm_medium', utm_medium,
      'utm_campaign', utm_campaign,
      'referrer_host', referrer_host,
      'landing_path', landing_path,
      'submit_path', submit_path
    ) order by created_at desc)
    from site_contact.inquiries
    where test = false
      and (p_lane is null or lane = p_lane)
  ), '[]'::jsonb);
end $$;
