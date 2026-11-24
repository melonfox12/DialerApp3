# `features/performance.py`

**Purpose:** Performance page numbers. Pure functions over prospects, sessions and a clock: no storage, HTTP or I/O.

## Functions
### `is_connected_record` (line 53)
_A connect is a dial where the agent was bridged to the prospect (picked up)._

**Pseudocode:**
- Return is_connected_call_log_entry(...).

**Calls →**
1. `shared.dial_policy.is_connected_call_log_entry`

**Called by ←**
- `fn:features/performance.py:live_connect_for_metrics`

### `parse_moment` (line 58)

**Pseudocode:**
- Try:
-   Set moment to datetime.fromisoformat(...).
- On <ast.Name object at 0x00000242BC166D10>:
-   Return None.
- If moment.tzinfo compared to ...:
-   Set moment to moment.replace(...).
- Return moment.

**Calls →**
1. `datetime.datetime.fromisoformat`
2. `features.performance.str`
3. `moment.replace`

**Called by ←**
- `fn:features/performance.py:call_duration_seconds`
- `fn:features/performance.py:dial_moment`
- `fn:features/performance.py:latest_into_booked`
- `fn:features/performance.py:segments_for_dial`
- `fn:features/performance.py:status_history_for`
- `fn:features/performance.py:transcript_talk_from_segments`

### `local_zone` (line 68)
_The browser's IANA zone, or UTC when it is missing or unknown._

**Pseudocode:**
- Try:
-   Return ZoneInfo(...).
- On <ast.Tuple object at 0x00000242BC167790>:
-   Return timezone.utc.

**Calls →**
1. `zoneinfo.ZoneInfo`
2. `features.performance.str`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `rate` (line 76)
_A 0 to 1 ratio, or None when there is nothing to divide by._

**Pseudocode:**
- If denominator:
-   Return None.
- Return numerator op denominator.

**Called by ←**
- `fn:features/performance.py:funnel_rates`

### `format_funnel_percent` (line 83)
_Whole numbers above 10%, one decimal below, dash when unknown._

**Pseudocode:**
- If a boolean condition:
-   Return '—'.
- Set percent to value op 100.
- If percent compared to ...:
-   Return JoinedStr.
- Return JoinedStr.

**Calls →**
1. `features.performance.isinstance`
2. `features.performance.float`
3. `features.performance.float`
4. `features.performance.float`
5. `features.performance.round`

### `call_duration_seconds` (line 93)
_Connected talk time for one call_log row (pickup through hangup)._

**Pseudocode:**
- Set seconds to entry.get(...).
- If a boolean condition:
-   Return int(...).
- Set start to parse_moment(...).
- Set end to parse_moment(...).
- If a boolean condition:
-   Return int(...).
- Return 0.

**Calls →**
1. `entry.get`
2. `features.performance.isinstance`
3. `features.performance.isinstance`
4. `features.performance.int`
5. `features.performance.parse_moment`
6. `entry.get`
7. `features.performance.parse_moment`
8. `entry.get`
9. `features.performance.int`

**Called by ←**
- `fn:features/performance.py:call_records`

### `dial_moment` (line 105)
_When the dial counts for Total dials and Performance windows (ended, else started)._

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `features.performance.parse_moment`
2. `entry.get`
3. `features.performance.parse_moment`
4. `entry.get`

**Called by ←**
- `fn:features/performance.py:call_records`

### `segments_for_dial` (line 110)
_Transcript lines on the lead that fall within this call_log row's time window._

**Pseudocode:**
- Set start to parse_moment(...).
- If start compared to ...:
-   Return a list.
- Set end to parse_moment(...).
- Set slack to timedelta(...).
- Set matched to a list.
- For each segment in a boolean condition:
-   Set moment to parse_moment(...).

**Calls →**
1. `features.performance.parse_moment`
2. `entry.get`
3. `features.performance.parse_moment`
4. `entry.get`
5. `datetime.timedelta`
6. `lead.get`
7. `features.performance.parse_moment`
8. `segment.get`
9. `matched.append`
10. `matched.append`

**Called by ←**
- `fn:features/performance.py:call_records`
- `fn:features/performance.py:effective_transcript_lines`

### `transcript_talk_from_segments` (line 130)
_Talk span from first to last transcript timestamp on this dial._

**Pseudocode:**
- Set moments to ListComp.
- Set moments to ListComp.
- If len(...) compared to ...:
-   Return 0.
- Return max(...).

**Calls →**
1. `features.performance.parse_moment`
2. `item.get`
3. `features.performance.len`
4. `features.performance.max`
5. `features.performance.int`
6. `features.performance.max`
7. `features.performance.min`

**Called by ←**
- `fn:features/performance.py:call_records`

### `effective_transcript_lines` (line 139)

**Pseudocode:**
- Set stored to entry.get(...).
- Set count to IfExp.
- Set segments to segments_for_dial(...).
- Return max(...).

**Calls →**
1. `entry.get`
2. `features.performance.isinstance`
3. `features.performance.isinstance`
4. `features.performance.int`
5. `features.performance.segments_for_dial`
6. `features.performance.max`
7. `features.performance.len`

**Called by ←**
- `fn:features/performance.py:call_records`

### `live_connect_for_metrics` (line 146)
_Same intent as Total dials: live connect or a transcribed conversation._

**Pseudocode:**
- If is_connected_record(...):
-   Return True.
- If transcript_lines compared to ...:
-   Return False.
- Set answered to str(...).
- If a boolean condition:
-   Return False.
- Return True.

**Calls →**
1. `features.performance.is_connected_record`
2. `features.performance.str`
3. `entry.get`

**Called by ←**
- `fn:features/performance.py:call_records`

### `call_records` (line 158)

**Pseudocode:**
- Set records to a list.
- For each lead in leads:
-   For each entry in a boolean condition:
-     If entry.get(...) compared to ...:
-     Set at to dial_moment(...).
-     If at compared to ...:
-     Set segments to segments_for_dial(...).
-     Set transcript_lines to effective_transcript_lines(...).

**Calls →**
1. `lead.get`
2. `entry.get`
3. `features.performance.dial_moment`
4. `features.performance.segments_for_dial`
5. `features.performance.effective_transcript_lines`
6. `features.performance.live_connect_for_metrics`
7. `features.performance.transcript_talk_from_segments`
8. `features.performance.call_duration_seconds`
9. `entry.get`
10. `records.append`
11. `lead.get`
12. `features.performance.max`
13. `entry.get`
14. `records.sort`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `is_talk_time` (line 186)

**Pseudocode:**
- Return a boolean condition.

**Called by ←**
- `fn:features/performance.py:window_counts`

### `is_conversation` (line 190)
_Any dial in the period with a transcript (call_log count or lead segments), not voicemail._

**Pseudocode:**
- If record.get(...) compared to ...:
-   Return False.
- Return str(...) compared to ....

**Calls →**
1. `record.get`
2. `features.performance.str`
3. `record.get`

**Called by ←**
- `fn:features/performance.py:build_performance`
- `fn:features/performance.py:trend_buckets`
- `fn:features/performance.py:window_counts`

### `leads_index` (line 197)

**Pseudocode:**
- Return DictComp.

**Calls →**
1. `features.performance.str`
2. `lead.get`
3. `lead.get`

**Called by ←**
- `fn:features/performance.py:trend_buckets`
- `fn:features/performance.py:window_counts`

### `is_booked_lead_dial` (line 201)
_Dial in range to a prospect whose CRM status is Booked (chart booked series)._

**Pseudocode:**
- Set lead to leads_by_id.get(...).
- If lead:
-   Return False.
- Return canonical_status(...) compared to ....

**Calls →**
1. `leads_by_id.get`
2. `features.performance.str`
3. `call.get`
4. `shared.vocabulary.canonical_status`
5. `lead.get`

**Called by ←**
- `fn:features/performance.py:trend_buckets`
- `fn:features/performance.py:window_counts`

### `transcript_talk_seconds` (line 209)
_Talk time on transcript dials (segment span or connected duration)._

**Pseudocode:**
- If record.get(...) compared to ...:
-   Return 0.
- If str(...) compared to ...:
-   Return 0.
- Return record[...].

**Calls →**
1. `record.get`
2. `features.performance.str`
3. `record.get`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `in_window` (line 218)

**Pseudocode:**
- Return a boolean condition.

**Called by ←**
- `fn:features/performance.py:build_performance`
- `fn:features/performance.py:trend_buckets`
- `fn:features/performance.py:window_counts`

### `status_history_for` (line 222)
_Stored history plus a single estimated into-booked row when needed._

**Pseudocode:**
- Set history to ListComp.
- If any(...):
-   Return history.
- If canonical_status(...) compared to ...:
-   Return history.
- Set at to parse_moment(...).
- If a boolean condition:
-   Set lead_calls to a boolean condition.

**Calls →**
1. `features.performance.dict`
2. `lead.get`
3. `features.performance.isinstance`
4. `features.performance.any`
5. `item.get`
6. `shared.vocabulary.canonical_status`
7. `lead.get`
8. `features.performance.parse_moment`
9. `lead.get`
10. `calls_by_lead.get`
11. `lead.get`
12. `features.performance.max`
13. `at.isoformat`

**Called by ←**
- `fn:features/performance.py:active_booking_moment`

### `latest_into_booked` (line 244)

**Pseudocode:**
- Set latest to None.
- For each entry in history:
-   If entry.get(...) compared to ...:
-   Set at to parse_moment(...).
-   If at compared to ...:
-   If a boolean condition:
-     Set latest to a dict.
- Return latest.

**Calls →**
1. `entry.get`
2. `features.performance.parse_moment`
3. `entry.get`
4. `features.performance.bool`
5. `entry.get`

**Called by ←**
- `fn:features/performance.py:active_booking_moment`

### `active_booking_moment` (line 257)
_When this prospect counts as booked, or None if they are not Booked now._

**Pseudocode:**
- If canonical_status(...) compared to ...:
-   Return None.
- Return latest_into_booked(...).

**Calls →**
1. `shared.vocabulary.canonical_status`
2. `lead.get`
3. `features.performance.latest_into_booked`
4. `features.performance.status_history_for`

**Called by ←**
- `fn:features/performance.py:count_booked_from_history`

### `count_booked_in_pipeline` (line 264)
_Prospects whose CRM status is Booked — the pipeline view._

**Pseudocode:**
- Return sum(...).

**Calls →**
1. `features.performance.sum`
2. `shared.vocabulary.canonical_status`
3. `lead.get`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `count_booked_from_history` (line 269)
_Booked prospects using the same active-booking rule as Performance._

**Pseudocode:**
- Return sum(...).

**Calls →**
1. `features.performance.sum`
2. `features.performance.active_booking_moment`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `range_windows` (line 274)
_Day = rolling last ``DAY_RANGE_HOURS``; week/month = rolling windows ending at ``now``._

**Pseudocode:**
- If range_key compared to ...:
-   Raise an error.
- Set end to now.astimezone(...).
- If range_key compared to ...:
-   Return Tuple.
- If range_key compared to ...:
-   Return Tuple.
- Return Tuple.

**Calls →**
1. `features.performance.ValueError`
2. `now.astimezone`
3. `datetime.timedelta`
4. `datetime.timedelta`
5. `datetime.timedelta`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `window_counts` (line 286)

**Pseudocode:**
- Set chosen to ListComp.
- Set connected to ListComp.
- Set leads_by_id to leads_index(...).
- Set booked to sum(...).
- Return a dict.

**Calls →**
1. `features.performance.in_window`
2. `features.performance.leads_index`
3. `features.performance.sum`
4. `features.performance.is_booked_lead_dial`
5. `features.performance.len`
6. `features.performance.len`
7. `features.performance.sum`
8. `features.performance.is_conversation`
9. `features.performance.sum`
10. `features.performance.is_talk_time`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `funnel_rates` (line 300)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `features.performance.rate`
2. `features.performance.rate`
3. `features.performance.rate`
4. `features.performance.rate`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `trend_buckets` (line 309)
_One bucket per hour (day) or per calendar day (week/month) from period start through end._

**Pseudocode:**
- Set chosen to ListComp.
- Set grain to IfExp.
- Set keys to a list.
- If grain compared to ...:
-   Set local_start to start.astimezone(...).replace(...).
-   Set local_end to end.astimezone(...).replace(...).
-   Set cursor to local_start.
-   While cursor compared to ...:

**Calls →**
1. `features.performance.in_window`
2. `start.astimezone`
3. `end.astimezone`
4. `keys.append`
5. `cursor.astimezone`
6. `datetime.timedelta`
7. `start.astimezone`
8. `end.astimezone`
9. `keys.append`
10. `datetime.timedelta`
11. `features.performance.leads_index`
12. `datetime.timedelta`
13. `datetime.timedelta`
14. `key.isoformat`
15. `key.astimezone`
16. `datetime.datetime.combine`
17. `datetime.datetime.combine`
18. `key.isoformat`
19. `features.performance.in_window`
20. `features.performance.min`
21. `features.performance.sum`
22. `features.performance.is_conversation`
23. `features.performance.sum`
24. `features.performance.is_booked_lead_dial`
25. `buckets.append`
26. `features.performance.len`

**Called by ←**
- `fn:features/performance.py:build_performance`

### `build_performance` (line 354)
_JSON-ready payload for the simplified Performance page._

**Pseudocode:**
- Set zone to local_zone(...).
- Set calls to call_records(...).
- Set calls_by_lead to a dict.
- For each call in calls:
-   Call calls_by_lead.setdefault(...).append(...).
- Set Tuple to range_windows(...).
- Set counts to window_counts(...).
- Set Tuple to trend_buckets(...).

**Calls →**
1. `features.performance.local_zone`
2. `features.performance.call_records`
3. `calls_by_lead.setdefault`
4. `features.performance.range_windows`
5. `features.performance.window_counts`
6. `features.performance.trend_buckets`
7. `now.astimezone`
8. `features.performance.in_window`
9. `features.performance.sum`
10. `features.performance.is_conversation`
11. `features.performance.sum`
12. `features.performance.transcript_talk_seconds`
13. `features.performance.any`
14. `features.performance.getattr`
15. `features.performance.funnel_rates`
16. `start.isoformat`
17. `end.isoformat`
18. `features.performance.int`
19. `goal.get`
20. `features.performance.int`
21. `goal.get`
22. `goal.get`
23. `features.performance.count_booked_in_pipeline`
24. `features.performance.count_booked_from_history`

**Called by ←**
- `fn:features/metrics.py:get_performance`
