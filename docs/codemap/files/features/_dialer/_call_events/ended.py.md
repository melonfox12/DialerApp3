# `features/_dialer/_call_events/ended.py`

**Purpose:** Prospect and agent call endings.

## Functions
### `_call_ended` (line 11)

**Pseudocode:**
- Set log_entry to None.
- Set should_schedule_advance to False.
- Set should_top_up to False.
- Set others to a list.
- With state.lock:
-   If call[...] compared to ...:
-     Call _agent_call_ended(...).
-     Return nothing.

**Calls →**
1. `features._dialer._call_events.ended._agent_call_ended`
2. `call.get`
3. `call.get`
4. `call.get`
5. `state.in_flight.pop`
6. `call.get`
7. `call.get`
8. `features.ai_voice_runtime.end_session`
9. `call.get`
10. `features._dialer.live_transcript.commit_partials`
11. `call.get`
12. `call.get`
13. `state.in_flight.pop`
14. `call.get`
15. `features._dialer.calls._dial_record`
16. `features._dialer._call_events.ended.bool`
17. `call.get`
18. `state.in_flight.pop`
19. `features._dialer.rules.clear_stale_active`
20. `call.get`
21. `call.get`
22. `features._dialer._call_events.ended.int`
23. `features._dialer._call_events.ended.float`
24. `params.get`
25. `params.get`
26. `params.get`
27. `features._dialer.rules._bump`
28. `features._dialer.rules._bump`
29. `call.get`
30. `call.get`

**Called by ←**
- `fn:features/_dialer/call_events.py:handle_webhook`

### `_agent_call_ended` (line 121)

**Pseudocode:**
- With state.lock:
-   Set state.agent_ready to False.
-   If a boolean condition:
-     Set state.last_event to 'Computer audio disconnected; reconnecting…'.

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/call_events.py:handle_webhook`
