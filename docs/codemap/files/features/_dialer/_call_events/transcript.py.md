# `features/_dialer/_call_events/transcript.py`

**Purpose:** Live conference TwiML and transcription callbacks.

## Functions
### `_live_twiml` (line 12)
_Bridge the prospect into the agent conference. Transcription starts after media is up._

**Pseudocode:**
- Set conf to twilio.escape_xml(...).
- Return JoinedStr.

**Calls →**
1. `features._dialer.twilio.escape_xml`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`

### `_agent_call` (line 22)

**Pseudocode:**
- With state.lock:
-   Set token to state.agent_call_token.
-   Return IfExp.

**Calls →**
1. `state.calls.get`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:schedule_live_transcription`

### `_storage_call` (line 28)
_Prospect row that receives transcript lines (agent leg events attach to the live prospect)._

**Pseudocode:**
- With state.lock:
-   If call.get(...) compared to ...:
-     Set pinned to call.get(...).
-     If a boolean condition:
-       Return state.calls[...].
-   If call.get(...):
-     Return call.
- Return None.

**Calls →**
1. `call.get`
2. `call.get`
3. `call.get`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`

### `_speaker_for` (line 40)

**Pseudocode:**
- Set value to str(...).lower(...).
- Set inbound to 'inbound' compared to ....
- Set outbound to 'outbound' compared to ....
- If call_kind compared to ...:
-   If inbound:
-     Return 'Agent'.
-   If outbound:
-     Return 'Prospect'.

**Calls →**
1. `features._dialer._call_events.transcript.str`
2. `features._dialer._call_events.transcript.str`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`

### `schedule_live_transcription` (line 65)
_Start live transcription on the agent browser leg once the prospect is in the conference._

**Pseudocode:**
- With state.lock:
-   Set agent to _agent_call(...).
-   Set agent_uuid to IfExp.
-   If a boolean condition:
-     Set agent[...] to prospect_call[...].
-     If agent.get(...):
-       Return nothing.
-     Set media_call to agent.

**Calls →**
1. `features._dialer._call_events.transcript._agent_call`
2. `agent.get`
3. `prospect_call.get`
4. `prospect_call.get`
5. `prospect_call.get`
6. `features._dialer.twilio._url`
7. `time.sleep`
8. `features._dialer.twilio._start_live_transcription`
9. `media_call.get`
10. `media_call.pop`
11. `state.record_activity`
12. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/call_events.py:handle_webhook`

### `_live_prospect` (line 106)

**Pseudocode:**
- With state.lock:
-   If media_call.get(...) compared to ...:
-     Set token to media_call.get(...).
-     Set prospect to IfExp.
-   Else:
-     Set prospect to media_call.
-   If a boolean condition:
-     Return None.

**Calls →**
1. `media_call.get`
2. `media_call.get`
3. `state.calls.get`
4. `prospect.get`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_call_still_connected`

### `_call_still_connected` (line 118)

**Pseudocode:**
- With state.lock:
-   Set prospect to _live_prospect(...).
-   If prospect compared to ...:
-     Set prospect to IfExp.
-   If prospect compared to ...:
-     Return False.
-   Return bool(...).

**Calls →**
1. `features._dialer._call_events.transcript._live_prospect`
2. `media_call.get`
3. `features._dialer._call_events.transcript.bool`
4. `prospect.get`
5. `prospect.get`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_resume_transcription`
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`

### `_resume_transcription` (line 133)
_Twilio ends a transcript session on its own. Open another while the call is up._

**Pseudocode:**
- With state.lock:
-   If _call_still_connected(...):
-     Return nothing.
-   Set now to time.monotonic(...).
-   If now op float(...) compared to ...:
-     Return nothing.
-   Set media_call[...] to now.
-   Set count to int(...) op 1.

**Calls →**
1. `features._dialer._call_events.transcript._call_still_connected`
2. `time.monotonic`
3. `features._dialer._call_events.transcript.float`
4. `media_call.get`
5. `features._dialer._call_events.transcript.int`
6. `media_call.get`
7. `media_call.get`
8. `features._dialer.twilio._start_live_transcription`
9. `features._dialer.twilio._url`
10. `state.record_activity`
11. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`

### `_transcription_event` (line 160)

**Pseudocode:**
- Set storage to _storage_call(...).
- Set call_kind to a boolean condition.
- Set event to params.get(...).
- If event compared to ...:
-   With state.lock:
-     Set call[...] to True.
-     If storage:
-       Set storage[...] to True.

**Calls →**
1. `features._dialer._call_events.transcript._storage_call`
2. `call.get`
3. `params.get`
4. `state.record_activity`
5. `features._dialer.live_transcript.commit_partials`
6. `features._dialer._call_events.transcript._call_still_connected`
7. `features._dialer._call_events.transcript._resume_transcription`
8. `state.record_activity`
9. `params.get`
10. `state.record_activity`
11. `features._dialer._call_events.transcript._call_still_connected`
12. `features._dialer._call_events.transcript._resume_transcription`
13. `json.loads`
14. `params.get`
15. `features._dialer._call_events.transcript.str`
16. `data.get`
17. `params.get`
18. `params.get`
19. `params.get`
20. `params.get`
21. `features._dialer._call_events.transcript._speaker_for`
22. `params.get`
23. `datetime.datetime.now`
24. `features._dialer._call_events.transcript.str`
25. `params.get`
26. `features._dialer.live_transcript.append_partial`
27. `params.get`
28. `call.get`
29. `params.get`
30. `features._dialer.live_transcript.append_final`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`
