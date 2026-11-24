# `features/accounts.py`

**Purpose:** Backend choice, signed-in sessions, and the Google bearer check.

## Functions
### `__init__` (line 18)

**Pseudocode:**
- Set self.crm to crm.
- Set self.metrics to metrics.
- Set self.dialer to dialer.
- Set self.dial_archive to dial_archive.
- Set self.dial_records to dial_records.

### `__init__` (line 27)

**Pseudocode:**
- Set self.client to None.
- Set self.storage_name to 'local JSON files'.
- Set self.local to None.
- Set self.sessions to a dict.
- Set self.session_lock to threading.Lock(...).
- Set self.tokens to TokenIndex(...).
- Set self._health_at to 0.
- Set self._health to a dict.

**Calls →**
1. `threading.Lock`
2. `features.dialer.TokenIndex`

### `configure` (line 37)

**Pseudocode:**
- Set values to read_env(...).
- Set client to SupabaseClient.from_env(...).
- Set self.tokens to TokenIndex(...).
- If a boolean condition:
-   Raise an error.
- If client:
-   Set self.client to client.
-   Set self.storage_name to 'Supabase'.

**Calls →**
1. `shared.config.read_env`
2. `shared.infra.SupabaseClient.from_env`
3. `features.dialer.TokenIndex`
4. `features.accounts.ValueError`
5. `features.accounts.AppRuntime._ping`
6. `features.prospects.ProspectStore`
7. `features.metrics.MetricsStore`
8. `features._prospects.dial_archive.DialArchiveStore`
9. `features._prospects.dial_records.DialRecordsStore`
10. `features.dialer.Dialer`
11. `features.accounts.Account`
12. `shared.config.read_env`
13. `crm.sync_pipeline_from_account_values`

### `health` (line 72)

**Pseudocode:**
- If self.client:
-   Return a dict.
- Set now to time.time(...).
- If now op self._health_at compared to ...:
-   Return self._health.
- Try:
-   Call self._ping(...).
- On <ast.Name object at 0x00000242BC225C90>:

**Calls →**
1. `time.time`
2. `features.accounts.AppRuntime._ping`
3. `features.accounts.str`

### `session_for` (line 87)

**Pseudocode:**
- Set user_id to user[...].
- With self.session_lock:
-   Set existing to self.sessions.get(...).
- If existing:
-   Set existing.dialer.account_email to a boolean condition.
-   Try:
-     Set membership to org.sync_user_on_login(...).
-   On <ast.Name object at 0x00000242BC226590>:

**Calls →**
1. `features.accounts.AppRuntime.sessions.get`
2. `user.get`
3. `features.org.sync_user_on_login`
4. `features.org.load_membership`
5. `features.org.attach_membership_to_dialer`
6. `features.prospects.ProspectStore`
7. `features.metrics.SupabaseMetricsStore`
8. `features._prospects.dial_archive.DialArchiveStore`
9. `features._prospects.dial_records.DialRecordsStore`
10. `features.dialer.Dialer`
11. `user.get`
12. `features.settings.load_app_settings`
13. `features.accounts.AppRuntime.persist_settings`
14. `shared.config.read_env`
15. `crm.sync_pipeline_from_account_values`
16. `features.org.sync_user_on_login`
17. `features.org.load_membership`
18. `features.org.attach_membership_to_dialer`
19. `features.accounts.Account`
20. `features.accounts.AppRuntime.sessions.get`

### `persist_settings` (line 130)

**Pseudocode:**
- Set user_id to getattr(...).
- If a boolean condition:
-   Return nothing.
- Try:
-   Call save_app_settings(...).
- On <ast.Name object at 0x00000242BC2BC750>:
-   Set message to str(...).
-   If a boolean condition:

**Calls →**
1. `features.accounts.getattr`
2. `features.settings.save_app_settings`
3. `features.accounts.values`
4. `features.accounts.str`
5. `message.lower`
6. `features.accounts.OSError`

**Called by ←**
- `fn:features/accounts.py:session_for`

### `reload_settings` (line 147)

**Pseudocode:**
- Set user_id to getattr(...).
- If a boolean condition:
-   Return nothing.
- Set remote to load_app_settings(...).
- If remote:
-   Call dialer.account_values.update(...).
-   Try:
-     Call dialer.crm.sync_pipeline_from_account_values(...).

**Calls →**
1. `features.accounts.getattr`
2. `features.settings.load_app_settings`
3. `dialer.account_values.update`
4. `dialer.crm.sync_pipeline_from_account_values`

### `resolve_account` (line 160)

**Pseudocode:**
- Set google to bool(...).
- If a boolean condition:
-   Return Tuple.
- Set header to a boolean condition.
- Set token to IfExp.
- Set user to runtime.client.auth_user(...).
- If user:
-   Return Tuple.

**Calls →**
1. `features.accounts.bool`
2. `path.startswith`
3. `header.lower`
4. `runtime.client.auth_user`
5. `runtime.session_for`

**Called by ←**
- `fn:web.py:open_account`
