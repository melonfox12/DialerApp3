# `features/_dialer/calls.py`

**Purpose:** Caller rotation, call create/cancel, and the call dict. Below slots.

## Functions
### `_callback_due` (line 30)

**Pseudocode:**
- Return callback_due(...).

**Calls →**
1. `shared.dial_policy.callback_due`

### `_dialed_recently` (line 34)

**Pseudocode:**
- Return dialed_recently(...).

**Calls →**
1. `shared.dial_policy.dialed_recently`

### `_contact_keys` (line 38)

**Pseudocode:**
- Return contact_keys(...).

**Calls →**
1. `shared.dial_policy.contact_keys`

**Called by ←**
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `_busy_lead_ids` (line 42)
_Leads on a line, ringing, waiting for an outcome, or with an unfinished dial log row._

**Pseudocode:**
- Set leads to state.crm.snapshot(...).
- With state.lock:
-   Set busy to SetComp.
-   If a boolean condition:
-     Call busy.add(...).
-   If state.pending_outcome:
-     Call busy.add(...).
- Update busy with BitOr open_dial_lead_ids(...).

**Calls →**
1. `state.crm.snapshot`
2. `state.in_flight.values`
3. `call.get`
4. `state.active.get`
5. `busy.add`
6. `busy.add`
7. `shared.dial_policy.open_dial_lead_ids`

**Called by ←**
- `fn:features/_dialer/calls.py:_pool_leads`
- `fn:features/_dialer/projection.py:crm_catalog`
- `fn:features/ai_agents.py:agents_public_view`
- `fn:features/ai_agents.py:boot_agent_pool`
- `fn:features/ai_agents.py:dialable_pool_for_agent`
- `fn:features/ai_agents.py:global_pool_snapshot`

### `_pool_leads` (line 55)

**Pseudocode:**
- Set leads to IfExp.
- If a boolean condition:
-   Return ai_agents.dialable_pool_for_agent(...).
- Return pool_leads(...).

**Calls →**
1. `state.crm.snapshot`
2. `features._dialer.calls.getattr`
3. `features._dialer.calls.getattr`
4. `ai_agents.dialable_pool_for_agent`
5. `shared.dial_policy.pool_leads`
6. `shared.dial_policy.resolve_pool_status`
7. `features._dialer.calls.getattr`
8. `features._dialer.calls._busy_lead_ids`
9. `shared.infra.utc_now`
10. `features._dialer.calls.getattr`

**Called by ←**
- `fn:features/_dialer/projection.py:crm_catalog`
- `fn:features/_dialer/queue.py:_current_queue_id`
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/slots.py:_place_prospect_call`
- `fn:features/ai_agents.py:dialable_pool_for_agent`

### `_next_caller` (line 70)

**Pseudocode:**
- With state.lock:
-   If state.callers:
-     Raise an error.
-   Set caller to state.callers[...].
-   Update state.caller_index with Add 1.
-   Return caller.

**Calls →**
1. `features._dialer.twilio.TwilioError`
2. `features._dialer.calls.len`

**Called by ←**
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/calls.py:_launch_call`
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `_launch_call` (line 78)

**Pseudocode:**
- If call.get(...):
-   Set call[...] to _next_caller(...).
- Call threading.Thread(...).start(...).

**Calls →**
1. `call.get`
2. `features._dialer.calls._next_caller`
3. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `_create_call` (line 83)

**Pseudocode:**
- Set caller to a boolean condition.
- Set call[...] to caller.
- Set number to a boolean condition.
- Set data to a dict.
- If call[...] compared to ...:
-   Call data.update(...).
- Set lead_name to display_name(...).
- Call state.record_activity(...).

**Calls →**
1. `call.get`
2. `features._dialer.calls._next_caller`
3. `features._dialer.twilio.normalize_phone`
4. `features._dialer.calls.str`
5. `features._dialer.twilio._url`
6. `features._dialer.twilio._url`
7. `data.update`
8. `features._dialer.twilio._url`
9. `shared.prospect_schema.display_name`
10. `call.get`
11. `state.record_activity`
12. `features._dialer.twilio.twilio_request`
13. `result.get`
14. `features._dialer.twilio.TwilioError`
15. `features._dialer.twilio._hangup_call`
16. `state.record_activity`
17. `threading.Timer`
18. `timer.start`
19. `features._dialer.calls.str`
20. `call.get`
21. `state.in_flight.pop`
22. `features._dialer.rules._bump`
23. `state.in_flight.values`
24. `features._dialer.calls.str`
25. `state.in_flight.pop`
26. `features._dialer.rules._bump`
27. `features._dialer.rules._flush_metrics`
28. `state.record_activity`
29. `state.calls.get`
30. `features._dialer.calls._cancel_call`

### `_expire_silent_call` (line 165)
_Drop a line Twilio stopped reporting, so the queue does not sit on it._

**Pseudocode:**
- With state.lock:
-   Set call to state.calls.get(...).
-   If a boolean condition:
-     Return nothing.
-   Set call_uuid to call.get(...).
- If call_uuid:
-   Call twilio._hangup_call(...).
- Call ended._call_ended(...).

**Calls →**
1. `state.calls.get`
2. `call.get`
3. `call.get`
4. `call.get`
5. `call.get`
6. `call.get`
7. `features._dialer.twilio._hangup_call`
8. `ended._call_ended`

### `_replace_line_after_delay` (line 185)
_Move a failed prospect back and wait before filling that open line._

**Pseudocode:**
- If lead_id:
-   Try:
-     Call state.crm.defer(...).
-   On <ast.Tuple object at 0x00000242BC263950>:
-     No-op.
- Call timing._schedule_advance(...).

**Calls →**
1. `state.crm.defer`
2. `timing._schedule_advance`

**Called by ←**
- `fn:features/_dialer/calls.py:_create_call`

### `_cancel_call` (line 195)

**Pseudocode:**
- With state.lock:
-   If call[...]:
-     Return nothing.
-   Set call[...] to True.
-   Set call[...] to 'cancelled'.
-   Call state.in_flight.pop(...).
-   If state.active compared to ...:
-     Set state.active to None.

**Calls →**
1. `state.in_flight.pop`
2. `call.get`
3. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_drop_line`
- `fn:features/_dialer/calls.py:_create_call`

### `_dial_record` (line 208)
_The one call-log entry for a finished dial. It replaces the entry written at dial time._

**Pseudocode:**
- Set answered to a boolean condition.
- If answered:
-   Set answered to IfExp.
- Return a dict.

**Calls →**
1. `call.get`
2. `call.get`
3. `call.get`
4. `call.get`
5. `call.get`
6. `datetime.datetime.now`
7. `call.get`
8. `features._dialer.calls.len`
9. `call.get`
10. `features._dialer.calls.bool`
11. `call.get`
12. `features._dialer.calls.str`
13. `call.get`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/pickup.py:_drop_line`

### `_new_call` (line 226)

**Pseudocode:**
- Set token to secrets.token_urlsafe(...).
- Set call to a dict.
- Call voice_session.attach_call_voice_defaults(...).
- If slot_index compared to ...:
-   Set call[...] to int(...).
- Set state.calls[...] to call.
- Call _watch_token(...).
- If kind compared to ...:

**Calls →**
1. `secrets.token_urlsafe`
2. `shared.infra.utc_now`
3. `features._dialer.voice_session.attach_call_voice_defaults`
4. `features._dialer.calls.int`
5. `features._dialer.calls._watch_token`
6. `features._dialer.rules._bump`
7. `features._dialer.rules._save_session`
8. `lead.get`
9. `state.crm.append_call_log`

**Called by ←**
- `fn:features/_dialer/queue.py:rejoin_browser_voice`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/slots.py:_place_prospect_call`

### `_watch_token` (line 277)

**Pseudocode:**
- Set index to state.token_index.
- If index compared to ...:
-   Call index.register(...).

**Calls →**
1. `index.register`

**Called by ←**
- `fn:features/_dialer/calls.py:_new_call`

### `_release_tokens` (line 282)

**Pseudocode:**
- Set index to state.token_index.
- If index compared to ...:
-   Return nothing.
- For each token in list(...):
-   Call index.forget(...).

**Calls →**
1. `features._dialer.calls.list`
2. `index.forget`

**Called by ←**
- `fn:features/_dialer/queue.py:start`

### `_dialable_lead` (line 289)

**Pseudocode:**
- Set lead_id to str(...).strip(...).
- If lead_id:
-   Raise an error.
- Set lead to next(...).
- If lead compared to ...:
-   Raise an error.
- If str(...).strip(...):
-   Raise an error.

**Calls →**
1. `features._dialer.calls.str`
2. `features._dialer.calls.ValueError`
3. `features._dialer.calls.next`
4. `state.crm.snapshot`
5. `features._dialer.calls.KeyError`
6. `features._dialer.calls.str`
7. `lead.get`
8. `features._dialer.calls.ValueError`
9. `shared.dial_policy.is_never_dial_status`
10. `lead.get`
11. `features._dialer.calls.ValueError`

**Called by ←**
- `fn:features/_dialer/queue.py:dial_lead`
- `fn:features/_dialer/queue.py:start`

### `_claim_manual_lead` (line 302)
_The pinned prospect, unless they are closed, already on a line, or the same person as someone who is._

**Pseudocode:**
- Set lead_id to state.manual_lead_id.
- If lead_id:
-   Return None.
- Set lead to next(...).
- Set blocked to manual_lead_blocked(...).
- If blocked:
-   Set state.manual_lead_id to None.
-   Return None.

**Calls →**
1. `features._dialer.calls.next`
2. `shared.dial_policy.manual_lead_blocked`

**Called by ←**
- `fn:features/_dialer/slots.py:_place_prospect_call`
