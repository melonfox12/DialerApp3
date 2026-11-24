# `features/_dialer/queue.py`

**Purpose:** Session start, pause, stop, and manual dial. Imports calls, then slots, then timing.

## Functions
### `repair_total_dials_callbacks` (line 29)
_Backfill Callback (2h) on prospects that have dial-log rows but are still New._

**Pseudocode:**
- Set updated to state.crm.repair_total_dials_callbacks(...).
- If updated:
-   Call rules._flush_metrics(...).
- Return updated.

**Calls →**
1. `state.crm.repair_total_dials_callbacks`
2. `features._dialer.rules._flush_metrics`

**Called by ←**
- `fn:features/_dialer/queue.py:maintain_crm`
- `fn:features/_dialer/queue.py:scan_crm`
- `fn:features/_dialer/queue.py:start`
- `fn:features/dialer.py:backfill_new_dial_callbacks`

### `_nov5_static_callback_migration_done` (line 37)

**Pseudocode:**
- If str(...).lower(...) compared to ...:
-   Return True.
- Set path to getattr(...).
- If path compared to ...:
-   Return migration_done(...).
- Return False.

**Calls →**
1. `features._dialer.queue.str`
2. `features._dialer.queue.getattr`
3. `features._dialer.queue.getattr`
4. `features._prospects.migration_flags.migration_done`
5. `features._dialer.queue.str`

**Called by ←**
- `fn:features/_dialer/queue.py:ensure_nov5_static_callback_migration`

### `_mark_nov5_static_callback_migration_done` (line 46)

**Pseudocode:**
- Set state.account_values[...] to 'true'.
- Set saver to getattr(...).
- If a boolean condition:
-   Try:
-     Call saver(...).
-   On <ast.Name object at 0x000001E0F8F10F50>:
-     No-op.
- Set path to getattr(...).

**Calls →**
1. `features._dialer.queue.getattr`
2. `features._dialer.queue.getattr`
3. `features._dialer.queue.saver`
4. `features._dialer.queue.getattr`
5. `features._prospects.migration_flags.mark_migration_done`
6. `features._dialer.queue.str`

**Called by ←**
- `fn:features/_dialer/queue.py:ensure_nov5_static_callback_migration`

### `ensure_nov5_static_callback_migration` (line 59)
_One-time backfill for Nov 5, 2026 dialed prospects still marked New._

**Pseudocode:**
- If a boolean condition:
-   Return 0.
- Set archived to a list.
- If dial_archive compared to ...:
-   Try:
-     Set archived to dial_archive.snapshot(...).
-   On <ast.Name object at 0x000001E0F8E85490>:
-     Set archived to a list.

**Calls →**
1. `features._dialer.queue._nov5_static_callback_migration_done`
2. `dial_archive.snapshot`
3. `state.crm.migrate_nov5_2026_static_callbacks`
4. `features._dialer.queue._mark_nov5_static_callback_migration_done`
5. `features._dialer.rules._flush_metrics`
6. `state.record_activity`
7. `state.record_activity`

**Called by ←**
- `fn:features/dialer.py:_maybe_run_nov5_static_callback_migration`
- `fn:features/dialer.py:post_backfill_nov5_static_callbacks`

### `maintain_crm` (line 84)
_CRM backfill and callback dial-list repair. Never call from GET /api/state or /api/live._

**Pseudocode:**
- Set shifted to state.crm.migrate_callback_timers_to_two_hours(...).
- If shifted:
-   Set noun to IfExp.
-   Call state.record_activity(...).
- Call remember_open_skips(...).
- Call repair_total_dials_callbacks(...).
- Call maybe_enforce_dial_caps(...).

**Calls →**
1. `state.crm.migrate_callback_timers_to_two_hours`
2. `state.record_activity`
3. `features._dialer.queue.remember_open_skips`
4. `features._dialer.queue.repair_total_dials_callbacks`
5. `features._dialer.queue.maybe_enforce_dial_caps`

**Called by ←**
- `fn:features/dialer.py:maintain_crm`

### `scan_crm` (line 95)
_Copy an open callback onto new prospects with the same name and location._

**Pseudocode:**
- Set plan to calls.callback_sync_plan(...).
- Set synced to 0.
- For each item in plan:
-   Try:
-     Call state.crm.set_status(...).
-   On <ast.Name object at 0x000001E0F8EA6890>:
-   Update synced with Add 1.
- Set dial_caps to state.crm.enforce_dial_caps(...).

**Calls →**
1. `features._dialer.calls.callback_sync_plan`
2. `state.crm.snapshot`
3. `shared.infra.utc_now`
4. `state.crm.set_status`
5. `state.crm.enforce_dial_caps`
6. `state.record_activity`
7. `dial_caps.get`
8. `state.record_activity`
9. `dial_caps.get`
10. `state.record_activity`
11. `features._dialer.queue.remember_open_skips`
12. `features._dialer.queue.repair_total_dials_callbacks`
13. `state.record_activity`
14. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:scan_crm`

### `maybe_enforce_dial_caps` (line 131)
_Backfill dial-cap disqualifications at most once a minute while the app is open._

**Pseudocode:**
- Set now to time.time(...).
- With state.lock:
-   If now op state.dial_cap_enforced_at compared to ...:
-     Return 0.
-   Set state.dial_cap_enforced_at to now.
- Set dial_caps to state.crm.enforce_dial_caps(...).
- Set capped to dial_caps.get(...).
- If capped:

**Calls →**
1. `time.time`
2. `state.crm.enforce_dial_caps`
3. `dial_caps.get`
4. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_drop_line`
- `fn:features/_dialer/queue.py:maintain_crm`

### `_prospect_lines_busy` (line 146)

**Pseudocode:**
- With state.lock:
-   If state.pending_outcome:
-     Return True.
-   Set active to state.active.
-   If a boolean condition:
-     Return True.
-   Return any(...).

**Calls →**
1. `active.get`
2. `features._dialer.queue.any`
3. `call.get`
4. `state.in_flight.values`

**Called by ←**
- `fn:features/_dialer/queue.py:set_caller_id_group`

### `set_caller_id_group` (line 156)

**Pseudocode:**
- Set parsed to str(...).strip(...).lower(...).
- If parsed compared to ...:
-   Raise an error.
- Set callers to caller_ids_for_group(...).
- With state.lock:
-   Set current_key to resolve_caller_id_group(...).
-   If a boolean condition:
-     Set state.caller_id_group to parsed.

**Calls →**
1. `features._dialer.queue.str`
2. `features._dialer.queue.ValueError`
3. `shared.vocabulary.caller_ids_for_group`
4. `shared.vocabulary.resolve_caller_id_group`
5. `features._dialer.queue.getattr`
6. `features._dialer.queue.list`
7. `features._dialer.projection.public_state`
8. `features._dialer.queue._prospect_lines_busy`
9. `features._dialer.queue.ValueError`
10. `state.record_activity`
11. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:set_caller_id_group`

### `set_pool_filters` (line 178)

**Pseudocode:**
- Set leads to state.crm.snapshot(...).
- With state.lock:
-   If timezone compared to ...:
-     Set state.selected_timezone to a boolean condition.
-   If pool_status compared to ...:
-     Set parsed to canonical_status(...).
-     If parsed compared to ...:
-       Raise an error.

**Calls →**
1. `state.crm.snapshot`
2. `features._dialer.queue.str`
3. `shared.vocabulary.canonical_status`
4. `features._dialer.queue.ValueError`
5. `shared.vocabulary.resolve_dial_business_type`
6. `features._dialer.queue.len`
7. `features._dialer.calls._pool_leads`
8. `shared.vocabulary.DIAL_POOL_STATUS_LABELS.get`
9. `shared.vocabulary.dial_business_type_label`
10. `parts.append`
11. `parts.append`
12. `parts.append`
13. `features._dialer.voice_session.slots_may_dial`
14. `features._dialer.slots.fill_slots`
15. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/_dialer/queue.py:set_timezone_filter`
- `fn:features/dialer.py:set_pool_filters`

### `set_timezone_filter` (line 212)

**Pseudocode:**
- Return set_pool_filters(...).

**Calls →**
1. `features._dialer.queue.set_pool_filters`

**Called by ←**
- `fn:features/dialer.py:set_timezone_filter`

### `start` (line 215)

**Pseudocode:**
- Set priority to IfExp.
- With state.lock:
-   If state.running:
-     Return projection.public_state(...).
-   Call state.activity_log.clear(...).
-   Set state.activity_sequence to 0.
- Call state.record_activity(...).
- Set raw to state.read_values(...).

**Calls →**
1. `features._dialer.calls._dialable_lead`
2. `features._dialer.projection.public_state`
3. `state.activity_log.clear`
4. `state.record_activity`
5. `state.read_values`
6. `raw.get`
7. `features._dialer.queue.ValueError`
8. `urllib.parse.parse.urlsplit`
9. `features._dialer.queue.ValueError`
10. `state.read_settings`
11. `shared.vocabulary.caller_ids_for_group`
12. `state.record_activity`
13. `features._dialer.queue.len`
14. `features._dialer.twilio.prepare_browser_voice`
15. `features._dialer.calls._pool_leads`
16. `features._dialer.queue.getattr`
17. `features._dialer.queue.getattr`
18. `ai_voice_runtime.voice_configured`
19. `features._dialer.queue.ValueError`
20. `features._dialer.queue.ValueError`
21. `shared.vocabulary.DIAL_POOL_STATUS_LABELS.get`
22. `shared.vocabulary.dial_business_type_label`
23. `features._dialer.queue.ValueError`
24. `state.in_flight.clear`
25. `features._dialer.calls._release_tokens`
26. `state.calls.clear`
27. `secrets.token_hex`
28. `features._dialer.rules.new_session`
29. `features._dialer.queue.int`
30. `features._dialer.queue.all`

**Called by ←**
- `fn:features/_dialer/queue.py:dial_lead`
- `fn:features/ai_agents.py:start_agent`
- `fn:features/dialer.py:start`

### `rejoin_browser_voice` (line 311)
_Issue a desk token so the browser can re-enter the conference mid-session._

**Pseudocode:**
- If voice_session.uses_browser_agent_leg(...):
-   Raise an error.
- With state.lock:
-   If state.running:
-     Raise an error.
-   Set call to IfExp.
-   If a boolean condition:
-     Set call to calls._new_call(...).

**Calls →**
1. `features._dialer.voice_session.uses_browser_agent_leg`
2. `features._dialer.queue.ValueError`
3. `features._dialer.queue.ValueError`
4. `state.calls.get`
5. `call.get`
6. `features._dialer.calls._new_call`
7. `state.record_activity`
8. `features._dialer.rules._flush_metrics`
9. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:rejoin_browser_voice`

### `_current_queue_id` (line 334)

**Pseudocode:**
- With state.lock:
-   Set active to state.active.
-   If a boolean condition:
-     Return active[...].
-   If state.pending_outcome:
-     Return state.pending_outcome.
-   For each call in state.in_flight.values(...):
-     If a boolean condition:

**Calls →**
1. `active.get`
2. `active.get`
3. `state.in_flight.values`
4. `call.get`
5. `call.get`
6. `features._dialer.calls._pool_leads`

**Called by ←**
- `fn:features/_dialer/queue.py:pass_next`

### `drop_prospect_call` (line 350)
_Hang up every line to this prospect._

**Pseudocode:**
- Set hung to a list.
- Set talked to False.
- With state.lock:
-   For each Tuple in list(...):
-     If a boolean condition:
-     Set call[...] to True.
-     Set call[...] to True.
-     If call.get(...):

**Calls →**
1. `features._dialer.queue.list`
2. `state.in_flight.items`
3. `call.get`
4. `call.get`
5. `call.get`
6. `state.in_flight.pop`
7. `call.get`
8. `hung.append`
9. `active.get`
10. `active.get`
11. `active.get`
12. `active.get`
13. `hung.append`
14. `state.calls.values`
15. `call.get`
16. `call.get`
17. `features._dialer.rules.clear_stale_active`
18. `features._dialer.voice_session.slots_may_dial`
19. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/queue.py:pass_next`

### `remember_skip` (line 408)

**Pseudocode:**
- Set moment to when.replace(...).isoformat(...).
- Try:
-   Call state.crm.append_call_log(...).
- On <ast.Name object at 0x000001E0F8F02D90>:
-   Call state.record_activity(...).

**Calls →**
1. `when.replace`
2. `state.crm.append_call_log`
3. `secrets.token_urlsafe`
4. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/queue.py:pass_next`
- `fn:features/_dialer/queue.py:remember_open_skips`
- `fn:features/_dialer/queue.py:schedule_callback`

### `_has_dial_record` (line 420)
_True when the dial list already shows what started this callback: a skip, or a dial made around then._

**Pseudocode:**
- Set floor to due op calls.CALLBACK_HOLD op timedelta(...).
- For each item in log:
-   If item.get(...) compared to ...:
-     Return True.
-   Try:
-     Set started to datetime.fromisoformat(...).
-   On <ast.Name object at 0x000001E0F8F15150>:
-   If started.tzinfo compared to ...:

**Calls →**
1. `datetime.timedelta`
2. `item.get`
3. `datetime.datetime.fromisoformat`
4. `features._dialer.queue.str`
5. `item.get`
6. `started.replace`

**Called by ←**
- `fn:features/_dialer/queue.py:remember_open_skips`

### `remember_open_skips` (line 436)
_Keep an open callback that has no matching dial record in the dial list._

**Pseudocode:**
- Set now to utc_now(...).
- For each lead in state.crm.snapshot(...):
-   If a boolean condition:
-   Try:
-     Set due to datetime.fromisoformat(...).
-   On <ast.Name object at 0x000001E0F8F17CD0>:
-   If due.tzinfo compared to ...:
-   Set remaining to due op now.

**Calls →**
1. `shared.infra.utc_now`
2. `state.crm.snapshot`
3. `lead.get`
4. `lead.get`
5. `datetime.datetime.fromisoformat`
6. `features._dialer.queue.str`
7. `datetime.timedelta`
8. `features._dialer.queue._has_dial_record`
9. `lead.get`
10. `features._dialer.queue.remember_skip`

**Called by ←**
- `fn:features/_dialer/queue.py:maintain_crm`
- `fn:features/_dialer/queue.py:scan_crm`

### `schedule_callback` (line 455)
_Set a manual callback (2 hours by default). log_skip adds the dial-list entry for it._

**Pseudocode:**
- Set now to utc_now(...).replace(...).
- Set due to a boolean condition.
- Set lead to state.crm.set_status(...).
- If log_skip:
-   Call remember_skip(...).
- Return lead.

**Calls →**
1. `shared.infra.utc_now`
2. `state.crm.set_status`
3. `features._dialer.queue.remember_skip`

**Called by ←**
- `fn:features/_dialer/call_events.py:skip_active`
- `fn:features/_dialer/outcomes.py:end_call_with_status`

### `pass_next` (line 464)

**Pseudocode:**
- Set lead_id to a boolean condition.
- If lead_id:
-   Raise an error.
- Set leads to state.crm.snapshot(...).
- Set lead to next(...).
- If lead compared to ...:
-   Raise an error.
- Call remember_skip(...).

**Calls →**
1. `features._dialer.queue.str`
2. `features._dialer.queue._current_queue_id`
3. `state.crm.snapshot`
4. `features._dialer.queue.ValueError`
5. `state.crm.snapshot`
6. `features._dialer.queue.next`
7. `features._dialer.queue.KeyError`
8. `features._dialer.queue.remember_skip`
9. `shared.infra.utc_now`
10. `features._dialer.queue.next`
11. `state.crm.snapshot`
12. `features._dialer.queue.drop_prospect_call`
13. `shared.prospect_schema.display_name`
14. `state.record_activity`
15. `features._dialer.slots.fill_slots`
16. `features._dialer.timing._schedule_advance`
17. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/_dialer/call_events.py:skip_active`
- `fn:features/dialer.py:pass_next`

### `dial_lead` (line 486)

**Pseudocode:**
- Set lead to calls._dialable_lead(...).
- Set name to display_name(...).
- With state.lock:
-   Set running to state.running.
- If running:
-   Set view to start(...).
-   If view.get(...):
-     Set view[...] to 'started'.

**Calls →**
1. `features._dialer.calls._dialable_lead`
2. `shared.prospect_schema.display_name`
3. `features._dialer.queue.start`
4. `view.get`
5. `state.record_activity`
6. `features._dialer.queue._pin_manual_dial`

**Called by ←**
- `fn:features/dialer.py:dial_lead`

### `_pin_manual_dial` (line 499)

**Pseudocode:**
- With state.lock:
-   Set on_line to a boolean condition.
-   If on_line:
-     Set status to 'already'.
-   Else:
-     Set state.manual_lead_id to lead[...].
-     If state.advance_timer:
-       Call state.advance_timer.cancel(...).

**Calls →**
1. `state.active.get`
2. `features._dialer.queue.any`
3. `call.get`
4. `state.in_flight.values`
5. `state.advance_timer.cancel`
6. `features._dialer.voice_session.slots_may_dial`
7. `features._dialer.slots.fill_slots`
8. `features._dialer.projection.public_state`
9. `state.record_activity`
10. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/queue.py:dial_lead`

### `pause` (line 531)

**Pseudocode:**
- With state.lock:
-   If state.running:
-     Return projection.public_state(...).
-   Set state.paused to state.paused.
-   Set state.last_event to IfExp.
-   Set should_fill to a boolean condition.
-   If a boolean condition:
-     Set state.advance_remaining to IfExp.

**Calls →**
1. `features._dialer.projection.public_state`
2. `features._dialer.voice_session.slots_may_dial`
3. `features._dialer.queue.max`
4. `time.time`
5. `state.advance_timer.cancel`
6. `state.calling_window_timer.cancel`
7. `features._dialer.slots.fill_slots`
8. `features._dialer.timing._schedule_advance`
9. `features._dialer.slots._schedule_calling_window_check`
10. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:pause`

### `stop` (line 558)

**Pseudocode:**
- With state.lock:
-   Set calls to list(...).
-   For each call in calls:
-     Set call[...] to True.
-   Set state.running to False.
-   Set state.paused to False.
-   Set state.agent_ready to False.
- Call rules._flush_metrics(...).

**Calls →**
1. `features._dialer.queue.list`
2. `state.calls.values`
3. `features._dialer.voice_session.reset_voice_session`
4. `ai_voice_runtime.purge_sessions`
5. `state.in_flight.clear`
6. `state.advance_timer.cancel`
7. `state.calling_window_timer.cancel`
8. `features._dialer.rules.session_summary`
9. `state.session.update`
10. `features._dialer.rules._save_session`
11. `features._dialer.rules._flush_metrics`
12. `state.record_activity`
13. `call.get`
14. `threading.Thread`
15. `features._dialer.projection.public_state`
16. `features._dialer.queue.next`
17. `state.metrics.recent_sessions`
18. `item.get`

**Called by ←**
- `fn:features/ai_agents.py:stop_agent`
- `fn:features/dialer.py:stop`
