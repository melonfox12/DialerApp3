#!/usr/bin/env python3
"""Start DialerApp in isolated local-JSON mode for Playwright (no Supabase login gate)."""

import os
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from _web.hooks import make_hook_handler
from features.accounts import AppRuntime
from server import QuietThreadingHTTPServer
from web import make_app_handler

_ISOLATED = (
    "SUPABASE_URL",
    "SUPABASE_SECRET_KEY",
    "SUPABASE_SERVICE_ROLE_KEY",
    "SUPABASE_ANON_KEY",
    "SUPABASE_PUBLISHABLE_KEY",
)
HOST = os.environ.get("E2E_HOST", "127.0.0.1")
PORT = int(os.environ.get("E2E_PORT", "8000"))


def main():
    tmp = tempfile.mkdtemp(prefix="dialer-e2e-")
    import features.accounts as accounts

    saved_env = {key: os.environ.pop(key) for key in _ISOLATED if key in os.environ}
    saved_paths = (accounts.ENV_PATH, accounts.CRM_PATH, accounts.METRICS_PATH)
    accounts.ENV_PATH = os.path.join(tmp, ".env")
    accounts.CRM_PATH = os.path.join(tmp, "crm.json")
    accounts.METRICS_PATH = os.path.join(tmp, "metrics.json")
    Path(accounts.ENV_PATH).write_text("", encoding="utf-8")
    runtime = AppRuntime().configure()
    if runtime.storage_name != "local JSON files":
        print("E2E server expected local storage; check Supabase env isolation.", file=sys.stderr)
        return 1
    app = QuietThreadingHTTPServer((HOST, PORT), make_app_handler(runtime))
    hook = QuietThreadingHTTPServer((HOST, PORT + 65), make_hook_handler(runtime))
    for server in (app, hook):
        threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"E2E local app http://{HOST}:{PORT}", flush=True)
    try:
        app.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        app.shutdown()
        hook.shutdown()
        accounts.ENV_PATH, accounts.CRM_PATH, accounts.METRICS_PATH = saved_paths
        os.environ.update(saved_env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())