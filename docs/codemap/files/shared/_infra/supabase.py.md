# `shared/_infra/supabase.py`

**Purpose:** (no module docstring)

## Routes
- `GET` `/auth/v1/user` → `None`

## Functions
### `__init__` (line 7)

**Pseudocode:**
- Set self.host to host.
- Set self.timeout to timeout.
- Set self.size to size.
- Set self._lock to threading.Lock(...).
- Set self._idle to a list.

**Calls →**
1. `threading.Lock`

### `send` (line 17)

**Pseudocode:**
- Set last_error to None.
- For each _attempt in range(...):
-   With self._lock:
-     Set conn to IfExp.
-   If conn compared to ...:
-     Set conn to self._new(...).
-   Try:
-     Call conn.request(...).

**Calls →**
1. `shared._infra.supabase.range`
2. `shared._infra.supabase._ConnectionPool._idle.pop`
3. `shared._infra.supabase._ConnectionPool._new`
4. `conn.request`
5. `conn.getresponse`
6. `response.read`
7. `conn.close`
8. `shared._infra.supabase.len`
9. `shared._infra.supabase._ConnectionPool._idle.append`
10. `conn.close`
11. `shared._infra.supabase.OSError`

### `__init__` (line 48)

**Pseudocode:**
- Set parsed to urllib.parse.urlsplit(...).
- If a boolean condition:
-   Raise an error.
- If service_key:
-   Raise an error.
- If service_key.startswith(...):
-   Raise an error.
- If service_key.count(...) compared to ...:

**Calls →**
1. `urllib.parse.parse.urlsplit`
2. `shared._infra.supabase.ValueError`
3. `shared._infra.supabase.ValueError`
4. `service_key.startswith`
5. `shared._infra.supabase.ValueError`
6. `service_key.count`
7. `service_key.split`
8. `json.loads`
9. `base64.urlsafe_b64decode`
10. `shared._infra.supabase.len`
11. `shared._infra.supabase.ValueError`
12. `shared._infra.supabase.isinstance`
13. `claims.get`
14. `shared._infra.supabase.ValueError`
15. `url.rstrip`
16. `shared._infra.supabase._ConnectionPool`
17. `urllib.parse.parse.urlsplit`
18. `threading.Lock`

### `from_env` (line 79)

**Pseudocode:**
- Set url to values.get(...).strip(...).
- Set key to a boolean condition.
- Set anon to a boolean condition.
- If bool(...) compared to ...:
-   Raise an error.
- Return IfExp.

**Calls →**
1. `values.get`
2. `values.get`
3. `values.get`
4. `values.get`
5. `values.get`
6. `shared._infra.supabase.bool`
7. `shared._infra.supabase.bool`
8. `shared._infra.supabase.ValueError`
9. `shared._infra.supabase.cls`

### `auth_user` (line 96)

**Pseudocode:**
- Set token to a boolean condition.strip(...).
- If token:
-   Return None.
- Set now to time.time(...).
- With self._auth_lock:
-   Set cached to self._auth_cache.get(...).
-   If a boolean condition:
-     Return cached[...].

**Calls →**
1. `time.time`
2. `shared._infra.supabase.SupabaseClient._auth_cache.get`
3. `shared._infra.supabase.SupabaseClient._fetch_auth_user`
4. `shared._infra.supabase.len`
5. `shared._infra.supabase.SupabaseClient._auth_cache.items`

### `request` (line 134)

**Pseudocode:**
- Set path to '/rest/v1/' op resource.
- If params:
-   Update path with Add '?' op urllib.parse.urlencode(...).
- Set body to IfExp.
- Set headers to a dict.
- If body compared to ...:
-   Set headers[...] to 'application/json'.
- If prefer:

**Calls →**
1. `urllib.parse.parse.urlencode`
2. `json.dumps`
3. `shared._infra.supabase.SupabaseClient._pool.send`
4. `json.loads`
5. `result.decode`
6. `shared._infra.supabase.isinstance`
7. `shared._infra.supabase.ValueError`
8. `error_body.get`
9. `shared._infra.supabase.OSError`
10. `json.loads`
11. `result.decode`
12. `shared._infra.supabase.OSError`

**Called by ←**
- `fn:shared/_infra/supabase.py:select_all`

### `select_all` (line 165)

**Pseudocode:**
- Set rows to a list.
- Set offset to 0.
- While True:
-   Set page_params to dict(...).
-   Call page_params.update(...).
-   Set page to self.request(...).
-   If isinstance(...):
-     Raise an error.

**Calls →**
1. `shared._infra.supabase.dict`
2. `page_params.update`
3. `shared._infra.supabase.str`
4. `shared._infra.supabase.str`
5. `shared._infra.supabase.SupabaseClient.request`
6. `shared._infra.supabase.isinstance`
7. `shared._infra.supabase.OSError`
8. `rows.extend`
9. `shared._infra.supabase.len`
