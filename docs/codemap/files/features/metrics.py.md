# `features/metrics.py`

**Purpose:** Local JSON and Supabase dialing metrics.

## Routes
- `POST` `rpc/increment_metric` → `payload`
- `GET` `dialer_sessions` → `self`
- `GET` `dialer_metric_daily` → `self`
- `GET` `dialer_metric_totals` → `self`
- `GET` `/api/metrics` → `get_metrics`
- `GET` `/api/performance` → `get_performance`
- `POST` `/api/performance/goal` → `post_goal`
- `POST` `/api/bookings` → `post_booking`

## Functions
### `__init__` (line 16)

**Pseudocode:**
- Set self.path to Path(...).
- Set self.lock to threading.RLock(...).
- Set self.data to a dict.
- Call self.load(...).

**Calls →**
1. `pathlib.Path`
2. `threading.RLock`
3. `features.metrics.MetricsStore.load`

### `load` (line 22)

**Pseudocode:**
- With self.lock:
-   If self.path.exists(...):
-     Try:
-       Set data to json.loads(...).
-       If isinstance(...):
-         Set self.data to data.
-     On <ast.Tuple object at 0x00000242BC309F90>:
-       No-op.

**Calls →**
1. `features.metrics.MetricsStore.path.exists`
2. `json.loads`
3. `features.metrics.MetricsStore.path.read_text`
4. `features.metrics.isinstance`
5. `features.metrics.MetricsStore.data.setdefault`
6. `features.metrics.MetricsStore.data.setdefault`
7. `features.metrics.MetricsStore.data.setdefault`

**Called by ←**
- `fn:features/metrics.py:__init__`

### `save` (line 35)

**Pseudocode:**
- With self.lock:
-   Call self.path.parent.mkdir(...).
-   Set temp_path to self.path.with_suffix(...).
-   Call temp_path.write_text(...).
-   Call temp_path.replace(...).

**Calls →**
1. `features.metrics.MetricsStore.path.parent.mkdir`
2. `features.metrics.MetricsStore.path.with_suffix`
3. `temp_path.write_text`
4. `json.dumps`
5. `temp_path.replace`

**Called by ←**
- `fn:features/metrics.py:bump`
- `fn:features/metrics.py:save_session`

### `bump` (line 46)

**Pseudocode:**
- With self.lock:
-   Set bucket to self.data[...].setdefault(...).
-   Set bucket[...] to bucket.get(...) op amount.
-   Set self.data[...][...] to self.data[...].get(...) op amount.
-   Call self.save(...).

**Calls →**
1. `features.metrics.MetricsStore._today`
2. `bucket.get`
3. `features.metrics.MetricsStore.save`

### `save_session` (line 53)

**Pseudocode:**
- With self.lock:
-   Set sessions to self.data.setdefault(...).
-   For each Tuple in enumerate(...):
-     If stored.get(...) compared to ...:
-       Set sessions[...] to dict(...).
-   Set self.data[...] to sessions[...].
-   Call self.save(...).

**Calls →**
1. `features.metrics.MetricsStore.data.setdefault`
2. `features.metrics.enumerate`
3. `stored.get`
4. `session.get`
5. `features.metrics.dict`
6. `sessions.append`
7. `features.metrics.dict`
8. `features.metrics.MetricsStore.save`

### `recent_sessions` (line 65)

**Pseudocode:**
- With self.lock:
-   Return ListComp.

**Calls →**
1. `features.metrics.dict`
2. `features.metrics.reversed`
3. `features.metrics.MetricsStore.data.get`

### `snapshot` (line 69)

**Pseudocode:**
- With self.lock:
-   Set today to dict(...).
-   Set all_time to dict(...).
-   Set series to a list.
-   Set now to utc_now(...).
-   For each offset in range(...):
-     Set day to now op timedelta(...).strftime(...).
-     Set bucket to self.data[...].get(...).

**Calls →**
1. `features.metrics.dict`
2. `features.metrics.MetricsStore._today`
3. `features.metrics.dict`
4. `shared.infra.utc_now`
5. `features.metrics.range`
6. `datetime.timedelta`
7. `series.append`
8. `bucket.get`
9. `bucket.get`
10. `bucket.get`

### `__init__` (line 88)

**Pseudocode:**
- Set self.client to client.
- Set self.user_id to user_id.
- Set self._cached_snapshot to None.
- Set self._cached_at to 0.

### `bump` (line 100)

**Pseudocode:**
- If key compared to ...:
-   Raise an error.
- If a boolean condition:
-   Raise an error.
- If self.user_id:
-   Raise an error.
- Set self._cached_snapshot to None.
- Set day to utc_now(...).date(...).isoformat(...).

**Calls →**
1. `features.metrics.ValueError`
2. `features.metrics.isinstance`
3. `features.metrics.ValueError`
4. `features.metrics.ValueError`
5. `shared.infra.utc_now`
6. `features.metrics.SupabaseMetricsStore.client.request`
7. `features.metrics.str`
8. `features.metrics.SupabaseMetricsStore._increment_rows`
9. `shared.infra.debug_event`

### `save_session` (line 151)

**Pseudocode:**
- Call self.client.request(...).

**Calls →**
1. `features.metrics.SupabaseMetricsStore.client.request`
2. `session.get`

### `recent_sessions` (line 166)

**Pseudocode:**
- Set rows to self.client.request(...).
- If a boolean condition:
-   Raise an error.
- Return ListComp.

**Calls →**
1. `features.metrics.SupabaseMetricsStore.client.request`
2. `features.metrics.SupabaseMetricsStore._scope`
3. `features.metrics.str`
4. `features.metrics.isinstance`
5. `features.metrics.any`
6. `features.metrics.isinstance`
7. `row.get`
8. `features.metrics.OSError`

### `snapshot` (line 176)

**Pseudocode:**
- If a boolean condition:
-   Return self._cached_snapshot.
- Set result to self._load_snapshot(...).
- Set self._cached_snapshot to result.
- Set self._cached_at to time.time(...).
- Return result.

**Calls →**
1. `time.time`
2. `features.metrics.SupabaseMetricsStore._load_snapshot`
3. `time.time`

### `get_metrics` (line 238)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC2B1F10>:
-   Call request.report_storage_error(...).

**Calls →**
1. `request.send_json`
2. `request.account.metrics.snapshot`
3. `request.report_storage_error`

### `get_performance` (line 248)

**Pseudocode:**
- Set query to urllib.parse.parse_qs(...).
- Set range_key to a boolean condition[...].
- Set range_key to LEGACY_PERFORMANCE_RANGES.get(...).
- Set dialer to request.account.dialer.
- Set sessions to request.account.metrics.recent_sessions(...).
- With dialer.lock:
-   Set live to IfExp.
- If live:

**Calls →**
1. `urllib.parse.parse.parse_qs`
2. `urllib.parse.parse.urlsplit`
3. `query.get`
4. `LEGACY_PERFORMANCE_RANGES.get`
5. `request.account.metrics.recent_sessions`
6. `features.metrics.dict`
7. `item.get`
8. `live.get`
9. `features.performance.build_performance`
10. `request.account.crm.snapshot`
11. `features.settings.daily_goal`
12. `dialer.read_settings`
13. `query.get`
14. `shared.infra.utc_now`
15. `live.get`
16. `features.metrics.str`
17. `request.send_json`
18. `features.metrics.str`
19. `request.send_json`

### `post_goal` (line 275)

**Pseudocode:**
- Set goal to request.account.dialer.save_goal(...).
- Call request.send_json(...).

**Calls →**
1. `request.account.dialer.save_goal`
2. `request.send_json`

### `post_booking` (line 280)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set lead to dialer.log_booking(...).
- Call request.send_json(...).

**Calls →**
1. `dialer.log_booking`
2. `features.metrics.str`
3. `data.get`
4. `data.get`
5. `request.send_json`
6. `dialer.public_state`
