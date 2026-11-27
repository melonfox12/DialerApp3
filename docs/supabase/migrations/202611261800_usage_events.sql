-- Timestamped usage telemetry for team manager timelines (session, stage, disposition, UI tab).

create table if not exists public.usage_events (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references public.organizations (id) on delete cascade,
    user_id uuid not null,
    kind text not null,
    at timestamptz not null default now(),
    payload jsonb not null default '{}'::jsonb
);

create index if not exists usage_events_org_user_at_idx
    on public.usage_events (org_id, user_id, at desc);

create index if not exists usage_events_org_at_idx
    on public.usage_events (org_id, at desc);

alter table public.usage_events enable row level security;

revoke all on public.usage_events from public, anon, authenticated;
grant all on public.usage_events to service_role;