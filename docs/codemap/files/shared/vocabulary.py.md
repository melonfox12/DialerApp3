# `shared/vocabulary.py`

**Purpose:** Single definitions for statuses, dispositions, metrics, stages, timezones, and setting keys.

## Functions
### `resolve_dial_business_type` (line 64)
_Map API or UI text to a dial-pool industry filter. Empty string means no filter._

**Pseudocode:**
- Set text to str(...).strip(...).
- Set folded to text.casefold(...).
- If a boolean condition:
-   Return ''.
- Return text.

**Calls →**
1. `shared.vocabulary.str`
2. `text.casefold`

**Called by ←**
- `fn:features/_dialer/queue.py:set_pool_filters`

### `dial_business_type_label` (line 73)

**Pseudocode:**
- Set folded to str(...).strip(...).casefold(...).
- For each item in DIAL_BUSINESS_TYPE_OPTIONS:
-   If item[...].casefold(...) compared to ...:
-     Return item[...].
- Return str(...).strip(...).

**Calls →**
1. `shared.vocabulary.str`
2. `shared.vocabulary.str`

**Called by ←**
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_dialer/queue.py:start`

### `pipeline_wait_hours` (line 199)

**Pseudocode:**
- Return PIPELINE_WAIT_BY_KEY.get(...).

**Calls →**
1. `PIPELINE_WAIT_BY_KEY.get`
2. `shared.vocabulary.str`

### `pipeline_step_to_status` (line 203)
_CRM status for a prospect in this pipeline column (keys are stable; labels are UI)._

**Pseudocode:**
- Set k to str(...).strip(...).
- If k compared to ...:
-   Return 'dialed'.
- If k compared to ...:
-   Return 'contact_engaged'.
- Return 'qualified'.

**Calls →**
1. `shared.vocabulary.str`

**Called by ←**
- `fn:features/prospects.py:set_pipeline_step`

### `resolve_caller_id_group` (line 258)

**Pseudocode:**
- Set parsed to str(...).strip(...).lower(...).
- Return IfExp.

**Calls →**
1. `shared.vocabulary.str`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/_dialer/queue.py:set_caller_id_group`
- `fn:shared/vocabulary.py:caller_ids_for_group`

### `caller_ids_for_group` (line 263)

**Pseudocode:**
- Return list(...).

**Calls →**
1. `shared.vocabulary.list`
2. `shared.vocabulary.resolve_caller_id_group`

**Called by ←**
- `fn:features/_dialer/queue.py:set_caller_id_group`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/state.py:__init__`

### `parse_prospect_status` (line 352)
_Map API, CSV, or UI text to a STATUS_KEYS value. Returns None when it cannot._

**Pseudocode:**
- If value compared to ...:
-   Return None.
- Set text to str(...).strip(...).
- If text:
-   Return None.
- If text compared to ...:
-   Return text.
- If text compared to ...:

**Calls →**
1. `shared.vocabulary.str`
2. `text.casefold`
3. `CRM_STATUS_LABELS.items`
4. `label.casefold`
5. `LEGACY_STATUSES.get`

**Called by ←**
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/outcomes.py:update_status`
- `fn:features/_prospects/csv_import.py:build_manual_lead`
- `fn:features/prospects.py:agent_finalize_status`
- `fn:features/prospects.py:set_status`
- `fn:shared/vocabulary.py:canonical_status`

### `agent_reserved_name` (line 375)

**Pseudocode:**
- Set fields to a boolean condition.
- Set direct to str(...).strip(...).
- Return direct.

**Calls →**
1. `shared.vocabulary.str`
2. `fields.get`

**Called by ←**
- `fn:shared/vocabulary.py:agent_use_status_text`

### `agent_use_status_text` (line 381)
_CRM label while a prospect is locked to an AI agent seat._

**Pseudocode:**
- Set name to agent_reserved_name(...).
- If name:
-   Return JoinedStr.
- Return CRM_STATUS_LABELS.get(...).

**Calls →**
1. `shared.vocabulary.agent_reserved_name`
2. `CRM_STATUS_LABELS.get`

**Called by ←**
- `fn:features/ai_agents.py:assert_lead_mutable_by_user`
- `fn:features/prospects.py:agent_finalize_status`
- `fn:features/prospects.py:reserve_for_agent`
- `fn:features/prospects.py:set_status`

### `canonical_status` (line 389)
_The current status for a stored one. Missing or unknown labels read as new when possible._

**Pseudocode:**
- If status compared to ...:
-   Return 'new'.
- Set text to str(...).strip(...).
- If text:
-   Return 'new'.
- Set parsed to parse_prospect_status(...).
- If parsed compared to ...:
-   Return parsed.

**Calls →**
1. `shared.vocabulary.str`
2. `shared.vocabulary.parse_prospect_status`

**Called by ←**
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_prospects/csv_export.py:csv_bytes_for`
- `fn:features/_prospects/dial_archive.py:archive_record_from_csv_row`
- `fn:features/_prospects/dial_archive.py:archive_record_from_lead`
- `fn:features/_prospects/dials_csv_export.py:_row`
- `fn:features/performance.py:active_booking_moment`
- `fn:features/performance.py:count_booked_in_pipeline`
- `fn:features/performance.py:is_booked_lead_dial`
- `fn:features/performance.py:status_history_for`
- `fn:features/prospects.py:add_lead`
- `fn:features/prospects.py:agent_finalize_status`
- `fn:features/prospects.py:enforce_dial_caps`
- `fn:features/prospects.py:migrate_nov5_2026_static_callbacks`
- `fn:features/prospects.py:repair_total_dials_callbacks`
- `fn:features/prospects.py:reserve_for_agent`
- `fn:features/prospects.py:set_pipeline_step`
- `fn:features/prospects.py:set_status`
- `fn:features/prospects.py:snapshot`
- `fn:shared/dial_policy.py:apply_dial_cap_to_lead`
- `fn:shared/dial_policy.py:apply_static_callback_status`
- `fn:shared/dial_policy.py:apply_total_dials_callback_status`
- `fn:shared/dial_policy.py:is_agent_reserved`
- `fn:shared/dial_policy.py:is_dialable_callback`
- `fn:shared/dial_policy.py:is_never_dial_status`
- `fn:shared/dial_policy.py:matches_ai_agent_dial`
- `fn:shared/dial_policy.py:matches_dial_pool`
- `fn:shared/dial_policy.py:repair_dial_status_for_lead`
- `fn:shared/dial_policy.py:resolve_pool_status`

### `browser_vocabulary` (line 402)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `shared.vocabulary.dict`
2. `shared.vocabulary.list`
3. `shared.vocabulary.list`
4. `shared.vocabulary.dict`
5. `shared.vocabulary.list`
6. `shared.vocabulary.list`
7. `shared.vocabulary.dict`
8. `shared.vocabulary.dict`
9. `shared.vocabulary.dict`
10. `shared.vocabulary.dict`
11. `shared.vocabulary.list`
12. `shared.vocabulary.dict`
13. `shared.vocabulary.list`
14. `shared.vocabulary.list`
15. `shared.vocabulary.list`
16. `shared.vocabulary.dict`
17. `shared.vocabulary.dict`
18. `shared.vocabulary.list`
19. `shared.vocabulary.list`
20. `shared.vocabulary.dict`

**Called by ←**
- `fn:shared/vocabulary.py:vocabulary_json`

### `vocabulary_json` (line 447)

**Pseudocode:**
- Return json.dumps(...).replace(...).

**Calls →**
1. `json.dumps`
2. `shared.vocabulary.browser_vocabulary`

**Called by ←**
- `fn:_web/respond.py:send_app_page`
