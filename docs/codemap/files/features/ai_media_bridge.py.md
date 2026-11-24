# `features/ai_media_bridge.py`

**Purpose:** Twilio Media Stream websocket bridge (inbound mulaw → dialer, outbound TTS ← dialer).

## Functions
### `api_json` (line 17)

**Pseudocode:**
- Set body to None.
- Set headers to a dict.
- If payload compared to ...:
-   Set body to json.dumps(...).encode(...).
- Set request to urllib.request.Request(...).
- With urllib.request.urlopen(...):
-   Return json.loads(...).

**Calls →**
1. `json.dumps`
2. `urllib.request.request.Request`
3. `app_url.rstrip`
4. `urllib.request.request.urlopen`
5. `json.loads`
6. `response.read`

**Called by ←**
- `fn:features/ai_media_bridge.py:poll_and_send`
- `fn:features/ai_media_bridge.py:twilio_handler`

### `poll_and_send` (line 27)

**Pseudocode:**
- While True:
-   Try:
-     Set data to api_json(...).
-   On <ast.Tuple object at 0x00000242BC217E10>:
-   If data.get(...):
-   For each chunk in a boolean condition:
-     If a boolean condition:

**Calls →**
1. `asyncio.sleep`
2. `features.ai_media_bridge.api_json`
3. `urllib.request.parse.quote`
4. `data.get`
5. `data.get`
6. `ws.send`
7. `json.dumps`

**Called by ←**
- `fn:features/ai_media_bridge.py:twilio_handler`

### `twilio_handler` (line 51)

**Pseudocode:**
- Set session_id to ''.
- Set stream_sid to ''.
- If a boolean condition:
-   Set query to urllib.parse.parse_qs(...).
-   Set session_id to a boolean condition[...].
- Set poll_task to None.
- Set inbound_batches to a list.
- Set inbound_task to None.

**Calls →**
1. `urllib.request.parse.parse_qs`
2. `path.split`
3. `query.get`
4. `asyncio.sleep`
5. `inbound_batches.clear`
6. `base64.b64encode`
7. `features.ai_media_bridge.api_json`
8. `json.loads`
9. `data.get`
10. `data.get`
11. `data.get`
12. `params.get`
13. `features.ai_media_bridge.api_json`
14. `asyncio.create_task`
15. `features.ai_media_bridge.poll_and_send`
16. `asyncio.create_task`
17. `features.ai_media_bridge.flush_inbound`
18. `data.get`
19. `inbound_batches.append`
20. `base64.b64decode`
21. `features.ai_media_bridge.api_json`
22. `poll_task.cancel`
23. `inbound_task.cancel`

**Called by ←**
- `fn:features/ai_media_bridge.py:serve_forever`

### `serve_forever` (line 111)

**Pseudocode:**
- If websockets compared to ...:
-   Raise an error.

**Calls →**
1. `features.ai_media_bridge.RuntimeError`
2. `features.ai_media_bridge.twilio_handler`
3. `websockets.serve`
4. `features.ai_media_bridge.print`
5. `asyncio.Future`

**Called by ←**
- `fn:features/ai_media_bridge.py:run_blocking`

### `run_blocking` (line 122)

**Pseudocode:**
- Call asyncio.run(...).

**Calls →**
1. `asyncio.run`
2. `features.ai_media_bridge.serve_forever`

### `run_in_thread` (line 126)

**Pseudocode:**
- Set thread to threading.Thread(...).
- Call thread.start(...).
- Return thread.

**Calls →**
1. `threading.Thread`
2. `thread.start`

**Called by ←**
- `fn:features/ai_media_bridge.py:maybe_start_embedded`

### `maybe_start_embedded` (line 137)
_Start bridge in-process when AI_BRIDGE_EMBEDDED=true and secret is set._

**Pseudocode:**
- Set values to read_env(...).
- If str(...).lower(...) compared to ...:
-   Return None.
- Set secret to str(...).strip(...).
- If secret:
-   Call print(...).
-   Return None.
- Set app_url to str(...).rstrip(...).

**Calls →**
1. `features.ai_media_bridge.read_env`
2. `features.ai_media_bridge.str`
3. `values.get`
4. `features.ai_media_bridge.str`
5. `values.get`
6. `features.ai_media_bridge.print`
7. `features.ai_media_bridge.str`
8. `values.get`
9. `features.ai_media_bridge.str`
10. `values.get`
11. `features.ai_media_bridge.int`
12. `values.get`
13. `features.ai_media_bridge.run_in_thread`
