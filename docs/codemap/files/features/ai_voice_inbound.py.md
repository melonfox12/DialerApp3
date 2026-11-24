# `features/ai_voice_inbound.py`

**Purpose:** Buffer bridge mulaw; detect end of utterance; STT.

## Functions
### `ingest_mulaw` (line 14)

**Pseudocode:**
- Set session to ai_voice_runtime.get_session(...).
- If a boolean condition:
-   Return nothing.
- Try:
-   Set chunk to base64.b64decode(...).
- On <ast.Tuple object at 0x00000242BC12D090>:
-   Return nothing.
- If chunk:

**Calls →**
1. `features.ai_voice_runtime.get_session`
2. `session.get`
3. `base64.b64decode`
4. `state.ai_voice_sessions.get`
5. `session.get`
6. `session.setdefault`
7. `features.ai_voice_inbound.bytearray`
8. `buf.extend`
9. `features.ai_voice_stt.mulaw_rms`
10. `features.ai_voice_inbound.int`
11. `session.get`
12. `session.get`
13. `features.ai_voice_inbound.int`
14. `session.get`
15. `features.ai_voice_inbound.len`
16. `features.ai_voice_inbound.bytes`
17. `buf.clear`
18. `threading.Thread`

**Called by ←**
- `fn:features/ai_voice_routes.py:post_ai_voice_inbound`

### `_transcribe_and_reply` (line 51)

**Pseudocode:**
- Set text to ai_voice_stt.transcribe_mulaw(...).
- If text:
-   Return nothing.
- With state.lock:
-   Set session to state.ai_voice_sessions.get(...).
-   If session:
-     Return nothing.
-   Set call to state.calls.get(...).

**Calls →**
1. `features.ai_voice_stt.transcribe_mulaw`
2. `state.read_settings`
3. `state.ai_voice_sessions.get`
4. `state.calls.get`
5. `session.get`
6. `features.ai_voice_runtime.on_prospect_text`
