"""CSV import and manual prospect construction for the normalized prospect schema."""

import csv
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from io import StringIO

from shared.infra import utc_now
from shared.prospect_schema import LEAD_TIERS, display_name, map_csv_header, normalize_header
from shared.vocabulary import (
    MANUAL_CALLBACK_HOURS,
    TIMEZONE_ALIASES,
    UTC_OFFSET_ZONES,
    parse_prospect_status,
)

SCIENTIFIC_NUMBER = re.compile(r"^(\d)(?:\.(\d+))?[eE]\+?(\d+)$")
TIMEZONE_ABBREVIATION = re.compile(r"\b(e[sd]t|c[sd]t|m[sd]t|p[sd]t|akst|akdt|hst)\b", re.I)


def _phone(value):
    text = str(value or "").strip()
    text = re.sub(r"^(?:tel|phone|mobile|cell)\s*:\s*", "", text, flags=re.I)
    text = re.sub(r"\s*(?:ext\.?|extension|x|#)\s*\d{1,6}\s*$", "", text, flags=re.I)
    scientific = SCIENTIFIC_NUMBER.match(text)
    if scientific:
        if len(scientific.group(1) + (scientific.group(2) or "")) < int(scientific.group(3)) + 1:
            return None
        try:
            text = str(int(Decimal(text)))
        except (InvalidOperation, OverflowError):
            return None
    elif re.fullmatch(r"\d+\.0+", text):
        text = text.split(".", 1)[0]
    if not re.fullmatch(r"\+?[\d\s().\-]+", text):
        return None
    digits = re.sub(r"\D", "", text)
    if text.startswith("00"):
        return "+" + digits[2:] if 8 <= len(digits) - 2 <= 15 else None
    if text.startswith("+") and 8 <= len(digits) <= 15:
        return "+" + digits
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    return None


def _timezone(value):
    text = str(value or "").strip()
    if not text:
        return None
    lower = text.lower()
    alias = TIMEZONE_ALIASES.get(lower) or TIMEZONE_ALIASES.get(lower.replace(" ", "_"))
    if alias:
        return alias
    for word, zone in (
        ("eastern", "Eastern"), ("central", "Central"), ("mountain", "Mountain"),
        ("pacific", "Pacific"), ("alaska", "Alaska"), ("hawaii", "Hawaii"),
    ):
        if word in lower:
            return zone
    abbrev = TIMEZONE_ABBREVIATION.search(lower)
    if abbrev:
        zone = TIMEZONE_ALIASES.get(abbrev.group(1))
        if zone:
            return zone
    if "utc" in lower or "gmt" in lower or re.fullmatch(r"[+-]\d{1,2}(:?\d{2})?", text):
        offset = re.search(r"([+-])\s?(\d{1,2})(?::?\d{2})?", text)
        if offset:
            hours = (-1 if offset.group(1) == "-" else 1) * int(offset.group(2))
            zone = UTC_OFFSET_ZONES.get(hours)
            if zone:
                return zone
    return text


def _text(value, *, limit=500):
    text = str(value if value is not None else "").strip()
    if len(text) > limit:
        raise ValueError("Field value is too long.")
    return text


def _state_code(value):
    text = _text(value, limit=8).upper()
    if not text:
        return ""
    if len(text) == 2 and text.isalpha():
        return text
    return text[:2] if len(text) >= 2 else text


def _tier(value):
    text = str(value or "").strip().upper()
    return text if text in LEAD_TIERS else "C"


def _score(value):
    text = str(value if value is not None else "").strip().replace(",", "")
    if not text:
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    return float(number)


def _date(value):
    text = str(value or "").strip()
    if not text:
        return None
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        try:
            return date.fromisoformat(text[:10])
        except ValueError:
            pass
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if match:
        try:
            return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return None
    return None


def _choose_dialect(text):
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.excel
    first = next((line for line in sample.splitlines() if line.strip()), "")
    if first.count(dialect.delimiter) == 0 and first.count(",") > 0:
        return csv.excel
    return dialect


def _read_csv(data):
    if isinstance(data, str):
        text = data
    else:
        payload = bytes(data).replace(b"\x00", b"")
        text = None
        for encoding in ("utf-8-sig", "utf-16", "cp1252"):
            try:
                text = payload.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            text = payload.decode("latin-1")
    text = text.replace("\x00", "").strip()
    if not text:
        return []
    dialect = _choose_dialect(text)
    return [[cell.strip() for cell in row] for row in csv.reader(StringIO(text), dialect) if any(cell.strip() for cell in row)]


def _blank_lead():
    return {
        "company": "",
        "contact_name": "",
        "office_manager": "",
        "phone": "",
        "alt_phone": None,
        "email": "",
        "street": "",
        "city": "",
        "state": "",
        "zip": "",
        "lead_tier": "C",
        "lead_score": None,
        "score_reasons": "",
        "signal": "",
        "signal_date": None,
        "now_open_or_moved": "",
        "category": "",
        "property_type": "",
        "hygiene_focus": "",
        "website": "",
        "county": "",
        "providers_listed": "",
        "source": "",
        "source_file": "",
        "property_verdict": "",
        "residential_check": "",
        "remote_or_mobile": "",
        "shared_address": None,
        "suite_in_address": None,
        "status": "new",
        "scheduled_until": None,
        "timezone": "Unknown",
        "transcript": [],
        "call_log": [],
        "pipeline_step": None,
        "pipeline_step_entered_at": None,
        "pipeline_history": [],
        "status_history": [],
        "booked_at": None,
        "passed_at": None,
        "agent_reserved_name": "",
        "agent_reserved_id": "",
        "archived_at": None,
    }


def _assign_field(lead, field, value):
    if field == "phone":
        phone = _phone(value)
        if phone and not lead.get("phone"):
            lead["phone"] = phone
        elif phone and lead.get("phone") and phone != lead["phone"] and not lead.get("alt_phone"):
            lead["alt_phone"] = phone
        return
    if field == "website":
        text = _text(value, limit=500)
        if text and not lead.get("website"):
            lead["website"] = text
        return
    if field == "lead_score":
        score = _score(value)
        if score is not None and lead.get("lead_score") is None:
            lead["lead_score"] = score
        return
    if field == "lead_tier":
        if str(value or "").strip():
            lead["lead_tier"] = _tier(value)
        return
    if field == "signal_date":
        parsed = _date(value)
        if parsed:
            lead["signal_date"] = parsed.isoformat()
        return
    if field == "state":
        lead["state"] = _state_code(value)
        return
    if field == "timezone":
        zone = _timezone(value)
        if zone:
            lead["timezone"] = zone
        return
    if field in ("shared_address", "suite_in_address"):
        lead[field] = _coerce_bool_field(value)
        return
    if field in lead:
        lead[field] = _text(value, limit=2000 if field == "score_reasons" else 500)


def _manual_transcript(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [dict(item) for item in value]
    text = _text(value, limit=2000)
    if not text:
        return []
    return [{
        "id": "",
        "timestamp": utc_now().isoformat(),
        "speaker": "Prospect",
        "text": text,
    }]


def _coerce_bool_field(value):
    if value is None or value == "":
        return None
    text = str(value).strip().lower()
    if text in ("1", "true", "yes", "y"):
        return True
    if text in ("0", "false", "no", "n"):
        return False
    return None


def parse_csv(data, known_phones=()):
    rows = _read_csv(data)
    if not rows:
        return [], {"duplicates": 0, "skipped": 0, "columns": [], "total": 0, "added": 0}
    headers = rows[0]
    records = rows[1:]
    columns = [str(h).strip() for h in headers]
    mapped = []
    for header in headers:
        field = map_csv_header(header)
        mapped.append(field)

    seen = set(known_phones)
    leads = []
    duplicates = skipped = 0
    for row in records:
        lead = _blank_lead()
        score_fallback = None
        for index, cell in enumerate(row):
            field = mapped[index] if index < len(mapped) else None
            if not field or not str(cell).strip():
                continue
            if field == "__score_fallback__":
                score_fallback = cell
                continue
            _assign_field(lead, field, cell)
        if lead.get("lead_score") is None and score_fallback is not None:
            _assign_field(lead, "lead_score", score_fallback)
        phone = lead.get("phone")
        if not phone:
            skipped += 1
            continue
        if phone in seen:
            duplicates += 1
            continue
        seen.add(phone)
        if not lead.get("company"):
            lead["company"] = display_name(lead) if lead.get("contact_name") else phone
        if not lead.get("contact_name"):
            lead["contact_name"] = lead["company"]
        leads.append(lead)
    return leads, {"duplicates": duplicates, "skipped": skipped, "columns": columns, "added": 0, "total": 0}


def build_manual_lead(payload, known_phones=()):
    if not isinstance(payload, dict):
        raise ValueError("Prospect details must be an object.")
    lead = _blank_lead()
    allowed = set(_blank_lead().keys()) - {"status", "scheduled_until", "transcript", "call_log"}
    for key in allowed:
        if key in payload:
            _assign_field(lead, key, payload[key])
    phone = _phone(payload.get("phone"))
    if not phone:
        raise ValueError("Enter a valid phone number.")
    if phone in set(known_phones):
        raise ValueError("A prospect with that phone number already exists.")
    lead["phone"] = phone
    status = parse_prospect_status(str(payload.get("status") or "new").strip() or "new")
    from shared.vocabulary import STATUS_KEYS
    if status not in STATUS_KEYS:
        raise ValueError("Unknown prospect status.")
    lead["status"] = status
    lead["timezone"] = _timezone(payload.get("timezone")) or "Unknown"
    if not lead.get("company"):
        lead["company"] = _text(payload.get("company") or display_name(lead), limit=200)
    if not lead.get("contact_name"):
        lead["contact_name"] = _text(payload.get("contact_name") or lead["company"], limit=200)
    if status == "dialed":
        lead["scheduled_until"] = (utc_now() + timedelta(hours=MANUAL_CALLBACK_HOURS)).isoformat()
    if status == "booked":
        lead["booked_at"] = utc_now().isoformat()
    if "transcript" in payload:
        lead["transcript"] = _manual_transcript(payload.get("transcript"))
    return lead


def update_lead_fields(lead, payload, known_phones=()):
    if not isinstance(payload, dict):
        raise ValueError("Prospect details must be an object.")
    changed = False
    if "phone" in payload:
        phone = _phone(payload.get("phone"))
        if not phone:
            raise ValueError("Enter a valid phone number.")
        if phone in set(known_phones):
            raise ValueError("A prospect with that phone number already exists.")
        if phone != lead.get("phone"):
            lead["phone"] = phone
            changed = True
    for key, value in payload.items():
        if key in ("phone", "id", "status", "call_log", "transcript"):
            continue
        if key not in lead:
            continue
        before = lead.get(key)
        _assign_field(lead, key, value)
        if lead.get(key) != before:
            changed = True
    if not changed and "phone" not in payload:
        raise ValueError("No prospect fields to update.")
    return lead


# Legacy no-ops removed from CRM (import hooks).
def apply_pitch_segment_from_fields(lead):
    return False


def apply_business_type_default_to_lead(lead):
    return False