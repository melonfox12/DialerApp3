# `features/_dialer/call_events.py`

**Purpose:** Webhook and browser-voice dispatch. Imports pickup, transcript, then ended.

## Functions
### `_uuid` (line 12)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `params.get`
2. `params.get`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`

### `handle_webhook` (line 15)

**Pseudocode:**
- With state.lock:
-   Set call to state.calls.get(...).
-   If call:
-     Return Tuple.
-   Set call_uuid to _uuid(...).
-   If call_uuid:
-     Set call[...] to call_uuid.
-     If call[...] compared to ...:

**Calls →**
1. `state.calls.get`
2. `features._dialer.call_events._uuid`
3. `state.record_activity`
4. `params.get`
5. `call.get`
6. `call.get`
7. `features._dialer.twilio._hangup_call`
8. `features._dialer.voice_session.uses_browser_agent_leg`
9. `threading.Thread`
10. `features._dialer.twilio.escape_xml`
11. `features._dialer.rules.clear_stale_active`
12. `call.get`
13. `call.get`
14. `features._dialer.voice_session.is_ai_voice`
15. `call.get`
16. `features.ai_voice_runtime.start_call_session`
17. `features.ai_voice_runtime.voice_configured`
18. `state.read_settings`
19. `features._dialer._call_events.transcript.schedule_live_transcription`
20. `features.ai_voice_runtime.ai_stream_twiml`
21. `features._dialer._call_events.transcript.schedule_live_transcription`
22. `features._dialer.call_events.str`
23. `features._dialer._call_events.transcript._live_twiml`
24. `features._dialer.twilio.waiting_twiml`
25. `state.read_settings`
26. `call.get`
27. `features._dialer.call_events.str`
28. `settings.get`
29. `features._dialer.twilio.escape_xml`
30. `features._dialer._call_events.pickup._machine_result`

**Called by ←**
- `fn:features/dialer.py:handle_webhook`

### `handle_client_voice` (line 98)

**Pseudocode:**
- If voice_session.uses_browser_agent_leg(...):
-   Return Tuple.
- Set token to a boolean condition.
- With state.lock:
-   Set call to state.calls.get(...).
-   If a boolean condition:
-     Return Tuple.
-   Set call_uuid to params.get(...).

**Calls →**
1. `features._dialer.voice_session.uses_browser_agent_leg`
2. `params.get`
3. `params.get`
4. `state.calls.get`
5. `params.get`
6. `state.record_activity`
7. `threading.Thread`
8. `features._dialer.twilio.escape_xml`
9. `features._dialer.twilio._url`
10. `features._dialer.twilio.escape_xml`

**Called by ←**
- `fn:features/dialer.py:handle_client_voice`

### `hangup_active` (line 121)

**Pseudocode:**
- With state.lock:
-   Set call to a boolean condition.
-   Set call_uuid to IfExp.
-   If a boolean condition:
-     Set ai_mode to getattr(...).
-     If a boolean condition:
-       Set call[...] to True.
-       If ai_mode:

**Calls →**
1. `features._dialer.call_events.next`
2. `state.in_flight.values`
3. `call.get`
4. `features._dialer.call_events.getattr`
5. `call.get`
6. `state.in_flight.pop`
7. `threading.Thread`
8. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:hangup_active`

### `skip_active` (line 150)

**Pseudocode:**
- With state.lock:
-   Set call to a boolean condition.
-   If call:
-     Raise an error.
-   Set lead_id to call.get(...).
-   Set picked_up to a boolean condition.
- If a boolean condition:
-   Return queue.pass_next(...).

**Calls →**
1. `features._dialer.call_events.next`
2. `state.in_flight.values`
3. `features._dialer.call_events.ValueError`
4. `call.get`
5. `features._dialer.call_events.bool`
6. `call.get`
7. `features._dialer.queue.pass_next`
8. `call.get`
9. `features._dialer.call_events.getattr`
10. `features._dialer.queue.schedule_callback`
11. `features._dialer.rules._bump`
12. `features._dialer.rules._flush_metrics`
13. `features._dialer.call_events.getattr`
14. `state.record_activity`
15. `threading.Thread`
16. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:skip_active`
