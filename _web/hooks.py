"""Twilio callback routes (dedicated hook port and /hooks on the main app)."""

import time
import traceback
import urllib.parse
from http.server import BaseHTTPRequestHandler

from shared.infra import debug_event
from _web.respond import HandlerMixin, log_server_fault


def resolve_hook_dialer(runtime, path, params, parts):
    if path == "/hooks/voice":
        token = params.get("DeskToken") or params.get("CallToken")
    else:
        token = None
    if not token and len(parts) == 3 and parts[0] == "hooks":
        token = parts[1]
    dialer = runtime.tokens.lookup(token)
    if dialer is None and runtime.local:
        dialer = runtime.local.dialer
    return dialer


def dispatch_twilio_hook(runtime, method, raw_path, headers, body_values=None):
    """Return (status, content_type, body_text) for a Twilio HTTP callback."""
    parsed = urllib.parse.urlsplit(raw_path)
    path = parsed.path
    query = urllib.parse.parse_qs(parsed.query)
    params = {key: vals[-1] for key, vals in query.items()}
    if body_values:
        params.update({key: vals[-1] for key, vals in body_values.items()})
    parts = path.strip("/").split("/")
    started = time.perf_counter()
    try:
        dialer = resolve_hook_dialer(runtime, path, params, parts)
        if dialer is None:
            status, content_type, content = 404, "text/plain", "Unknown call"
        else:
            callback_url = dialer.public_base_url + path
            sign_params = body_values if body_values is not None else query
            valid = dialer.validate_webhook(
                callback_url,
                headers.get("X-Twilio-Signature", ""),
                sign_params,
            )
            if not valid:
                dialer.record_activity("Rejected unsigned Twilio callback", "error")
                status, content_type, content = 403, "text/plain", "Invalid Twilio signature"
            else:
                dialer.record_activity(f"Twilio callback: {parts[-1] if parts else 'unknown'}", "webhook")
                if path == "/hooks/voice":
                    status, content_type, content = dialer.handle_client_voice(params)
                elif len(parts) == 3 and parts[0] == "hooks":
                    status, content_type, content = dialer.handle_webhook(parts[1], parts[2], params)
                else:
                    status, content_type, content = 404, "text/plain", "Not found"
    except Exception:
        debug_event("error", f"hook {path}", traceback.format_exc())
        status, content_type, content = 500, "text/plain", "Callback failed"
    elapsed = int((time.perf_counter() - started) * 1000)
    summary = " ".join(
        f"{key}={params.get(key)}"
        for key in ("CallStatus", "DialCallStatus", "AnsweredBy", "ErrorCode")
        if params.get(key)
    )
    debug_event("hook", f"{method} {path} -> {status} {elapsed}ms", summary)
    return status, content_type, content


def make_hook_handler(runtime):
    class HookHandler(HandlerMixin, BaseHTTPRequestHandler):
        def do_GET(self):
            self.dispatch()

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            if length > 256 * 1024:
                self.send_response(413)
                self.end_headers()
                return
            body = self.rfile.read(length).decode("utf-8", errors="replace")
            values = urllib.parse.parse_qs(body, keep_blank_values=True)
            self.dispatch(values)

        def dispatch(self, body_values=None):
            status, content_type, content = dispatch_twilio_hook(
                self.runtime, self.command, self.path, self.headers, body_values
            )
            body = content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_error(self, format, *args):
            log_server_fault(format, *args)

        def log_message(self, format, *args):
            return

    HookHandler.runtime = runtime
    return HookHandler