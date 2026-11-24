# `features/ai_voice_cartesia.py`

**Purpose:** Cartesia TTS → mulaw chunks for Twilio media streams.

## Routes
- `POST` `/tts/sse` → `body`

## Functions
### `_parse_error_detail` (line 19)

**Pseudocode:**
- Try:
-   Set payload to json.loads(...).
- On <ast.Attribute object at 0x000001E0F8E51A50>:
-   Return raw[...].
- If isinstance(...):
-   For each key in Tuple:
-     Set value to payload.get(...).
-     If value:

**Calls →**
1. `json.loads`
2. `features.ai_voice_cartesia.isinstance`
3. `payload.get`
4. `features.ai_voice_cartesia.str`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:_cartesia_sse_request`
- `fn:features/ai_voice_cartesia.py:_fetch_tts_bytes`

### `_normalize_voice_id` (line 32)

**Pseudocode:**
- Set voice_id to str(...).strip(...).strip(...).strip(...).
- If voice_id:
-   Return ''.
- If _UUID_RE.match(...):
-   Return voice_id.lower(...).
- Return ''.

**Calls →**
1. `features.ai_voice_cartesia.str`
2. `_UUID_RE.match`
3. `voice_id.lower`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:_fetch_tts_bytes`
- `fn:features/ai_voice_cartesia.py:_voice_id`

### `_voice_id` (line 41)
_Cartesia API (2026-08-14) expects voice as a UUID string or {"id": "..."}, not legacy mode/id._

**Pseudocode:**
- Set raw to str(...).strip(...).
- Set custom to _normalize_voice_id(...).
- If a boolean condition:
-   Call debug_event(...).
- Return a boolean condition.

**Calls →**
1. `features.ai_voice_cartesia.str`
2. `features.ai_voice_cartesia._normalize_voice_id`
3. `shared.infra.debug_event`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:_cartesia_sse_request`
- `fn:features/ai_voice_cartesia.py:_fetch_tts_bytes`

### `_fetch_tts_bytes` (line 50)

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   Return Tuple.
- Set key to str(...).strip(...).
- If key:
-   Return Tuple.
- Set model_id to a boolean condition.
- Set voice_id to _voice_id(...).

**Calls →**
1. `features.ai_voice_cartesia.str`
2. `features.ai_voice_cartesia.str`
3. `features.ai_voice_cartesia.str`
4. `features.ai_voice_cartesia._voice_id`
5. `features.ai_voice_cartesia._normalize_voice_id`
6. `shared.infra.debug_event`
7. `json.dumps`
8. `urllib.request.request.Request`
9. `urllib.request.request.urlopen`
10. `response.read`
11. `exc.read`
12. `features.ai_voice_cartesia._parse_error_detail`
13. `shared.infra.debug_event`
14. `shared.infra.debug_event`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_mulaw_chunks`
- `fn:features/ai_voice_cartesia.py:tts_sandbox_chunks`

### `_chunk_bytes` (line 100)

**Pseudocode:**
- Set chunks to a list.
- For each offset in range(...):
-   Call chunks.append(...).
- Return chunks.

**Calls →**
1. `features.ai_voice_cartesia.range`
2. `features.ai_voice_cartesia.len`
3. `chunks.append`
4. `base64.b64encode`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_mulaw_chunks`
- `fn:features/ai_voice_cartesia.py:tts_sandbox_chunks`

### `tts_mulaw_chunks` (line 107)
_Return (base64 mulaw chunk strings, error message). error is "" on success._

**Pseudocode:**
- Set Tuple to _fetch_tts_bytes(...).
- If err:
-   Return Tuple.
- Return Tuple.

**Calls →**
1. `features.ai_voice_cartesia._fetch_tts_bytes`
2. `features.ai_voice_cartesia._chunk_bytes`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_mulaw_stream`

### `tts_sandbox_chunks` (line 115)
_Higher-fidelity PCM for browser headphones (not Twilio 8 kHz mulaw)._

**Pseudocode:**
- Set Tuple to _fetch_tts_bytes(...).
- If err:
-   Return Tuple.
- Return Tuple.

**Calls →**
1. `features.ai_voice_cartesia._fetch_tts_bytes`
2. `features.ai_voice_cartesia._chunk_bytes`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_sandbox_stream`

### `_emit_pcm_chunks` (line 136)

**Pseudocode:**
- While len(...) compared to ...:
-   Set piece to bytes(...).
-   Call emit(...).

**Calls →**
1. `features.ai_voice_cartesia.len`
2. `features.ai_voice_cartesia.bytes`
3. `features.ai_voice_cartesia.emit`
4. `base64.b64encode`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_mulaw_stream`
- `fn:features/ai_voice_cartesia.py:tts_sandbox_stream`

### `_cartesia_sse_request` (line 143)

**Pseudocode:**
- Set key to str(...).strip(...).
- If key:
-   Return 'Cartesia API key is missing — add CARTESIA_AP...'.
- Set model_id to a boolean condition.
- Set voice_id to _voice_id(...).
- Set payload to a dict.
- Set body to json.dumps(...).encode(...).
- Set conn to http.client.HTTPSConnection(...).

**Calls →**
1. `features.ai_voice_cartesia.str`
2. `features.ai_voice_cartesia.str`
3. `features.ai_voice_cartesia._voice_id`
4. `json.dumps`
5. `http.client.client.HTTPSConnection`
6. `conn.request`
7. `conn.getresponse`
8. `response.read`
9. `features.ai_voice_cartesia._parse_error_detail`
10. `response.readline`
11. `raw.strip`
12. `json.loads`
13. `data_line.decode`
14. `event.get`
15. `base64.b64decode`
16. `event.get`
17. `features.ai_voice_cartesia.on_pcm`
18. `features.ai_voice_cartesia.str`
19. `event.get`
20. `event.get`
21. `line.startswith`
22. `conn.close`

**Called by ←**
- `fn:features/ai_voice_cartesia.py:tts_mulaw_stream`
- `fn:features/ai_voice_cartesia.py:tts_sandbox_stream`

### `tts_sandbox_stream` (line 211)
_Stream sandbox PCM via Cartesia SSE; emit_chunk(b64) as bytes arrive._

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   Return 'empty transcript'.
- Set pending to bytearray(...).
- Set err to _cartesia_sse_request(...).
- If err:
-   Set Tuple to tts_sandbox_chunks(...).
-   If fallback_err:

**Calls →**
1. `features.ai_voice_cartesia.str`
2. `features.ai_voice_cartesia.bytearray`
3. `pending.extend`
4. `features.ai_voice_cartesia._emit_pcm_chunks`
5. `features.ai_voice_cartesia._cartesia_sse_request`
6. `features.ai_voice_cartesia.tts_sandbox_chunks`
7. `features.ai_voice_cartesia.emit_chunk`
8. `features.ai_voice_cartesia.emit_chunk`
9. `base64.b64encode`
10. `features.ai_voice_cartesia.bytes`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_run_sandbox_tts`

### `tts_mulaw_stream` (line 241)

**Pseudocode:**
- Set pending to bytearray(...).
- Set err to _cartesia_sse_request(...).
- If err:
-   Set Tuple to tts_mulaw_chunks(...).
-   If fallback_err:
-     Return IfExp.
-   For each chunk in chunks:
-     Call emit_chunk(...).

**Calls →**
1. `features.ai_voice_cartesia.bytearray`
2. `pending.extend`
3. `features.ai_voice_cartesia._emit_pcm_chunks`
4. `features.ai_voice_cartesia._cartesia_sse_request`
5. `features.ai_voice_cartesia.tts_mulaw_chunks`
6. `features.ai_voice_cartesia.emit_chunk`
7. `features.ai_voice_cartesia.emit_chunk`
8. `base64.b64encode`
9. `features.ai_voice_cartesia.bytes`

**Called by ←**
- `fn:features/ai_voice_runtime.py:_queue_speech`
