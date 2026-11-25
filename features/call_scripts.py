"""Call script library keyed by industry, prospect type, and variation (1–3)."""

import json
import threading
from pathlib import Path

from shared.vocabulary import (
    CALL_SCRIPT_INDUSTRIES,
    CALL_SCRIPT_INDUSTRY_KEYS,
    CALL_SCRIPT_PROSPECT_TYPE_KEYS,
    CALL_SCRIPT_PROSPECT_TYPES,
    CALL_SCRIPT_VARIATION_KEYS,
    CALL_SCRIPT_VARIATIONS,
    DEFAULT_CALL_SCRIPT_INDUSTRY,
    DEFAULT_CALL_SCRIPT_PROSPECT_TYPE,
    DEFAULT_CALL_SCRIPT_VARIATION,
)


def _script_key(industry, prospect_type, variation):
    return f"{industry}|{prospect_type}|{variation}"


def _normalize_industry(value):
    key = str(value or "").strip().lower()
    return key if key in CALL_SCRIPT_INDUSTRY_KEYS else DEFAULT_CALL_SCRIPT_INDUSTRY


def _normalize_prospect_type(value):
    key = str(value or "").strip().lower()
    return key if key in CALL_SCRIPT_PROSPECT_TYPE_KEYS else DEFAULT_CALL_SCRIPT_PROSPECT_TYPE


def _normalize_variation(value):
    if value is None or value == "":
        return DEFAULT_CALL_SCRIPT_VARIATION
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = DEFAULT_CALL_SCRIPT_VARIATION
    return number if number in CALL_SCRIPT_VARIATION_KEYS else DEFAULT_CALL_SCRIPT_VARIATION


def _variation_options():
    return [{"key": key, "label": label} for key, label in CALL_SCRIPT_VARIATIONS]


def panel_payload(store, user_id, industry=None, prospect_type=None, variation=None):
    if not store:
        industry = _normalize_industry(industry)
        prospect_type = _normalize_prospect_type(prospect_type)
        variation = _normalize_variation(variation)
        return {
            "industries": [{"key": key, "label": label} for key, label in CALL_SCRIPT_INDUSTRIES],
            "prospect_types": [{"key": key, "label": label} for key, label in CALL_SCRIPT_PROSPECT_TYPES],
            "variations": _variation_options(),
            "industry": industry,
            "prospect_type": prospect_type,
            "variation": variation,
            "body": "",
        }
    prefs = store.load_prefs(user_id)
    industry = _normalize_industry(industry or prefs.get("industry"))
    prospect_type = _normalize_prospect_type(prospect_type or prefs.get("prospect_type"))
    variation = _normalize_variation(variation if variation is not None else prefs.get("variation"))
    body = store.load_body(user_id, industry, prospect_type, variation)
    return {
        "industries": [{"key": key, "label": label} for key, label in CALL_SCRIPT_INDUSTRIES],
        "prospect_types": [{"key": key, "label": label} for key, label in CALL_SCRIPT_PROSPECT_TYPES],
        "variations": _variation_options(),
        "industry": industry,
        "prospect_type": prospect_type,
        "variation": variation,
        "body": body,
    }


class LocalCallScriptsStore:
    def __init__(self, crm_path):
        path = Path(crm_path)
        if path.is_dir() or not path.suffix:
            self.path = path / "call_scripts.json"
        else:
            self.path = path.with_name("call_scripts.json")
        self.lock = threading.RLock()
        self._cache = None

    def _load(self):
        if self._cache is not None:
            return self._cache
        try:
            if self.path.is_file():
                data = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self._cache = data
                    if "variation" not in self._cache:
                        self._cache["variation"] = DEFAULT_CALL_SCRIPT_VARIATION
                    self._migrate_script_keys_locked()
                    return self._cache
        except (OSError, json.JSONDecodeError):
            pass
        self._cache = {
            "industry": DEFAULT_CALL_SCRIPT_INDUSTRY,
            "prospect_type": DEFAULT_CALL_SCRIPT_PROSPECT_TYPE,
            "variation": DEFAULT_CALL_SCRIPT_VARIATION,
            "scripts": {},
        }
        self._save_locked()
        return self._cache

    def _migrate_script_keys_locked(self):
        scripts = self._cache.get("scripts")
        if not isinstance(scripts, dict):
            return
        migrated = {}
        changed = False
        for key, body in scripts.items():
            parts = str(key).split("|")
            if len(parts) == 2:
                migrated[_script_key(parts[0], parts[1], DEFAULT_CALL_SCRIPT_VARIATION)] = body
                changed = True
            else:
                migrated[key] = body
        if changed:
            self._cache["scripts"] = migrated
            self._save_locked()

    def _save_locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(self._cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(self.path)

    def load_prefs(self, user_id=None):
        with self.lock:
            data = self._load()
            return {
                "industry": _normalize_industry(data.get("industry")),
                "prospect_type": _normalize_prospect_type(data.get("prospect_type")),
                "variation": _normalize_variation(data.get("variation")),
            }

    def save_prefs(self, user_id, industry, prospect_type, variation):
        with self.lock:
            data = self._load()
            data["industry"] = _normalize_industry(industry)
            data["prospect_type"] = _normalize_prospect_type(prospect_type)
            data["variation"] = _normalize_variation(variation)
            self._save_locked()

    def load_body(self, user_id, industry, prospect_type, variation):
        with self.lock:
            data = self._load()
            scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
            industry = _normalize_industry(industry)
            prospect_type = _normalize_prospect_type(prospect_type)
            variation = _normalize_variation(variation)
            key = _script_key(industry, prospect_type, variation)
            if key in scripts:
                return str(scripts.get(key, "") or "")
            legacy_key = f"{industry}|{prospect_type}"
            if variation == DEFAULT_CALL_SCRIPT_VARIATION and legacy_key in scripts:
                return str(scripts.get(legacy_key, "") or "")
            return ""

    def save_body(self, user_id, industry, prospect_type, variation, body):
        with self.lock:
            data = self._load()
            scripts = data.setdefault("scripts", {})
            if not isinstance(scripts, dict):
                scripts = {}
                data["scripts"] = scripts
            variation = _normalize_variation(variation)
            scripts[_script_key(_normalize_industry(industry), _normalize_prospect_type(prospect_type), variation)] = str(body or "")
            self._save_locked()


class SupabaseCallScriptsStore:
    def __init__(self, client):
        self.client = client
        self.lock = threading.RLock()

    def _table_missing(self, exc, name):
        message = str(exc).lower()
        return name in message and ("404" in message or "does not exist" in message or "pgrst205" in message)

    def _missing_variation_column(self, exc):
        message = str(exc).lower()
        return "variation" in message and ("column" in message or "pgrst" in message)

    def load_prefs(self, user_id):
        default = {
            "industry": DEFAULT_CALL_SCRIPT_INDUSTRY,
            "prospect_type": DEFAULT_CALL_SCRIPT_PROSPECT_TYPE,
            "variation": DEFAULT_CALL_SCRIPT_VARIATION,
        }
        if not user_id:
            return default
        try:
            rows = self.client.request(
                "GET",
                "call_script_prefs",
                {"user_id": f"eq.{user_id}", "select": "industry,prospect_type,variation", "limit": "1"},
            ) or []
        except OSError as exc:
            if self._table_missing(exc, "call_script_prefs"):
                return default
            if self._missing_variation_column(exc):
                rows = self.client.request(
                    "GET",
                    "call_script_prefs",
                    {"user_id": f"eq.{user_id}", "select": "industry,prospect_type", "limit": "1"},
                ) or []
                if not rows:
                    return default
                row = rows[0]
                return {
                    "industry": _normalize_industry(row.get("industry")),
                    "prospect_type": _normalize_prospect_type(row.get("prospect_type")),
                    "variation": DEFAULT_CALL_SCRIPT_VARIATION,
                }
            raise
        if not rows:
            return default
        row = rows[0]
        return {
            "industry": _normalize_industry(row.get("industry")),
            "prospect_type": _normalize_prospect_type(row.get("prospect_type")),
            "variation": _normalize_variation(row.get("variation")),
        }

    def save_prefs(self, user_id, industry, prospect_type, variation):
        if not user_id:
            raise ValueError("Sign in to save call script preferences.")
        body = {
            "user_id": user_id,
            "industry": _normalize_industry(industry),
            "prospect_type": _normalize_prospect_type(prospect_type),
            "variation": _normalize_variation(variation),
        }
        try:
            self.client.request(
                "POST",
                "call_script_prefs",
                {"on_conflict": "user_id"},
                body,
                "resolution=merge-duplicates,return=minimal",
            )
        except OSError as exc:
            if self._table_missing(exc, "call_script_prefs"):
                raise OSError(
                    "The call_script_prefs table is missing in Supabase. "
                    "Run docs/supabase/migrations/202611241230_call_scripts.sql in the SQL editor."
                ) from exc
            if self._missing_variation_column(exc):
                raise OSError(
                    "The call_script_prefs.variation column is missing in Supabase. "
                    "Run docs/supabase/migrations/202611241300_call_script_variations.sql in the SQL editor."
                ) from exc
            raise

    def load_body(self, user_id, industry, prospect_type, variation):
        if not user_id:
            return ""
        industry = _normalize_industry(industry)
        prospect_type = _normalize_prospect_type(prospect_type)
        variation = _normalize_variation(variation)
        try:
            rows = self.client.request(
                "GET",
                "call_script_entries",
                {
                    "user_id": f"eq.{user_id}",
                    "industry": f"eq.{industry}",
                    "prospect_type": f"eq.{prospect_type}",
                    "variation": f"eq.{variation}",
                    "select": "body",
                    "limit": "1",
                },
            ) or []
        except OSError as exc:
            if self._table_missing(exc, "call_script_entries"):
                return ""
            if self._missing_variation_column(exc) and variation == DEFAULT_CALL_SCRIPT_VARIATION:
                rows = self.client.request(
                    "GET",
                    "call_script_entries",
                    {
                        "user_id": f"eq.{user_id}",
                        "industry": f"eq.{industry}",
                        "prospect_type": f"eq.{prospect_type}",
                        "select": "body",
                        "limit": "1",
                    },
                ) or []
            elif self._missing_variation_column(exc):
                return ""
            else:
                raise
        if not rows:
            return ""
        return str(rows[0].get("body") or "")

    def save_body(self, user_id, industry, prospect_type, variation, body):
        if not user_id:
            raise ValueError("Sign in to save call scripts.")
        payload = {
            "user_id": user_id,
            "industry": _normalize_industry(industry),
            "prospect_type": _normalize_prospect_type(prospect_type),
            "variation": _normalize_variation(variation),
            "body": str(body or ""),
        }
        conflict = "user_id,industry,prospect_type,variation"
        try:
            self.client.request(
                "POST",
                "call_script_entries",
                {"on_conflict": conflict},
                payload,
                "resolution=merge-duplicates,return=minimal",
            )
        except OSError as exc:
            if self._table_missing(exc, "call_script_entries"):
                raise OSError(
                    "The call_script_entries table is missing in Supabase. "
                    "Run docs/supabase/migrations/202611241230_call_scripts.sql in the SQL editor."
                ) from exc
            if self._missing_variation_column(exc):
                if _normalize_variation(variation) != DEFAULT_CALL_SCRIPT_VARIATION:
                    raise OSError(
                        "The call_script_entries.variation column is missing in Supabase. "
                        "Run docs/supabase/migrations/202611241300_call_script_variations.sql in the SQL editor."
                    ) from exc
                legacy = {
                    "user_id": user_id,
                    "industry": _normalize_industry(industry),
                    "prospect_type": _normalize_prospect_type(prospect_type),
                    "body": str(body or ""),
                }
                self.client.request(
                    "POST",
                    "call_script_entries",
                    {"on_conflict": "user_id,industry,prospect_type"},
                    legacy,
                    "resolution=merge-duplicates,return=minimal",
                )
                return
            raise


def CallScriptsStore(*, client=None, crm_path=None):
    if client is not None:
        return SupabaseCallScriptsStore(client)
    return LocalCallScriptsStore(crm_path)


def get_call_script(request):
    dialer = request.account.dialer
    store = getattr(dialer, "call_scripts_store", None)
    user_id = getattr(dialer, "account_user_id", None)
    request.send_json(200, panel_payload(store, user_id))


def post_call_script(request, data):
    try:
        dialer = request.account.dialer
        store = getattr(dialer, "call_scripts_store", None)
        if not store:
            request.send_json(400, {"error": "Call scripts are not available in this session."})
            return
        user_id = getattr(dialer, "account_user_id", None)
        industry = data.get("industry")
        prospect_type = data.get("prospect_type")
        variation = data.get("variation")
        body = data.get("body") if "body" in data else None
        prefs = store.load_prefs(user_id)
        active_industry = _normalize_industry(industry) if industry is not None else prefs.get("industry")
        active_type = _normalize_prospect_type(prospect_type) if prospect_type is not None else prefs.get("prospect_type")
        active_variation = _normalize_variation(variation) if variation is not None else prefs.get("variation")
        if industry is not None or prospect_type is not None or variation is not None:
            store.save_prefs(user_id, active_industry, active_type, active_variation)
        if body is not None:
            if len(str(body)) > 12000:
                raise ValueError("Call script must be 12,000 characters or fewer.")
            store.save_body(user_id, active_industry, active_type, active_variation, body)
        request.send_json(
            200,
            panel_payload(
                store,
                user_id,
                industry=active_industry,
                prospect_type=active_type,
                variation=active_variation,
            ),
        )
    except ValueError as exc:
        request._trace_error = str(exc)
        request.send_json(400, {"error": str(exc)})
    except OSError as exc:
        request.report_storage_error(exc)


ROUTES = [
    ("GET", "/api/call-script", get_call_script, "GET reads"),
    ("POST", "/api/call-script", post_call_script, "POST"),
]