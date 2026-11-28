"""Script performance from call_log script tags (industry, prospect_type, variation)."""

import urllib.parse
from collections import Counter, defaultdict
from datetime import timedelta

from features import org, performance
from features.call_scripts import (
    _normalize_industry,
    _normalize_prospect_type,
    _normalize_variation,
)
from features.prospects import ProspectStore
from shared.infra import utc_now
from shared.vocabulary import (
    CALL_SCRIPT_INDUSTRIES,
    CALL_SCRIPT_PROSPECT_TYPES,
    CALL_SCRIPT_VARIATIONS,
    DEFAULT_CALL_SCRIPT_VARIATION,
)


def _label_map(pairs):
    return {key: label for key, label in pairs}


INDUSTRY_LABELS = _label_map(CALL_SCRIPT_INDUSTRIES)
TYPE_LABELS = _label_map(CALL_SCRIPT_PROSPECT_TYPES)
VARIATION_LABELS = {str(k): label for k, label in CALL_SCRIPT_VARIATIONS}


def script_key_from_record(record):
    industry = _normalize_industry(record.get("script_industry"))
    prospect_type = _normalize_prospect_type(record.get("script_prospect_type"))
    variation = _normalize_variation(record.get("script_variation"))
    return industry, prospect_type, variation


def leads_for_subject(runtime, dialer, subject_user_id=None):
    """CRM snapshot for self or a team member (managers only for other users)."""
    if not subject_user_id or str(subject_user_id) == str(dialer.account_user_id or ""):
        return dialer.crm.snapshot()
    target = str(subject_user_id)
    client = getattr(runtime, "client", None)
    if not client:
        if dialer.account_user_id:
            return dialer.crm.snapshot()
        raise PermissionError("Team script analytics require Supabase.")
    membership = getattr(dialer, "org_membership", None) or {}
    org.assert_can_view_member(client, dialer.account_user_id, membership, target)
    store = ProspectStore(client=client, user_id=target)
    return store.snapshot()


def aggregate_segments(records, start, end):
    buckets = defaultdict(lambda: {
        "dials": 0,
        "connected": 0,
        "conversations": 0,
        "booked": 0,
        "talk_seconds": 0,
        "by_outcome": Counter(),
    })
    for record in records:
        if not performance.in_window(record["at"], start, end):
            continue
        key = script_key_from_record(record)
        bucket = buckets[key]
        bucket["dials"] += 1
        if record["connected"]:
            bucket["connected"] += 1
            bucket["talk_seconds"] += int(record.get("duration") or 0)
        if performance.is_conversation(record):
            bucket["conversations"] += 1
        outcome = record.get("outcome")
        if outcome:
            bucket["by_outcome"][str(outcome)] += 1
            if str(outcome) == "booked":
                bucket["booked"] += 1
    segments = []
    for (industry, prospect_type, variation), counts in sorted(buckets.items()):
        dials = counts["dials"]
        connected = counts["connected"]
        conversations = counts["conversations"]
        booked = counts["booked"]
        segments.append({
            "industry": industry,
            "prospect_type": prospect_type,
            "variation": variation,
            "industry_label": INDUSTRY_LABELS.get(industry, industry),
            "prospect_type_label": TYPE_LABELS.get(prospect_type, prospect_type),
            "variation_label": VARIATION_LABELS.get(str(variation), str(variation)),
            "counts": {
                "dials": dials,
                "connected": connected,
                "conversations": conversations,
                "booked": booked,
                "talk_seconds": counts["talk_seconds"],
            },
            "rates": {
                "connect_rate": performance.rate(connected, dials),
                "conversation_rate": performance.rate(conversations, connected),
                "book_rate": performance.rate(booked, dials),
            },
            "by_outcome": dict(counts["by_outcome"]),
        })
    return segments


def build_payload(leads, *, days=7, tz_name="", subject_user_id=None, subject_label=None):
    try:
        days = max(1, min(90, int(days)))
    except (TypeError, ValueError):
        days = 7
    zone = performance.local_zone(tz_name)
    now = utc_now()
    start = now - timedelta(days=days)
    end = now
    records = performance.call_records(leads)
    totals = performance.window_counts(records, leads, {}, start, end)
    return {
        "user_id": str(subject_user_id or ""),
        "subject_label": subject_label or "",
        "days": days,
        "timezone": getattr(zone, "key", "UTC"),
        "updated_at": now.isoformat(),
        "totals": totals,
        "segments": aggregate_segments(records, start, end),
        "industries": [{"key": k, "label": v} for k, v in CALL_SCRIPT_INDUSTRIES],
        "prospect_types": [{"key": k, "label": v} for k, v in CALL_SCRIPT_PROSPECT_TYPES],
        "variations": [{"key": k, "label": v} for k, v in CALL_SCRIPT_VARIATIONS],
    }


def payload_for_dialer(runtime, dialer, subject_user_id=None, days=7, tz_name=""):
    leads = leads_for_subject(runtime, dialer, subject_user_id)
    uid = str(subject_user_id or dialer.account_user_id or "")
    label = dialer.account_email if not subject_user_id or uid == str(dialer.account_user_id or "") else ""
    return build_payload(leads, days=days, tz_name=tz_name, subject_user_id=uid, subject_label=label)


def get_scripts_performance(request):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
    days = (query.get("days") or ["7"])[-1]
    tz_name = (query.get("tz") or [""])[-1]
    subject = (query.get("user_id") or [""])[-1].strip() or None
    dialer = request.account.dialer
    try:
        if subject and subject != str(dialer.account_user_id or ""):
            if not org.can_manage_team((dialer.org_membership or {}).get("role")):
                raise PermissionError("Only managers can view another member's script analytics.")
        payload = payload_for_dialer(request.runtime, dialer, subject_user_id=subject, days=days, tz_name=tz_name)
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
        return
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
        return
    except OSError as exc:
        request.report_storage_error(exc)
        return
    request.send_json(200, payload)


def get_member_scripts_performance(request, member_user_id):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
    days = (query.get("days") or ["7"])[-1]
    tz_name = (query.get("tz") or [""])[-1]
    dialer = request.account.dialer
    try:
        payload = payload_for_dialer(
            request.runtime,
            dialer,
            subject_user_id=member_user_id,
            days=days,
            tz_name=tz_name,
        )
    except PermissionError as exc:
        request._trace_error = str(exc)
        request.send_json(403, {"error": str(exc)})
        return
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
        return
    except OSError as exc:
        request.report_storage_error(exc)
        return
    request.send_json(200, payload)


ROUTES = [
    ("GET", "/api/scripts/performance", get_scripts_performance, "GET reads"),
    ("GET", "/api/team/members/{user_id}/scripts/performance", get_member_scripts_performance, "GET reads"),
]