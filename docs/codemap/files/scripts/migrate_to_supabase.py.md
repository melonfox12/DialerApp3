# `scripts/migrate_to_supabase.py`

**Purpose:** Import existing local JSON data into Supabase without overwriting other records.

## Routes
- `POST` `dialer_sessions` → `payload`

## Functions
### `migrate_local_data` (line 14)
_Import local JSON data without overwriting different remote records._

**Pseudocode:**
- Set prospects to ProspectStore(...).leads.
- Set metric_data to MetricsStore(...).data.
- Set local_prospects to DictComp.
- Set local_daily to DictComp.
- Set local_totals to metric_data.get(...).
- Set existing_prospects to client.select_all(...).
- Set existing_daily to client.select_all(...).
- Set existing_totals to client.select_all(...).

**Calls →**
1. `scripts.migrate_to_supabase.ProspectStore`
2. `scripts.migrate_to_supabase.MetricsStore`
3. `metric_data.get`
4. `values.items`
5. `metric_data.get`
6. `client.select_all`
7. `client.select_all`
8. `client.select_all`
9. `client.select_all`
10. `scripts.migrate_to_supabase.isinstance`
11. `scripts.migrate_to_supabase.ValueError`
12. `local_prospects.get`
13. `row.get`
14. `row.get`
15. `scripts.migrate_to_supabase.ValueError`
16. `scripts.migrate_to_supabase.isinstance`
17. `scripts.migrate_to_supabase.ValueError`
18. `local_daily.get`
19. `scripts.migrate_to_supabase.str`
20. `row.get`
21. `row.get`
22. `row.get`
23. `scripts.migrate_to_supabase.ValueError`
24. `scripts.migrate_to_supabase.isinstance`
25. `scripts.migrate_to_supabase.ValueError`
26. `local_totals.get`
27. `row.get`
28. `row.get`
29. `scripts.migrate_to_supabase.ValueError`
30. `metric_data.get`

**Called by ←**
- `fn:scripts/migrate_to_supabase.py:main`

### `_user_id` (line 106)

**Pseudocode:**
- Try:
-   Return str(...).
- On <ast.Name object at 0x00000242BC216B10>:
-   Raise an error.

**Calls →**
1. `scripts.migrate_to_supabase.str`
2. `uuid.UUID`
3. `argparse.ArgumentTypeError`

### `main` (line 113)

**Pseudocode:**
- Set parser to argparse.ArgumentParser(...).
- Call parser.add_argument(...).
- Set args to parser.parse_args(...).
- Set values to read_env(...).
- Set client to SupabaseClient.from_env(...).
- If client:
-   Raise an error.
- Set result to migrate_local_data(...).

**Calls →**
1. `argparse.ArgumentParser`
2. `parser.add_argument`
3. `parser.parse_args`
4. `shared.config.read_env`
5. `os.path.join`
6. `shared.infra.SupabaseClient.from_env`
7. `scripts.migrate_to_supabase.SystemExit`
8. `scripts.migrate_to_supabase.migrate_local_data`
9. `os.path.join`
10. `os.path.join`
11. `scripts.migrate_to_supabase.print`
