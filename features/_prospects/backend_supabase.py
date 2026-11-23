"""Supabase prospect persistence (normalized columns)."""

import threading
from datetime import datetime

from features._prospects.csv_export import csv_bytes_for
from features._prospects.csv_import import build_manual_lead, parse_csv
from shared.infra import utc_now
from shared.prospect_schema import (
    active_leads,
    db_payload_from_lead,
    row_from_db,
)

_ACTIVE_FILTER = "archived_at.is.null"


class SupabaseBackend:
    def __init__(self, client, user_id=None):
        self.client = client
        self.user_id = user_id
        self.lock = threading.RLock()
        self._cache = None
        self.revision = 0

    def _scope(self, params=None):
        scoped = dict(params or {})
        if self.user_id:
            scoped["user_id"] = f"eq.{self.user_id}"
        return scoped

    def _touch(self):
        self.revision += 1

    def bump_revision(self):
        self._touch()

    def _fetch(self):
        params = self._scope({
            "select": "*",
            "archived_at": "is.null",
            "order": "lead_tier.asc,lead_score.desc.nullslast,signal_date.desc.nullslast",
        })
        rows = self.client.select_all("prospects", params)
        leads = []
        for row in rows:
            if not isinstance(row, dict):
                raise OSError("Supabase contains an invalid prospect record.")
            leads.append(row_from_db(row))
        return leads

    def _all(self):
        if self._cache is None:
            self._cache = self._fetch()
        return self._cache

    def _write(self, lead):
        payload = db_payload_from_lead(lead, user_id=self.user_id)
        rows = self.client.request(
            "PATCH",
            "prospects",
            self._scope({"id": f"eq.{lead['id']}"}),
            payload,
            "return=representation",
        )
        if not rows:
            raise KeyError("Prospect not found")
        return row_from_db(rows[0])

    def _insert(self, lead):
        payload = db_payload_from_lead(lead, user_id=self.user_id, for_insert=True)
        rows = self.client.request(
            "POST",
            "prospects",
            None,
            payload,
            "return=representation",
        )
        if not rows:
            raise OSError("Supabase did not return the new prospect.")
        row = rows[0] if isinstance(rows, list) else rows
        created = row_from_db(row)
        lead.update(created)
        return created

    def _expire(self, leads):
        now = utc_now()
        for lead in leads:
            deadline = lead.get("scheduled_until")
            if lead.get("status") == "dialed" and deadline:
                try:
                    due = datetime.fromisoformat(deadline)
                except ValueError:
                    due = now
                if due <= now:
                    lead["scheduled_until"] = None
                    self._write(lead)
                    self._touch()

    def snapshot(self):
        with self.lock:
            leads = active_leads(self._all())
            self._expire(leads)
            return [dict(lead) for lead in leads]

    def timezone_groups(self, leads=None):
        counts = {}
        for lead in self.snapshot() if leads is None else leads:
            if lead.get("status") != "new":
                continue
            timezone = lead.get("timezone") or "Unknown"
            counts[timezone] = counts.get(timezone, 0) + 1
        return sorted(counts.items(), key=lambda item: (item[0] == "Unknown", -item[1], item[0]))

    def csv_bytes(self):
        return csv_bytes_for(self.snapshot())

    def add_lead(self, payload):
        with self.lock:
            leads = self._all()
            self._expire(leads)
            lead = build_manual_lead(payload, (item["phone"] for item in leads))
            created = self._insert(lead)
            leads.append(created)
            self._touch()
            return dict(created)

    def add_csv(self, data):
        with self.lock:
            leads = self._all()
            self._expire(leads)
            additions, info = parse_csv(data, (lead["phone"] for lead in leads))
            for lead in additions:
                self._insert(lead)
            leads.extend(additions)
            info["added"] = len(additions)
            info["total"] = len(active_leads(leads))
            if additions:
                self._touch()
            return info

    def leads_locked(self):
        return self._all()

    def expire_locked(self, leads):
        self._expire(leads)

    def save_locked(self, lead):
        updated = self._write(lead)
        lead.update(updated)
        leads = self._all()
        for index, item in enumerate(leads):
            if item["id"] == lead["id"]:
                leads[index] = lead
        self._touch()

    def remove(self, lead_id):
        with self.lock:
            archived_at = utc_now().isoformat()
            rows = self.client.request(
                "PATCH",
                "prospects",
                self._scope({"id": f"eq.{lead_id}", "select": "id"}),
                {"archived_at": archived_at},
                "return=representation",
            )
            if not rows:
                raise KeyError("Prospect not found")
            if self._cache is not None:
                self._cache = [lead for lead in self._cache if lead["id"] != lead_id]
            self._touch()