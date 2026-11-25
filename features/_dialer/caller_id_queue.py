"""Outbound caller ID pool and FIFO rotation (local file or Supabase)."""

import json
import threading
from pathlib import Path

from shared.vocabulary import DEFAULT_CALLER_ID_POOL


def queue_scope_id(dialer):
    membership = getattr(dialer, "org_membership", None) or {}
    org_id = str(membership.get("org_id") or "").strip()
    if org_id:
        return org_id
    user_id = str(getattr(dialer, "account_user_id", None) or "").strip()
    if user_id:
        return user_id
    return "local"


def build_caller_id_queue_view(ordered, in_use, dialing_active, max_preview=3):
    """UI snapshot: in-use lines, next numbers at the queue head, full ordered list."""
    ordered = [str(item or "").strip() for item in (ordered or []) if str(item or "").strip()]
    in_use = [str(item or "").strip() for item in (in_use or []) if str(item or "").strip()]
    in_use_set = set(in_use)
    front = [phone for phone in ordered if phone not in in_use_set]
    cap = max(1, int(max_preview or 3))
    up_next = front[: min(cap, len(front))]
    status_by_phone = {}
    if dialing_active:
        for phone in in_use:
            status_by_phone[phone] = "in_use"
    for phone in up_next:
        if phone not in status_by_phone:
            status_by_phone[phone] = "up_next"
    rows = [{"phone": phone, "status": status_by_phone.get(phone, "waiting")} for phone in ordered]
    return {
        "ordered": ordered,
        "in_use": in_use,
        "up_next": up_next,
        "dialing_active": bool(dialing_active),
        "rows": rows,
    }


def in_use_from_state(state):
    lines = []
    for call in (getattr(state, "in_flight", None) or {}).values():
        if not isinstance(call, dict) or call.get("kind") == "agent":
            continue
        caller = str(call.get("caller_id") or "").strip()
        if caller and caller not in lines:
            lines.append(caller)
    return lines


def dialing_active_on_state(state):
    if not getattr(state, "running", False):
        return False
    for call in (getattr(state, "in_flight", None) or {}).values():
        if not isinstance(call, dict) or call.get("kind") == "agent":
            continue
        if str(call.get("caller_id") or "").strip():
            return True
    return False


class LocalCallerIdQueueStore:
    def __init__(self, crm_path):
        self.path = Path(crm_path)
        if self.path.is_dir() or not self.path.suffix:
            self.path = self.path / "caller_id_queue.json"
        else:
            self.path = self.path.with_name("caller_id_queue.json")
        self.lock = threading.RLock()
        self._cache = None

    def _load(self):
        if self._cache is not None:
            return list(self._cache)
        try:
            if self.path.is_file():
                data = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self._cache = [dict(row) for row in data]
                    return list(self._cache)
        except (OSError, json.JSONDecodeError):
            pass
        self._cache = [
            {"phone_e164": phone, "queue_position": index + 1, "enabled": True}
            for index, phone in enumerate(DEFAULT_CALLER_ID_POOL)
        ]
        self._save_locked()
        return list(self._cache)

    def _save_locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(self._cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(self.path)

    def ensure_pool(self, _scope_id, seed=None):
        with self.lock:
            rows = self._load()
            if rows:
                return rows
            numbers = list(seed or DEFAULT_CALLER_ID_POOL)
            self._cache = [
                {"phone_e164": phone, "queue_position": index + 1, "enabled": True}
                for index, phone in enumerate(numbers)
            ]
            self._save_locked()
            return list(self._cache)

    def list_ordered(self, scope_id):
        with self.lock:
            rows = sorted(self._load(), key=lambda row: int(row.get("queue_position") or 0))
            return [str(row.get("phone_e164") or "").strip() for row in rows if row.get("enabled", True)]

    def dequeue(self, scope_id):
        with self.lock:
            rows = self._load()
            enabled = [row for row in rows if row.get("enabled", True)]
            if not enabled:
                raise ValueError("No caller ID numbers are configured.")
            enabled.sort(key=lambda row: int(row.get("queue_position") or 0))
            picked = enabled[0]
            max_pos = max(int(row.get("queue_position") or 0) for row in rows)
            picked["queue_position"] = max_pos + 1
            self._save_locked()
            return str(picked.get("phone_e164") or "").strip()

    def dequeue_many(self, scope_id, count):
        count = max(0, int(count or 0))
        if count == 0:
            return []
        return [self.dequeue(scope_id) for _ in range(count)]


class SupabaseCallerIdQueueStore:
    def __init__(self, client):
        self.client = client
        self.lock = threading.RLock()

    def _table_missing(self, exc):
        message = str(exc).lower()
        return "caller_id_queue" in message and (
            "404" in message or "does not exist" in message or "pgrst205" in message
        )

    def _list_rows(self, scope_id):
        return self.client.request(
            "GET",
            "caller_id_queue",
            {
                "scope_id": f"eq.{scope_id}",
                "select": "id,phone_e164,queue_position,enabled",
                "order": "queue_position.asc",
            },
        ) or []

    def ensure_pool(self, scope_id, seed=None):
        if not scope_id or scope_id == "local":
            raise ValueError("Account scope is required to load caller ID queue.")
        numbers = list(seed or DEFAULT_CALLER_ID_POOL)
        try:
            existing = self._list_rows(scope_id)
        except OSError as exc:
            if self._table_missing(exc):
                raise OSError(
                    "The caller_id_queue table is missing in Supabase. "
                    "Run docs/supabase/migrations/202611241200_caller_id_queue.sql in the SQL editor."
                ) from exc
            raise
        if existing:
            return existing
        rows = [
            {
                "scope_id": scope_id,
                "phone_e164": phone,
                "queue_position": index + 1,
                "enabled": True,
            }
            for index, phone in enumerate(numbers)
        ]
        with self.lock:
            self.client.request(
                "POST",
                "caller_id_queue",
                {},
                rows,
                "return=minimal",
            )
            return self._list_rows(scope_id)

    def list_ordered(self, scope_id):
        try:
            rows = self._list_rows(scope_id)
        except OSError as exc:
            if self._table_missing(exc):
                return list(DEFAULT_CALLER_ID_POOL)
            raise
        return [
            str(row.get("phone_e164") or "").strip()
            for row in rows
            if row.get("enabled", True) and str(row.get("phone_e164") or "").strip()
        ]

    def dequeue(self, scope_id):
        try:
            rows = self.client.request(
                "POST",
                "rpc/dequeue_caller_id",
                {},
                {"p_scope_id": scope_id},
            )
        except OSError as exc:
            if self._table_missing(exc):
                raise ValueError("Caller ID queue is not configured in Supabase.") from exc
            raise
        phone = ""
        if isinstance(rows, str):
            phone = rows.strip()
        elif isinstance(rows, list) and rows:
            phone = str(rows[0] or "").strip()
        if not phone:
            raise ValueError("No caller ID numbers are available in the queue.")
        return phone

    def dequeue_many(self, scope_id, count):
        count = max(0, int(count or 0))
        if count == 0:
            return []
        try:
            rows = self.client.request(
                "POST",
                "rpc/dequeue_caller_ids",
                {},
                {"p_scope_id": scope_id, "p_count": count},
            )
        except OSError as exc:
            if self._table_missing(exc):
                raise ValueError("Caller ID queue is not configured in Supabase.") from exc
            raise
        if not isinstance(rows, list) or len(rows) < count:
            raise ValueError("Not enough caller ID numbers are available in the queue.")
        return [str(item or "").strip() for item in rows]


def CallerIdQueueStore(*, client=None, crm_path=None):
    if client is not None:
        return SupabaseCallerIdQueueStore(client)
    return LocalCallerIdQueueStore(crm_path or Path("crm_data"))


def sync_dialer_caller_pool(state, *, bootstrap=False):
    store = getattr(state, "caller_id_queue_store", None)
    if not store:
        state.callers = list(DEFAULT_CALLER_ID_POOL)
        return state.callers
    scope = queue_scope_id(state)
    try:
        if bootstrap or not getattr(state, "_caller_queue_ready", False):
            store.ensure_pool(scope)
            state._caller_queue_ready = True
        state.callers = store.list_ordered(scope)
    except (OSError, ValueError):
        state.callers = list(DEFAULT_CALLER_ID_POOL)
    if not state.callers:
        state.callers = list(DEFAULT_CALLER_ID_POOL)
    return state.callers


def public_queue_view(state):
    store = getattr(state, "caller_id_queue_store", None)
    scope = queue_scope_id(state)
    if store:
        try:
            ordered = store.list_ordered(scope)
        except OSError:
            ordered = list(state.callers or DEFAULT_CALLER_ID_POOL)
    else:
        ordered = list(state.callers or DEFAULT_CALLER_ID_POOL)
    in_use = in_use_from_state(state)
    dialing_active = dialing_active_on_state(state)
    return build_caller_id_queue_view(ordered, in_use, dialing_active)