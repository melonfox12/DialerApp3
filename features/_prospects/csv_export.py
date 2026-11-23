import csv
from io import StringIO

from shared.prospect_schema import REP_FACING_KEYS, display_name, days_since_signal
from shared.vocabulary import canonical_status

_CRM_EXPORT_HEADERS = [
    "Company",
    "Contact name",
    "Office manager",
    "Phone",
    "Alt phone",
    "Email",
    "Street",
    "City",
    "State",
    "Zip",
    "Lead tier",
    "Lead score",
    "Score reasons",
    "Signal",
    "Signal date",
    "Days since signal",
    "Category",
    "Property type",
    "Hygiene focus",
    "Website",
    "Call status",
    "Timezone",
    "scheduled_until",
    "Call transcript",
]

_HEADER_BY_KEY = {
    "company": "Company",
    "contact_name": "Contact name",
    "office_manager": "Office manager",
    "phone": "Phone",
    "alt_phone": "Alt phone",
    "email": "Email",
    "street": "Street",
    "city": "City",
    "state": "State",
    "zip": "Zip",
    "lead_tier": "Lead tier",
    "lead_score": "Lead score",
    "score_reasons": "Score reasons",
    "signal": "Signal",
    "signal_date": "Signal date",
    "days_since_signal": "Days since signal",
    "category": "Category",
    "property_type": "Property type",
    "hygiene_focus": "Hygiene focus",
    "website": "Website",
}


def _csv_number(value):
    if value is None or value == "":
        return ""
    return value


def csv_bytes_for(leads):
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=_CRM_EXPORT_HEADERS, extrasaction="ignore")
    writer.writeheader()
    for lead in leads:
        row = {
            header: _csv_number(lead.get(key))
            for key, header in _HEADER_BY_KEY.items()
            if key in REP_FACING_KEYS or key == "days_since_signal"
        }
        row["Days since signal"] = _csv_number(days_since_signal(lead))
        row["Call status"] = canonical_status(lead.get("status", "new"))
        row["Timezone"] = lead.get("timezone") or ""
        row["scheduled_until"] = lead.get("scheduled_until") or ""
        row["Call transcript"] = "\n".join(
            f"{entry.get('timestamp', '')} {entry.get('speaker', 'Speaker')}: {entry.get('text', '')}"
            for entry in lead.get("transcript", [])
        )
        if not row.get("Company"):
            row["Company"] = display_name(lead)
        writer.writerow(row)
    return output.getvalue().encode("utf-8-sig")