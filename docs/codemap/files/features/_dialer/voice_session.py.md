# `features/_dialer/voice_session.py`

**Purpose:** Voice session profile: human browser desk vs AI line (Cartesia).

## Functions
### `voice_profile` (line 6)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `features._dialer.voice_session.getattr`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/_dialer/voice_session.py:attach_call_voice_defaults`
- `fn:features/_dialer/voice_session.py:is_ai_voice`

### `is_ai_voice` (line 10)

**Pseudocode:**
- Return voice_profile(...) compared to ....

**Calls →**
1. `features._dialer.voice_session.voice_profile`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_connect_prospect`
- `fn:features/_dialer/_call_events/pickup.py:_machine_result`
- `fn:features/_dialer/_call_events/transcript.py:_transcription_event`
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/_dialer/voice_session.py:slots_may_dial`
- `fn:features/_dialer/voice_session.py:uses_browser_agent_leg`
- `fn:features/ai_voice_runtime.py:on_prospect_text`
- `fn:features/ai_voice_runtime.py:start_call_session`

### `uses_browser_agent_leg` (line 14)
_Whether the session expects a Twilio browser / agent conference leg._

**Pseudocode:**
- Return is_ai_voice(...).

**Calls →**
1. `features._dialer.voice_session.is_ai_voice`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_client_voice`
- `fn:features/_dialer/call_events.py:handle_webhook`
- `fn:features/_dialer/queue.py:rejoin_browser_voice`
- `fn:features/_dialer/voice_session.py:requires_browser_voice`

### `slots_may_dial` (line 19)
_Whether parallel prospect slots may be filled._

**Pseudocode:**
- If a boolean condition:
-   Return False.
- If is_ai_voice(...):
-   Return bool(...).
- Return bool(...).

**Calls →**
1. `features._dialer.voice_session.is_ai_voice`
2. `features._dialer.voice_session.bool`
3. `features._dialer.voice_session.getattr`
4. `features._dialer.voice_session.bool`

**Called by ←**
- `fn:features/_dialer/queue.py:_pin_manual_dial`
- `fn:features/_dialer/queue.py:drop_prospect_call`
- `fn:features/_dialer/queue.py:pause`
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_dialer/slots.py:_check_calling_window`
- `fn:features/_dialer/slots.py:_place_prospect_call`
- `fn:features/_dialer/timing.py:_advance_queue`

### `begin_human_voice_session` (line 28)

**Pseudocode:**
- With state.lock:
-   Set state.voice_profile to VOICE_PROFILE_HUMAN_BROWSER.
-   Set state.ai_voice_armed to False.
-   Set state.agent_ready to False.

**Called by ←**
- `fn:features/_dialer/queue.py:start`

### `begin_ai_voice_session` (line 35)

**Pseudocode:**
- With state.lock:
-   Set state.voice_profile to VOICE_PROFILE_AI_CARTESIA.
-   Set state.ai_voice_armed to True.
-   Set state.agent_ready to True.
-   Set state.last_event to 'AI voice armed'.

**Called by ←**
- `fn:features/_dialer/queue.py:start`

### `reset_voice_session` (line 43)

**Pseudocode:**
- With state.lock:
-   Set state.voice_profile to VOICE_PROFILE_HUMAN_BROWSER.
-   Set state.ai_voice_armed to False.

**Called by ←**
- `fn:features/_dialer/queue.py:stop`

### `attach_call_voice_defaults` (line 49)

**Pseudocode:**
- Set call[...] to voice_profile(...).
- Call call.setdefault(...).
- Call call.setdefault(...).

**Calls →**
1. `features._dialer.voice_session.voice_profile`
2. `call.setdefault`
3. `call.setdefault`

**Called by ←**
- `fn:features/_dialer/calls.py:_new_call`

### `requires_browser_voice` (line 55)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `features._dialer.voice_session.uses_browser_agent_leg`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
