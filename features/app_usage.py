"""Browser app-time accumulation from /api/live heartbeats (signed-in tab open)."""

import time
from datetime import date, datetime, timezone

from shared.vocabulary import APP_SESSION_GAP_SECONDS, APP_USAGE_MAX_TICK_SECONDS


def utc_now():
    return datetime.now(timezone.utc)


def utc_today():
    return utc_now().date()


def utc_week_key(day=None):
    day = day or utc_today()
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def utc_month_key(day=None):
    day = day or utc_today()
    return f"{day.year}-{day.month:02d}"


def parse_iso(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _rollover_seconds(row, key_field, seconds_field, current_key):
    stored = str(row.get(key_field) or "").strip()
    if stored != current_key:
        return 0
    return max(0, int(row.get(seconds_field) or 0))


def empty_state(now=None):
    now = now or utc_now()
    today = utc_today()
    return {
        "app_today_date": today.isoformat(),
        "app_today_seconds": 0,
        "app_week_key": utc_week_key(today),
        "app_week_seconds": 0,
        "app_month_key": utc_month_key(today),
        "app_month_seconds": 0,
        "app_session_seconds": 0,
        "app_session_started_at": now.isoformat(),
        "last_seen_at": now.isoformat(),
    }


def _session_gap_seconds(last_seen, now):
    if not last_seen:
        return None
    return (now - last_seen).total_seconds()


def _close_browser_session(state, *, now, ended_at=None):
    """End the current live session; return a Supabase payload when time was tracked."""
    seconds = max(0, int(state.get("app_session_seconds") or 0))
    started_at = state.get("app_session_started_at") or ""
    state["app_session_seconds"] = 0
    state["app_session_started_at"] = now.isoformat()
    if seconds <= 0:
        return None
    end = ended_at or now
    return {
        "seconds": seconds,
        "started_at": started_at or end.isoformat(),
        "ended_at": end.isoformat(),
    }


def state_from_presence(row, now=None):
    now = now or utc_now()
    row = row or {}
    today = utc_today()
    week_key = utc_week_key(today)
    month_key = utc_month_key(today)

    today_date = str(row.get("app_today_date") or "")[:10] or today.isoformat()
    try:
        if date.fromisoformat(today_date) != today:
            today_seconds = 0
            today_date = today.isoformat()
        else:
            today_seconds = int(row.get("app_today_seconds") or 0)
    except ValueError:
        today_date = today.isoformat()
        today_seconds = 0

    week_seconds = _rollover_seconds(row, "app_week_key", "app_week_seconds", week_key)
    month_seconds = _rollover_seconds(row, "app_month_key", "app_month_seconds", month_key)

    last_seen = parse_iso(row.get("last_seen_at"))
    session_seconds = int(row.get("app_session_seconds") or 0)
    session_started = row.get("app_session_started_at") or ""
    pending_close = None
    gap = _session_gap_seconds(last_seen, now)
    if gap is not None and gap > APP_SESSION_GAP_SECONDS:
        state_stub = {
            "app_session_seconds": session_seconds,
            "app_session_started_at": session_started or (last_seen.isoformat() if last_seen else ""),
        }
        pending_close = _close_browser_session(state_stub, now=now, ended_at=last_seen or now)
        session_seconds = 0
        session_started = now.isoformat()
    elif not session_started:
        session_started = row.get("last_seen_at") or now.isoformat()

    out = {
        "app_today_date": today_date,
        "app_today_seconds": max(0, today_seconds),
        "app_week_key": week_key,
        "app_week_seconds": week_seconds,
        "app_month_key": month_key,
        "app_month_seconds": month_seconds,
        "app_session_seconds": max(0, session_seconds),
        "app_session_started_at": session_started,
        "last_seen_at": (last_seen or now).isoformat(),
    }
    if pending_close:
        out["_pending_browser_session_close"] = pending_close
    return out


def apply_tick(state, *, delta_seconds, now=None, online_gap_seconds=None):
    """Add capped active seconds; reset browser session after an offline gap."""
    now = now or utc_now()
    state = state or empty_state(now=now)
    today = utc_today()
    week_key = utc_week_key(today)
    month_key = utc_month_key(today)

    stored_day = str(state.get("app_today_date") or "")[:10]
    try:
        if date.fromisoformat(stored_day) != today:
            state["app_today_date"] = today.isoformat()
            state["app_today_seconds"] = 0
    except ValueError:
        state["app_today_date"] = today.isoformat()
        state["app_today_seconds"] = 0

    if str(state.get("app_week_key") or "") != week_key:
        state["app_week_key"] = week_key
        state["app_week_seconds"] = 0
    if str(state.get("app_month_key") or "") != month_key:
        state["app_month_key"] = month_key
        state["app_month_seconds"] = 0

    gap = online_gap_seconds
    if gap is None:
        last_seen = parse_iso(state.get("last_seen_at"))
        if last_seen:
            gap = (now - last_seen).total_seconds()
    pending_close = None
    if gap is not None and gap > APP_SESSION_GAP_SECONDS:
        pending_close = _close_browser_session(state, now=now)

    tick = max(0.0, min(float(delta_seconds or 0), float(APP_USAGE_MAX_TICK_SECONDS)))
    added = int(round(tick))
    state["app_session_seconds"] = int(state.get("app_session_seconds") or 0) + added
    state["app_today_seconds"] = int(state.get("app_today_seconds") or 0) + added
    state["app_week_seconds"] = int(state.get("app_week_seconds") or 0) + added
    state["app_month_seconds"] = int(state.get("app_month_seconds") or 0) + added
    state["last_seen_at"] = now.isoformat()
    if not state.get("app_session_started_at"):
        state["app_session_started_at"] = now.isoformat()
    if pending_close:
        state["_pending_browser_session_close"] = pending_close
    return state


def pop_pending_browser_session_close(state):
    if not state:
        return None
    return state.pop("_pending_browser_session_close", None)


def presence_fields_from_state(state):
    """Presence upsert body fragment; drops ephemeral session-close markers."""
    fields = dict(state or {})
    fields.pop("_pending_browser_session_close", None)
    return fields


def live_extra_seconds(dialer):
    last = float(getattr(dialer, "_team_presence_at", 0) or 0)
    if last <= 0:
        return 0
    delta = time.monotonic() - last
    return int(min(max(0.0, delta), float(APP_USAGE_MAX_TICK_SECONDS)))


def _minutes(seconds):
    return round(max(0, int(seconds)) / 60, 1)


def public_app_usage(state, *, live_extra_seconds=0):
    state = state or empty_state()
    extra = max(0, int(live_extra_seconds or 0))
    today = int(state.get("app_today_seconds") or 0) + extra
    week = int(state.get("app_week_seconds") or 0) + extra
    month = int(state.get("app_month_seconds") or 0) + extra
    session = int(state.get("app_session_seconds") or 0) + extra
    return {
        "app_seconds_today": today,
        "app_seconds_week": week,
        "app_seconds_month": month,
        "app_seconds_session": session,
        "app_minutes_today": _minutes(today),
        "app_minutes_week": _minutes(week),
        "app_minutes_month": _minutes(month),
        "app_minutes_session": _minutes(session),
        "app_week_key": state.get("app_week_key") or utc_week_key(),
        "app_month_key": state.get("app_month_key") or utc_month_key(),
        "app_session_started_at": state.get("app_session_started_at") or "",
    }


_PERIOD_SECOND_KEYS = (
    "app_today_seconds",
    "app_week_seconds",
    "app_month_seconds",
    "app_session_seconds",
)


def hydrate_app_usage_state(dialer, presence_row, *, client=None, user_id=None):
    """Load persisted Supabase counters into an in-memory dialer session if missing."""
    if dialer is None or getattr(dialer, "_app_usage_state", None):
        return
    row = presence_row
    if client and user_id:
        try:
            from features import org_storage

            full = org_storage.get_presence(client, user_id)
            if full:
                row = full
        except OSError:
            pass
    dialer._app_usage_state = state_from_presence(row or {})


def merged_usage_state(presence_row, dialer=None):
    """Combine persisted presence with live session counters (never drop stored totals)."""
    stored = state_from_presence(presence_row or {})
    if dialer is None or not getattr(dialer, "_app_usage_state", None):
        return stored
    live = dialer._app_usage_state
    merged = dict(stored)
    for key in ("app_today_seconds", "app_week_seconds", "app_month_seconds"):
        merged[key] = max(int(stored.get(key) or 0), int(live.get(key) or 0))
    merged["app_session_seconds"] = max(0, int(live.get("app_session_seconds") or 0))
    for key in ("app_today_date", "app_week_key", "app_month_key", "app_session_started_at", "last_seen_at"):
        if live.get(key):
            merged[key] = live.get(key)
    return merged


def usage_summary_from_app_payload(app_payload):
    """API-facing usage cards (minutes, one decimal)."""
    app_payload = app_payload or {}
    return {
        "live_session_minutes": float(app_payload.get("app_minutes_session") or 0),
        "today_minutes": float(app_payload.get("app_minutes_today") or 0),
        "week_minutes": float(app_payload.get("app_minutes_week") or 0),
        "month_minutes": float(app_payload.get("app_minutes_month") or 0),
    }


def app_usage_for_view(presence_row, dialer=None):
    """Presence row from DB, optional live dialer for same-server minute updates."""
    merged = merged_usage_state(presence_row, dialer)
    extra = live_extra_seconds(dialer) if dialer is not None else 0
    return public_app_usage(merged, live_extra_seconds=extra)