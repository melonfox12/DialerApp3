"""Organization membership rules: roles, login hooks, and access checks."""

import threading
import time

from features import org_storage
from shared.vocabulary import ORG_MANAGER_ROLES, TEAM_ONLINE_SECONDS

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
            "status": str(member.get("status") or ""),
            "can_manage_team": can_manage_team(member.get("role")),
        }
    with _membership_lock:
        _membership_cache[key] = (now + _MEMBERSHIP_TTL, dict(cached))
        if len(_membership_cache) > 128:
            _membership_cache = {
                item_key: item for item_key, item in _membership_cache.items() if item[0] > now
            }
    return cached


def clear_membership_cache(user_id=None):
    with _membership_lock:
        if user_id is None:
            _membership_cache.clear()
            return
        _membership_cache.pop(_cache_key(user_id), None)


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
    return load_membership(client, user_id)


def attach_membership_to_dialer(dialer, membership):
    dialer.org_membership = dict(membership or _empty_membership())


def membership_for_auth(dialer):
    base = getattr(dialer, "org_membership", None) or _empty_membership()
    return {
        "org_id": base.get("org_id") or "",
        "org_name": base.get("org_name") or "",
        "role": base.get("role") or "",
        "can_manage_team": bool(base.get("can_manage_team")),
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