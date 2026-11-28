-- Week and month browser app-time counters on dialer_presence (UTC ISO week + calendar month).

alter table public.dialer_presence
    add column if not exists app_week_key text not null default '',
    add column if not exists app_week_seconds integer not null default 0 check (app_week_seconds >= 0),
    add column if not exists app_month_key text not null default '',
    add column if not exists app_month_seconds integer not null default 0 check (app_month_seconds >= 0);