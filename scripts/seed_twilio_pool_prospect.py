#!/usr/bin/env python3
"""Add a dialable E2E prospect and clear identity-blocked duplicates."""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import read_env


def main():
    token = (read_env(str(ROOT / ".env")).get("E2E_ACCESS_TOKEN") or "").strip()
    if not token:
        print("Run scripts/mint_e2e_access_token.py first.")
        return 1
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def get(path):
        req = urllib.request.Request(f"http://127.0.0.1:8000{path}", headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())

    def post(path, body=None):
        data = json.dumps(body or {}).encode() if body is not None else b"{}"
        req = urllib.request.Request(
            f"http://127.0.0.1:8000{path}",
            data=data,
            method="POST",
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())

    leads = get("/api/leads")
    closed = 0
    for lead in leads.get("leads") or []:
        if (lead.get("contact_name") or "") == "E2E Twilio Prospect":
            try:
                post(f"/api/leads/{lead['id']}/status", {"status": "closed", "crm_only": True})
                closed += 1
            except urllib.error.HTTPError:
                pass
    stamp = int(time.time())
    created = post(
        "/api/leads",
        {
            "contact_name": f"E2E Live Dial {stamp}",
            "company": f"E2E Co {stamp}",
            "phone": "+15005550006",
            "timezone": "Eastern",
            "status": "new",
        },
    )
    lead = created.get("lead") or created
    post("/api/dials/scan", {})
    catalog = get("/api/leads")
    pool = catalog.get("pool") or []
    print(f"Closed {closed} old E2E rows blocking the pool.")
    print(f"Added: {lead.get('contact_name')} {lead.get('phone')} ({lead.get('id')})")
    print(f"Dial pool (New): {len(pool)} prospect(s)")
    if pool:
        first = pool[0]
        print(f"  Next: {first.get('contact_name')} · {first.get('phone')}")
    return 0 if pool else 1


if __name__ == "__main__":
    sys.exit(main() or 0)