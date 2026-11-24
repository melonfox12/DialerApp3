-- Saved Total-dials snapshots (replaces legacy prospects.data blob).

create table if not exists public.dial_records_snapshots (
    user_id uuid primary key,
    saved jsonb not null default '[]'::jsonb check (jsonb_typeof(saved) = 'array')
);

alter table public.dial_records_snapshots enable row level security;

revoke all on public.dial_records_snapshots from public, anon, authenticated;
grant all on public.dial_records_snapshots to service_role;