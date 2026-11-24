# `features/ai_voice_routes.py`

**Purpose:** HTTP surface for the Twilio media bridge (shared-secret auth).

## Routes
- `GET` `/api/ai-voice/bootstrap` → `get_ai_voice_bootstrap`
- `GET` `/api/ai-voice/stream-sync` → `get_ai_voice_stream_sync`
- `POST` `/api/ai-voice/stream-started` → `post_ai_voice_stream_started`
- `POST` `/api/ai-voice/stream-stopped` → `post_ai_voice_stream_stopped`
- `POST` `/api/ai-voice/inbound` → `post_ai_voice_inbound`

## Functions
### `_secret` (line 8)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `request.headers.get`
2. `request.headers.get`

**Called by ←**
- `fn:features/ai_voice_routes.py:_require_bridge`

### `_query` (line 12)

**Pseudocode:**
- Set query to urllib.parse.parse_qs(...).
- Return a boolean condition[...].

**Calls →**
1. `urllib.parse.parse.parse_qs`
2. `urllib.parse.parse.urlsplit`
3. `query.get`

**Called by ←**
- `fn:features/ai_voice_routes.py:get_ai_voice_bootstrap`
- `fn:features/ai_voice_routes.py:get_ai_voice_stream_sync`

### `_dialer_for_request` (line 17)

**Pseudocode:**
- Set accounts to a list.
- If runtime.local:
-   Call accounts.append(...).
- Call accounts.extend(...).
- For each account in accounts:
-   Set dialer to account.dialer.
-   With dialer.lock:
-     If a boolean condition:

**Calls →**
1. `accounts.append`
2. `accounts.extend`
3. `runtime.sessions.values`

**Called by ←**
- `fn:features/ai_voice_routes.py:get_ai_voice_bootstrap`
- `fn:features/ai_voice_routes.py:get_ai_voice_stream_sync`
- `fn:features/ai_voice_routes.py:post_ai_voice_inbound`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_started`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_stopped`

### `_require_bridge` (line 32)

**Pseudocode:**
- If ai_voice_runtime.bridge_secret_ok(...):
-   Call request.send_json(...).
-   Return False.
- Return True.

**Calls →**
1. `features.ai_voice_runtime.bridge_secret_ok`
2. `features.ai_voice_routes._secret`
3. `request.send_json`

**Called by ←**
- `fn:features/ai_voice_routes.py:get_ai_voice_bootstrap`
- `fn:features/ai_voice_routes.py:get_ai_voice_stream_sync`
- `fn:features/ai_voice_routes.py:post_ai_voice_inbound`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_started`
- `fn:features/ai_voice_routes.py:post_ai_voice_stream_stopped`

### `get_ai_voice_bootstrap` (line 39)

**Pseudocode:**
- Set session_id to a boolean condition.
- Set dialer to _dialer_for_request(...).
- If dialer compared to ...:
-   Call request.send_json(...).
-   Return nothing.
- If _require_bridge(...):
-   Return nothing.
- Set payload to ai_voice_runtime.bootstrap(...).

**Calls →**
1. `features.ai_voice_routes._query`
2. `features.ai_voice_routes._query`
3. `features.ai_voice_routes._dialer_for_request`
4. `request.send_json`
5. `features.ai_voice_routes._require_bridge`
6. `features.ai_voice_runtime.bootstrap`
7. `request.send_json`
8. `request.send_json`

### `get_ai_voice_stream_sync` (line 54)

**Pseudocode:**
- Set session_id to a boolean condition.
- Set dialer to _dialer_for_request(...).
- If dialer compared to ...:
-   Call request.send_json(...).
-   Return nothing.
- If _require_bridge(...):
-   Return nothing.
- Call request.send_json(...).

**Calls →**
1. `features.ai_voice_routes._query`
2. `features.ai_voice_routes._query`
3. `features.ai_voice_routes._dialer_for_request`
4. `request.send_json`
5. `features.ai_voice_routes._require_bridge`
6. `request.send_json`
7. `features.ai_voice_runtime.stream_sync`

### `post_ai_voice_stream_started` (line 65)

**Pseudocode:**
- Set session_id to str(...).strip(...).
- Set dialer to _dialer_for_request(...).
- If dialer compared to ...:
-   Call request.send_json(...).
-   Return nothing.
- If _require_bridge(...):
-   Return nothing.
- Call ai_voice_runtime.mark_stream_started(...).

**Calls →**
1. `features.ai_voice_routes.str`
2. `data.get`
3. `data.get`
4. `features.ai_voice_routes._dialer_for_request`
5. `request.send_json`
6. `features.ai_voice_routes._require_bridge`
7. `features.ai_voice_runtime.mark_stream_started`
8. `features.ai_voice_runtime.stream_sync`
9. `request.send_json`

### `post_ai_voice_inbound` (line 78)

**Pseudocode:**
- Set session_id to str(...).strip(...).
- Set dialer to _dialer_for_request(...).
- If dialer compared to ...:
-   Call request.send_json(...).
-   Return nothing.
- If _require_bridge(...):
-   Return nothing.
- Set payload to a boolean condition.

**Calls →**
1. `features.ai_voice_routes.str`
2. `data.get`
3. `data.get`
4. `features.ai_voice_routes._dialer_for_request`
5. `request.send_json`
6. `features.ai_voice_routes._require_bridge`
7. `data.get`
8. `features.ai_voice_inbound.ingest_mulaw`
9. `data.get`
10. `features.ai_voice_inbound.ingest_mulaw`
11. `request.send_json`

### `post_ai_voice_stream_stopped` (line 95)

**Pseudocode:**
- Set session_id to str(...).strip(...).
- Set dialer to _dialer_for_request(...).
- If dialer compared to ...:
-   Call request.send_json(...).
-   Return nothing.
- If _require_bridge(...):
-   Return nothing.
- Call ai_voice_runtime.end_session(...).

**Calls →**
1. `features.ai_voice_routes.str`
2. `data.get`
3. `data.get`
4. `features.ai_voice_routes._dialer_for_request`
5. `request.send_json`
6. `features.ai_voice_routes._require_bridge`
7. `features.ai_voice_runtime.end_session`
8. `request.send_json`
