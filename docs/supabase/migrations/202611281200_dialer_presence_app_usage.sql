-- Browser app time tracked from /api/live heartbeats while signed in (team tracker).

alter table public.dialer_presence
    add column if not exists app_today_date date not null default (timezone('utc', now()))::date,
    add column if not exists app_today_seconds integer not null default 0 check (app_today_seconds >= 0),
    add column if not exists app_week_key text not null default '',
    add column if not exists app_week_seconds integer not null default 0 check (app_week_seconds >= 0),
    add column if not exists app_month_key text not null default '',
    add column if not exists app_month_seconds integer not null default 0 check (app_month_seconds >= 0),
    add column if not exists app_session_seconds integer not null default 0 check (app_session_seconds >= 0),
    add column if not exists app_session_started_at timestamptz;