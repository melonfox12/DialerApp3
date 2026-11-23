import uuid
from copy import deepcopy

from features._prospects.csv_import import build_manual_lead
def prospect(**overrides):
    lead = build_manual_lead({
        "contact_name": "Onyx",
        "company": "Onyx Garage Floors",
        "phone": "+12025550123",
        "timezone": "Eastern",
        "status": "new",
    })
    lead["id"] = overrides.pop("id", lead.get("id") or "prospect-1")
    if not lead.get("id"):
        lead["id"] = str(uuid.uuid4())
    lead.update(overrides)
    return lead


class FakeSupabaseClient:
    def __init__(self, lead=None, *, user_id=None):
        self.leads = {}
        self.user_ids = {}
        self.loads = 0
        self.default_user_id = user_id
        if lead:
            row = dict(lead)
            row.setdefault("id", str(uuid.uuid4()))
            self.leads[row["id"]] = row
            self.user_ids[row["id"]] = user_id

    def select_all(self, resource, params):
        if resource != "prospects":
            raise AssertionError(f"Unexpected resource: {resource}")
        self.loads += 1
        rows = []
        for lead_id, row in self.leads.items():
            if (params or {}).get("archived_at") == "is.null" and row.get("archived_at"):
                continue
            user_filter = (params or {}).get("user_id", "")
            if user_filter.startswith("eq."):
                wanted = user_filter.removeprefix("eq.")
                if self.user_ids.get(lead_id) != wanted:
                    continue
            rows.append(dict(row, id=lead_id))
        return rows

    def request(self, method, resource, params=None, payload=None, prefer=None):
        if method == "POST" and resource == "prospects":
            row = dict(payload or {})
            new_id = row.get("id") or str(uuid.uuid4())
            stored = dict(row, id=new_id)
            self.leads[new_id] = stored
            uid = row.get("user_id") or self.default_user_id
            if uid:
                self.user_ids[new_id] = uid
            return [stored]
        if method == "PATCH" and resource == "prospects":
            lead_id = params["id"].removeprefix("eq.")
            if lead_id not in self.leads:
                return []
            patch = payload if isinstance(payload, dict) else {}
            self.leads[lead_id].update(patch)
            return [dict(self.leads[lead_id])]
        raise AssertionError(f"Unexpected request: {method} {resource}")