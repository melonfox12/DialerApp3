# `features/_dialer/_call_events/pickup.py`

**Purpose:** Pickup and answer detection.

## Functions
### `_name` (line 15)

**Pseudocode:**
- Set lead to a boolean condition.
- Return IfExp.

**Calls →**
1. `call.get`
2. `shared.prospect_schema.display_name`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_drop_line`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/_call_events/pickup.py:_pickup`

### `_drop_line` (line 19)
_Hang up a line that will not reach the agent and log it once._

**Pseudocode:**
- With state.lock:
-   If a boolean condition:
-     Return False.
-   Set call[...] to True.
- Call calls._cancel_call(...).
- Set lead_id to call.get(...).
- If lead_id:
-   Try:

**Calls →**
1. `call.get`
2. `call.get`
3. `features._dialer.calls._cancel_call`
4. `call.get`
5. `state.crm.append_call_log`
6. `features._dialer.calls._dial_record`
7. `features._dialer.queue.maybe_enforce_dial_caps`
8. `state.record_activity`
9. `features._dialer._call_events.pickup._name`
10. `answered_by.replace`
11. `state.record_activity`
12. `features._dialer._call_events.pickup._name`
13. `features._dialer.slots.request_top_up`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/_call_events/pickup.py:_pickup`

### `_pickup` (line 41)
_Connect the first answer into the conference and drop the other lines._

**Pseudocode:**
- With state.lock:
-   If a boolean condition:
-     Return False.
-   Call rules.clear_stale_active(...).
-   If call.get(...):
-     Return state.active compared to ....
-   If a boolean condition:
-     Set lost to True.

**Calls →**
1. `features._dialer.rules.clear_stale_active`
2. `call.get`
3. `datetime.datetime.now`
4. `call.get`
5. `features._dialer.rules.add_connect`
6. `features._dialer.rules._save_session`
7. `features._dialer._call_events.pickup._name`
8. `call.get`
9. `state.in_flight.values`
10. `features._dialer._call_events.pickup._drop_line`
11. `features._dialer.rules._flush_metrics`
12. `features._dialer._call_events.pickup._drop_line`
13. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`

### `_amd_should_connect` (line 76)
_Bridge the agent only when Twilio says human or could not decide (often a live hello)._

**Pseudocode:**
- Return a boolean condition.lower(...) compared to ....

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_amd_is_voicemail`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`

### `_amd_is_voicemail` (line 80)
_Hang up on machine signals; do not connect machine_start or finished voicemail beeps._

**Pseudocode:**
- If _amd_should_connect(...):
-   Return False.
- Set answered_by to a boolean condition.lower(...).
- If answered_by.startswith(...):
-   Return True.
- Set blob to a boolean condition.lower(...).
- Return any(...).

**Calls →**
1. `features._dialer._call_events.pickup._amd_should_connect`
2. `answered_by.startswith`
3. `features._dialer._call_events.pickup.any`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`

### `_connect_prospect` (line 90)

**Pseudocode:**
- If a boolean condition:
-   If voice_session.is_ai_voice(...):
-     Call ai_voice_runtime.start_call_session(...).
-     If ai_voice_runtime.voice_configured(...):
-       Call transcript.schedule_live_transcription(...).
-   Call twilio._redirect_call(...).
- Set kept to a boolean condition.
- Return IfExp.

**Calls →**
1. `call.get`
2. `features._dialer._call_events.pickup._pickup`
3. `features._dialer.voice_session.is_ai_voice`
4. `features.ai_voice_runtime.start_call_session`
5. `features.ai_voice_runtime.voice_configured`
6. `state.read_settings`
7. `features._dialer._call_events.transcript.schedule_live_transcription`
8. `features._dialer.twilio._redirect_call`
9. `call.get`
10. `features._dialer.twilio._url`
11. `call.get`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`

### `_machine_result` (line 100)

**Pseudocode:**
- Set answered_by to str(...).lower(...).
- Call state.record_activity(...).
- Set result to ' '.join(...).lower(...).
- Set connect to _amd_should_connect(...).
- Set voicemail to _amd_is_voicemail(...).
- Set label to IfExp.
- With state.lock:
-   If a boolean condition:

**Calls →**
1. `features._dialer._call_events.pickup.str`
2. `params.get`
3. `params.get`
4. `state.record_activity`
5. `features._dialer._call_events.pickup.str`
6. `params.get`
7. `features._dialer._call_events.pickup._amd_should_connect`
8. `features._dialer._call_events.pickup._amd_is_voicemail`
9. `call.get`
10. `call.get`
11. `features._dialer.rules._bump`
12. `features._dialer._call_events.pickup._name`
13. `features._dialer.rules._flush_metrics`
14. `call.get`
15. `state.read_settings`
16. `features._dialer.voice_session.is_ai_voice`
17. `features._dialer._call_events.pickup.str`
18. `settings.get`
19. `call.get`
20. `features._dialer._call_events.pickup.str`
21. `settings.get`
22. `features._dialer.twilio._redirect_call`
23. `call.get`
24. `features._dialer.twilio._url`
25. `features._dialer._call_events.pickup._drop_line`
26. `call.get`
27. `features._dialer.twilio._call_is_live`
28. `call.get`
29. `features._dialer._call_events.pickup._connect_prospect`
30. `features._dialer._call_events.pickup._drop_line`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`
