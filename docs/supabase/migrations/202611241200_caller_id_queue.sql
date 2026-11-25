-- FIFO outbound caller ID pool per organization.

create table if not exists public.caller_id_queue (
    id uuid primary key default gen_random_uuid(),
    scope_id uuid not null,
    phone_e164 text not null,
    queue_position integer not null check (queue_position > 0),
    enabled boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (scope_id, phone_e164),
    unique (scope_id, queue_position)
);

create index if not exists caller_id_queue_scope_id_idx on public.caller_id_queue (scope_id);

alter table public.caller_id_queue enable row level security;
revoke all on public.caller_id_queue from public, anon, authenticated;
grant all on public.caller_id_queue to service_role;

create or replace function public.dequeue_caller_id(p_scope_id uuid)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
    picked public.caller_id_queue%rowtype;
    max_pos integer;
begin
    if p_scope_id is null then
        raise exception 'scope_id is required';
    end if;
    select *
    into picked
    from public.caller_id_queue
    where scope_id = p_scope_id and enabled
    order by queue_position
    limit 1
    for update;
    if not found then
        return '';
    end if;
    select coalesce(max(queue_position), 0)
    into max_pos
    from public.caller_id_queue
    where scope_id = p_scope_id;
    update public.caller_id_queue
    set queue_position = max_pos + 1, updated_at = now()
    where id = picked.id;
    return picked.phone_e164;
end;
$$;

create or replace function public.dequeue_caller_ids(p_scope_id uuid, p_count integer default 1)
returns text[]
language plpgsql
security definer
set search_path = public
as $$
declare
    result text[] := '{}';
    i integer;
    phone text;
begin
    if p_count is null or p_count < 1 then
        return result;
    end if;
    for i in 1..p_count loop
        phone := public.dequeue_caller_id(p_scope_id);
        if phone = '' then
            raise exception 'Caller ID queue is empty';
        end if;
        result := array_append(result, phone);
    end loop;
    return result;
end;
$$;

revoke all on function public.dequeue_caller_id(uuid) from public, anon, authenticated;
revoke all on function public.dequeue_caller_ids(uuid, integer) from public, anon, authenticated;
grant execute on function public.dequeue_caller_id(uuid) to service_role;
grant execute on function public.dequeue_caller_ids(uuid, integer) to service_role;