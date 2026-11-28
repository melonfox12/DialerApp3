#!/usr/bin/env python3
"""Mint a short-lived Supabase access JWT for Playwright (service-role admin only)."""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import read_env


def _request(url, key, path, *, method="GET", body=None, anon=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url.rstrip("/") + path,
        data=data,
        method=method,
        headers={
            "apikey": anon or key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
        return json.loads(raw.decode("utf-8")) if raw else {}


def pick_owner_user_id(url, key):
    req = urllib.request.Request(
        f"{url.rstrip('/')}/rest/v1/org_members?select=user_id,role,status&status=eq.active&role=eq.owner&limit=1",
        headers={"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        rows = json.loads(resp.read().decode("utf-8"))
    if rows and rows[0].get("user_id"):
        return rows[0]["user_id"]
    users = _request(url, key, "/auth/v1/admin/users?per_page=1")
    batch = users.get("users") or []
    if batch:
        return batch[0].get("id")
    raise SystemExit("No Supabase users found.")


def mint_token_for_user(url, service_key, anon_key, user_id, email, temp_password):
    body = json.dumps({"password": temp_password}).encode()
    req = urllib.request.Request(
        f"{url.rstrip('/')}/auth/v1/admin/users/{user_id}",
        data=body,
        method="PUT",
        headers={
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json",
        },
    )
    urllib.request.urlopen(req, timeout=30)
    tok_body = json.dumps({"email": email, "password": temp_password}).encode()
    tok_req = urllib.request.Request(
        f"{url.rstrip('/')}/auth/v1/token?grant_type=password",
        data=tok_body,
        method="POST",
        headers={"apikey": anon_key or service_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(tok_req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    token = (payload.get("access_token") or "").strip()
    refresh = (payload.get("refresh_token") or "").strip()
    if not token:
        raise SystemExit("Supabase did not return access_token")
    return token, refresh


def upsert_env_token(env_path: Path, token: str, refresh: str):
    text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""

    def set_line(key: str, value: str):
        nonlocal text
        line = f"{key}={value}"
        if re.search(rf"^{re.escape(key)}=", text, flags=re.M):
            text = re.sub(rf"^{re.escape(key)}=.*$", line, text, flags=re.M)
        else:
            if not text.endswith("\n") and text:
                text += "\n"
            text += line + "\n"

    set_line("E2E_ACCESS_TOKEN", token)
    if refresh:
        set_line("E2E_REFRESH_TOKEN", refresh)
    if not re.search(r"^E2E_TWILIO_LIVE=", text, flags=re.M):
        text += "E2E_TWILIO_LIVE=1\n"
    env_path.write_text(text, encoding="utf-8")


def main():
    env = read_env(str(ROOT / ".env"))
    url = (env.get("SUPABASE_URL") or "").strip()
    key = (env.get("SUPABASE_SECRET_KEY") or env.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
    anon = (env.get("SUPABASE_ANON_KEY") or env.get("SUPABASE_PUBLISHABLE_KEY") or "").strip()
    if not url or not key:
        raise SystemExit("SUPABASE_URL and SUPABASE_SECRET_KEY required in .env")
    user_id = pick_owner_user_id(url, key)
    users = _request(url, key, f"/auth/v1/admin/users/{user_id}")
    email = (users.get("email") or "").strip()
    if not email:
        raise SystemExit(f"No email for user {user_id}")
    temp_password = "E2eTempDialer99!"
    token, refresh = mint_token_for_user(url, key, anon, user_id, email, temp_password)
    upsert_env_token(ROOT / ".env", token, refresh)
    print(f"Wrote E2E_ACCESS_TOKEN for {email} ({user_id[:8]}…)")


if __name__ == "__main__":
    main()