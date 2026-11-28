#!/usr/bin/env python3
"""Set Settings public_base_url to the current https ngrok tunnel."""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ngrok_https():
    with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=5) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    for tunnel in body.get("tunnels") or []:
        url = str(tunnel.get("public_url") or "").rstrip("/")
        if url.startswith("https://"):
            return url
    raise SystemExit("No https ngrok tunnel on :4040")


def e2e_token():
    text = (ROOT / ".env").read_text(encoding="utf-8")
    match = re.search(r"^E2E_ACCESS_TOKEN=(.+)$", text, flags=re.M)
    if not match:
        raise SystemExit("E2E_ACCESS_TOKEN missing in .env — run scripts/mint_e2e_access_token.py")
    return match.group(1).strip()


def main():
    pub = ngrok_https()
    token = e2e_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request("http://127.0.0.1:8000/api/settings", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        settings = json.loads(resp.read().decode("utf-8"))
    body = {
        "public_base_url": pub,
        "account_sid": settings.get("account_sid", ""),
        "api_key": settings.get("api_key", ""),
        "twiml_app_sid": settings.get("twiml_app_sid", ""),
        "session_goal": str(settings.get("session_goal", 20)),
        "conversation_threshold": str(settings.get("conversation_threshold", 30)),
        "auto_advance_delay": str(settings.get("auto_advance_delay", 3)),
        "sounds_enabled": settings.get("sounds_enabled", True),
        "sound_volume": settings.get("sound_volume", 35),
        "calling_start_hour": str(settings.get("calling_start_hour", 0)),
        "calling_end_hour": str(settings.get("calling_end_hour", 24)),
    }
    post = urllib.request.Request(
        "http://127.0.0.1:8000/api/settings",
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(post, timeout=30) as resp:
            print(f"Updated public_base_url -> {pub} (HTTP {resp.status})")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"POST /api/settings failed: {exc.code} {exc.read().decode()[:300]}") from exc
    with urllib.request.urlopen(req, timeout=20) as resp:
        verify = json.loads(resp.read().decode("utf-8"))
    if verify.get("public_base_url", "").rstrip("/") != pub:
        raise SystemExit("public_base_url did not persist")
    twilio_ok = bool(
        verify.get("account_sid")
        and verify.get("api_key")
        and verify.get("twiml_app_sid")
        and verify.get("has_auth_token")
        and verify.get("has_api_secret")
    )
    print(f"twilio_complete={twilio_ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)