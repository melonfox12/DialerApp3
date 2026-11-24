# `features/_dialer/live_transcript.py`

**Purpose:** Single write path for live conversation text (Twilio today, Cartesia bridge later).

## Functions
### `append_partial` (line 8)

**Pseudocode:**
- If a boolean condition:
-   Return nothing.
- Set text to str(...).strip(...).
- If text:
-   Return nothing.
- Set timestamp to a boolean condition.
- Set partial to a dict.
- With state.lock:

**Calls →**
1. `features._dialer.live_transcript.str`
2. `datetime.datetime.now`
3. `storage_call.setdefault`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`

### `append_final` (line 27)

**Pseudocode:**
- If a boolean condition:
-   Return False.
- Set text to str(...).strip(...).
- If text:
-   Return False.
- Set timestamp to a boolean condition.
- Set leg_id to a boolean condition.
- Set segment_id to a boolean condition.

**Calls →**
1. `features._dialer.live_transcript.str`
2. `datetime.datetime.now`
3. `storage_call.get`
4. `storage_call.get`
5. `state.crm.append_transcript`
6. `state.record_activity`
7. `storage_call.setdefault`
8. `storage_call.setdefault`
9. `features._dialer.live_transcript.any`
10. `item.get`
11. `lines.append`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`
- `fn:features/_dialer/live_transcript.py:commit_partials`
- `fn:features/ai_voice_runtime.py:_queue_speech`
- `fn:features/ai_voice_runtime.py:on_prospect_text`

### `commit_partials` (line 77)
_Promote in-progress partial lines when a transcript session closes._

**Pseudocode:**
- If storage_call:
-   Return nothing.
- With state.lock:
-   Set partials to list(...).
-   Call storage_call[...].clear(...).
-   Set leg_id to a boolean condition.
- For each Tuple in partials:
-   Set text to str(...).strip(...).

**Calls →**
1. `features._dialer.live_transcript.list`
2. `storage_call.get`
3. `storage_call.get`
4. `features._dialer.live_transcript.str`
5. `datetime.datetime.now`
6. `features._dialer.live_transcript.append_final`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`
