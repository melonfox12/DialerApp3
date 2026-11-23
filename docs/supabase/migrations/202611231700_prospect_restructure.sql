-- Clean slate: normalized prospects (uuid ids). Drops legacy jsonb prospects only.
-- Does not touch auth, dialer_settings, metrics, dial_archive, or dialer_sessions.

begin;

drop trigger if exists prospects_set_updated_at on public.prospects;
drop view if exists public.prospects_view;
drop table if exists public.prospects cascade;

create table public.prospects (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    archived_at timestamptz,
    company text not null default '',
    contact_name text not null default '',
    office_manager text not null default '',
    phone text not null default '',
    alt_phone text,
    email text not null default '',
    street text not null default '',
    city text not null default '',
    state text not null default '',
    zip text not null default '',
    lead_tier text not null default 'C' check (lead_tier in ('A', 'B', 'C', 'D')),
    lead_score numeric,
    score_reasons text not null default '',
    signal text not null default '',
    signal_date date,
    now_open_or_moved text not null default '',
    category text not null default '',
    property_type text not null default '',
    hygiene_focus text not null default '',
    website text not null default '',
    county text not null default '',
    providers_listed text not null default '',
    source text not null default '',
    source_file text not null default '',
    property_verdict text not null default '',
    residential_check text not null default '',
    remote_or_mobile text not null default '',
    shared_address boolean,
    suite_in_address boolean,
    -- Dialer workflow (not imported from CSV; app-owned)
    status text not null default 'new',
    scheduled_until timestamptz,
    timezone text not null default 'Unknown',
    transcript jsonb not null default '[]'::jsonb check (jsonb_typeof(transcript) = 'array'),
    call_log jsonb not null default '[]'::jsonb check (jsonb_typeof(call_log) = 'array'),
    pipeline_step text,
    pipeline_step_entered_at timestamptz,
    pipeline_history jsonb not null default '[]'::jsonb,
    status_history jsonb not null default '[]'::jsonb,
    booked_at timestamptz,
    passed_at timestamptz,
    agent_reserved_name text not null default '',
    agent_reserved_id text not null default ''
);

create index prospects_user_id_idx on public.prospects (user_id);
create index prospects_phone_idx on public.prospects (phone);
create index prospects_lead_tier_idx on public.prospects (lead_tier);
create index prospects_lead_score_idx on public.prospects (lead_score);
create index prospects_signal_date_idx on public.prospects (signal_date);
create index prospects_state_idx on public.prospects (state);
create index prospects_archived_at_idx on public.prospects (archived_at);

create or replace function public.prospects_touch_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger prospects_set_updated_at
before update on public.prospects
for each row execute function public.prospects_touch_updated_at();

create view public.prospects_view as
select
    p.*,
    case
        when p.signal_date is null then null::integer
        else (current_date - p.signal_date)::integer
    end as days_since_signal
from public.prospects p;

alter table public.prospects enable row level security;

drop policy if exists prospects_own on public.prospects;
create policy prospects_own on public.prospects
for all to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

revoke all on public.prospects from public, anon;
grant select, insert, update, delete on public.prospects to authenticated;
grant all on public.prospects to service_role;
grant select on public.prospects_view to authenticated, service_role;

commit;