"""Prospect row shape (DB snake_case), API JSON, and CSV header mapping."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any

LEAD_TIERS = ("A", "B", "C", "D")

REMOVED_HEADER_TOKENS = frozenset({
    "score",
    "websitephone",
    "phonesource",
    "websitephonesource",
    "websitesource",
    "websiteconfidence",
    "websiteevidence",
    "previouswebsite",
    "extractedwebsite",
    "sourceid",
    "matchedaddress",
    "lookupnotes",
    "propertyuse",
    "dayssincesignal",
})

PROSPECT_DB_COLUMNS = (
    "id",
    "user_id",
    "created_at",
    "updated_at",
    "archived_at",
    "company",
    "contact_name",
    "office_manager",
    "phone",
    "alt_phone",
    "email",
    "street",
    "city",
    "state",
    "zip",
    "lead_tier",
    "lead_score",
    "score_reasons",
    "signal",
    "signal_date",
    "now_open_or_moved",
    "category",
    "property_type",
    "hygiene_focus",
    "website",
    "county",
    "providers_listed",
    "source",
    "source_file",
    "property_verdict",
    "residential_check",
    "remote_or_mobile",
    "shared_address",
    "suite_in_address",
    "status",
    "scheduled_until",
    "timezone",
    "transcript",
    "call_log",
    "pipeline_step",
    "pipeline_step_entered_at",
    "pipeline_history",
    "status_history",
    "booked_at",
    "passed_at",
    "agent_reserved_name",
    "agent_reserved_id",
)

REP_FACING_KEYS = (
    "company",
    "contact_name",
    "office_manager",
    "phone",
    "alt_phone",
    "email",
    "street",
    "city",
    "state",
    "zip",
    "lead_tier",
    "lead_score",
    "score_reasons",
    "signal",
    "signal_date",
    "now_open_or_moved",
    "category",
    "property_type",
    "hygiene_focus",
    "website",
)

INTERNAL_KEYS = (
    "county",
    "providers_listed",
    "source",
    "source_file",
    "property_verdict",
    "residential_check",
    "remote_or_mobile",
    "shared_address",
    "suite_in_address",
    "timezone",
)

WORKFLOW_KEYS = (
    "status",
    "scheduled_until",
    "transcript",
    "call_log",
    "pipeline_step",
    "pipeline_step_entered_at",
    "pipeline_history",
    "status_history",
    "booked_at",
    "passed_at",
    "agent_reserved_name",
    "agent_reserved_id",
)

# CamelCase keys for TypeScript / generated types (wire format matches snake_case in JSON API).
CAMEL_BY_SNAKE = {
    "contact_name": "contactName",
    "office_manager": "officeManager",
    "alt_phone": "altPhone",
    "lead_tier": "leadTier",
    "lead_score": "leadScore",
    "score_reasons": "scoreReasons",
    "signal_date": "signalDate",
    "now_open_or_moved": "nowOpenOrMoved",
    "property_type": "propertyType",
    "hygiene_focus": "hygieneFocus",
    "providers_listed": "providersListed",
    "source_file": "sourceFile",
    "property_verdict": "propertyVerdict",
    "residential_check": "residentialCheck",
    "remote_or_mobile": "remoteOrMobile",
    "shared_address": "sharedAddress",
    "suite_in_address": "suiteInAddress",
    "created_at": "createdAt",
    "updated_at": "updatedAt",
    "archived_at": "archivedAt",
    "scheduled_until": "scheduledUntil",
    "call_log": "callLog",
    "pipeline_step": "pipelineStep",
    "pipeline_step_entered_at": "pipelineStepEnteredAt",
    "pipeline_history": "pipelineHistory",
    "status_history": "statusHistory",
    "booked_at": "bookedAt",
    "passed_at": "passedAt",
    "days_since_signal": "daysSinceSignal",
}


def normalize_header(label: str) -> str:
    return re.sub(r"[\s_]+", "", str(label or "").strip().lower())


_HEADER_TO_FIELD = {
    "prospect": "contact_name",
    "name": "contact_name",
    "contactname": "contact_name",
    "contact": "contact_name",
    "company": "company",
    "business": "company",
    "businessname": "company",
    "organization": "company",
    "organisation": "company",
    "officemanager": "office_manager",
    "phone": "phone",
    "phonenumber": "phone",
    "websitephone": "phone",
    "mobile": "phone",
    "cell": "phone",
    "telephone": "phone",
    "businessphone": "phone",
    "altphone": "alt_phone",
    "alternatephone": "alt_phone",
    "phone2": "alt_phone",
    "email": "email",
    "street": "street",
    "address": "street",
    "city": "city",
    "state": "state",
    "zip": "zip",
    "zipcode": "zip",
    "postal": "zip",
    "leadtier": "lead_tier",
    "tier": "lead_tier",
    "leadscore": "lead_score",
    "scorereasons": "score_reasons",
    "signal": "signal",
    "signaldate": "signal_date",
    "nowopenormoved": "now_open_or_moved",
    "nowopen": "now_open_or_moved",
    "category": "category",
    "businesstype": "category",
    "industry": "category",
    "propertytype": "property_type",
    "hygienefocus": "hygiene_focus",
    "website": "website",
    "url": "website",
    "extractedwebsite": "website",
    "previouswebsite": "website",
    "county": "county",
    "providerslisted": "providers_listed",
    "source": "source",
    "sourcefile": "source_file",
    "propertyverdict": "property_verdict",
    "residentialcheck": "residential_check",
    "remotemobile": "remote_or_mobile",
    "remoteormobile": "remote_or_mobile",
    "sharedaddress": "shared_address",
    "suiteinaddress": "suite_in_address",
    "timezone": "timezone",
    "tz": "timezone",
    "callstatus": "status",
    "status": "status",
}

# Headers we intentionally ignore (removed legacy columns).
_IGNORE_HEADERS = REMOVED_HEADER_TOKENS | frozenset({"id", "uuid", "leadid", "prospectid"})


def map_csv_header(label: str) -> str | None:
    key = normalize_header(label)
    if key in _IGNORE_HEADERS:
        return None
    if key in _HEADER_TO_FIELD:
        return _HEADER_TO_FIELD[key]
    if key == "score":
        return "__score_fallback__"
    return None


def display_name(lead: dict) -> str:
    return (
        str(lead.get("contact_name") or "").strip()
        or str(lead.get("company") or "").strip()
        or str(lead.get("phone") or "").strip()
        or "Prospect"
    )


def days_since_signal(lead: dict, *, today: date | None = None) -> int | None:
    raw = lead.get("signal_date")
    if not raw:
        return None
    try:
        if isinstance(raw, date):
            signal_day = raw
        else:
            signal_day = date.fromisoformat(str(raw)[:10])
    except ValueError:
        return None
    ref = today or datetime.now(timezone.utc).date()
    return max(0, (ref - signal_day).days)


def _coerce_bool(value: Any) -> bool | None:
    if value is None or value == "":
        return None
    text = str(value).strip().lower()
    if text in ("1", "true", "yes", "y"):
        return True
    if text in ("0", "false", "no", "n"):
        return False
    return None


def row_from_db(record: dict) -> dict:
    """Normalize a Supabase prospects row into an in-memory lead dict."""
    if not isinstance(record, dict):
        raise ValueError("Invalid prospect row")
    lead = {key: record.get(key) for key in PROSPECT_DB_COLUMNS if key in record or key not in ("user_id",)}
    lead["id"] = str(record.get("id", ""))
    if record.get("user_id"):
        lead["user_id"] = str(record["user_id"])
    for key in ("transcript", "call_log", "pipeline_history", "status_history"):
        if lead.get(key) is None:
            lead[key] = []
    lead["days_since_signal"] = days_since_signal(lead)
    return lead


_SKIP_DB_WRITE = frozenset({"days_since_signal"})


def db_payload_from_lead(lead: dict, *, user_id: str | None = None, for_insert: bool = False) -> dict:
    payload = {}
    for key in PROSPECT_DB_COLUMNS:
        if key in _SKIP_DB_WRITE:
            continue
        if key == "id" and for_insert:
            continue
        if key == "user_id":
            if user_id:
                payload["user_id"] = user_id
            continue
        if key in lead:
            payload[key] = lead[key]
    if not for_insert and lead.get("id"):
        payload["id"] = lead["id"]
    return payload


def is_archived(lead: dict) -> bool:
    return bool(lead.get("archived_at"))


def active_leads(leads: list[dict]) -> list[dict]:
    return [lead for lead in leads if not is_archived(lead)]