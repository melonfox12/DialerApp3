-- Repair missing dial_archive + increment_metric (safe if prospects migration already applied).

create table if not exists public.dial_archive (
    id text primary key,
    user_id uuid,
    data jsonb not null check (jsonb_typeof(data) = 'object')
);

alter table public.dial_archive enable row level security;

drop policy if exists dial_archive_own on public.dial_archive;
create policy dial_archive_own on public.dial_archive
for all to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

revoke all on public.dial_archive from public, anon;
grant select, insert, update, delete on public.dial_archive to authenticated;
grant all on public.dial_archive to service_role;

create index if not exists dial_archive_user_id_idx on public.dial_archive (user_id);

create or replace function public.increment_metric(p_user_id uuid, p_day date, p_metric_key text, p_amount bigint)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
    if p_user_id is null or p_day is null then
        raise exception 'A user and day are required to increment dialer metrics';
    end if;
    if p_metric_key not in (
        'booked', 'call_later', 'connected', 'disqualified', 'interested',
        'dials', 'failed', 'talk_seconds', 'voicemail'
    ) then
        raise exception 'Unknown dialer metric';
    end if;
    if p_amount is null or p_amount <= 0 then
        raise exception 'Metric increment must be positive';
    end if;

    insert into public.dialer_metric_daily as daily (user_id, day, metric_key, value)
    values (p_user_id, p_day, p_metric_key, p_amount)
    on conflict (user_id, day, metric_key)
    do update set value = daily.value + excluded.value;

    insert into public.dialer_metric_totals as totals (user_id, metric_key, value)
    values (p_user_id, p_metric_key, p_amount)
    on conflict (user_id, metric_key)
    do update set value = totals.value + excluded.value;
end;
$$;

revoke all on function public.increment_metric(uuid, date, text, bigint) from public, anon, authenticated;
grant execute on function public.increment_metric(uuid, date, text, bigint) to service_role;