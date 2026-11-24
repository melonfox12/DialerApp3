# `features/ai_voice_runtime.py`

**Purpose:** In-call AI voice sessions: prompt, LLM turns, outbound audio queue.

## Functions
### `get_session` (line 18)

**Pseudocode:**
- With state.lock:
-   Return state.ai_voice_sessions.get(...).

**Calls →**
1. `state.ai_voice_sessions.get`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`
- `fn:features/ai_voice_inbound.py:ingest_mulaw`
- `fn:features/ai_voice_runtime.py:_queue_speech`
- `fn:features/ai_voice_runtime.py:_schedule_watchers`
- `fn:features/ai_voice_runtime.py:bootstrap`
- `fn:features/ai_voice_runtime.py:kickoff_conversation`
- `fn:features/ai_voice_runtime.py:on_prospect_text`
- `fn:features/ai_voice_runtime.py:start_call_session`

### `voice_configured` (line 23)

**Pseudocode:**
- Set settings to a boolean condition.
- Return bool(...).

**Calls →**
1. `features.ai_voice_runtime.bool`
2. `features.ai_voice_runtime.str`
3. `settings.get`
4. `features.ai_voice_runtime.str`
5. `settings.get`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/ai_voice_runtime.py:ai_stream_twiml`
- `fn:features/ai_voice_runtime.py:public_status`

### `bridge_secret_ok` (line 31)

**Pseudocode:**
- Set expected to str(...).strip(...).
- If expected:
-   Return False.
- Return secrets.compare_digest(...).

**Calls →**
1. `features.ai_voice_runtime.str`
2. `state.read_settings`
3. `secrets.compare_digest`
4. `features.ai_voice_runtime.str`

**Called by ←**
- `fn:features/ai_voice_routes.py:_require_bridge`

### `_lead_context` (line 38)

**Pseudocode:**
- Set lead to a boolean condition.
- Return a dict.

**Calls →**
1. `lead.get`
2. `lead.get`
3. `lead.get`
4. `shared.prospect_schema.display_name`
5. `lead.get`
6. `lead.get`

**Called by ←**
- `fn:features/ai_voice_runtime.py:start_call_session`

### `_touch` (line 50)

**Pseudocode:**
- Set session[...] to time.monotonic(...).

**Calls →**
1. `time.monotonic`

**Called by ←**
- `fn:features/ai_voice_runtime.py:_queue_speech`
- `fn:features/ai_voice_runtime.py:mark_stream_started`
- `fn:features/ai_voice_runtime.py:on_prospect_text`

### `_schedule_watchers` (line 54)

**Pseudocode:**
- Call threading.Timer(...).start(...).
- Call threading.Thread(...).start(...).

**Calls →**
1. `features.ai_voice_runtime.get_session`
2. `session.get`
3. `session.get`
4. `features._dialer.twilio._hangup_call`
5. `time.sleep`
6. `features.ai_voice_runtime.get_session`
7. `session.get`
8. `features.ai_voice_runtime.float`
9. `session.get`
10. `time.monotonic`
11. `session.get`
12. `features._dialer.twilio._hangup_call`
13. `threading.Timer`
14. `threading.Thread`

**Called by ←**
- `fn:features/ai_voice_runtime.py:mark_stream_started`

### `start_call_session` (line 80)

**Pseudocode:**
- If voice_session.is_ai_voice(...):
-   Return None.
- Set existing to call.get(...).
- If a boolean condition:
-   Return existing.
- Set settings to state.read_settings(...).
- Set agent_id to a boolean condition.
- Set agent_name to ai_agents._agent_name(...).

**Calls →**
1. `features._dialer.voice_session.is_ai_voice`
2. `call.get`
3. `features.ai_voice_runtime.get_session`
4. `state.read_settings`
5. `features.ai_voice_runtime.getattr`
6. `features.ai_agents._agent_name`
7. `features.ai_agent_playbook.get_playbook`
8. `secrets.token_hex`
9. `features.ai_voice_runtime._lead_context`
10. `call.get`
11. `lead_ctx.items`
12. `call.get`
13. `call.get`
14. `features.ai_voice_runtime.bytearray`
15. `time.monotonic`
16. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/call_events.py:handle_webhook`

### `ai_stream_twiml` (line 121)

**Pseudocode:**
- Set settings to state.read_settings(...).
- If voice_configured(...):
-   Set msg to twilio.escape_xml(...).
-   Return JoinedStr.
- Set wss to str(...).strip(...).
- Set session_id to a boolean condition.
- Set joiner to IfExp.
- Set stream_url to JoinedStr.

**Calls →**
1. `state.read_settings`
2. `features.ai_voice_runtime.voice_configured`
3. `features._dialer.twilio.escape_xml`
4. `features.ai_voice_runtime.str`
5. `settings.get`
6. `call.get`
7. `urllib.parse.parse.quote`
8. `features._dialer.twilio.escape_xml`
9. `features._dialer.twilio.escape_xml`
10. `features._dialer.twilio.escape_xml`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`

### `_queue_speech` (line 143)

**Pseudocode:**
- Set session to get_session(...).
- If a boolean condition:
-   Return nothing.
- With state.lock:
-   Set storage to state.calls.get(...).
-   Call _touch(...).
- If storage:
-   Call live_transcript.append_final(...).

**Calls →**
1. `features.ai_voice_runtime.get_session`
2. `state.calls.get`
3. `features.ai_voice_runtime._touch`
4. `features._dialer.live_transcript.append_final`
5. `state.read_settings`
6. `state.ai_voice_sessions.get`
7. `features.ai_voice_cartesia.tts_mulaw_stream`
8. `state.record_activity`
9. `state.ai_voice_sessions.get`
10. `live.get`
11. `state.record_activity`

**Called by ←**
- `fn:features/ai_voice_runtime.py:kickoff_conversation`
- `fn:features/ai_voice_runtime.py:on_prospect_text`

### `kickoff_conversation` (line 172)

**Pseudocode:**
- Call threading.Thread(...).start(...).

**Calls →**
1. `features.ai_voice_runtime.get_session`
2. `features.ai_voice_llm.chat_reply`
3. `state.read_settings`
4. `state.record_activity`
5. `features.ai_voice_llm._fallback_reply`
6. `state.ai_voice_sessions.get`
7. `features.ai_voice_runtime._queue_speech`
8. `threading.Thread`

**Called by ←**
- `fn:features/ai_voice_runtime.py:mark_stream_started`

### `on_prospect_text` (line 197)

**Pseudocode:**
- If voice_session.is_ai_voice(...):
-   Return nothing.
- Set session_id to call.get(...).
- Set text to str(...).strip(...).
- If a boolean condition:
-   Return nothing.
- If source compared to ...:
-   Set session to get_session(...).

**Calls →**
1. `features._dialer.voice_session.is_ai_voice`
2. `call.get`
3. `features.ai_voice_runtime.str`
4. `features.ai_voice_runtime.get_session`
5. `session.get`
6. `text.lower`
7. `state.ai_voice_sessions.get`
8. `session.get`
9. `session.get`
10. `features.ai_voice_runtime._touch`
11. `features._dialer.live_transcript.append_final`
12. `state.ai_voice_sessions.get`
13. `session.get`
14. `features.ai_voice_runtime.list`
15. `features.ai_voice_llm.chat_reply`
16. `state.read_settings`
17. `state.record_activity`
18. `reply.lower`
19. `reply.replace`
20. `state.ai_voice_sessions.get`
21. `features.ai_voice_runtime._queue_speech`
22. `call.get`
23. `threading.Timer`
24. `threading.Thread`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`
- `fn:features/ai_voice_inbound.py:_transcribe_and_reply`

### `mark_stream_started` (line 249)

**Pseudocode:**
- With state.lock:
-   Set session to state.ai_voice_sessions.get(...).
-   If session:
-     Set session[...] to True.
-     Call _touch(...).
- Call _schedule_watchers(...).
- Call kickoff_conversation(...).

**Calls →**
1. `state.ai_voice_sessions.get`
2. `features.ai_voice_runtime._touch`
3. `features.ai_voice_runtime._schedule_watchers`
4. `features.ai_voice_runtime.kickoff_conversation`

**Called by ←**
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_started`

### `stream_sync` (line 259)

**Pseudocode:**
- With state.lock:
-   Set session to state.ai_voice_sessions.get(...).
-   If session:
-     Return a dict.
-   Set start to session[...].
-   Set chunks to session[...][...].
-   Set session[...] to len(...).

**Calls →**
1. `state.ai_voice_sessions.get`
2. `features.ai_voice_runtime.len`
3. `features.ai_voice_runtime.bool`
4. `session.get`

**Called by ←**
- `fn:features/ai_voice_routes.py:get_ai_voice_stream_sync`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_started`

### `finish_session` (line 270)

**Pseudocode:**
- Set lead_id to None.
- Set agent_id to None.
- Set messages to a list.
- With state.lock:
-   Set session to state.ai_voice_sessions.pop(...).
-   If session:
-     Return nothing.
-   Set session[...] to True.

**Calls →**
1. `state.ai_voice_sessions.pop`
2. `session.get`
3. `session.get`
4. `session.get`
5. `state.calls.get`
6. `session.get`
7. `features.ai_voice_disposition.suggest_status`
8. `state.read_settings`
9. `features.ai_voice_runtime.next`
10. `state.crm.snapshot`
11. `item.get`
12. `shared.dial_policy.agent_reservation_blocks_other_apps`
13. `state.crm.agent_finalize_status`

**Called by ←**
- `fn:features/ai_voice_runtime.py:end_session`
- `fn:features/ai_voice_runtime.py:purge_sessions`

### `end_session` (line 294)

**Pseudocode:**
- Call finish_session(...).

**Calls →**
1. `features.ai_voice_runtime.finish_session`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_stopped`

### `purge_sessions` (line 298)

**Pseudocode:**
- With state.lock:
-   Set ids to list(...).
- For each session_id in ids:
-   Call finish_session(...).

**Calls →**
1. `features.ai_voice_runtime.list`
2. `features.ai_voice_runtime.finish_session`

### `bootstrap` (line 305)

**Pseudocode:**
- Set session to get_session(...).
- If session:
-   Return None.
- Return a dict.

**Calls →**
1. `features.ai_voice_runtime.get_session`
2. `session.get`
3. `session.get`
4. `session.get`

**Called by ←**
- `fn:features/ai_voice_routes.py:get_ai_voice_bootstrap`

### `public_status` (line 317)

**Pseudocode:**
- Set settings to state.read_settings(...).
- Set active to 0.
- With state.lock:
-   Set active to sum(...).
- Return a dict.

**Calls →**
1. `state.read_settings`
2. `features.ai_voice_runtime.sum`
3. `state.ai_voice_sessions.values`
4. `item.get`
5. `features.ai_voice_runtime.voice_configured`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
