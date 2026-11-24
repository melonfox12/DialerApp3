# `web.py`

**Purpose:** HTTP glue: tracing, static files, page assembly, and the route table.

## Routes
- `GET` `/api/auth/config` → `get_auth_config`
- `GET` `/api/health` → `get_health`
- `GET` `/api/auth/me` → `get_auth_me`
- `POST` `/api/debug` → `ingest_client_debug`

## Functions
### `get_auth_config` (line 16)

**Pseudocode:**
- Set client to request.runtime.client.
- Set google to bool(...).
- Call request.send_json(...).

**Calls →**
1. `web.bool`
2. `request.send_json`

**Called by ←**
- `fn:web.py:do_GET`

### `get_health` (line 26)

**Pseudocode:**
- Set payload to request.runtime.health(...).
- Call request.send_json(...).

**Calls →**
1. `request.runtime.health`
2. `request.send_json`
3. `payload.get`

**Called by ←**
- `fn:web.py:do_GET`

### `get_auth_me` (line 31)

**Pseudocode:**
- Set user to IfExp.
- Set email to IfExp.
- Set user_id to IfExp.
- Set payload to a dict.
- If user:
-   Call payload.update(...).
- Else:
-   Call payload.update(...).

**Calls →**
1. `web.getattr`
2. `web.getattr`
3. `payload.update`
4. `features.org.membership_for_auth`
5. `payload.update`
6. `request.send_json`

**Called by ←**
- `fn:web.py:do_GET`

### `ingest_client_debug` (line 43)

**Pseudocode:**
- Set length to int(...).
- If length compared to ...:
-   Call request.send_response(...).
-   Call request.send_header(...).
-   Call request.end_headers(...).
-   Return nothing.
- Set raw to IfExp.
- Try:

**Calls →**
1. `web.int`
2. `request.headers.get`
3. `request.send_response`
4. `request.send_header`
5. `request.end_headers`
6. `request.rfile.read`
7. `json.loads`
8. `raw.decode`
9. `web.isinstance`
10. `web.str`
11. `data.get`
12. `request.send_response`
13. `request.send_header`
14. `request.end_headers`
15. `shared.infra.debug_event`
16. `web.str`
17. `data.get`
18. `data.get`
19. `data.get`
20. `request.send_response`
21. `request.send_header`
22. `request.send_header`
23. `request.end_headers`

**Called by ←**
- `fn:web.py:do_POST`

### `all_routes` (line 84)

**Pseudocode:**
- Return SYSTEM_ROUTES op FEATURE_ROUTES.

**Called by ←**
- `fn:web.py:match_route`

### `match_route` (line 88)

**Pseudocode:**
- For each Tuple in all_routes(...):
-   If route_method compared to ...:
-   Set params to _match_pattern(...).
-   If params compared to ...:
-     Return Tuple.
- Return None.

**Calls →**
1. `web.all_routes`
2. `web._match_pattern`

**Called by ←**
- `fn:web.py:do_GET`
- `fn:web.py:do_POST`
- `fn:web.py:request_refusal`

### `_match_pattern` (line 98)

**Pseudocode:**
- If '{' compared to ...:
-   Return IfExp.
- Set pattern_parts to pattern.split(...).
- Set path_parts to path.split(...).
- If a boolean condition:
-   Return a dict.
- If len(...) compared to ...:
-   Return None.

**Calls →**
1. `pattern.split`
2. `path.split`
3. `path.startswith`
4. `urllib.parse.parse.unquote`
5. `web.len`
6. `web.len`
7. `web.len`
8. `web.zip`
9. `expected.startswith`
10. `expected.endswith`
11. `urllib.parse.parse.unquote`

**Called by ←**
- `fn:web.py:match_route`

### `request_refusal` (line 119)

**Pseudocode:**
- Set hosts to Set.
- If str(...).strip(...).lower(...) compared to ...:
-   Return Tuple.
- If method compared to ...:
-   Return None.
- Set origin to headers.get(...).
- If a boolean condition:
-   Return Tuple.

**Calls →**
1. `web.str`
2. `headers.get`
3. `headers.get`
4. `origin.strip`
5. `web.match_route`
6. `web.str`
7. `headers.get`

**Called by ←**
- `fn:web.py:refuse_untrusted`

### `refuse_untrusted` (line 138)

**Pseudocode:**
- Set refusal to request_refusal(...).
- If refusal compared to ...:
-   Return False.
- Set Tuple to refusal.
- Set self._trace_error to message.
- Call self.send_json(...).
- Return True.

**Calls →**
1. `web.request_refusal`
2. `web.AppHandler.send_json`

**Called by ←**
- `fn:web.py:do_DELETE`
- `fn:web.py:do_GET`
- `fn:web.py:do_POST`

### `open_account` (line 147)

**Pseudocode:**
- Set Tuple to resolve_account(...).
- If error:
-   Call self.send_json(...).
-   Return False.
- Set self.account to account.
- Set self.ctx to FeatureContext(...).
- Return True.

**Calls →**
1. `features.accounts.resolve_account`
2. `web.AppHandler.headers.get`
3. `web.AppHandler.send_json`
4. `web.FeatureContext`

**Called by ←**
- `fn:web.py:do_DELETE`
- `fn:web.py:do_GET`
- `fn:web.py:do_POST`

### `report_storage_error` (line 156)

**Pseudocode:**
- Set self._trace_error to str(...).
- Set account to getattr(...).
- If account:
-   Call account.dialer.record_activity(...).
- Call self.send_json(...).

**Calls →**
1. `web.str`
2. `web.getattr`
3. `account.dialer.record_activity`
4. `web.AppHandler.send_json`

**Called by ←**
- `fn:web.py:do_GET`

### `do_GET` (line 163)

**Pseudocode:**
- Call self.begin_trace(...).
- Set path to self._trace_path.
- If self.refuse_untrusted(...):
-   Return nothing.
- If path compared to ...:
-   Call get_auth_config(...).
-   Return nothing.
- If path compared to ...:

**Calls →**
1. `web.AppHandler.begin_trace`
2. `web.AppHandler.refuse_untrusted`
3. `web.get_auth_config`
4. `web.get_health`
5. `web.AppHandler.serve_static`
6. `web.AppHandler.open_account`
7. `web.get_auth_me`
8. `web.AppHandler.send_json`
9. `path.startswith`
10. `dialer_session.record_activity`
11. `web.match_route`
12. `web.AppHandler.send_json`
13. `web.handler`
14. `web.str`
15. `web.AppHandler.send_json`
16. `web.str`
17. `web.handler`
18. `web.AppHandler.report_storage_error`
19. `web.handler`

### `do_POST` (line 208)

**Pseudocode:**
- Call self.begin_trace(...).
- Set path to self._trace_path.
- If self.refuse_untrusted(...):
-   Return nothing.
- If path compared to ...:
-   Call ingest_client_debug(...).
-   Return nothing.
- If self.open_account(...):

**Calls →**
1. `web.AppHandler.begin_trace`
2. `web.AppHandler.refuse_untrusted`
3. `web.ingest_client_debug`
4. `web.AppHandler.open_account`
5. `web.AppHandler.send_json`
6. `path.startswith`
7. `dialer_session.record_activity`
8. `web.AppHandler.read_body`
9. `web.match_route`
10. `web.AppHandler.send_json`
11. `web.handler`
12. `web.AppHandler.read_json`
13. `web.handler`
14. `web.handler`
15. `web.AppHandler.read_json`
16. `web.handler`
17. `web.str`
18. `path.startswith`
19. `dialer_session.record_activity`
20. `web.AppHandler.send_json`
21. `web.str`
22. `web.str`
23. `path.startswith`
24. `dialer_session.record_activity`
25. `web.AppHandler.send_json`
26. `web.str`
27. `shared.infra.debug_event`
28. `traceback.format_exc`
29. `path.startswith`
30. `dialer_session.record_activity`

### `do_DELETE` (line 275)

**Pseudocode:**
- Call self.begin_trace(...).
- Set path to self._trace_path.
- If self.refuse_untrusted(...):
-   Return nothing.
- If self.open_account(...):
-   Return nothing.
- Set account to self.account.
- If account compared to ...:

**Calls →**
1. `web.AppHandler.begin_trace`
2. `web.AppHandler.refuse_untrusted`
3. `web.AppHandler.open_account`
4. `web.AppHandler.send_json`
5. `path.startswith`
6. `features.prospects.delete_lead`
7. `web.AppHandler.send_json`

### `__init__` (line 293)

**Pseudocode:**
- Set self.request to request.

### `state` (line 296)

**Pseudocode:**
- Return self.request.account.dialer.public_state(...).

**Calls →**
1. `web.FeatureContext.request.account.dialer.public_state`

### `log` (line 299)

**Pseudocode:**
- Call self.request.account.dialer.record_activity(...).

**Calls →**
1. `web.FeatureContext.request.account.dialer.record_activity`

### `reload_settings` (line 302)

**Pseudocode:**
- Call self.request.runtime.reload_settings(...).

**Calls →**
1. `web.FeatureContext.request.runtime.reload_settings`

### `save_posted_settings` (line 305)

**Pseudocode:**
- Set session to self.request.account.dialer.
- Set before to dict(...).
- Call session.save_settings(...).
- If session.account_user_id:
-   Call session.account_values.update(...).
- Set after to dict(...).
- Try:
-   Call session.crm.sync_pipeline_from_merged_values(...).

**Calls →**
1. `web.dict`
2. `session.save_settings`
3. `session.account_values.update`
4. `shared.config.read_env`
5. `web.dict`
6. `session.crm.sync_pipeline_from_merged_values`

### `settings_view` (line 317)

**Pseudocode:**
- Return self.request.account.dialer.settings_state(...).

**Calls →**
1. `web.FeatureContext.request.account.dialer.settings_state`

### `make_app_handler` (line 321)

**Pseudocode:**
- Set AppHandler.runtime to runtime.
- Return AppHandler.

**Called by ←**
- `fn:server.py:serve`
