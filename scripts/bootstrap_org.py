#!/usr/bin/env python3
"""Create an organization and attach an owner, optionally invite reps by email.

Usage:
  python -m scripts.bootstrap_org --owner-user-id UUID [--org-name "Acme Sales"]
  python -m scripts.bootstrap_org --owner-user-id UUID --invite rep@example.com

Owner user id: Supabase Dashboard → Authentication → Users → copy user UUID after first Google sign-in.
Run docs/supabase/migrations/202611232200_org_structure.sql in the SQL editor first.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Bootstrap organization and owner membership.")
    parser.add_argument("--owner-user-id", required=True, help="Supabase auth user UUID for the manager/owner")
    parser.add_argument("--org-name", default="My team", help="Display name for the organization")
    parser.add_argument("--invite", action="append", default=[], help="Rep email to pre-invite (repeatable)")
    parser.add_argument("--owner-email", default="", help="Optional email stored on profile row")
    args = parser.parse_args()

    sys.path.insert(0, str(ROOT))
    from shared.config import ENV_PATH, read_env
    from shared._infra.supabase import SupabaseClient
    from features import org_storage
    from shared.vocabulary import DEFAULT_ORG_NAME

    import os

    values = read_env(ENV_PATH)
    try:
        client = SupabaseClient.from_env(values)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not client:
        url = values.get("SUPABASE_URL", "").strip()
        key = (
            values.get("SUPABASE_SECRET_KEY", "").strip()
            or values.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        )
        hints = []
        if not os.path.exists(ENV_PATH):
            hints.append(f"Create {ENV_PATH} (see .env.example)")
        if not url:
            hints.append("Set SUPABASE_URL")
        if not key:
            hints.append("Set SUPABASE_SECRET_KEY or SUPABASE_SERVICE_ROLE_KEY")
        detail = "; ".join(hints) if hints else "SUPABASE_URL and server secret must both be set"
        print(f"Configure Supabase in .env before bootstrapping an org. ({detail})", file=sys.stderr)
        return 1

    owner_id = str(args.owner_user_id).strip()
    if not owner_id:
        print("owner-user-id is required.", file=sys.stderr)
        return 1

    existing = org_storage.get_active_membership(client, owner_id)
    if existing:
        org = org_storage.get_organization(client, existing["org_id"])
        print(f"User already belongs to org {org.get('name') if org else existing['org_id']} as {existing.get('role')}.")
        org_id = existing["org_id"]
    else:
        org = org_storage.create_organization(client, args.org_name or DEFAULT_ORG_NAME)
        org_id = org["id"]
        org_storage.add_member(client, org_id, user_id=owner_id, role="owner", status="active")
        print(f"Created organization {org.get('name')} ({org_id}) with owner {owner_id}.")

    if args.owner_email:
        org_storage.upsert_profile(client, owner_id, args.owner_email)

    for email in args.invite or []:
        row = org_storage.invite_member(client, org_id, email, role="rep")
        print(f"Invited {row.get('invited_email')} ({row.get('id')})")

    print("Done. Manager signs in with Google and opens the Team tab.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())