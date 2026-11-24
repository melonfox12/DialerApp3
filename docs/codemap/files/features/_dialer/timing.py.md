# `features/_dialer/timing.py`

**Purpose:** Auto-advance timer. Imports slots, not queue.

## Functions
### `_schedule_advance` (line 10)

**Pseudocode:**
- With state.lock:
-   Call rules.clear_stale_active(...).
-   If a boolean condition:
-     Return nothing.
-   If state.advance_timer:
-     Call state.advance_timer.cancel(...).
-   Set seconds to max(...).
-   Set state.advance_at to time.time(...) op seconds.

**Calls →**
1. `features._dialer.rules.clear_stale_active`
2. `state.advance_timer.cancel`
3. `features._dialer.timing.max`
4. `features._dialer.timing.float`
5. `state.settings.get`
6. `time.time`
7. `threading.Timer`
8. `state.advance_timer.start`

**Called by ←**
- `fn:features/_dialer/_call_events/ended.py:_call_ended`
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/queue.py:pass_next`
- `fn:features/_dialer/queue.py:pause`

### `_advance_queue` (line 25)

**Pseudocode:**
- With state.lock:
-   Set state.advance_timer to None.
-   Set state.advance_at to None.
-   Set state.advance_remaining to None.
-   Call rules.clear_stale_active(...).
-   Set prospect_lines to ListComp.
- If should_fill:
-   Call slots.fill_slots(...).

**Calls →**
1. `features._dialer.rules.clear_stale_active`
2. `state.in_flight.values`
3. `call.get`
4. `features._dialer.voice_session.slots_may_dial`
5. `features._dialer.timing.len`
6. `features._dialer.timing.len`
7. `features._dialer.slots.fill_slots`

### `advance_now` (line 43)

**Pseudocode:**
- With state.lock:
-   If a boolean condition:
-     Raise an error.
-   Call state.advance_timer.cancel(...).
-   Set state.advance_timer to None.
-   Set state.advance_at to None.
-   Set state.advance_remaining to None.
- Call slots.fill_slots(...).

**Calls →**
1. `features._dialer.timing.ValueError`
2. `state.advance_timer.cancel`
3. `features._dialer.slots.fill_slots`
4. `features._dialer.projection.public_state`

**Called by ←**
- `fn:features/dialer.py:advance_now`
