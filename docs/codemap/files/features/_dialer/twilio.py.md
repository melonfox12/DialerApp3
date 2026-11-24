# `features/_dialer/twilio.py`

**Purpose:** Twilio REST, TwiML helpers, webhook signature, and the call-token index.

## Functions
### `twilio_request` (line 21)

**Pseudocode:**
- Set url to TWILIO_API.format(...) op path.
- If params:
-   Update url with Add '?' op urllib.parse.urlencode(...).
- Set body to IfExp.
- Set request to urllib.request.Request(...).
- Set auth to base64.b64encode(...).decode(...).
- Call request.add_header(...).
- If body compared to ...:

**Calls →**
1. `TWILIO_API.format`
2. `urllib.request.parse.quote`
3. `urllib.request.parse.urlencode`
4. `urllib.request.parse.urlencode`
5. `urllib.request.request.Request`
6. `base64.b64encode`
7. `request.add_header`
8. `request.add_header`
9. `urllib.request.request.urlopen`
10. `response.read`
11. `json.loads`
12. `json.loads`
13. `exc.read`
14. `payload.get`
15. `payload.get`
16. `features._dialer.twilio.str`
17. `features._dialer.twilio.str`
18. `features._dialer.twilio.TwilioError`
19. `features._dialer.twilio.TwilioError`

**Called by ←**
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/twilio.py:_api_key_accepted`
- `fn:features/_dialer/twilio.py:_call_is_live`
- `fn:features/_dialer/twilio.py:_hangup_call`
- `fn:features/_dialer/twilio.py:_point_voice_app`
- `fn:features/_dialer/twilio.py:_redirect_call`
- `fn:features/_dialer/twilio.py:_start_live_transcription`

### `escape_xml` (line 45)

**Pseudocode:**
- Return str(...).replace(...).replace(...).replace(...).replace(...).replace(...).

**Calls →**
1. `features._dialer.twilio.str`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_live_twiml`
- `fn:features/_dialer/call_events.py:handle_client_voice`
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/ai_voice_runtime.py:ai_stream_twiml`

### `waiting_twiml` (line 49)
_Stay silent on the answered line until Twilio decides a person is there._

**Pseudocode:**
- Return '<Response><Pause length="20"/></Response>'.

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`

### `__init__` (line 60)

**Pseudocode:**
- Set self._lock to threading.Lock(...).
- Set self._tokens to a dict.

**Calls →**
1. `threading.Lock`

### `register` (line 64)

**Pseudocode:**
- With self._lock:
-   Set self._tokens[...] to dialer.

### `forget` (line 68)

**Pseudocode:**
- With self._lock:
-   Call self._tokens.pop(...).

**Calls →**
1. `features._dialer.twilio.TokenIndex._tokens.pop`

### `lookup` (line 72)

**Pseudocode:**
- If token:
-   Return None.
- With self._lock:
-   Return self._tokens.get(...).

**Calls →**
1. `features._dialer.twilio.TokenIndex._tokens.get`

### `validate_webhook` (line 78)

**Pseudocode:**
- Set stored to a boolean condition.
- Set auth_token to stored.get(...).
- If a boolean condition:
-   Return False.
- Set signed to url.
- For each key in sorted(...):
-   Set values to params[...].
-   If isinstance(...):

**Calls →**
1. `state.read_values`
2. `stored.get`
3. `features._dialer.twilio.sorted`
4. `features._dialer.twilio.isinstance`
5. `features._dialer.twilio.sorted`
6. `features._dialer.twilio.str`
7. `hmac.new`
8. `auth_token.encode`
9. `signed.encode`
10. `base64.b64encode`
11. `hmac.compare_digest`

**Called by ←**
- `fn:features/dialer.py:validate_webhook`

### `_url` (line 94)

**Pseudocode:**
- Return JoinedStr.

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/_call_events/transcript.py:_resume_transcription`
- `fn:features/_dialer/_call_events/transcript.py:schedule_live_transcription`
- `fn:features/_dialer/call_events.py:handle_client_voice`
- `fn:features/_dialer/calls.py:_create_call`

### `_hangup_call` (line 97)

**Pseudocode:**
- Try:
-   Call twilio_request(...).
- On <ast.Tuple object at 0x00000242BC188D90>:
-   No-op.

**Calls →**
1. `features._dialer.twilio.twilio_request`
2. `urllib.request.parse.quote`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/calls.py:_expire_silent_call`
- `fn:features/ai_voice_runtime.py:_schedule_watchers`

### `_start_live_transcription` (line 104)
_Start another live transcript on a call that is still connected._

**Pseudocode:**
- If a boolean condition:
-   Return nothing.
- Call twilio_request(...).

**Calls →**
1. `features._dialer.twilio.twilio_request`
2. `urllib.request.parse.quote`

**Called by ←**
- `fn:features/_dialer/_call_events/transcript.py:_resume_transcription`
- `fn:features/_dialer/_call_events/transcript.py:schedule_live_transcription`

### `_call_is_live` (line 125)
_False only when Twilio confirms the call already ended. Any lookup problem counts as live._

**Pseudocode:**
- If call_uuid:
-   Return True.
- Try:
-   Set info to twilio_request(...).
- On <ast.Tuple object at 0x00000242BC292B10>:
-   Return True.
- Return str(...).lower(...) compared to ....

**Calls →**
1. `features._dialer.twilio.twilio_request`
2. `urllib.request.parse.quote`
3. `features._dialer.twilio.str`
4. `info.get`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`

### `_redirect_call` (line 136)
_Point an answered call at new TwiML once we know a person is on the line._

**Pseudocode:**
- If a boolean condition:
-   Return nothing.
- Try:
-   Call twilio_request(...).
- On <ast.Tuple object at 0x00000242BC2710D0>:
-   No-op.

**Calls →**
1. `features._dialer.twilio.twilio_request`
2. `urllib.request.parse.quote`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`

### `prepare_browser_voice` (line 147)
_Check the API key, then point the TwiML app at this dialer's voice URL._

**Pseudocode:**
- Set account to values[...].
- Set token to values[...].
- If _api_key_accepted(...):
-   Raise an error.
- Set voice_url to JoinedStr.
- Call _point_voice_app(...).

**Calls →**
1. `features._dialer.twilio._api_key_accepted`
2. `features._dialer.twilio.TwilioError`
3. `features._dialer.twilio._point_voice_app`

**Called by ←**
- `fn:features/_dialer/queue.py:start`

### `_api_key_accepted` (line 159)

**Pseudocode:**
- Try:
-   Call twilio_request(...).
- On <ast.Name object at 0x00000242BC26BD50>:
-   Set message to str(...).
-   If 'permissions' compared to ...:
-     Return True.
-   If 'Twilio error 401' compared to ...:
-     Return False.

**Calls →**
1. `features._dialer.twilio.twilio_request`
2. `features._dialer.twilio.str`
3. `message.lower`

**Called by ←**
- `fn:features/_dialer/twilio.py:prepare_browser_voice`

### `_point_voice_app` (line 172)

**Pseudocode:**
- Set path to '/Applications/' op urllib.parse.quote(...) op '.json'.
- Try:
-   Set app to twilio_request(...).
- On <ast.Name object at 0x00000242BC12E150>:
-   If 'Twilio error 404' compared to ...:
-     Raise an error.
-   Raise an error.
- Set current to str(...).rstrip(...).

**Calls →**
1. `urllib.request.parse.quote`
2. `features._dialer.twilio.twilio_request`
3. `features._dialer.twilio.str`
4. `features._dialer.twilio.TwilioError`
5. `features._dialer.twilio.str`
6. `app.get`
7. `features._dialer.twilio.str`
8. `app.get`
9. `features._dialer.twilio.twilio_request`
10. `state.record_activity`

**Called by ←**
- `fn:features/_dialer/twilio.py:prepare_browser_voice`

### `voice_access_token` (line 188)

**Pseudocode:**
- Call state.record_activity(...).
- Set values to state.read_values(...).
- Set required to Tuple.
- Set missing to ListComp.
- If missing:
-   Raise an error.
- Set token to AccessToken(...).
- Call token.add_grant(...).

**Calls →**
1. `state.record_activity`
2. `state.read_values`
3. `values.get`
4. `features._dialer.twilio.ValueError`
5. `twilio.jwt.access_token.AccessToken`
6. `token.add_grant`
7. `twilio.jwt.access_token.grants.VoiceGrant`
8. `token.to_jwt`

**Called by ←**
- `fn:features/dialer.py:voice_access_token`
