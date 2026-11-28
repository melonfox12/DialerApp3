#!/usr/bin/env python3
"""Non-secret checks before Twilio live Playwright (ngrok + /api/health)."""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import read_env


def get_json(url: str, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    errors = []
    ok = True
    try:
        health = get_json("http://127.0.0.1:8000/api/health")
        print(f"health: ok={health.get('ok')} storage={health.get('storage')}")
    except (urllib.error.URLError, OSError) as exc:
        errors.append(f"Dialer not on :8000 — {exc}")
        ok = False

    ngrok = None
    try:
        tunnels = get_json("http://127.0.0.1:4040/api/tunnels")
        for t in tunnels.get("tunnels") or []:
            url = str(t.get("public_url") or "")
            if url.startswith("https://"):
                ngrok = url.rstrip("/")
                break
        if ngrok:
            print(f"ngrok: {ngrok}")
        else:
            errors.append("No https ngrok tunnel on :4040 (run: ngrok http 8000)")
            ok = False
    except (urllib.error.URLError, OSError) as exc:
        errors.append(f"ngrok API unavailable — {exc}")
        ok = False

    token = (
        __import__("os").environ.get("E2E_ACCESS_TOKEN", "").strip()
        or (read_env(str(ROOT / ".env")).get("E2E_ACCESS_TOKEN") or "").strip()
    )
    if not token:
        errors.append("E2E_ACCESS_TOKEN not set (add Supabase JWT to .env for authenticated preflight)")
    else:
        try:
            settings = get_json(
                "http://127.0.0.1:8000/api/settings",
                headers={"Authorization": f"Bearer {token}"},
            )
            pub = (settings.get("public_base_url") or "").rstrip("/")
            twilio = bool(
                settings.get("account_sid")
                and settings.get("api_key")
                and settings.get("twiml_app_sid")
                and settings.get("has_auth_token")
                and settings.get("has_api_secret")
            )
            print(f"settings: twilio_complete={twilio} public_base_url_set={bool(pub)}")
            if not twilio:
                errors.append("Twilio fields incomplete in Settings")
                ok = False
            if not pub.startswith("https://"):
                errors.append("PUBLIC_BASE_URL must be https in Settings")
                ok = False
            elif ngrok and pub != ngrok:
                errors.append(f"PUBLIC_BASE_URL ({pub}) != current ngrok ({ngrok})")
                ok = False
        except urllib.error.HTTPError as exc:
            errors.append(f"/api/settings HTTP {exc.code}")
            ok = False

    if errors:
        print("\nIssues:")
        for line in errors:
            print(f"  - {line}")
        sys.exit(1)
    print("\nPreflight OK for Twilio live Playwright (E2E_TWILIO_LIVE=1).")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)