"""Usage event recording (Supabase) and HTTP routes for tab focus."""

import time
import urllib.parse

from features import org, org_storage
from shared.infra import utc_now
from shared.vocabulary import DEFAULT_USAGE_TIMELINE_MINUTES, USAGE_EVENT_KINDS, USAGE_TAB_THROTTLE_SECONDS


def client_for_dialer(dialer):
    crm = getattr(dialer, "crm", None)
    return getattr(crm, "client", None)


def _org_context(dialer):
    user_id = getattr(dialer, "account_user_id", None)
    membership = getattr(dialer, "org_membership", None) or {}
    org_id = str(membership.get("org_id") or "")
    if not user_id or not org_id:
        return None, None, None
    client = client_for_dialer(dialer)
    if not client:
        return None, None, None
    return client, str(user_id), org_id


def record(dialer, kind, payload=None):
    if kind not in USAGE_EVENT_KINDS:
        return
    client, user_id, org_id = _org_context(dialer)
    if not client:
        return
    body = dict(payload or {})
    try:
        org_storage.insert_usage_event(client, org_id, user_id, kind, body)
    except OSError:
        pass


def maybe_record_stage(dialer, stage):
    stage = str(stage or "idle")
    last = getattr(dialer, "_usage_last_stage", None)
    if last == stage:
        return
    dialer._usage_last_stage = stage
    record(dialer, "stage_change", {"stage": stage})


def record_tab_focus(dialer, tab):
    tab = str(tab or "").strip()
    if not tab:
        return
    now = time.monotonic()
    last = float(getattr(dialer, "_usage_tab_at", 0) or 0)
    if now - last < USAGE_TAB_THROTTLE_SECONDS:
        return
    dialer._usage_tab_at = now
    record(dialer, "tab_focus", {"tab": tab})


def member_usage_payload(runtime, dialer, member_user_id, minutes=None):
    from datetime import timedelta

    client = runtime.client
    membership = getattr(dialer, "org_membership", None) or {}
    org_id = org.assert_can_view_member(client, dialer.account_user_id, membership, member_user_id)
    try:
        window = int(minutes if minutes is not None else DEFAULT_USAGE_TIMELINE_MINUTES)
    except (TypeError, ValueError):
        window = DEFAULT_USAGE_TIMELINE_MINUTES
    window = max(5, min(240, window))
    since = (utc_now() - timedelta(minutes=window)).isoformat()
    events = org_storage.list_usage_events(client, org_id, str(member_user_id), since_iso=since)
    return {
        "user_id": str(member_user_id),
        "minutes": window,
        "events": events,
    }


def get_member_usage(request, member_user_id):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
    minutes = (query.get("minutes") or [None])[-1]
    try:
        request.send_json(200, member_usage_payload(
            request.runtime,
            request.account.dialer,
            member_user_id,
            minutes=minutes,
        ))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


def post_tab_focus(request, data):
    record_tab_focus(request.account.dialer, data.get("tab"))
    request.send_response(204)
    request.send_header("Content-Length", "0")
    request.send_header("Cache-Control", "no-store")
    request.end_headers()


ROUTES = [
    ("GET", "/api/team/members/{user_id}/usage", get_member_usage, "GET reads"),
    ("POST", "/api/usage/tab", post_tab_focus, "POST"),
]