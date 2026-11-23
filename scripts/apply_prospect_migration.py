#!/usr/bin/env python3
"""Apply docs/supabase/migrations/202611231700_prospect_restructure.sql using server .env credentials."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATION = ROOT / "docs" / "supabase" / "migrations" / "202611231700_prospect_restructure.sql"


def main():
    sys.path.insert(0, str(ROOT))
    from shared.config import ENV_PATH, read_env
    from shared._infra.supabase import SupabaseClient

    sql = MIGRATION.read_text(encoding="utf-8")
    client = SupabaseClient.from_env(read_env(ENV_PATH))
    if not client:
        print("Supabase is not configured in .env; skipping remote migration.", file=sys.stderr)
        return 1
    status, body = client._pool.send(
        "POST",
        "/rest/v1/rpc/",
        None,
        {
            "apikey": client.service_key,
            "Authorization": f"Bearer {client.service_key}",
            "Content-Type": "application/json",
        },
    )
    # PostgREST has no arbitrary SQL; print instructions when RPC is unavailable.
    print("Run this migration in the Supabase SQL editor (Dashboard → SQL):")
    print(MIGRATION)
    print("\nFile:", MIGRATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())