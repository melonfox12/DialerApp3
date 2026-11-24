# `scripts/apply_prospect_migration.py`

**Purpose:** Apply docs/supabase/migrations/202611231700_prospect_restructure.sql using server .env credentials.

## Routes
- `POST` `/rest/v1/rpc/` → `None`

## Functions
### `main` (line 11)

**Pseudocode:**
- Call sys.path.insert(...).
- Set sql to MIGRATION.read_text(...).
- Set client to SupabaseClient.from_env(...).
- If client:
-   Call print(...).
-   Return 1.
- Set Tuple to client._pool.send(...).
- Call print(...).

**Calls →**
1. `sys.path.insert`
2. `scripts.apply_prospect_migration.str`
3. `MIGRATION.read_text`
4. `SupabaseClient.from_env`
5. `scripts.apply_prospect_migration.read_env`
6. `scripts.apply_prospect_migration.print`
7. `client._pool.send`
8. `scripts.apply_prospect_migration.print`
9. `scripts.apply_prospect_migration.print`
10. `scripts.apply_prospect_migration.print`
