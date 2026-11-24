# `shared/config.py`

**Purpose:** Paths, ports, and .env read/write.

## Functions
### `read_env` (line 35)

**Pseudocode:**
- Set values to a dict.
- If os.path.exists(...):
-   With open(...):
-     For each line in env_file:
-       Set line to line.strip(...).
-       If a boolean condition:
-         Set Tuple to line.split(...).
-         Set key to key.strip(...).

**Calls →**
1. `os.path.exists`
2. `shared.config.open`
3. `line.strip`
4. `line.startswith`
5. `line.split`
6. `key.strip`
7. `value.strip`
8. `json.loads`
9. `json.loads`
10. `shared.config.isinstance`
11. `json.dumps`
12. `value.strip`
13. `values.setdefault`
14. `os.environ.get`

**Called by ←**
- `fn:features/accounts.py:configure`
- `fn:features/accounts.py:session_for`
- `fn:features/prospects.py:post_save_pipeline_settings`
- `fn:features/settings.py:values`
- `fn:scripts/migrate_to_supabase.py:main`
- `fn:shared/config.py:write_env`
- `fn:web.py:save_posted_settings`

### `write_env` (line 67)

**Pseudocode:**
- Set values to read_env(...).
- For each Tuple in updates.items(...):
-   Set stripped to str(...).strip(...).
-   If key compared to ...:
-     Set values[...] to json.dumps(...).
-   Else:
-     If key compared to ...:
-       If isinstance(...):

**Calls →**
1. `shared.config.read_env`
2. `updates.items`
3. `shared.config.str`
4. `json.dumps`
5. `shared.config.isinstance`
6. `json.dumps`
7. `values.items`
8. `shared.config.open`
9. `env_file.write`
10. `os.replace`
11. `os.chmod`
12. `shared.config.dict`
13. `shared.config.isinstance`
14. `json.loads`

**Called by ←**
- `fn:features/prospects.py:post_save_pipeline_settings`
- `fn:features/settings.py:save_goal`
- `fn:features/settings.py:save_settings`
