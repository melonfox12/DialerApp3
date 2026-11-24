-- Organizations, membership roles, profiles, and dialer presence for manager dashboards.

create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),
    name text not null default '',
    created_at timestamptz not null default now()
);

create table if not exists public.profiles (
    user_id uuid primary key,
    email text not null default '',
    display_name text not null default '',
    updated_at timestamptz not null default now()
);

create table if not exists public.org_members (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references public.organizations (id) on delete cascade,
    user_id uuid,
    role text not null check (role in ('owner', 'manager', 'rep')),
    status text not null default 'active' check (status in ('active', 'invited', 'disabled')),
    invited_email text not null default '',
    created_at timestamptz not null default now(),
    joined_at timestamptz
);

create unique index if not exists org_members_active_user_idx
    on public.org_members (user_id)
    where status = 'active' and user_id is not null;

create unique index if not exists org_members_org_invited_email_idx
    on public.org_members (org_id, lower(invited_email))
    where status = 'invited' and invited_email <> '';

create table if not exists public.dialer_presence (
    user_id uuid primary key,
    org_id uuid not null,
    last_seen_at timestamptz not null default now(),
    running boolean not null default false,
    paused boolean not null default false,
    stage text not null default 'idle',
    active_lead_id text not null default '',
    in_flight_count integer not null default 0 check (in_flight_count >= 0)
);

create index if not exists org_members_org_id_idx on public.org_members (org_id);
create index if not exists dialer_presence_org_id_idx on public.dialer_presence (org_id);

alter table public.organizations enable row level security;
alter table public.profiles enable row level security;
alter table public.org_members enable row level security;
alter table public.dialer_presence enable row level security;

revoke all on public.organizations from public, anon, authenticated;
revoke all on public.profiles from public, anon, authenticated;
revoke all on public.org_members from public, anon, authenticated;
revoke all on public.dialer_presence from public, anon, authenticated;

grant all on public.organizations to service_role;
grant all on public.profiles to service_role;
grant all on public.org_members to service_role;
grant all on public.dialer_presence to service_role;