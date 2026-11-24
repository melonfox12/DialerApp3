# `features/_dialer/slots.py`

**Purpose:** Fill the open prospect lines, and the calling-window timer that refills them.

## Functions
### `_prune_finished_lines` (line 11)
_Drop ended lines still listed in in_flight so open slots can refill._

**Pseudocode:**
- With state.lock:
-   Call rules.clear_stale_active(...).
-   For each Tuple in list(...):
-     If a boolean condition:
-       Call state.in_flight.pop(...).
-       If state.active compared to ...:
-         Set state.active to None.
-     Else:

**Calls →**
1. `features._dialer.rules.clear_stale_active`
2. `features._dialer.slots.list`
3. `state.in_flight.items`
4. `call.get`
5. `call.get`
6. `state.in_flight.pop`
7. `call.get`
8. `call.get`
9. `state.in_flight.pop`

**Called by ←**
- `fn:features/_dialer/slots.py:_check_calling_window`
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `fill_slots` (line 26)

**Pseudocode:**
- Try:
-   Call _place_prospect_call(...).
- On <ast.Name object at 0x000001E0F8E57C50>:
-   Call state.record_activity(...).

**Calls →**
1. `features._dialer.slots._place_prospect_call`
2. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/queue.py:_pin_manual_dial`
- `fn:features/_dialer/queue.py:pass_next`
- `fn:features/_dialer/queue.py:pause`
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_dialer/slots.py:_check_calling_window`
- `fn:features/_dialer/timing.py:_advance_queue`
- `fn:features/_dialer/timing.py:advance_now`
- `fn:features/ai_agents.py:try_resume_agent_dial`
- `fn:features/dialer.py:fill_slots`

### `request_top_up` (line 33)
_Fill any open dial slots while other lines may still be ringing._

**Pseudocode:**
- Call threading.Thread(...).start(...).

**Calls →**
1. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_drop_line`

### `_place_prospect_call` (line 38)

**Pseudocode:**
- Call _prune_finished_lines(...).
- Set launches to a list.
- Set none_ready to False.
- With state.lock:
-   Call rules.clear_stale_active(...).
-   If a boolean condition:
-     Return nothing.
-   Set prospect_lines to ListComp.

**Calls →**
1. `features._dialer.slots._prune_finished_lines`
2. `features._dialer.rules.clear_stale_active`
3. `features._dialer.voice_session.slots_may_dial`
4. `state.in_flight.values`
5. `call.get`
6. `features._dialer.slots.max`
7. `features._dialer.slots.len`
8. `features._dialer.slots.len`
9. `state.crm.snapshot`
10. `features._dialer.slots.getattr`
11. `features._dialer.calls._pool_leads`
12. `features._dialer.slots.len`
13. `state.in_flight.values`
14. `call.get`
15. `features._dialer.slots.set`
16. `features._dialer.slots.getattr`
17. `features._dialer.calls._claim_manual_lead`
18. `selected.append`
19. `active_leads.add`
20. `features._dialer.calls._contact_keys`
21. `features._dialer.calls._pool_leads`
22. `features._dialer.calls._contact_keys`
23. `features._dialer.slots.getattr`
24. `features._dialer.slots.min`
25. `features._dialer.slots.len`
26. `features._dialer.slots.int`
27. `item.get`
28. `features._dialer.slots.range`
29. `features._dialer.slots.min`
30. `features._dialer.slots.len`

**Called by ←**
- `fn:features/_dialer/slots.py:fill_slots`

### `_schedule_calling_window_check` (line 112)

**Pseudocode:**
- With state.lock:
-   If state.calling_window_timer:
-     Call state.calling_window_timer.cancel(...).
-     Set state.calling_window_timer to None.
-   If a boolean condition:
-     Return nothing.
-   Set state.calling_window_timer to threading.Timer(...).
-   Set state.calling_window_timer.daemon to True.

**Calls →**
1. `state.calling_window_timer.cancel`
2. `threading.Timer`
3. `state.calling_window_timer.start`

**Called by ←**
- `fn:features/_dialer/queue.py:pause`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/slots.py:_check_calling_window`
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `_check_calling_window` (line 124)

**Pseudocode:**
- Call _prune_finished_lines(...).
- With state.lock:
-   Set state.calling_window_timer to None.
-   Call rules.clear_stale_active(...).
-   Set prospect_lines to ListComp.
-   Set should_fill to a boolean condition.
- If should_fill:
-   Call fill_slots(...).

**Calls →**
1. `features._dialer.slots._prune_finished_lines`
2. `features._dialer.rules.clear_stale_active`
3. `state.in_flight.values`
4. `call.get`
5. `features._dialer.voice_session.slots_may_dial`
6. `features._dialer.slots.len`
7. `features._dialer.slots.len`
8. `features._dialer.slots.fill_slots`
9. `features._dialer.slots._schedule_calling_window_check`
