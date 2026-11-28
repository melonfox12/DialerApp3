"""Manager team roster, metrics, live snapshots, and presence."""

import time
import urllib.parse

from features import app_usage, org, org_storage
from features.metrics import SupabaseMetricsStore
from shared.vocabulary import TEAM_PRESENCE_WRITE_SECONDS


def maybe_record_presence(runtime, dialer, live_payload):
    client = getattr(runtime, "client", None)
    user_id = getattr(dialer, "account_user_id", None)
    membership = getattr(dialer, "org_membership", None) or {}
    org_id = membership.get("org_id")
    if not client or not user_id or not org_id:
        return
    now = time.monotonic()
    last = float(getattr(dialer, "_team_presence_at", 0) or 0)
    if now - last < TEAM_PRESENCE_WRITE_SECONDS:
        return
    delta = (now - last) if last > 0 else 0.0
    if not getattr(dialer, "_app_usage_state", None):
        row = org_storage.get_presence(client, user_id)
        dialer._app_usage_state = app_usage.state_from_presence(row) if row else app_usage.empty_state()
    app_usage.apply_tick(dialer._app_usage_state, delta_seconds=delta)
    dialer._team_presence_at = now
    pending = app_usage.pop_pending_browser_session_close(dialer._app_usage_state)
    if pending:
        try:
            org_storage.insert_usage_event(client, org_id, user_id, "browser_session", pending)
        except OSError:
            pass
    in_flight = live_payload.get("in_flight") if isinstance(live_payload, dict) else []
    usage_fields = app_usage.presence_fields_from_state(dialer._app_usage_state)
    org_storage.upsert_presence(client, user_id, org_id, {
        "running": bool(live_payload.get("running")),
        "paused": bool(live_payload.get("paused")),
        "stage": live_payload.get("stage") or "idle",
        "active_lead_id": live_payload.get("active_lead_id") or "",
        "in_flight_count": len(in_flight) if isinstance(in_flight, list) else 0,
        **usage_fields,
    })


def _member_contact(client, user_id, member_row, profiles):
    profile = profiles.get(str(user_id or "")) or {}
    email = profile.get("email") or member_row.get("invited_email") or ""
    display = profile.get("display_name") or email.split("@")[0] if email else "Team member"
    return {"email": email, "display_name": display}


def _browser_live_account(runtime, user_id):
    """In-memory dialer state only counts as online while the browser is still polling."""
    if not runtime or not user_id:
        return None
    account = runtime.sessions.get(user_id)
    if account and account.client_is_online():
        return account
    return None


def _today_metrics(metrics_store):
    snap = metrics_store.snapshot(days=1)
    today = snap.get("today") or {}
    return {
        "dials": int(today.get("dials") or 0),
        "connected": int(today.get("connected") or 0),
        "booked": int(today.get("booked") or 0),
        "talk_seconds": int(today.get("talk_seconds") or 0),
    }


def _roster_row(client, runtime, org_id, member_row, profiles, presence_by_user):
    user_id = str(member_row.get("user_id") or "")
    status = str(member_row.get("status") or "")
    contact = _member_contact(client, user_id, member_row, profiles)
    presence = presence_by_user.get(user_id) or {}
    online = org.presence_is_online(presence.get("last_seen_at")) if user_id else False
    live = None
    live_dialer = None
    account = _browser_live_account(runtime, user_id)
    if account:
        live_dialer = account.dialer
        view = account.dialer.live_state()
        live = {
            "stage": view.get("stage") or "idle",
            "running": bool(view.get("running")),
            "paused": bool(view.get("paused")),
            "in_flight_count": len(view.get("in_flight") or []),
            "active_lead_id": view.get("active_lead_id") or "",
        }
        online = True
    row = {
        "user_id": user_id,
        "email": contact["email"],
        "display_name": contact["display_name"],
        "role": str(member_row.get("role") or ""),
        "status": status,
        "online": online,
        "presence": {
            "stage": (live or {}).get("stage") or presence.get("stage") or "idle",
            "running": (live or {}).get("running", presence.get("running")),
            "paused": (live or {}).get("paused", presence.get("paused")),
            "in_flight_count": (live or {}).get("in_flight_count", presence.get("in_flight_count") or 0),
            "last_seen_at": presence.get("last_seen_at") or "",
        },
        "app_usage": app_usage.app_usage_for_view(presence, live_dialer),
    }
    if user_id and status == "active":
        metrics = SupabaseMetricsStore(client, user_id=user_id)
        row["today"] = _today_metrics(metrics)
    else:
        row["today"] = {"dials": 0, "connected": 0, "booked": 0, "talk_seconds": 0}
    return row


def roster_payload(runtime, dialer):
    client = runtime.client
    membership = getattr(dialer, "org_membership", None) or {}
    if not org.can_manage_team(membership.get("role")):
        raise PermissionError("Team views are available to managers and owners only.")
    org_id = str(membership.get("org_id") or "")
    if not org_id:
        raise PermissionError("You are not part of an organization yet.")
    members = org_storage.list_org_members(client, org_id)
    user_ids = [str(row["user_id"]) for row in members if row.get("user_id")]
    profiles = org_storage.get_profiles(client, user_ids)
    presence_by_user = org_storage.list_presence_for_org(client, org_id)
    roster = [_roster_row(client, runtime, org_id, row, profiles, presence_by_user) for row in members]
    return {
        "org_id": org_id,
        "org_name": membership.get("org_name") or "",
        "members": roster,
    }


def member_metrics_payload(runtime, dialer, member_user_id, days=7):
    client = runtime.client
    membership = getattr(dialer, "org_membership", None) or {}
    org.assert_can_view_member(client, dialer.account_user_id, membership, member_user_id)
    try:
        days = max(1, min(90, int(days)))
    except (TypeError, ValueError):
        days = 7
    metrics = SupabaseMetricsStore(client, user_id=str(member_user_id))
    return {"user_id": str(member_user_id), "metrics": metrics.snapshot(days=days)}


def member_live_payload(runtime, dialer, member_user_id):
    client = runtime.client
    membership = getattr(dialer, "org_membership", None) or {}
    org.assert_can_view_member(client, dialer.account_user_id, membership, member_user_id)
    target = str(member_user_id)
    presence = org_storage.list_presence_for_org(client, membership["org_id"]).get(target) or {}
    account = _browser_live_account(runtime, target)
    if account:
        app_usage.hydrate_app_usage_state(account.dialer, presence, client=client, user_id=target)
        view = account.dialer.live_state()
        active = view.get("active_lead") or {}
        return {
            "user_id": target,
            "online": True,
            "source": "live",
            "stage": view.get("stage") or "idle",
            "running": bool(view.get("running")),
            "paused": bool(view.get("paused")),
            "in_flight_count": len(view.get("in_flight") or []),
            "active_lead_id": view.get("active_lead_id") or "",
            "active_lead_name": active.get("name") or active.get("contact_name") or "",
            "session_stats": view.get("session_stats") or {},
            "app_usage": app_usage.app_usage_for_view(presence, account.dialer),
        }
    return {
        "user_id": target,
        "online": org.presence_is_online(presence.get("last_seen_at")),
        "source": "presence",
        "stage": presence.get("stage") or "idle",
        "running": bool(presence.get("running")),
        "paused": bool(presence.get("paused")),
        "in_flight_count": int(presence.get("in_flight_count") or 0),
        "active_lead_id": presence.get("active_lead_id") or "",
        "active_lead_name": "",
        "session_stats": {},
        "last_seen_at": presence.get("last_seen_at") or "",
        "app_usage": app_usage.app_usage_for_view(presence),
    }


def get_roster(request):
    try:
        request.send_json(200, roster_payload(request.runtime, request.account.dialer))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


def get_member_metrics(request, member_user_id):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
    days = (query.get("days") or ["7"])[-1]
    try:
        request.send_json(200, member_metrics_payload(request.runtime, request.account.dialer, member_user_id, days=days))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


def get_member_live(request, member_user_id):
    try:
        request.send_json(200, member_live_payload(request.runtime, request.account.dialer, member_user_id))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


def post_invite(request, data):
    dialer = request.account.dialer
    membership = getattr(dialer, "org_membership", None) or {}
    if not org.can_manage_team(membership.get("role")):
        request.send_json(403, {"error": "Only managers and owners can invite team members."})
        return
    org_id = str(membership.get("org_id") or "")
    if not org_id:
        request.send_json(403, {"error": "You are not part of an organization yet."})
        return
    role = str(data.get("role") or "rep").strip().lower()
    if role not in ("rep", "manager"):
        request.send_json(400, {"error": "Invite role must be rep or manager."})
        return
    try:
        row = org_storage.invite_member(request.runtime.client, org_id, data.get("email"), role=role)
        org.clear_membership_cache()
        request.send_json(200, {
            "invite": {
                "id": str(row.get("id") or ""),
                "invited_email": row.get("invited_email") or "",
                "role": row.get("role") or "",
                "status": row.get("status") or "",
            }
        })
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


ROUTES = [
    ("GET", "/api/team/roster", get_roster, "GET reads"),
    ("GET", "/api/team/members/{user_id}/metrics", get_member_metrics, "GET reads"),
    ("GET", "/api/team/members/{user_id}/live", get_member_live, "GET reads"),
    ("POST", "/api/team/invites", post_invite, "POST"),
]