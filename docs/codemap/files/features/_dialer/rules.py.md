# `features/_dialer/rules.py`

**Purpose:** Stage, session accounting, local time, and metric bumps.

## Functions
### `stale_active_call` (line 10)
_True when a finished line still referenced by state.active must not block the next connect._

**Pseudocode:**
- If isinstance(...):
-   Return True.
- If call.get(...):
-   Return True.
- If call.get(...) compared to ...:
-   Return True.
- If a boolean condition:
-   Return True.

**Calls →**
1. `features._dialer.rules.isinstance`
2. `call.get`
3. `call.get`
4. `call.get`
5. `call.get`
6. `call.get`

**Called by ←**
- `fn:features/_dialer/rules.py:clear_stale_active`
- `fn:features/_dialer/rules.py:dialer_stage`

### `clear_stale_active` (line 25)
_Clear state.active when it still points at a finished call. Caller must hold state.lock._

**Pseudocode:**
- Set active to state.active.
- If a boolean condition:
-   Set state.active to None.
-   Return None.
- Return active.

**Calls →**
1. `features._dialer.rules.stale_active_call`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_pickup`
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/_dialer/queue.py:drop_prospect_call`
- `fn:features/_dialer/slots.py:_check_calling_window`
- `fn:features/_dialer/slots.py:_place_prospect_call`
- `fn:features/_dialer/slots.py:_prune_finished_lines`
- `fn:features/_dialer/timing.py:_advance_queue`
- `fn:features/_dialer/timing.py:_schedule_advance`

### `dialer_stage` (line 34)

**Pseudocode:**
- If running:
-   Return 'idle'.
- If paused:
-   Return 'paused'.
- If a boolean condition:
-   Set active to None.
- Set wrapping to a boolean condition.
- If a boolean condition:

**Calls →**
1. `features._dialer.rules.isinstance`
2. `features._dialer.rules.stale_active_call`
3. `features._dialer.rules.isinstance`
4. `active.get`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`

### `status_for_disposition` (line 51)

**Pseudocode:**
- Try:
-   Return DISPOSITION_TO_STATUS[...].
- On <ast.Name object at 0x00000242BC260050>:
-   Raise an error.

**Calls →**
1. `features._dialer.rules.ValueError`

**Called by ←**
- `fn:features/_dialer/outcomes.py:update_status`

### `new_session` (line 58)

**Pseudocode:**
- Set started to a boolean condition.
- Return a dict.

**Calls →**
1. `datetime.datetime.now`
2. `features._dialer.rules.int`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/_dialer/queue.py:start`

### `add_connect` (line 76)

**Pseudocode:**
- Set now to a boolean condition.
- If isinstance(...):
-   Set now to datetime.fromisoformat(...).
- Set times to ListComp.
- If a boolean condition:
-   Set session[...] to session.get(...) op 1.
- Else:
-   Set session[...] to 1.

**Calls →**
1. `datetime.datetime.now`
2. `features._dialer.rules.isinstance`
3. `datetime.datetime.fromisoformat`
4. `datetime.datetime.fromisoformat`
5. `session.get`
6. `datetime.timedelta`
7. `session.get`
8. `features._dialer.rules.max`
9. `session.get`
10. `times.append`
11. `datetime.timedelta`
12. `value.isoformat`
13. `session.get`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_pickup`

### `record_conversation` (line 92)

**Pseudocode:**
- Set session[...] to session.get(...) op 1.
- If a boolean condition:
-   Set session[...] to datetime.now(...).isoformat(...).
- Return True.

**Calls →**
1. `session.get`
2. `session.get`
3. `session.get`
4. `datetime.datetime.now`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`

### `record_disposition` (line 102)

**Pseudocode:**
- If status compared to ...:
-   Set session[...] to session.get(...) op 1.

**Calls →**
1. `session.get`

**Called by ←**
- `fn:features/_dialer/outcomes.py:_set_booked`

### `recent_streak` (line 107)

**Pseudocode:**
- Set instant to a boolean condition.
- If isinstance(...):
-   Set instant to datetime.fromisoformat(...).
- Set cutoff to instant op timedelta(...).
- Set times to ListComp.
- Return sum(...).

**Calls →**
1. `datetime.datetime.now`
2. `features._dialer.rules.isinstance`
3. `datetime.datetime.fromisoformat`
4. `datetime.timedelta`
5. `datetime.datetime.fromisoformat`
6. `session.get`
7. `features._dialer.rules.sum`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`

### `local_time` (line 116)

**Pseudocode:**
- Set zone_name to TIMEZONE_NAMES.get(...).
- If a boolean condition:
-   Return None.
- Try:
-   Set zone to ZoneInfo(...).
- On <ast.Tuple object at 0x00000242BC269910>:
-   Return None.
- Set instant to a boolean condition.

**Calls →**
1. `shared.vocabulary.TIMEZONE_NAMES.get`
2. `features._dialer.rules.str`
3. `zoneinfo.ZoneInfo`
4. `datetime.datetime.now`
5. `instant.replace`
6. `instant.astimezone`

**Called by ←**
- `fn:features/_dialer/rules.py:within_calling_window`

### `within_calling_window` (line 130)

**Pseudocode:**
- Set local to local_time(...).
- If local compared to ...:
-   Return False.
- If a boolean condition:
-   Raise an error.
- Set local_minutes to local.hour op 60 op local.minute.
- Return start_hour op 60 compared to ....

**Calls →**
1. `features._dialer.rules.local_time`
2. `features._dialer.rules.ValueError`

### `session_summary` (line 140)

**Pseudocode:**
- Set ended to a boolean condition.
- Set start to datetime.fromisoformat(...).
- Set finish to datetime.fromisoformat(...).
- Set result to dict(...).
- Set result[...] to ended.
- Set result[...] to max(...).
- Set result[...] to result.get(...).
- Call result.pop(...).

**Calls →**
1. `datetime.datetime.now`
2. `datetime.datetime.fromisoformat`
3. `datetime.datetime.fromisoformat`
4. `features._dialer.rules.dict`
5. `features._dialer.rules.max`
6. `features._dialer.rules.int`
7. `result.get`
8. `result.pop`
9. `result.pop`

**Called by ←**
- `fn:features/_dialer/queue.py:stop`

### `_save_session` (line 152)
_Record a session save. _flush_metrics performs it once state.lock is released._

**Pseudocode:**
- If a boolean condition:
-   Set state.session_save_pending to True.

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_pickup`
- `fn:features/_dialer/calls.py:_new_call`
- `fn:features/_dialer/outcomes.py:_set_booked`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/queue.py:stop`

### `_bump` (line 157)
_Record a metric bump. _flush_metrics performs it once state.lock is released._

**Pseudocode:**
- If state.metrics:
-   Call state.pending_bumps.append(...).

**Calls →**
1. `state.pending_bumps.append`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/call_events.py:skip_active`
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/calls.py:_new_call`
- `fn:features/_dialer/outcomes.py:_set_booked`
- `fn:features/_dialer/outcomes.py:end_call_with_status`

### `_flush_metrics` (line 162)
_Run recorded bumps and session saves. Never call while holding state.lock._

**Pseudocode:**
- With state.lock:
-   Set Tuple to Tuple.
-   Set session to None.
-   If a boolean condition:
-     Update state.session_version with Add 1.
-     Set session to Tuple.
-   Set state.session_save_pending to False.
- If a boolean condition:

**Calls →**
1. `copy.deepcopy`
2. `state.metrics.bump`
3. `state.record_activity`
4. `state.metrics.save_session`
5. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/_call_events/pickup.py:_pickup`
- `fn:features/_dialer/call_events.py:skip_active`
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/outcomes.py:_set_booked`
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/queue.py:ensure_nov5_static_callback_migration`
- `fn:features/_dialer/queue.py:rejoin_browser_voice`
- `fn:features/_dialer/queue.py:repair_total_dials_callbacks`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/queue.py:stop`
- `fn:features/_dialer/slots.py:_place_prospect_call`
