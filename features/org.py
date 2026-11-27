"""Organization membership rules: roles, login hooks, and access checks."""

import threading
import time

from features import org_storage
from shared.config import ENV_PATH
from shared.vocabulary import DEFAULT_ORG_NAME, ORG_MANAGER_ROLES, TEAM_ONLINE_SECONDS

_membership_cache = {}
_membership_lock = threading.Lock()
_MEMBERSHIP_TTL = 60


def _empty_membership():
    return {
        "org_id": "",
        "org_name": "",
        "role": "",
        "status": "",
        "can_manage_team": False,
    }


def can_manage_team(role):
    return str(role or "").strip().lower() in ORG_MANAGER_ROLES


def _cache_key(user_id):
    return str(user_id or "")


def load_membership(client, user_id):
    key = _cache_key(user_id)
    now = time.time()
    with _membership_lock:
        entry = _membership_cache.get(key)
        if entry and entry[0] > now:
            return dict(entry[1])
    if not client or not user_id:
        return _empty_membership()
    member = org_storage.get_active_membership(client, user_id)
    if not member:
        cached = _empty_membership()
    else:
        org = org_storage.get_organization(client, member["org_id"]) or {}
        cached = {
            "org_id": str(member.get("org_id") or ""),
            "org_name": str(org.get("name") or ""),
            "role": str(member.get("role") or ""),
            "status": str(member.get("status") or "active"),
            "can_manage_team": can_manage_team(member.get("role")),
        }
    with _membership_lock:
        _membership_cache[key] = (now + _MEMBERSHIP_TTL, dict(cached))
        if len(_membership_cache) > 128:
            for item_key in list(_membership_cache):
                if _membership_cache[item_key][0] <= now:
                    del _membership_cache[item_key]
    return cached


def clear_membership_cache(user_id=None):
    with _membership_lock:
        if user_id is None:
            _membership_cache.clear()
            return
        _membership_cache.pop(_cache_key(user_id), None)


def _org_name_for_new_owner(email):
    local = str(email or "").split("@")[0].strip()
    if local:
        return f"{local.title()}'s team"
    return DEFAULT_ORG_NAME


def bootstrap_owner_org(client, user_id, email=""):
    """First sign-in with no invite: create an org and make this user the owner."""
    existing = org_storage.get_active_membership(client, user_id)
    if existing:
        clear_membership_cache(user_id)
        return load_membership(client, user_id)
    org = org_storage.create_organization(client, _org_name_for_new_owner(email))
    org_storage.add_member(client, org["id"], user_id=user_id, role="owner", status="active")
    clear_membership_cache(user_id)
    return load_membership(client, user_id)


def sync_user_on_login(client, user):
    if not client:
        return _empty_membership()
    user_id = str(user.get("id") or "")
    email = str(user.get("email") or "").strip()
    if not user_id:
        return _empty_membership()
    org_storage.upsert_profile(client, user_id, email)
    invite = org_storage.find_invite_for_email(client, email)
    if invite and not invite.get("user_id"):
        org_storage.activate_invite(client, invite["id"], user_id)
        clear_membership_cache(user_id)
    membership = load_membership(client, user_id)
    if not membership.get("org_id"):
        try:
            membership = bootstrap_owner_org(client, user_id, email)
        except OSError:
            membership = load_membership(client, user_id)
    return membership


def attach_membership_to_dialer(dialer, membership):
    dialer.org_membership = dict(membership or _empty_membership())


def membership_for_auth(dialer):
    base = getattr(dialer, "org_membership", None) or _empty_membership()
    return {
        "org_id": base.get("org_id") or "",
        "org_name": base.get("org_name") or "",
        "role": base.get("role") or "",
        "status": base.get("status") or "",
        "can_manage_team": bool(base.get("can_manage_team")),
    }


def _voice_settings_ready(dialer):
    from features.settings import values

    user_id = getattr(dialer, "account_user_id", "") or ""
    account_values = getattr(dialer, "account_values", {}) or {}
    env_path = getattr(dialer, "env_path", ENV_PATH)
    current = values(env_path, account_values, signed_in=bool(user_id))
    return bool(
        current.get("TWILIO_ACCOUNT_SID")
        and current.get("TWILIO_AUTH_TOKEN")
        and current.get("TWILIO_API_KEY")
        and current.get("TWILIO_API_SECRET")
        and current.get("TWILIO_TWIML_APP_SID")
        and current.get("PUBLIC_BASE_URL")
    )


def account_setup_payload(runtime, dialer):
    """Onboarding state for signed-in accounts (org + voice credentials)."""
    membership = membership_for_auth(dialer)
    user_id = getattr(dialer, "account_user_id", "") or ""
    supabase = bool(getattr(runtime, "client", None))
    signed_in = bool(user_id) if supabase else True
    org_ready = bool(membership.get("org_id"))
    voice_ready = _voice_settings_ready(dialer)
    next_steps = []
    if supabase and not org_ready:
        next_steps.append("organization")
    if not voice_ready:
        next_steps.append("twilio_voice")
    return {
        "storage": getattr(runtime, "storage_name", "local JSON files"),
        "signed_in": signed_in,
        "org_ready": org_ready,
        "voice_ready": voice_ready,
        "membership": membership,
        "next_steps": next_steps,
    }


def assert_can_view_member(client, viewer_user_id, viewer_membership, target_user_id):
    if not can_manage_team(viewer_membership.get("role")):
        raise PermissionError("Team views are available to managers and owners only.")
    org_id = str(viewer_membership.get("org_id") or "")
    if not org_id:
        raise PermissionError("You are not part of an organization yet.")
    target = str(target_user_id or "")
    if not target:
        raise ValueError("Member id is required.")
    if target == str(viewer_user_id or ""):
        return org_id
    member = org_storage.get_active_membership(client, target)
    if not member or str(member.get("org_id") or "") != org_id:
        raise PermissionError("That team member is not in your organization.")
    return org_id


def presence_is_online(last_seen_at, now=None):
    from datetime import datetime, timezone

    if not last_seen_at:
        return False
    if now is None:
        now = datetime.now(timezone.utc)
    try:
        seen = datetime.fromisoformat(str(last_seen_at).replace("Z", "+00:00"))
    except ValueError:
        return False
    if seen.tzinfo is None:
        seen = seen.replace(tzinfo=timezone.utc)
    return (now - seen).total_seconds() <= TEAM_ONLINE_SECONDS