-- Per-user call scripts (industry × prospect type) and last panel selection.

create table if not exists public.call_script_prefs (
    user_id uuid primary key,
    industry text not null,
    prospect_type text not null,
    updated_at timestamptz not null default now()
);

create table if not exists public.call_script_entries (
    user_id uuid not null,
    industry text not null,
    prospect_type text not null,
    body text not null default '',
    updated_at timestamptz not null default now(),
    primary key (user_id, industry, prospect_type)
);

create index if not exists call_script_entries_user_id_idx on public.call_script_entries (user_id);

alter table public.call_script_prefs enable row level security;
alter table public.call_script_entries enable row level security;
revoke all on public.call_script_prefs from public, anon, authenticated;
revoke all on public.call_script_entries from public, anon, authenticated;
grant all on public.call_script_prefs to service_role;
grant all on public.call_script_entries to service_role;