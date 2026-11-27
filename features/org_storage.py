"""Supabase reads and writes for organizations, members, profiles, and presence."""

from datetime import datetime, timezone

from shared.vocabulary import ORG_ROLES


def _iso_now():
    return datetime.now(timezone.utc).isoformat()


def _row(rows):
    if not rows:
        return None
    return rows[0] if isinstance(rows, list) else rows


def get_organization(client, org_id):
    rows = client.request("GET", "organizations", {
        "select": "id,name,created_at",
        "id": f"eq.{org_id}",
        "limit": "1",
    }) or []
    return _row(rows)


def get_active_membership(client, user_id):
    rows = client.request("GET", "org_members", {
        "select": "id,org_id,user_id,role,status,invited_email,joined_at",
        "user_id": f"eq.{user_id}",
        "status": "eq.active",
        "limit": "1",
    }) or []
    return _row(rows)


def list_org_members(client, org_id):
    rows = client.request("GET", "org_members", {
        "select": "id,org_id,user_id,role,status,invited_email,joined_at,created_at",
        "org_id": f"eq.{org_id}",
        "order": "created_at.asc",
    }) or []
    return list(rows) if isinstance(rows, list) else []


def find_invite_for_email(client, email):
    normalized = str(email or "").strip().lower()
    if not normalized:
        return None
    rows = client.request("GET", "org_members", {
        "select": "id,org_id,user_id,role,status,invited_email",
        "status": "eq.invited",
        "invited_email": f"eq.{normalized}",
        "limit": "1",
    }) or []
    row = _row(rows)
    if row and str(row.get("invited_email") or "").strip().lower() != normalized:
        return None
    return row


def activate_invite(client, member_id, user_id):
    client.request(
        "PATCH",
        "org_members",
        {"id": f"eq.{member_id}"},
        {
            "user_id": user_id,
            "status": "active",
            "joined_at": _iso_now(),
        },
        "return=minimal",
    )


def upsert_profile(client, user_id, email, display_name=""):
    body = {
        "user_id": user_id,
        "email": str(email or "").strip(),
        "display_name": str(display_name or "").strip(),
        "updated_at": _iso_now(),
    }
    client.request(
        "POST",
        "profiles",
        {"on_conflict": "user_id"},
        body,
        "resolution=merge-duplicates,return=minimal",
    )


def get_profiles(client, user_ids):
    if not user_ids:
        return {}
    ids = ",".join(user_ids)
    rows = client.request("GET", "profiles", {
        "select": "user_id,email,display_name",
        "user_id": f"in.({ids})",
    }) or []
    return {str(row["user_id"]): row for row in rows if row.get("user_id")}


def create_organization(client, name):
    rows = client.request("POST", "organizations", None, {"name": name or "My team"}, "return=representation")
    return _row(rows)


def add_member(client, org_id, *, user_id=None, role="rep", status="active", invited_email=""):
    if role not in ORG_ROLES:
        raise ValueError("Invalid organization role.")
    body = {
        "org_id": org_id,
        "role": role,
        "status": status,
        "invited_email": str(invited_email or "").strip().lower(),
    }
    if user_id:
        body["user_id"] = user_id
        body["joined_at"] = _iso_now()
    rows = client.request("POST", "org_members", None, body, "return=representation")
    return _row(rows)


def upsert_presence(client, user_id, org_id, fields):
    body = {
        "user_id": user_id,
        "org_id": org_id,
        "last_seen_at": _iso_now(),
        "running": bool(fields.get("running")),
        "paused": bool(fields.get("paused")),
        "stage": str(fields.get("stage") or "idle"),
        "active_lead_id": str(fields.get("active_lead_id") or ""),
        "in_flight_count": int(fields.get("in_flight_count") or 0),
    }
    client.request(
        "POST",
        "dialer_presence",
        {"on_conflict": "user_id"},
        body,
        "resolution=merge-duplicates,return=minimal",
    )


def list_presence_for_org(client, org_id):
    rows = client.request("GET", "dialer_presence", {
        "select": "user_id,org_id,last_seen_at,running,paused,stage,active_lead_id,in_flight_count",
        "org_id": f"eq.{org_id}",
    }) or []
    return {str(row["user_id"]): row for row in rows if row.get("user_id")}


def insert_usage_event(client, org_id, user_id, kind, payload=None, at_iso=None):
    body = {
        "org_id": org_id,
        "user_id": user_id,
        "kind": str(kind or ""),
        "payload": payload if isinstance(payload, dict) else {},
    }
    if at_iso:
        body["at"] = at_iso
    client.request("POST", "usage_events", None, body, "return=minimal")


def list_usage_events(client, org_id, user_id, *, since_iso, limit=250):
    rows = client.request("GET", "usage_events", {
        "select": "id,kind,at,payload",
        "org_id": f"eq.{org_id}",
        "user_id": f"eq.{user_id}",
        "at": f"gte.{since_iso}",
        "order": "at.desc",
        "limit": str(max(1, min(500, int(limit)))),
    }) or []
    return list(rows) if isinstance(rows, list) else []


def invite_member(client, org_id, email, role="rep"):
    if role not in ORG_ROLES:
        raise ValueError("Invalid organization role.")
    normalized = str(email or "").strip().lower()
    if not normalized or "@" not in normalized:
        raise ValueError("Enter a valid email address for the invite.")
    return add_member(client, org_id, role=role, status="invited", invited_email=normalized)