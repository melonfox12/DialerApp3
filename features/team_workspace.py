"""Manager workspace: per-member settings (with credentials) and analytics."""

import urllib.parse
from collections import Counter
from datetime import datetime, timedelta, timezone

from features import org, org_storage, settings as settings_feature
from features.metrics import MetricsStore, SupabaseMetricsStore
from shared.config import ENV_PATH
from shared.infra import utc_now
from shared.vocabulary import CALL_OUTCOME_KEYS, CONVERSATION_MIN_SECONDS


def _empty_metrics_snapshot():
    return {"today": {}, "daily": [], "all_time": {}, "series": []}


def _safe_metrics_snapshot(store, days=30):
    try:
        snap = store.snapshot(days=days)
        if "daily" not in snap and "series" in snap:
            snap["daily"] = snap.get("series") or []
        return snap
    except OSError as exc:
        message = str(exc).lower()
        if any(token in message for token in ("dialer_metric", "pgrst", "404", "does not exist", "could not read")):
            return _empty_metrics_snapshot()
        raise


def _metrics_store(runtime, user_id):
    client = getattr(runtime, "client", None)
    if client:
        return SupabaseMetricsStore(client, user_id=str(user_id))
    from features import accounts

    return MetricsStore(getattr(accounts, "METRICS_PATH", "metrics.json"))


def _sum_series(series, days, keys):
    if not series:
        return {key: 0 for key in keys}
    tail = series[-days:] if days else []
    totals = {key: 0 for key in keys}
    for row in tail:
        for key in keys:
            totals[key] += int(row.get(key) or 0)
    return totals


def _parse_event_time(value):
    try:
        moment = datetime.fromisoformat(str(value or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment


def _conversations_over_threshold(connected, talk_seconds):
    connected = int(connected or 0)
    talk_seconds = int(talk_seconds or 0)
    if connected <= 0:
        return 0
    if talk_seconds < CONVERSATION_MIN_SECONDS:
        return 0
    return min(connected, max(1, talk_seconds // CONVERSATION_MIN_SECONDS))


def _activity_for_span(span, session_stats, today_row, series):
    session_stats = session_stats or {}
    if span == "session":
        dials = int(session_stats.get("dials") or 0)
        connected = int(session_stats.get("connects") or session_stats.get("connected") or 0)
        talk = int(session_stats.get("talk_seconds") or 0)
        conversations = int(session_stats.get("conversations") or 0)
        if conversations <= 0:
            conversations = _conversations_over_threshold(connected, talk)
        return {"dials": dials, "connected": connected, "conversations_30s": conversations}
    if span == "today":
        bucket = today_row or {}
        connected = int(bucket.get("connected") or 0)
        talk = int(bucket.get("talk_seconds") or 0)
        return {
            "dials": int(bucket.get("dials") or 0),
            "connected": connected,
            "conversations_30s": _conversations_over_threshold(connected, talk),
        }
    days = 7 if span == "week" else 30
    totals = _sum_series(series, days, ("dials", "connected"))
    talk = int((today_row or {}).get("talk_seconds") or 0)
    connected = totals.get("connected", 0)
    return {
        "dials": totals.get("dials", 0),
        "connected": connected,
        "conversations_30s": _conversations_over_threshold(connected, talk),
    }


def _dispositions(client, org_id, user_id, since_iso):
    if not client:
        return []
    try:
        events = org_storage.list_usage_events(client, org_id, str(user_id), since_iso=since_iso)
    except OSError:
        return []
    counter = Counter()
    for event in events:
        if str(event.get("kind") or "") != "disposition":
            continue
        status = str((event.get("payload") or {}).get("status") or "unknown")
        counter[status] += 1
    rows = [{"key": key, "label": key.replace("_", " "), "count": count} for key, count in counter.most_common()]
    if rows:
        return rows
    return [{"key": key, "label": key.replace("_", " "), "count": 0} for key in CALL_OUTCOME_KEYS[:5]]


def _since_for_span(span):
    now = utc_now()
    if span == "session":
        return now - timedelta(hours=8)
    if span == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if span == "week":
        return now - timedelta(days=7)
    return now - timedelta(days=30)


def _line_series(metrics_snap, timeline, usage_events):
    series = metrics_snap.get("daily") or metrics_snap.get("series") or []
    if timeline == "month":
        points = []
        for row in series[-30:]:
            points.append({
                "t": row.get("date"),
                "value": int(row.get("dials") or 0),
            })
        return points
    if timeline == "week":
        points = []
        for row in series[-7:]:
            points.append({
                "t": row.get("date"),
                "value": int(row.get("dials") or 0),
            })
        return points
    # 8h — bucket usage events by hour
    now = utc_now()
    start = now - timedelta(hours=8)
    buckets = []
    for hour in range(8):
        edge = start + timedelta(hours=hour)
        end = edge + timedelta(hours=1)
        count = 0
        for event in usage_events or []:
            moment = _parse_event_time(event.get("at"))
            if not moment:
                continue
            if edge <= moment < end and str(event.get("kind") or "") in ("connect", "disposition", "session_start"):
                count += 1
        buckets.append({"t": edge.isoformat(), "value": count})
    if any(point["value"] for point in buckets):
        return buckets
    today_dials = int((metrics_snap.get("today") or {}).get("dials") or 0)
    return [{"t": start.isoformat(), "value": today_dials}]


def _assert_member_view(runtime, dialer, member_user_id):
    client = getattr(runtime, "client", None)
    membership = getattr(dialer, "org_membership", None) or {}
    if client:
        return org.assert_can_view_member(client, dialer.account_user_id, membership, member_user_id)
    if org.can_manage_team(membership.get("role")):
        return str(membership.get("org_id") or "local")
    if not client and getattr(runtime, "storage_name", "") == "local JSON files":
        return "local"
    raise PermissionError("Team views are available to managers and owners only.")


def member_analytics_payload(runtime, dialer, member_user_id, span="today", timeline="week"):
    client = getattr(runtime, "client", None)
    org_id = _assert_member_view(runtime, dialer, member_user_id)
    target = str(member_user_id)
    span = str(span or "today").strip().lower()
    if span not in ("session", "today", "week", "month"):
        span = "today"
    timeline = str(timeline or "week").strip().lower()
    if timeline not in ("8h", "week", "month"):
        timeline = "week"
    metrics_store = _metrics_store(runtime, target)
    snap = _safe_metrics_snapshot(metrics_store, days=30)
    today_row = snap.get("today") or {}
    series = snap.get("daily") or []
    session_stats = {}
    account = runtime.sessions.get(target) if getattr(runtime, "sessions", None) else None
    if account and account.client_is_online():
        session_stats = account.dialer.live_state().get("session_stats") or {}
    activity_bars = _activity_for_span(span, session_stats, today_row, series)
    since = _since_for_span(span)
    dispositions = _dispositions(client, org_id, target, since.isoformat())
    usage_events = []
    if client:
        try:
            usage_events = org_storage.list_usage_events(
                client,
                org_id,
                target,
                since_iso=(utc_now() - timedelta(hours=8)).isoformat(),
            )
        except OSError:
            usage_events = []
    line = _line_series(snap, timeline, usage_events)
    presence = {}
    if client and org_id and org_id != "local":
        try:
            presence = org_storage.list_presence_for_org(client, org_id).get(target) or {}
        except OSError:
            presence = {}
    from features import app_usage

    if account and client:
        app_usage.hydrate_app_usage_state(account.dialer, presence, client=client, user_id=target)
    app = app_usage.app_usage_for_view(presence, account.dialer if account else None)
    usage_summary = app_usage.usage_summary_from_app_payload(app)
    usage_summary["live_online"] = bool(account and account.client_is_online())
    return {
        "user_id": target,
        "span": span,
        "timeline": timeline,
        "usage_summary": usage_summary,
        "activity_bars": activity_bars,
        "dispositions": dispositions,
        "activity_line": line,
    }


def _member_settings_view(runtime, member_user_id, email=""):
    client = getattr(runtime, "client", None)
    if not client:
        from features import accounts

        account = getattr(runtime, "local", None)
        dialer = account.dialer if account else None
        values = dict(getattr(dialer, "account_values", None) or {})
        return settings_feature.settings_state(
            accounts.ENV_PATH,
            values,
            getattr(runtime, "storage_name", "local JSON files"),
            email,
            signed_in=False,
            include_credentials=True,
        )
    try:
        account_values = settings_feature.load_app_settings(client, member_user_id)
    except OSError:
        account_values = {}
    try:
        profile = (org_storage.get_profiles(client, [str(member_user_id)]) or {}).get(str(member_user_id)) or {}
    except OSError:
        profile = {}
    return settings_feature.settings_state(
        ENV_PATH,
        account_values,
        getattr(runtime, "storage_name", "Supabase"),
        email or profile.get("email") or "",
        signed_in=True,
        include_credentials=True,
    )


def member_settings_payload(runtime, dialer, member_user_id):
    _assert_member_view(runtime, dialer, member_user_id)
    view = _member_settings_view(runtime, member_user_id)
    view["user_id"] = str(member_user_id)
    view["managed_by_viewer"] = True
    return view


def save_member_settings(runtime, dialer, member_user_id, data):
    _assert_member_view(runtime, dialer, member_user_id)
    client = getattr(runtime, "client", None)
    if not client:
        from features import accounts

        account = getattr(runtime, "local", None)
        target = account.dialer if account else dialer
        values = dict(getattr(target, "account_values", None) or {})
        settings_feature.save_settings(
            accounts.ENV_PATH,
            values,
            getattr(target, "account_user_id", None),
            data,
            allow_credentials=True,
        )
        profile_email = getattr(target, "account_email", "")
        view = settings_feature.settings_state(
            accounts.ENV_PATH,
            values,
            getattr(runtime, "storage_name", "local JSON files"),
            profile_email,
            signed_in=False,
            include_credentials=True,
        )
        view["user_id"] = str(member_user_id)
        view["managed_by_viewer"] = True
        return view
    membership = getattr(dialer, "org_membership", None) or {}
    org.assert_can_view_member(client, dialer.account_user_id, membership, member_user_id)
    account_values = settings_feature.load_app_settings(client, member_user_id)

    def save_remote(stored):
        settings_feature.save_app_settings(client, stored, user_id=member_user_id)

    settings_feature.save_settings(
        ENV_PATH,
        account_values,
        member_user_id,
        data,
        save_remote,
        allow_credentials=True,
    )
    try:
        profile = (org_storage.get_profiles(client, [str(member_user_id)]) or {}).get(str(member_user_id)) or {}
    except OSError:
        profile = {}
    view = settings_feature.settings_state(
        ENV_PATH,
        account_values,
        getattr(runtime, "storage_name", "Supabase"),
        profile.get("email") or "",
        signed_in=True,
        include_credentials=True,
    )
    view["user_id"] = str(member_user_id)
    view["managed_by_viewer"] = True
    return view


def get_member_analytics(request, member_user_id):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
    span = (query.get("span") or ["today"])[-1]
    timeline = (query.get("timeline") or ["week"])[-1]
    try:
        request.send_json(
            200,
            member_analytics_payload(request.runtime, request.account.dialer, member_user_id, span=span, timeline=timeline),
        )
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request._trace_error = str(exc)
        fallback = _empty_analytics(member_user_id, span, timeline=timeline)
        fallback["storage_note"] = str(exc)
        request.send_json(200, fallback)


def _empty_analytics(member_user_id, span="today", timeline="week"):
    return {
        "user_id": str(member_user_id),
        "span": span,
        "timeline": timeline,
        "usage_summary": {
            "live_session_minutes": 0,
            "today_minutes": 0,
            "week_minutes": 0,
            "month_minutes": 0,
            "live_online": False,
        },
        "activity_bars": {"dials": 0, "connected": 0, "conversations_30s": 0},
        "dispositions": [],
        "activity_line": [],
        "partial": True,
    }


def get_member_settings(request, member_user_id):
    try:
        request.send_json(200, member_settings_payload(request.runtime, request.account.dialer, member_user_id))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request._trace_error = str(exc)
        request.send_json(200, {
            **_member_settings_view(request.runtime, member_user_id),
            "user_id": str(member_user_id),
            "managed_by_viewer": True,
            "partial": True,
            "storage_note": str(exc),
        })


def post_member_settings(request, member_user_id, data):
    try:
        request.send_json(200, save_member_settings(request.runtime, request.account.dialer, member_user_id, data))
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


ROUTES = [
    ("GET", "/api/team/members/{user_id}/analytics", get_member_analytics, "GET reads"),
    ("GET", "/api/team/members/{user_id}/settings", get_member_settings, "GET reads"),
    ("POST", "/api/team/members/{user_id}/settings", post_member_settings, "POST"),
]