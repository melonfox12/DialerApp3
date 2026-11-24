# `features/_dialer/outcomes.py`

**Purpose:** Disposition and prospect status changes during a call.

## Functions
### `live_outcome_lead_id` (line 19)
_The lead id (if any) currently eligible for an outcome: either the call_

**Pseudocode:**
- With state.lock:
-   If state.pending_outcome:
-     Return state.pending_outcome.
-   If state.active:
-     Return state.active.get(...).
-   Return None.

**Calls →**
1. `state.active.get`

### `_on_a_call` (line 29)
_True when this prospect is on a line, ringing, or waiting for an outcome after a call._

**Pseudocode:**
- With state.lock:
-   Return a boolean condition.

**Calls →**
1. `features._dialer.outcomes.bool`
2. `state.active.get`
3. `features._dialer.outcomes.any`
4. `call.get`
5. `call.get`
6. `state.in_flight.values`

**Called by ←**
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/outcomes.py:update_status`

### `end_call_with_status` (line 39)
_A status button: set the prospect's status, tag the call with it, and hang up._

**Pseudocode:**
- Set status to parse_prospect_status(...).
- If status compared to ...:
-   Raise an error.
- Set lead_id to str(...).strip(...).
- Set previous to next(...).
- If previous compared to ...:
-   Raise an error.
- Set on_call to _on_a_call(...).

**Calls →**
1. `shared.vocabulary.parse_prospect_status`
2. `features._dialer.outcomes.ValueError`
3. `features._dialer.outcomes.str`
4. `features._dialer.outcomes.next`
5. `state.crm.snapshot`
6. `features._dialer.outcomes.KeyError`
7. `features._dialer.outcomes._on_a_call`
8. `features._dialer.outcomes._set_booked`
9. `features._dialer.queue.schedule_callback`
10. `state.crm.set_status`
11. `features._dialer.outcomes._tag_recent_call`
12. `previous.get`
13. `features._dialer.rules._bump`
14. `shared.vocabulary.OUTCOME_METRIC.get`
15. `features._dialer.rules._flush_metrics`
16. `features._dialer.queue.drop_prospect_call`
17. `shared.prospect_schema.display_name`
18. `state.record_activity`
19. `features._dialer.slots.fill_slots`
20. `features._dialer.timing._schedule_advance`

**Called by ←**
- `fn:features/_dialer/outcomes.py:update_status`

### `_set_booked` (line 78)
_Mark a prospect booked from the CRM and count the meeting once._

**Pseudocode:**
- Set previous to next(...).
- Set lead to state.crm.set_status(...).
- Call _tag_recent_call(...).
- If a boolean condition:
-   Return lead.
- Call rules._bump(...).
- With state.lock:
-   If state.session:

**Calls →**
1. `features._dialer.outcomes.next`
2. `state.crm.snapshot`
3. `state.crm.set_status`
4. `features._dialer.outcomes._tag_recent_call`
5. `previous.get`
6. `features._dialer.rules._bump`
7. `features._dialer.rules.record_disposition`
8. `features._dialer.rules._save_session`
9. `features._dialer.rules._flush_metrics`

**Called by ←**
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/outcomes.py:log_booking`
- `fn:features/_dialer/outcomes.py:tag_call`
- `fn:features/_dialer/outcomes.py:update_status`

### `_tag_recent_call` (line 97)
_Put the tag on the most recent connected call when it was with this prospect._

**Pseudocode:**
- With state.lock:
-   Set call to state.taggable_call.
-   If a boolean condition:
-     Return False.
-   Set call[...] to outcome.
-   Set call_ids to Tuple.
- Try:
-   Call state.crm.set_call_outcome(...).

**Calls →**
1. `call.get`
2. `call.get`
3. `state.crm.set_call_outcome`
4. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/outcomes.py:_set_booked`
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/outcomes.py:tag_call`

### `tag_call` (line 111)
_Tag the last connected call. Booked also marks the prospect booked and counts the meeting once._

**Pseudocode:**
- If outcome compared to ...:
-   Raise an error.
- With state.lock:
-   Set call to state.taggable_call.
-   If a boolean condition:
-     Raise an error.
-   If a boolean condition:
-     Raise an error.

**Calls →**
1. `features._dialer.outcomes.ValueError`
2. `call.get`
3. `features._dialer.outcomes.ValueError`
4. `call.get`
5. `features._dialer.outcomes.ValueError`
6. `features._dialer.outcomes._set_booked`
7. `features._dialer.outcomes._tag_recent_call`
8. `features._dialer.outcomes.next`
9. `state.crm.snapshot`

**Called by ←**
- `fn:features/dialer.py:tag_call`

### `log_booking` (line 127)
_Count a meeting booked outside a live call, dated by the caller (ISO datetime with timezone)._

**Pseudocode:**
- Try:
-   Set when to datetime.fromisoformat(...).
- On <ast.Name object at 0x00000242BC1A9C90>:
-   Raise an error.
- If when.tzinfo compared to ...:
-   Raise an error.
- If when compared to ...:
-   Raise an error.

**Calls →**
1. `datetime.datetime.fromisoformat`
2. `features._dialer.outcomes.str`
3. `features._dialer.outcomes.ValueError`
4. `features._dialer.outcomes.ValueError`
5. `datetime.datetime.now`
6. `features._dialer.outcomes.ValueError`
7. `when.astimezone`
8. `features._dialer.outcomes.next`
9. `state.crm.snapshot`
10. `features._dialer.outcomes.KeyError`
11. `previous.get`
12. `features._dialer.outcomes.ValueError`
13. `previous.get`
14. `features._dialer.outcomes.ValueError`
15. `previous.get`
16. `state.crm.set_booked_at`
17. `features._dialer.outcomes._set_booked`
18. `state.crm.set_booked_at`
19. `state.record_activity`
20. `shared.prospect_schema.display_name`

**Called by ←**
- `fn:features/dialer.py:log_booking`

### `update_status` (line 156)

**Pseudocode:**
- Call ai_agents.assert_lead_mutable_by_user(...).
- If a boolean condition:
-   Set status to status_for_disposition(...).
- Set raw to status.
- Set status to parse_prospect_status(...).
- If status compared to ...:
-   If a boolean condition:
-     Set previous to next(...).

**Calls →**
1. `ai_agents.assert_lead_mutable_by_user`
2. `features._dialer.rules.status_for_disposition`
3. `shared.vocabulary.parse_prospect_status`
4. `features._dialer.outcomes.str`
5. `features._dialer.outcomes.next`
6. `state.crm.snapshot`
7. `features._dialer.outcomes.KeyError`
8. `features._dialer.outcomes.ValueError`
9. `features._dialer.outcomes._on_a_call`
10. `features._dialer.outcomes.end_call_with_status`
11. `features._dialer.outcomes._set_booked`
12. `state.crm.set_status`
13. `shared.prospect_schema.display_name`
14. `state.record_activity`

**Called by ←**
- `fn:features/dialer.py:update_status`
