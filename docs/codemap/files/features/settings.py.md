# `features/settings.py`

**Purpose:** Preference validation, settings view, and env or account persistence.

## Routes
- `GET` `/api/settings` → `get_settings`
- `POST` `/api/settings` → `post_settings`

## Functions
### `preferences` (line 20)

**Pseudocode:**
- Set result to dict(...).
- For each key in result:
-   If key compared to ...:
-     Set raw to values.get(...).
-     If raw compared to ...:
-       Set result[...] to ''.
-     Else:
-       If isinstance(...):

**Calls →**
1. `features.settings.dict`
2. `values.get`
3. `features.settings.isinstance`
4. `raw.strip`
5. `json.dumps`
6. `features.settings.str`
7. `values.get`
8. `features.settings.str`
9. `values.get`
10. `features.settings.int`
11. `features.settings.ValueError`
12. `key.replace`
13. `features.settings.ValueError`
14. `key.replace`
15. `features.settings.str`
16. `features.settings.int`
17. `features.settings.int`
18. `features.settings.ValueError`
19. `datetime.date.fromisoformat`
20. `features.settings.ValueError`
21. `features.settings.ValueError`
22. `features.settings.len`
23. `features.settings.ValueError`
24. `result.get`
25. `shared.pipeline_config.parse_custom_pipeline_steps_json`
26. `features.settings.ValueError`

**Called by ←**
- `fn:features/dialer.py:read_settings`
- `fn:features/settings.py:save_goal`
- `fn:features/settings.py:save_settings`
- `fn:features/settings.py:settings_state`

### `values` (line 76)

**Pseudocode:**
- Set server to read_env(...).
- If signed_in:
-   Set server to DictComp.
- Return a dict.

**Calls →**
1. `shared.config.read_env`
2. `server.items`

**Called by ←**
- `fn:features/dialer.py:read_values`
- `fn:features/settings.py:save_goal`
- `fn:features/settings.py:save_settings`
- `fn:features/settings.py:settings_state`

### `_pipeline_json_from_post` (line 83)
_Build PIPELINE_CUSTOM_STEPS_JSON from settings form POST._

**Pseudocode:**
- Set raw to data.get(...).
- If raw compared to ...:
-   Return str(...).strip(...).
- Set steps to data.get(...).
- If steps compared to ...:
-   Return None.
- If isinstance(...):
-   Return steps.strip(...).

**Calls →**
1. `data.get`
2. `features.settings.str`
3. `data.get`
4. `features.settings.isinstance`
5. `steps.strip`
6. `features.settings.isinstance`
7. `json.dumps`

**Called by ←**
- `fn:features/settings.py:save_settings`

### `settings_state` (line 98)

**Pseudocode:**
- Set current to values(...).
- Set parsed to preferences(...).
- Set Tuple to parse_custom_pipeline_steps_json(...).
- Return a dict.

**Calls →**
1. `features.settings.values`
2. `features.settings.preferences`
3. `shared.pipeline_config.parse_custom_pipeline_steps_json`
4. `parsed.get`
5. `current.get`
6. `current.get`
7. `current.get`
8. `current.get`
9. `current.get`
10. `features.settings.bool`
11. `current.get`
12. `features.settings.bool`
13. `current.get`
14. `features.settings.int`
15. `features.settings.int`
16. `features.settings.int`
17. `features.settings.int`
18. `features.settings.int`
19. `features.settings.int`
20. `features.settings.int`
21. `parsed.get`
22. `parsed.get`
23. `features.settings.bool`
24. `parsed.get`
25. `parsed.get`
26. `features.settings.bool`
27. `parsed.get`
28. `parsed.get`
29. `features.settings.bool`
30. `parsed.get`

**Called by ←**
- `fn:features/dialer.py:settings_state`

### `daily_goal` (line 144)
_The goal dict features.performance reads, from parsed preferences._

**Pseudocode:**
- Return a dict.

**Calls →**
1. `features.settings.int`
2. `features.settings.int`
3. `features.settings.int`
4. `features.settings.int`

**Called by ←**
- `fn:features/dialer.py:save_goal`
- `fn:features/metrics.py:get_performance`

### `save_goal` (line 155)
_Save only the daily goal keys. A weekly step counts from an anchor date: today, whenever the goal changes._

**Pseudocode:**
- Set signed_in to bool(...).
- Set current to values(...).
- Set minutes to data.get(...).
- Set conversations to data.get(...).
- Set step to data.get(...).
- If a boolean condition:
-   Raise an error.
- Set same to a boolean condition.

**Calls →**
1. `features.settings.bool`
2. `features.settings.values`
3. `data.get`
4. `data.get`
5. `current.get`
6. `data.get`
7. `current.get`
8. `data.get`
9. `current.get`
10. `features.settings.isinstance`
11. `features.settings.isinstance`
12. `features.settings.isinstance`
13. `features.settings.ValueError`
14. `features.settings.str`
15. `features.settings.str`
16. `current.get`
17. `features.settings.str`
18. `features.settings.str`
19. `current.get`
20. `features.settings.str`
21. `features.settings.str`
22. `current.get`
23. `current.get`
24. `today.isoformat`
25. `features.settings.preferences`
26. `features.settings.int`
27. `account_values.update`
28. `features.settings.save_remote`
29. `features.settings.values`
30. `shared.config.write_env`

**Called by ←**
- `fn:features/dialer.py:save_goal`

### `save_settings` (line 189)

**Pseudocode:**
- Set signed_in to bool(...).
- Set existing to values(...).
- Set candidate to a dict.
- If a boolean condition:
-   Set pj to _pipeline_json_from_post(...).
-   If pj compared to ...:
-     Set candidate[...] to pj.
- Set parsed to preferences(...).

**Calls →**
1. `features.settings.bool`
2. `features.settings.values`
3. `data.get`
4. `existing.get`
5. `data.get`
6. `existing.get`
7. `data.get`
8. `existing.get`
9. `data.get`
10. `data.get`
11. `data.get`
12. `features.settings.str`
13. `data.get`
14. `data.get`
15. `data.get`
16. `data.get`
17. `data.get`
18. `data.get`
19. `features.settings.str`
20. `data.get`
21. `existing.get`
22. `features.settings.str`
23. `data.get`
24. `existing.get`
25. `features.settings.str`
26. `data.get`
27. `existing.get`
28. `features.settings.str`
29. `data.get`
30. `existing.get`

**Called by ←**
- `fn:features/dialer.py:save_settings`

### `load_app_settings` (line 252)

**Pseudocode:**
- Set row_id to str(...).
- Try:
-   Set rows to client.request(...).
- On <ast.Name object at 0x00000242BC270E10>:
-   If a boolean condition:
-     Return a dict.
-   Raise an error.
- If rows:

**Calls →**
1. `features.settings.str`
2. `client.request`
3. `features.settings.str`
4. `features.settings.str`
5. `features.settings.str`
6. `features.settings.isinstance`
7. `features.settings.isinstance`
8. `features.settings.isinstance`
9. `features.settings.OSError`
10. `features.settings.str`
11. `stored.get`

**Called by ←**
- `fn:features/accounts.py:reload_settings`
- `fn:features/accounts.py:session_for`

### `save_app_settings` (line 276)

**Pseudocode:**
- Set payload to a dict.
- Call client.request(...).

**Calls →**
1. `features.settings.str`
2. `features.settings.str`
3. `stored_values.get`
4. `client.request`

**Called by ←**
- `fn:features/accounts.py:persist_settings`

### `get_settings` (line 290)

**Pseudocode:**
- Call request.ctx.reload_settings(...).
- Call request.send_json(...).

**Calls →**
1. `request.ctx.reload_settings`
2. `request.send_json`
3. `request.ctx.settings_view`

### `post_settings` (line 295)

**Pseudocode:**
- Call request.ctx.save_posted_settings(...).
- Call request.send_json(...).

**Calls →**
1. `request.ctx.save_posted_settings`
2. `request.send_json`
3. `request.ctx.settings_view`
