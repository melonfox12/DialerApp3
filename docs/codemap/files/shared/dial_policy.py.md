# `shared/dial_policy.py`

**Purpose:** Dial and CRM queue policy: who may be dialed, caps, repair, pool order, and live contact.

## Functions
### `normalize_phone` (line 54)

**Pseudocode:**
- Set text to str(...).strip(...).
- Set digits to ''.join(...).
- If a boolean condition:
-   Return '+' op digits.
- If len(...) compared to ...:
-   Return '+1' op digits.
- If a boolean condition:
-   Return '+' op digits.

**Calls →**
1. `shared.dial_policy.str`
2. `char.isdigit`
3. `text.startswith`
4. `shared.dial_policy.len`
5. `shared.dial_policy.len`
6. `shared.dial_policy.len`
7. `digits.startswith`

**Called by ←**
- `fn:shared/dial_policy.py:contact_keys`

### `location_text` (line 66)

**Pseudocode:**
- Return str(...).strip(...).

**Calls →**
1. `shared.dial_policy.str`

**Called by ←**
- `fn:shared/dial_policy.py:contact_keys`
- `fn:shared/dial_policy.py:identity_key`

### `_folded` (line 70)

**Pseudocode:**
- Return ' '.join(...).casefold(...).

**Calls →**
1. `shared.dial_policy.str`

**Called by ←**
- `fn:shared/dial_policy.py:contact_keys`
- `fn:shared/dial_policy.py:identity_key`

### `is_connected_call_log_entry` (line 74)
_True when the agent was bridged to the prospect on this dial (picked up)._

**Pseudocode:**
- Set connected to entry.get(...).
- If isinstance(...):
-   Return connected.
- Set answered to str(...).
- If answered compared to ...:
-   Return False.
- Return answered compared to ....

**Calls →**
1. `entry.get`
2. `shared.dial_policy.isinstance`
3. `shared.dial_policy.str`
4. `entry.get`

**Called by ←**
- `fn:features/performance.py:is_connected_record`
- `fn:shared/dial_policy.py:apply_total_dials_callback_status`
- `fn:shared/dial_policy.py:lead_has_live_contact`

### `lead_has_live_contact` (line 85)
_Transcript text or any connected call_log row counts as live contact._

**Pseudocode:**
- For each segment in a boolean condition:
-   If str(...).strip(...):
-     Return True.
- For each entry in a boolean condition:
-   If is_connected_call_log_entry(...):
-     Return True.
- Return False.

**Calls →**
1. `lead.get`
2. `shared.dial_policy.str`
3. `segment.get`
4. `lead.get`
5. `shared.dial_policy.is_connected_call_log_entry`

**Called by ←**
- `fn:features/prospects.py:enforce_dial_caps`
- `fn:shared/dial_policy.py:apply_dial_cap_to_lead`
- `fn:shared/dial_policy.py:repair_dial_status_for_lead`

### `total_dial_count` (line 96)
_Rows on Total dials: one per call_log entry._

**Pseudocode:**
- Return len(...).

**Calls →**
1. `shared.dial_policy.len`
2. `lead.get`

**Called by ←**
- `fn:shared/dial_policy.py:dial_cap_reached`

### `dial_entry_calendar_date` (line 104)

**Pseudocode:**
- Set item to a boolean condition.
- For each key in Tuple:
-   Set text to str(...).
-   If len(...) compared to ...:
-     Return text[...].
- Return ''.

**Calls →**
1. `shared.dial_policy.str`
2. `item.get`
3. `shared.dial_policy.len`

**Called by ←**
- `fn:shared/dial_policy.py:lead_has_dial_on_date`

### `dial_entry_local_calendar_dates` (line 113)
_Local calendar dates for a dial row (matches Total dials “today” for Eastern ops)._

**Pseudocode:**
- Set dates to set(...).
- Set zone to ZoneInfo(...).
- Set item to a boolean condition.
- For each key in Tuple:
-   Set text to str(...).strip(...).
-   If text:
-   Set parsed to text.replace(...).
-   Try:

**Calls →**
1. `shared.dial_policy.set`
2. `shared.dial_policy.ZoneInfo`
3. `shared.dial_policy.str`
4. `item.get`
5. `text.replace`
6. `datetime.datetime.fromisoformat`
7. `moment.replace`
8. `dates.add`
9. `moment.astimezone`
10. `shared.dial_policy.len`
11. `dates.add`

**Called by ←**
- `fn:shared/dial_policy.py:lead_has_dial_on_date`
- `fn:shared/dial_policy.py:lead_ids_with_dial_on_local_date`

### `lead_created_on_date` (line 136)

**Pseudocode:**
- Return str(...).startswith(...).

**Calls →**
1. `shared.dial_policy.str`
2. `shared.dial_policy.str`

### `lead_has_dial_on_date` (line 140)

**Pseudocode:**
- Set prefix to str(...).
- If prefix:
-   Return False.
- For each entry in a boolean condition:
-   If a boolean condition:
-     Return True.
- If a boolean condition:
-   Set stamps to sorted(...).

**Calls →**
1. `shared.dial_policy.str`
2. `shared.dial_policy.dial_entry_local_calendar_dates`
3. `shared.dial_policy.dial_entry_calendar_date`
4. `shared.dial_policy.sorted`
5. `line.get`
6. `line.get`
7. `shared.dial_policy.dial_entry_local_calendar_dates`
8. `shared.dial_policy.str`
9. `row.get`
10. `shared.dial_policy.isinstance`
11. `row.get`
12. `shared.dial_policy.dial_entry_local_calendar_dates`
13. `shared.dial_policy.dial_entry_calendar_date`

### `lead_ids_with_dial_on_local_date` (line 167)
_Prospect ids with any Total dials row on date_iso (live log, archive, transcript stub)._

**Pseudocode:**
- Set target to str(...).
- If target:
-   Return set(...).
- Set ids to set(...).
- For each record in collect_active_dial_records(...):
-   Set entry to a boolean condition.
-   If target compared to ...:
-   Set lead_id to str(...).strip(...).

**Calls →**
1. `shared.dial_policy.str`
2. `shared.dial_policy.set`
3. `shared.dial_policy.set`
4. `shared.dial_policy.collect_active_dial_records`
5. `record.get`
6. `shared.dial_policy.dial_entry_local_calendar_dates`
7. `shared.dial_policy.str`
8. `record.get`
9. `ids.add`

**Called by ←**
- `fn:features/prospects.py:migrate_nov5_2026_static_callbacks`

### `apply_static_callback_status` (line 185)
_Callback with no timer — dial pool + pipeline Dialed (ready)._

**Pseudocode:**
- Set moment to a boolean condition.isoformat(...).
- Set previous to canonical_status(...).
- If a boolean condition:
-   If previous compared to ...:
-     Call lead.setdefault(...).append(...).
-   Set lead[...] to 'dialed'.
-   Set lead[...] to None.
-   Return True.

**Calls →**
1. `shared.infra.utc_now`
2. `shared.vocabulary.canonical_status`
3. `lead.get`
4. `lead.get`
5. `lead.setdefault`

**Called by ←**
- `fn:features/prospects.py:migrate_nov5_2026_static_callbacks`

### `apply_total_dials_callback_status` (line 204)
_After a Total dials row is saved, set Callback (2h) unless the prospect has an explicit disposition._

**Pseudocode:**
- Set moment to a boolean condition.replace(...).
- Set status to canonical_status(...).
- If a boolean condition:
-   Return False.
- If a boolean condition:
-   Return False.
- If status compared to ...:
-   Set due to callback_due(...).

**Calls →**
1. `shared.infra.utc_now`
2. `shared.vocabulary.canonical_status`
3. `lead.get`
4. `shared.dial_policy.is_connected_call_log_entry`
5. `shared.dial_policy.callback_due`

**Called by ←**
- `fn:features/prospects.py:append_call_log`
- `fn:features/prospects.py:repair_total_dials_callbacks`

### `dial_cap_reached` (line 223)

**Pseudocode:**
- Return total_dial_count(...) compared to ....

**Calls →**
1. `shared.dial_policy.total_dial_count`

**Called by ←**
- `fn:features/prospects.py:enforce_dial_caps`
- `fn:shared/dial_policy.py:apply_dial_cap_to_lead`
- `fn:shared/dial_policy.py:repair_dial_status_for_lead`

### `apply_dial_cap_to_lead` (line 227)
_Mark closed after enough dials with no live contact. Returns True when changed._

**Pseudocode:**
- If dial_cap_reached(...):
-   Return False.
- If lead_has_live_contact(...):
-   Return False.
- If canonical_status(...) compared to ...:
-   Return False.
- Set lead[...] to 'closed'.
- Set lead[...] to None.

**Calls →**
1. `shared.dial_policy.dial_cap_reached`
2. `shared.dial_policy.lead_has_live_contact`
3. `shared.vocabulary.canonical_status`
4. `lead.get`

**Called by ←**
- `fn:features/prospects.py:append_call_log`

### `repair_dial_status_for_lead` (line 240)
_Fix prospects marked closed by the dial cap when the cap no longer applies._

**Pseudocode:**
- Set status to canonical_status(...).
- Set has_live to lead_has_live_contact(...).
- Set at_cap to dial_cap_reached(...).
- If status compared to ...:
-   Return None.
- If has_live:
-   Return None.
- If at_cap:

**Calls →**
1. `shared.vocabulary.canonical_status`
2. `lead.get`
3. `shared.dial_policy.lead_has_live_contact`
4. `shared.dial_policy.dial_cap_reached`

**Called by ←**
- `fn:features/prospects.py:repair_dial_statuses`

### `is_never_dial_status` (line 254)

**Pseudocode:**
- Return canonical_status(...) compared to ....

**Calls →**
1. `shared.vocabulary.canonical_status`

**Called by ←**
- `fn:features/_dialer/calls.py:_dialable_lead`
- `fn:shared/dial_policy.py:manual_lead_blocked`

### `resolve_pool_status` (line 258)

**Pseudocode:**
- Set status to canonical_status(...).
- Return IfExp.

**Calls →**
1. `shared.vocabulary.canonical_status`

**Called by ←**
- `fn:features/_dialer/calls.py:_pool_leads`
- `fn:features/_dialer/projection.py:crm_catalog`
- `fn:features/_dialer/projection.py:public_state`
- `fn:shared/dial_policy.py:leads_for_timezone_counts`
- `fn:shared/dial_policy.py:matches_dial_pool`
- `fn:shared/dial_policy.py:pool_leads`

### `unique_business_types` (line 263)
_Distinct non-empty category values from CRM rows, sorted for UI._

**Pseudocode:**
- Set seen to a dict.
- For each lead in a boolean condition:
-   Set text to str(...).strip(...).
-   If text:
-   Set folded to text.casefold(...).
-   If folded compared to ...:
-     Set seen[...] to text.
- Return sorted(...).

**Calls →**
1. `shared.dial_policy.str`
2. `text.casefold`
3. `shared.dial_policy.sorted`
4. `seen.values`
5. `value.casefold`

**Called by ←**
- `fn:features/_dialer/projection.py:crm_catalog`

### `lead_matches_dial_business_type` (line 276)
_True when the prospect's industry matches the dialer filter (case-insensitive)._

**Pseudocode:**
- If selected:
-   Return True.
- Set text to str(...).strip(...).casefold(...).
- Set target to str(...).strip(...).casefold(...).
- Return a boolean condition.

**Calls →**
1. `shared.dial_policy.str`
2. `shared.dial_policy.str`
3. `shared.dial_policy.bool`

**Called by ←**
- `fn:shared/dial_policy.py:leads_for_timezone_counts`
- `fn:shared/dial_policy.py:pool_leads`

### `dial_times` (line 285)

**Pseudocode:**
- Set log to a boolean condition.
- If log:
-   Return ListComp.
- Return ListComp.

**Calls →**
1. `lead.get`
2. `item.get`
3. `item.get`
4. `line.get`
5. `lead.get`

**Called by ←**
- `fn:shared/dial_policy.py:callback_sync_plan`
- `fn:shared/dial_policy.py:dial_windows`

### `contact_keys` (line 292)
_Phone and person keys used to dedupe the auto-dial pool._

**Pseudocode:**
- Set keys to set(...).
- Set phone to normalize_phone(...).
- If phone:
-   Call keys.add(...).
- Set name to _folded(...).
- Set business to _folded(...).
- Set city to _folded(...).
- Set state_name to _folded(...).

**Calls →**
1. `shared.dial_policy.set`
2. `shared.dial_policy.normalize_phone`
3. `lead.get`
4. `keys.add`
5. `shared.dial_policy._folded`
6. `lead.get`
7. `shared.dial_policy._folded`
8. `lead.get`
9. `shared.dial_policy._folded`
10. `shared.dial_policy.location_text`
11. `shared.dial_policy._folded`
12. `shared.dial_policy.location_text`
13. `keys.add`

**Called by ←**
- `fn:features/_dialer/calls.py:_contact_keys`
- `fn:shared/dial_policy.py:manual_lead_blocked`
- `fn:shared/dial_policy.py:off_limits_contact_keys`
- `fn:shared/dial_policy.py:pool_leads`

### `identity_key` (line 307)
_Name plus location for callback sync between duplicate imports._

**Pseudocode:**
- Set name to _folded(...).
- If name:
-   Return None.
- Set city to _folded(...).
- Set state_name to _folded(...).
- If a boolean condition:
-   Set place to Tuple.
- Else:

**Calls →**
1. `shared.dial_policy._folded`
2. `lead.get`
3. `shared.dial_policy._folded`
4. `shared.dial_policy.location_text`
5. `shared.dial_policy._folded`
6. `shared.dial_policy.location_text`
7. `shared.dial_policy._folded`
8. `lead.get`

**Called by ←**
- `fn:shared/dial_policy.py:callback_sync_plan`

### `callback_due` (line 321)

**Pseudocode:**
- Try:
-   Set moment to datetime.fromisoformat(...).
- On <ast.Tuple object at 0x000001E0F8E18950>:
-   Return None.
- If moment.tzinfo compared to ...:
-   Set moment to moment.replace(...).
- Return moment.

**Calls →**
1. `datetime.datetime.fromisoformat`
2. `shared.dial_policy.str`
3. `lead.get`
4. `moment.replace`

**Called by ←**
- `fn:features/_dialer/calls.py:_callback_due`
- `fn:shared/dial_policy.py:apply_callback_timer_migration_to_lead`
- `fn:shared/dial_policy.py:apply_total_dials_callback_status`
- `fn:shared/dial_policy.py:callback_sync_plan`
- `fn:shared/dial_policy.py:is_dialable_callback`

### `is_dialable_callback` (line 331)
_Callback status with no timer or an elapsed timer — eligible for the New dial pool._

**Pseudocode:**
- If canonical_status(...) compared to ...:
-   Return False.
- Set moment to a boolean condition.
- Set due to callback_due(...).
- If due compared to ...:
-   Return True.
- Return due compared to ....

**Calls →**
1. `shared.vocabulary.canonical_status`
2. `lead.get`
3. `shared.infra.utc_now`
4. `shared.dial_policy.callback_due`

**Called by ←**
- `fn:shared/dial_policy.py:matches_ai_agent_dial`
- `fn:shared/dial_policy.py:matches_dial_pool`

### `is_agent_reserved` (line 342)

**Pseudocode:**
- Return canonical_status(...) compared to ....

**Calls →**
1. `shared.vocabulary.canonical_status`

**Called by ←**
- `fn:features/ai_agents.py:release_agent_pool`
- `fn:shared/dial_policy.py:agent_reservation_blocks_other_apps`
- `fn:shared/dial_policy.py:manual_lead_blocked`
- `fn:shared/dial_policy.py:pick_agent_pool_ids`

### `agent_reservation_blocks_other_apps` (line 346)
_True when a lead is locked to an AI agent and this caller may not change it._

**Pseudocode:**
- If is_agent_reserved(...):
-   Return False.
- If agent_id:
-   Set reserved_id to str(...).strip(...).
-   Return reserved_id compared to ....
- Return True.

**Calls →**
1. `shared.dial_policy.is_agent_reserved`
2. `shared.dial_policy.str`
3. `shared.dial_policy.str`

**Called by ←**
- `fn:features/ai_agents.py:assert_lead_mutable_by_user`
- `fn:features/ai_agents.py:finalize_agent_call`
- `fn:features/ai_voice_runtime.py:finish_session`
- `fn:features/prospects.py:agent_finalize_status`
- `fn:features/prospects.py:reserve_for_agent`
- `fn:features/prospects.py:set_status`

### `matches_ai_agent_dial` (line 356)
_AI agents dial only fresh New rows and static Dialed (callback elapsed or no timer)._

**Pseudocode:**
- Set moment to a boolean condition.
- Set status to canonical_status(...).
- If status compared to ...:
-   Return True.
- If status compared to ...:
-   Return True.
- If status compared to ...:
-   Return is_dialable_callback(...).

**Calls →**
1. `shared.infra.utc_now`
2. `shared.vocabulary.canonical_status`
3. `lead.get`
4. `shared.dial_policy.is_dialable_callback`

**Called by ←**
- `fn:shared/dial_policy.py:agent_dial_queue`

### `matches_dial_pool` (line 369)
_Whether a prospect belongs in the active dial-pool mode._

**Pseudocode:**
- Set moment to a boolean condition.
- Set status to canonical_status(...).
- If status compared to ...:
-   Return False.
- Set pool_status to resolve_pool_status(...).
- If pool_status compared to ...:
-   Return status compared to ....
- If pool_status compared to ...:

**Calls →**
1. `shared.infra.utc_now`
2. `shared.vocabulary.canonical_status`
3. `lead.get`
4. `shared.dial_policy.resolve_pool_status`
5. `shared.dial_policy.is_dialable_callback`

**Called by ←**
- `fn:shared/dial_policy.py:leads_for_timezone_counts`
- `fn:shared/dial_policy.py:off_limits_contact_keys`
- `fn:shared/dial_policy.py:pool_leads`

### `apply_callback_timer_migration_to_lead` (line 387)
_One-time per lead: shift open callbacks forward after the 48h → 2h policy change._

**Pseudocode:**
- If a boolean condition:
-   Return False.
- If lead.get(...):
-   Return False.
- Set due to callback_due(...).
- Set lead[...] to True.
- If due compared to ...:
-   Return False.

**Calls →**
1. `lead.get`
2. `lead.get`
3. `lead.get`
4. `shared.dial_policy.callback_due`
5. `new_due.isoformat`

**Called by ←**
- `fn:features/prospects.py:migrate_callback_timers_to_two_hours`

### `retry_wait_for_log_entry` (line 405)
_How long before this dial-log row allows the same prospect back in the auto pool._

**Pseudocode:**
- Set answered to str(...).
- If answered:
-   Return RETRY_AFTER.get(...).
- Return NO_PICKUP_CALLBACK.

**Calls →**
1. `shared.dial_policy.str`
2. `RETRY_AFTER.get`

**Called by ←**
- `fn:shared/dial_policy.py:dial_windows`

### `open_dial_lead_ids` (line 413)
_Prospects with a call_log row still in progress (dialed but not finished)._

**Pseudocode:**
- Set ids to set(...).
- For each lead in a boolean condition:
-   Set lead_id to lead.get(...).
-   If lead_id:
-   For each entry in a boolean condition:
-     Set started to str(...).strip(...).
-     Set ended to str(...).strip(...).
-     Set answered to str(...).strip(...).

**Calls →**
1. `shared.dial_policy.set`
2. `lead.get`
3. `lead.get`
4. `shared.dial_policy.str`
5. `entry.get`
6. `shared.dial_policy.str`
7. `entry.get`
8. `shared.dial_policy.str`
9. `entry.get`
10. `ids.add`

**Called by ←**
- `fn:features/_dialer/calls.py:_busy_lead_ids`

### `dial_windows` (line 430)

**Pseudocode:**
- Set log to a boolean condition.
- If log:
-   Return ListComp.
- Return ListComp.

**Calls →**
1. `lead.get`
2. `item.get`
3. `item.get`
4. `shared.dial_policy.retry_wait_for_log_entry`
5. `shared.dial_policy.dial_times`

**Called by ←**
- `fn:shared/dial_policy.py:dialed_recently`

### `dialed_recently` (line 440)

**Pseudocode:**
- Set moment_now to a boolean condition.
- For each Tuple in dial_windows(...):
-   Try:
-     Set moment to datetime.fromisoformat(...).
-   On <ast.Tuple object at 0x000001E0F8ECF490>:
-   If moment.tzinfo compared to ...:
-     Set moment to moment.replace(...).
-   If moment compared to ...:

**Calls →**
1. `shared.infra.utc_now`
2. `shared.dial_policy.dial_windows`
3. `datetime.datetime.fromisoformat`
4. `shared.dial_policy.str`
5. `moment.replace`

**Called by ←**
- `fn:features/_dialer/calls.py:_dialed_recently`
- `fn:shared/dial_policy.py:agent_dial_queue`
- `fn:shared/dial_policy.py:leads_for_timezone_counts`
- `fn:shared/dial_policy.py:off_limits_contact_keys`
- `fn:shared/dial_policy.py:pool_leads`

### `off_limits_contact_keys` (line 454)
_Contact keys for people who must not be auto-dialed right now._

**Pseudocode:**
- Set keys to set(...).
- For each lead in leads:
-   If a boolean condition:
-     Update keys with BitOr contact_keys(...).
- Return keys.

**Calls →**
1. `shared.dial_policy.set`
2. `shared.dial_policy.matches_dial_pool`
3. `shared.dial_policy.dialed_recently`
4. `shared.dial_policy.contact_keys`

**Called by ←**
- `fn:shared/dial_policy.py:pool_leads`

### `pool_leads` (line 467)
_Ordered, deduped prospects eligible for auto-dial in the active pool mode._

**Pseudocode:**
- Set moment to a boolean condition.
- Set pool_status to resolve_pool_status(...).
- Set off_limits to off_limits_contact_keys(...).
- Set indexed to ListComp.
- If selected_timezone:
-   Set zone to selected_timezone.
-   Set indexed to ListComp.
- If pool_status compared to ...:

**Calls →**
1. `shared.infra.utc_now`
2. `shared.dial_policy.resolve_pool_status`
3. `shared.dial_policy.off_limits_contact_keys`
4. `shared.dial_policy.enumerate`
5. `shared.dial_policy.matches_dial_pool`
6. `shared.dial_policy.dialed_recently`
7. `shared.dial_policy.contact_keys`
8. `shared.dial_policy.lead_matches_dial_business_type`
9. `lead.get`
10. `indexed.sort`
11. `indexed.sort`
12. `shared.dial_policy.bool`
13. `shared.dial_policy.set`
14. `shared.dial_policy.contact_keys`
15. `people.append`

**Called by ←**
- `fn:features/_dialer/calls.py:_pool_leads`
- `fn:shared/dial_policy.py:global_dialer_pool`

### `leads_for_timezone_counts` (line 513)
_Prospects that count toward timezone menu buckets for the active pool._

**Pseudocode:**
- Set moment to a boolean condition.
- Set pool_status to resolve_pool_status(...).
- Return ListComp.

**Calls →**
1. `shared.infra.utc_now`
2. `shared.dial_policy.resolve_pool_status`
3. `shared.dial_policy.matches_dial_pool`
4. `shared.dial_policy.dialed_recently`
5. `shared.dial_policy.lead_matches_dial_business_type`

**Called by ←**
- `fn:features/_dialer/projection.py:crm_catalog`

### `callback_sync_plan` (line 524)
_New prospects that should inherit an open callback from a matching Total dials row._

**Pseudocode:**
- Set sources to a dict.
- For each lead in a boolean condition:
-   If a boolean condition:
-   Set due to callback_due(...).
-   If due compared to ...:
-   Set remaining to due op now.
-   If a boolean condition:
- Set copies to a list.

**Calls →**
1. `lead.get`
2. `shared.dial_policy.dial_times`
3. `shared.dial_policy.callback_due`
4. `datetime.timedelta`
5. `shared.dial_policy.identity_key`
6. `sources.get`
7. `due.isoformat`
8. `lead.get`
9. `lead.get`
10. `shared.dial_policy.identity_key`
11. `sources.get`
12. `lead.get`
13. `copies.append`

### `manual_lead_blocked` (line 554)
_Whether a pinned manual dial target cannot be claimed._

**Pseudocode:**
- If a boolean condition:
-   Return True.
- Set keys to contact_keys(...).
- Return any(...).

**Calls →**
1. `lead.get`
2. `shared.dial_policy.is_never_dial_status`
3. `lead.get`
4. `shared.dial_policy.is_agent_reserved`
5. `shared.dial_policy.contact_keys`
6. `shared.dial_policy.any`
7. `shared.dial_policy.contact_keys`
8. `shared.dial_policy.is_never_dial_status`
9. `other.get`
10. `shared.dial_policy.is_agent_reserved`

**Called by ←**
- `fn:features/_dialer/calls.py:_claim_manual_lead`

### `global_dialer_pool` (line 572)
_Every prospect eligible for the manual auto-dial pool app-wide (main caller pool ordering)._

**Pseudocode:**
- Return pool_leads(...).

**Calls →**
1. `shared.dial_policy.pool_leads`

**Called by ←**
- `fn:features/_dialer/projection.py:crm_catalog`
- `fn:features/ai_agents.py:global_pool_snapshot`
- `fn:shared/dial_policy.py:pick_agent_pool_ids`

### `pick_agent_pool_ids` (line 591)
_Top N prospects from the global pool that are not already reserved elsewhere._

**Pseudocode:**
- Set ordered to global_dialer_pool(...).
- Set chosen to a list.
- For each lead in ordered:
-   If lead[...] compared to ...:
-   If is_agent_reserved(...):
-   Call chosen.append(...).
-   If len(...) compared to ...:
- Return chosen.

**Calls →**
1. `shared.dial_policy.global_dialer_pool`
2. `shared.dial_policy.set`
3. `shared.dial_policy.is_agent_reserved`
4. `chosen.append`
5. `shared.dial_policy.len`

**Called by ←**
- `fn:features/ai_agents.py:boot_agent_pool`

### `agent_dial_queue` (line 619)
_Ordered prospects in an agent seat pool that are dialable right now._

**Pseudocode:**
- Set moment to a boolean condition.
- Set by_id to DictComp.
- Set queue to a list.
- For each lead_id in a boolean condition:
-   Set lead to by_id.get(...).
-   If a boolean condition:
-   If matches_ai_agent_dial(...):
-   If dialed_recently(...):

**Calls →**
1. `shared.infra.utc_now`
2. `lead.get`
3. `by_id.get`
4. `shared.dial_policy.matches_ai_agent_dial`
5. `shared.dial_policy.dialed_recently`
6. `queue.append`

**Called by ←**
- `fn:features/ai_agents.py:agents_public_view`
- `fn:features/ai_agents.py:dialable_pool_for_agent`

### `apply_agent_reservation` (line 636)
_Mark a prospect as locked to one AI agent seat._

**Pseudocode:**
- Set lead[...] to str(...).strip(...).
- Set lead[...] to str(...).strip(...).
- Set lead[...] to AGENT_USE_STATUS.
- Set lead[...] to None.

**Calls →**
1. `shared.dial_policy.str`
2. `shared.dial_policy.str`

### `clear_agent_reservation_fields` (line 644)

**Pseudocode:**
- For each key in Tuple:
-   Call lead.pop(...).

**Calls →**
1. `lead.pop`

**Called by ←**
- `fn:features/prospects.py:agent_finalize_status`
