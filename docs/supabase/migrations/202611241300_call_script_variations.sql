-- Add variation (1–3) to call script prefs and entries.

alter table public.call_script_prefs
    add column if not exists variation smallint not null default 1;

alter table public.call_script_prefs
    drop constraint if exists call_script_prefs_variation_check;

alter table public.call_script_prefs
    add constraint call_script_prefs_variation_check check (variation between 1 and 3);

alter table public.call_script_entries
    add column if not exists variation smallint not null default 1;

alter table public.call_script_entries
    drop constraint if exists call_script_entries_variation_check;

alter table public.call_script_entries
    add constraint call_script_entries_variation_check check (variation between 1 and 3);

alter table public.call_script_entries
    drop constraint if exists call_script_entries_pkey;

alter table public.call_script_entries
    add primary key (user_id, industry, prospect_type, variation);