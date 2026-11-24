# `features/ai_agent_sandbox.py`

**Purpose:** Desk sandbox: mic as prospect; agent uses same LLM + Cartesia path as live AI voice.

## Functions
### `_agent_name` (line 28)

**Pseudocode:**
- Return ai_agents._agent_name(...).

**Calls →**
1. `features.ai_agents._agent_name`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_system_prompt`
- `fn:features/ai_agent_sandbox.py:start`

### `_system_prompt` (line 32)

**Pseudocode:**
- Set playbook to ai_agent_playbook.get_playbook(...).
- Set system to playbook[...][...] op _SANDBOX_NOTE.
- Set prospect to a dict.
- Set block to '\n'.join(...).
- If block:
-   Set system to JoinedStr.
- Return system.

**Calls →**
1. `features.ai_agent_playbook.get_playbook`
2. `features.ai_agent_sandbox._agent_name`
3. `prospect.items`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:start`

### `_transcript_line` (line 44)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `datetime.datetime.now`
2. `datetime.datetime.now`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_apply_agent_reply`
- `fn:features/ai_agent_sandbox.py:_boot_session`
- `fn:features/ai_agent_sandbox.py:_prospect_turn`
- `fn:features/ai_agent_sandbox.py:_session_template`

### `_bump_transcript` (line 53)

**Pseudocode:**
- Call session[...].append(...).
- Set session[...] to int(...) op 1.

**Calls →**
1. `features.ai_agent_sandbox.int`
2. `session.get`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_apply_agent_reply`
- `fn:features/ai_agent_sandbox.py:_prospect_turn`

### `_mark_outbound_delivered` (line 58)

**Pseudocode:**
- Set session[...] to len(...).

**Calls →**
1. `features.ai_agent_sandbox.len`
2. `session.get`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_public`

### `_append_sandbox_chunk` (line 62)

**Pseudocode:**
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Return nothing.
-   Call session.setdefault(...).append(...).
-   Set session[...] to dict(...).

**Calls →**
1. `state.ai_sandbox_sessions.get`
2. `session.setdefault`
3. `features.ai_agent_sandbox.dict`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_run_sandbox_tts`

### `_run_sandbox_tts` (line 71)

**Pseudocode:**
- Set settings to state.read_settings(...).
- Try:
-   Set err to ai_voice_cartesia.tts_sandbox_stream(...).
-   If err:
-     Call state.record_activity(...).
-   Else:
-     With state.lock:
-       Set session to state.ai_sandbox_sessions.get(...).

**Calls →**
1. `state.read_settings`
2. `features.ai_agent_sandbox._append_sandbox_chunk`
3. `features.ai_voice_cartesia.tts_sandbox_stream`
4. `state.record_activity`
5. `state.ai_sandbox_sessions.get`
6. `features.ai_agent_sandbox.bool`
7. `session.get`
8. `state.record_activity`
9. `state.ai_sandbox_sessions.get`

### `_start_sandbox_tts` (line 97)

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   Return nothing.
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Return nothing.
-   Set session[...] to True.

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `state.ai_sandbox_sessions.get`
3. `threading.Thread`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_apply_agent_reply`
- `fn:features/ai_agent_sandbox.py:_boot_session`

### `_opening_reply` (line 109)

**Pseudocode:**
- Try:
-   Return ai_voice_llm.chat_reply(...).
- On <ast.Attribute object at 0x00000242BC2CD190>:
-   Return ai_voice_llm._fallback_reply(...).

**Calls →**
1. `features.ai_voice_llm.chat_reply`
2. `state.read_settings`
3. `features.ai_voice_llm._fallback_reply`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_boot_session`

### `_session_template` (line 120)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `features.ai_agent_sandbox._transcript_line`
2. `features.ai_agent_sandbox.bytearray`

### `_apply_agent_reply` (line 139)

**Pseudocode:**
- Set lowered to reply.lower(...).
- If '[end_call]' compared to ...:
-   Set reply to reply.replace(...).replace(...).strip(...).
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Return Tuple.
-   Call session[...].append(...).

**Calls →**
1. `reply.lower`
2. `reply.replace`
3. `state.ai_sandbox_sessions.get`
4. `features.ai_agent_sandbox._bump_transcript`
5. `features.ai_agent_sandbox._transcript_line`
6. `features.ai_agent_sandbox._start_sandbox_tts`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_prospect_turn`

### `_prospect_turn` (line 154)

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   If from_stt:
-     Return _public(...).
-   Raise an error.
- Set key to text.lower(...).
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `features.ai_agent_sandbox._public`
3. `features.ai_agent_sandbox.ValueError`
4. `text.lower`
5. `state.ai_sandbox_sessions.get`
6. `features.ai_agent_sandbox.ValueError`
7. `session.get`
8. `features.ai_agent_sandbox._public`
9. `session.get`
10. `features.ai_agent_sandbox._public`
11. `features.ai_agent_sandbox._bump_transcript`
12. `features.ai_agent_sandbox._transcript_line`
13. `features.ai_agent_sandbox.list`
14. `features.ai_voice_llm.chat_reply`
15. `state.read_settings`
16. `state.record_activity`
17. `features.ai_agent_sandbox._public`
18. `features.ai_agent_sandbox.ValueError`
19. `features.ai_agent_sandbox.str`
20. `features.ai_agent_sandbox._apply_agent_reply`
21. `features.ai_agent_sandbox._public`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_transcribe_and_turn`
- `fn:features/ai_agent_sandbox.py:turn`

### `_wait_playback_ready` (line 187)

**Pseudocode:**
- Set deadline to time.time(...) op timeout.
- While time.time(...) compared to ...:
-   With state.lock:
-     Set session to state.ai_sandbox_sessions.get(...).
-     If session:
-       Return False.
-     If session.get(...):
-       Return True.

**Calls →**
1. `time.time`
2. `time.time`
3. `state.ai_sandbox_sessions.get`
4. `session.get`
5. `time.sleep`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_boot_session`

### `_boot_session` (line 200)

**Pseudocode:**
- Set opening to _opening_reply(...).
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Return nothing.
-   Set session[...] to a list.
-   Set session[...] to a list.
-   Set session[...] to 1.

**Calls →**
1. `features.ai_agent_sandbox._opening_reply`
2. `state.ai_sandbox_sessions.get`
3. `features.ai_agent_sandbox._transcript_line`
4. `features.ai_agent_sandbox._wait_playback_ready`
5. `state.record_activity`
6. `features.ai_agent_sandbox._start_sandbox_tts`
7. `state.ai_sandbox_sessions.get`

### `mark_playback_ready` (line 218)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Set session[...] to True.
- Return _public(...).

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `state.ai_sandbox_sessions.get`
3. `features.ai_agent_sandbox._public`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_playback_ready`

### `start` (line 227)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If agent_id:
-   Raise an error.
- If state.running:
-   Raise an error.
- Set system to _system_prompt(...).
- Set prospect_merged to a dict.
- With state.lock:

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `features.ai_agent_sandbox.ValueError`
3. `features.ai_agent_sandbox.ValueError`
4. `features.ai_agent_sandbox._system_prompt`
5. `features.ai_agent_sandbox.bytearray`
6. `threading.Thread`
7. `state.record_activity`
8. `features.ai_agent_sandbox._agent_name`
9. `features.ai_agent_sandbox._public`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_start`

### `turn` (line 260)

**Pseudocode:**
- Return _prospect_turn(...).

**Calls →**
1. `features.ai_agent_sandbox._prospect_turn`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_turn`

### `_collect_utterances` (line 264)
_Step VAD in 20 ms mulaw frames (same cadence as the live media bridge)._

**Pseudocode:**
- Set utterances to a list.
- If chunk:
-   Return utterances.
- Set buf to session.setdefault(...).
- For each offset in range(...):
-   Set frame to chunk[...].
-   If len(...) compared to ...:
-     Set frame to frame op bytes(...).

**Calls →**
1. `session.setdefault`
2. `features.ai_agent_sandbox.bytearray`
3. `features.ai_agent_sandbox.range`
4. `features.ai_agent_sandbox.len`
5. `features.ai_agent_sandbox.len`
6. `features.ai_agent_sandbox.bytes`
7. `features.ai_agent_sandbox.len`
8. `buf.extend`
9. `features.ai_voice_stt.mulaw_rms`
10. `features.ai_agent_sandbox.int`
11. `session.get`
12. `session.get`
13. `features.ai_agent_sandbox.int`
14. `session.get`
15. `features.ai_agent_sandbox.len`
16. `utterances.append`
17. `features.ai_agent_sandbox.bytes`
18. `buf.clear`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:ingest_mulaw`

### `ingest_mulaw` (line 296)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Try:
-   Set chunk to base64.b64decode(...).
- On <ast.Tuple object at 0x00000242BC2BE190>:
-   Return nothing.
- If chunk:
-   Return nothing.
- Set utterances to a list.

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `base64.b64decode`
3. `state.ai_sandbox_sessions.get`
4. `session.get`
5. `session.get`
6. `features.ai_agent_sandbox._collect_utterances`
7. `threading.Thread`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_ingest`

### `_transcribe_and_turn` (line 314)

**Pseudocode:**
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If a boolean condition:
-     Return nothing.
-   Set session[...] to True.
- Try:
-   Set text to ai_voice_stt.transcribe_mulaw(...).
-   If text:

**Calls →**
1. `state.ai_sandbox_sessions.get`
2. `session.get`
3. `features.ai_voice_stt.transcribe_mulaw`
4. `state.read_settings`
5. `features.ai_agent_sandbox._prospect_turn`
6. `state.record_activity`
7. `state.ai_sandbox_sessions.get`

### `_audio_meta` (line 333)

**Pseudocode:**
- Set meta to dict(...).
- Return a dict.

**Calls →**
1. `features.ai_agent_sandbox.dict`
2. `session.get`
3. `features.ai_agent_sandbox.str`
4. `meta.get`
5. `features.ai_agent_sandbox.int`
6. `meta.get`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_public`
- `fn:features/ai_agent_sandbox.py:stream_sync`

### `stream_sync` (line 341)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
-   If session:
-     Return a dict.
-   Set start to int(...).
-   Set pending to list(...)[...].
-   If session.get(...):

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `state.ai_sandbox_sessions.get`
3. `features.ai_agent_sandbox.int`
4. `session.get`
5. `features.ai_agent_sandbox.list`
6. `session.get`
7. `session.get`
8. `features.ai_agent_sandbox.len`
9. `session.get`
10. `features.ai_agent_sandbox.bool`
11. `session.get`
12. `features.ai_agent_sandbox.list`
13. `session.get`
14. `features.ai_agent_sandbox.int`
15. `session.get`
16. `features.ai_agent_sandbox.bool`
17. `session.get`
18. `session.get`
19. `session.get`
20. `features.ai_agent_sandbox.bool`
21. `session.get`
22. `features.ai_agent_sandbox.bool`
23. `session.get`
24. `features.ai_agent_sandbox._audio_meta`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_sync`

### `reset` (line 374)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- With state.lock:
-   Call state.ai_sandbox_sessions.pop(...).
- Return a dict.

**Calls →**
1. `features.ai_agent_sandbox.str`
2. `state.ai_sandbox_sessions.pop`

**Called by ←**
- `fn:features/dialer.py:ai_sandbox_reset`

### `_public` (line 381)

**Pseudocode:**
- With state.lock:
-   Set session to state.ai_sandbox_sessions.get(...).
- If session:
-   Return a dict.
- Set payload to a dict.
- If audio_chunks:
-   Set payload[...] to list(...).
-   With state.lock:

**Calls →**
1. `state.ai_sandbox_sessions.get`
2. `features.ai_agent_sandbox.bool`
3. `session.get`
4. `features.ai_agent_sandbox.list`
5. `session.get`
6. `features.ai_agent_sandbox.int`
7. `session.get`
8. `features.ai_agent_sandbox.list`
9. `session.get`
10. `features.ai_agent_sandbox.dict`
11. `session.get`
12. `features.ai_agent_sandbox.bool`
13. `session.get`
14. `session.get`
15. `session.get`
16. `features.ai_agent_sandbox.bool`
17. `session.get`
18. `features.ai_agent_sandbox.bool`
19. `session.get`
20. `features.ai_agent_sandbox.list`
21. `state.ai_sandbox_sessions.get`
22. `features.ai_agent_sandbox._mark_outbound_delivered`
23. `payload.update`
24. `features.ai_agent_sandbox._audio_meta`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_prospect_turn`
- `fn:features/ai_agent_sandbox.py:mark_playback_ready`
- `fn:features/ai_agent_sandbox.py:start`

### `active_for_agent` (line 408)

**Pseudocode:**
- With state.lock:
-   Return bool(...).

**Calls →**
1. `features.ai_agent_sandbox.bool`
2. `state.ai_sandbox_sessions.get`
3. `features.ai_agent_sandbox.str`
