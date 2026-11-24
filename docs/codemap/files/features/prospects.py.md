# `features/prospects.py`

**Purpose:** Prospect rules shared by the local and Supabase backends.

## Routes
- `POST` `/api/leads` → `post_lead`
- `POST` `/api/leads/{id}/fields` → `post_fields`
- `POST` `/api/leads/{id}/pipeline` → `post_pipeline_step`
- `POST` `/api/pipeline/settings` → `post_save_pipeline_settings`
- `POST` `/api/import` → `post_import`
- `GET` `/api/export.csv` → `get_export`
- `DELETE` `/api/leads/{id}` → `delete_lead`

## Functions
### `__init__` (line 59)

**Pseudocode:**
- If client compared to ...:
-   Set self.backend to SupabaseBackend(...).
- Else:
-   Set self.backend to LocalBackend(...).
- Set self._pipeline_steps to merge_pipeline_steps(...).
- Set self._pipeline_step_keys to frozenset(...).
- Set self.pipeline_revision to 0.
- Call self.migrate_callback_timers_to_two_hours(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend`
2. `features._prospects.backend_local.LocalBackend`
3. `shared.pipeline_config.merge_pipeline_steps`
4. `features.prospects.frozenset`
5. `features.prospects.ProspectStore.migrate_callback_timers_to_two_hours`

### `set_pipeline_schema` (line 69)
_Replace active pipeline steps (full ordered list including Dialed + Contacted (engaged) (call_1))._

**Pseudocode:**
- Set steps to ListComp.
- If len(...) compared to ...:
-   Raise an error.
- If a boolean condition:
-   Raise an error.
- For each item in steps[...]:
-   Try:
-     Set wh to int(...).

**Calls →**
1. `features.prospects.dict`
2. `features.prospects.len`
3. `features.prospects.ValueError`
4. `features.prospects.ValueError`
5. `features.prospects.int`
6. `item.get`
7. `features.prospects.ValueError`
8. `features.prospects.frozenset`
9. `features.prospects.frozenset`
10. `features.prospects.dict`
11. `features.prospects.str`
12. `features.prospects.len`
13. `features.prospects.len`
14. `features.prospects.set`
15. `features.prospects.ValueError`
16. `features.prospects.frozenset`
17. `features.prospects.ProspectStore.backend.leads_locked`
18. `features.prospects.ProspectStore.backend.expire_locked`
19. `shared.pipeline_config.migrate_leads_pipeline_keys`
20. `features.prospects._copy_of`
21. `features.prospects.ProspectStore.backend.save_locked`
22. `features.prospects.len`
23. `features.prospects.dict`
24. `features.prospects.ProspectStore.backend.bump_revision`

**Called by ←**
- `fn:features/prospects.py:apply_pipeline_tail_from_settings`
- `fn:features/prospects.py:set_pipeline_tail`

### `pipeline_steps_for_catalog` (line 108)

**Pseudocode:**
- Return ListComp.

**Calls →**
1. `features.prospects.dict`

### `apply_pipeline_tail_from_settings` (line 111)
_Parse PIPELINE_CUSTOM_STEPS_JSON and merge with locked head; optionally remap CRM._

**Pseudocode:**
- Set Tuple to parse_custom_pipeline_steps_json(...).
- If err:
-   Raise an error.
- Set merged to merge_pipeline_steps(...).
- Return self.set_pipeline_schema(...).

**Calls →**
1. `shared.pipeline_config.parse_custom_pipeline_steps_json`
2. `features.prospects.ValueError`
3. `shared.pipeline_config.merge_pipeline_steps`
4. `features.prospects.ProspectStore.set_pipeline_schema`

**Called by ←**
- `fn:features/prospects.py:sync_pipeline_from_account_values`
- `fn:features/prospects.py:sync_pipeline_from_merged_values`

### `remap_pipeline_after_deletion` (line 119)
_After removing steps, move prospects off deleted keys (no extra validation)._

**Pseudocode:**
- Set new_keys to frozenset(...).
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set touched to migrate_leads_pipeline_keys(...).
-   For each lead_id in touched:
-     Set lead to _copy_of(...).
-     Call self.backend.save_locked(...).

**Calls →**
1. `features.prospects.frozenset`
2. `features.prospects.ProspectStore.backend.leads_locked`
3. `features.prospects.ProspectStore.backend.expire_locked`
4. `shared.pipeline_config.migrate_leads_pipeline_keys`
5. `features.prospects.frozenset`
6. `features.prospects._copy_of`
7. `features.prospects.ProspectStore.backend.save_locked`
8. `features.prospects.len`

### `sync_pipeline_from_account_values` (line 135)
_Load PIPELINE_CUSTOM_STEPS_JSON from merged env + account dict._

**Pseudocode:**
- Set raw to ''.
- If account_values:
-   Set raw to str(...).strip(...).
- Set prev to frozenset(...).
- Return self.apply_pipeline_tail_from_settings(...).

**Calls →**
1. `features.prospects.str`
2. `account_values.get`
3. `features.prospects.frozenset`
4. `features.prospects.ProspectStore.apply_pipeline_tail_from_settings`

### `sync_pipeline_from_merged_values` (line 143)
_Sync when settings merge changes; migrate if a custom step key was removed._

**Pseudocode:**
- Set raw_before to str(...).strip(...).
- Set raw_after to str(...).strip(...).
- If raw_before compared to ...:
-   Return 0.
- Set Tuple to parse_custom_pipeline_steps_json(...).
- If err_b:
-   Set custom_before to a list.
- Set Tuple to parse_custom_pipeline_steps_json(...).

**Calls →**
1. `features.prospects.str`
2. `features.prospects.str`
3. `shared.pipeline_config.parse_custom_pipeline_steps_json`
4. `shared.pipeline_config.parse_custom_pipeline_steps_json`
5. `features.prospects.ValueError`
6. `shared.pipeline_config.merge_pipeline_steps`
7. `shared.pipeline_config.merge_pipeline_steps`
8. `features.prospects.bool`
9. `features.prospects.ProspectStore.apply_pipeline_tail_from_settings`

### `set_pipeline_tail` (line 161)
_Replace configurable tail (after Contacted (engaged)). Dialed + call_1 stay fixed._

**Pseudocode:**
- Set Tuple to validate_pipeline_tail_payload(...).
- If err:
-   Raise an error.
- For each item in normalized:
-   If item[...] compared to ...:
-     Raise an error.
- Set merged to merge_pipeline_steps(...).
- Set prev to frozenset(...).

**Calls →**
1. `shared.pipeline_config.validate_pipeline_tail_payload`
2. `features.prospects.ValueError`
3. `features.prospects.ValueError`
4. `shared.pipeline_config.merge_pipeline_steps`
5. `features.prospects.frozenset`
6. `features.prospects.ProspectStore.set_pipeline_schema`

### `lock` (line 174)

**Pseudocode:**
- Return self.backend.lock.

### `leads` (line 182)

**Pseudocode:**
- Set self.backend.leads to value.

### `revision` (line 186)

**Pseudocode:**
- Return self.backend.revision.

### `snapshot` (line 189)
_Every prospect with a current status. Stored records are not rewritten._

**Pseudocode:**
- Set leads to ListComp.
- Set leads to active_leads(...).
- For each lead in leads:
-   Set lead[...] to canonical_status(...).
-   Set lead[...] to days_since_signal(...).
- Return leads.

**Calls →**
1. `features.prospects.ProspectStore.backend.snapshot`
2. `features._prospects.dial_archive.is_dial_archive_storage_lead`
3. `features._prospects.dial_records.is_dial_records_storage_lead`
4. `shared.prospect_schema.active_leads`
5. `shared.vocabulary.canonical_status`
6. `lead.get`
7. `shared.prospect_schema.days_since_signal`

**Called by ←**
- `fn:features/prospects.py:enforce_dial_caps`
- `fn:features/prospects.py:repair_dial_statuses`

### `repair_dial_statuses` (line 201)
_Undo wrongful closed-by-cap statuses and align dial-cap classification._

**Pseudocode:**
- Set counts to a dict.
- For each lead in self.snapshot(...):
-   Set next_status to repair_dial_status_for_lead(...).
-   If next_status:
-   Call self.set_status(...).
-   If next_status compared to ...:
-     Update counts[...] with Add 1.
-   Else:

**Calls →**
1. `features.prospects.ProspectStore.snapshot`
2. `shared.dial_policy.repair_dial_status_for_lead`
3. `features.prospects.ProspectStore.set_status`

**Called by ←**
- `fn:features/prospects.py:enforce_dial_caps`

### `migrate_callback_timers_to_two_hours` (line 215)
_Shift legacy 48-hour callback deadlines forward once per prospect._

**Pseudocode:**
- Set now to utc_now(...).
- Set shifted to 0.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   For each lead in leads:
-     If apply_callback_timer_migration_to_lead(...):
-       Call self.backend.save_locked(...).

**Calls →**
1. `shared.infra.utc_now`
2. `features.prospects.ProspectStore.backend.leads_locked`
3. `features.prospects.ProspectStore.backend.expire_locked`
4. `shared.dial_policy.apply_callback_timer_migration_to_lead`
5. `features.prospects.ProspectStore.backend.save_locked`

**Called by ←**
- `fn:features/prospects.py:__init__`

### `enforce_dial_caps` (line 228)
_Backfill closed at the dial cap. Repair runs only when requested (Scan CRM)._

**Pseudocode:**
- Set repair to IfExp.
- Set capped to 0.
- For each lead in self.snapshot(...):
-   If dial_cap_reached(...):
-   If lead_has_live_contact(...):
-   If canonical_status(...) compared to ...:
-   Call self.set_status(...).
-   Update capped with Add 1.

**Calls →**
1. `features.prospects.ProspectStore.repair_dial_statuses`
2. `features.prospects.ProspectStore.snapshot`
3. `shared.dial_policy.dial_cap_reached`
4. `shared.dial_policy.lead_has_live_contact`
5. `shared.vocabulary.canonical_status`
6. `lead.get`
7. `features.prospects.ProspectStore.set_status`

### `timezone_groups` (line 243)

**Pseudocode:**
- Return self.backend.timezone_groups(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.timezone_groups`

### `csv_bytes` (line 246)

**Pseudocode:**
- Return self.backend.csv_bytes(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.csv_bytes`

### `add_lead` (line 249)

**Pseudocode:**
- Set lead to self.backend.add_lead(...).
- If canonical_status(...) compared to ...:
-   Set lead to self.set_pipeline_step(...).
- Return lead.

**Calls →**
1. `features.prospects.ProspectStore.backend.add_lead`
2. `shared.vocabulary.canonical_status`
3. `lead.get`
4. `features.prospects.ProspectStore.set_pipeline_step`

### `update_fields` (line 282)

**Pseudocode:**
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set lead to _copy_of(...).
-   Set others to GeneratorExp.
-   Call update_lead_fields(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects.ProspectStore.backend.expire_locked`
3. `features.prospects._copy_of`
4. `item.get`
5. `features._prospects.csv_import.update_lead_fields`
6. `features.prospects.ProspectStore.backend.save_locked`
7. `features.prospects.dict`

### `set_pipeline_step` (line 292)

**Pseudocode:**
- Set step to str(...).strip(...).
- If step compared to ...:
-   Raise an error.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set lead to _copy_of(...).
-   If canonical_status(...) compared to ...:

**Calls →**
1. `features.prospects.str`
2. `features.prospects.ValueError`
3. `features.prospects.ProspectStore.backend.leads_locked`
4. `features.prospects.ProspectStore.backend.expire_locked`
5. `features.prospects._copy_of`
6. `shared.vocabulary.canonical_status`
7. `lead.get`
8. `features.prospects.ValueError`
9. `features.prospects.str`
10. `lead.get`
11. `shared.infra.utc_now`
12. `lead.setdefault`
13. `shared.vocabulary.pipeline_step_to_status`
14. `shared.vocabulary.canonical_status`
15. `lead.get`
16. `shared.vocabulary.canonical_status`
17. `lead.get`
18. `lead.setdefault`
19. `features.prospects.ProspectStore.backend.save_locked`
20. `features.prospects.dict`

**Called by ←**
- `fn:features/prospects.py:add_lead`

### `add_csv` (line 323)

**Pseudocode:**
- Return self.backend.add_csv(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.add_csv`

### `remove` (line 326)

**Pseudocode:**
- Return self.backend.remove(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.remove`

### `save` (line 329)

**Pseudocode:**
- Return self.backend.save(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.save`

### `defer` (line 332)

**Pseudocode:**
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set lead to _copy_of(...).
-   Set lead[...] to utc_now(...).isoformat(...).
-   Call self.backend.save_locked(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects.ProspectStore.backend.expire_locked`
3. `features.prospects._copy_of`
4. `shared.infra.utc_now`
5. `features.prospects.ProspectStore.backend.save_locked`
6. `features.prospects.dict`

### `set_status` (line 341)

**Pseudocode:**
- Set status to parse_prospect_status(...).
- If status compared to ...:
-   Raise an error.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set lead to _copy_of(...).
-   If agent_reservation_blocks_other_apps(...):

**Calls →**
1. `shared.vocabulary.parse_prospect_status`
2. `features.prospects.ValueError`
3. `features.prospects.ProspectStore.backend.leads_locked`
4. `features.prospects.ProspectStore.backend.expire_locked`
5. `features.prospects._copy_of`
6. `shared.dial_policy.agent_reservation_blocks_other_apps`
7. `features.prospects.ValueError`
8. `shared.vocabulary.agent_use_status_text`
9. `shared.vocabulary.canonical_status`
10. `lead.get`
11. `shared.infra.utc_now`
12. `lead.setdefault`
13. `features.prospects.ProspectStore._sync_pipeline_from_status`
14. `lead.get`
15. `datetime.datetime.fromisoformat`
16. `features.prospects.str`
17. `features.prospects.ValueError`
18. `features.prospects.ValueError`
19. `shared.infra.utc_now`
20. `features.prospects.ValueError`
21. `due.isoformat`
22. `shared.infra.utc_now`
23. `datetime.timedelta`
24. `features.prospects.ProspectStore.backend.save_locked`
25. `features.prospects.dict`

**Called by ←**
- `fn:features/prospects.py:enforce_dial_caps`
- `fn:features/prospects.py:repair_dial_statuses`

### `reserve_for_agent` (line 383)

**Pseudocode:**
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   If agent_reservation_blocks_other_apps(...):
-     Raise an error.
-   Set lead[...] to str(...).strip(...).
-   Set lead[...] to str(...).strip(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects._copy_of`
3. `shared.dial_policy.agent_reservation_blocks_other_apps`
4. `features.prospects.ValueError`
5. `shared.vocabulary.agent_use_status_text`
6. `features.prospects.str`
7. `features.prospects.str`
8. `shared.vocabulary.canonical_status`
9. `lead.get`
10. `shared.infra.utc_now`
11. `lead.setdefault`
12. `features.prospects.ProspectStore.backend.save_locked`
13. `features.prospects.dict`

### `agent_finalize_status` (line 404)

**Pseudocode:**
- Set status to parse_prospect_status(...).
- If a boolean condition:
-   Raise an error.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   If agent_reservation_blocks_other_apps(...):
-     Raise an error.

**Calls →**
1. `shared.vocabulary.parse_prospect_status`
2. `features.prospects.ValueError`
3. `features.prospects.ProspectStore.backend.leads_locked`
4. `features.prospects._copy_of`
5. `shared.dial_policy.agent_reservation_blocks_other_apps`
6. `features.prospects.ValueError`
7. `shared.vocabulary.agent_use_status_text`
8. `shared.dial_policy.clear_agent_reservation_fields`
9. `shared.vocabulary.canonical_status`
10. `lead.get`
11. `shared.infra.utc_now`
12. `lead.setdefault`
13. `features.prospects.ProspectStore._sync_pipeline_from_status`
14. `features.prospects.ProspectStore.backend.save_locked`
15. `features.prospects.dict`

### `append_transcript` (line 432)

**Pseudocode:**
- Set entry to a dict.
- If a boolean condition:
-   Raise an error.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   Set transcript to lead.setdefault(...).
-   If a boolean condition:

**Calls →**
1. `features.prospects.str`
2. `segment.get`
3. `features.prospects.str`
4. `segment.get`
5. `features.prospects.str`
6. `segment.get`
7. `features.prospects.str`
8. `segment.get`
9. `features.prospects.ValueError`
10. `features.prospects.ProspectStore.backend.leads_locked`
11. `features.prospects._copy_of`
12. `lead.setdefault`
13. `features.prospects.any`
14. `item.get`
15. `features.prospects.dict`
16. `transcript.append`
17. `transcript.sort`
18. `item.get`
19. `features.prospects.ProspectStore.backend.save_locked`
20. `features.prospects.dict`

### `clear_all_call_logs` (line 452)
_Remove every call_log row while keeping prospects and transcripts._

**Pseudocode:**
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   For each lead in leads:
-     If lead.get(...):
-       Set lead[...] to a list.
-       Call self.backend.save_locked(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `lead.get`
3. `features.prospects.ProspectStore.backend.save_locked`

### `append_call_log` (line 461)

**Pseudocode:**
- Set record to a dict.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   Set log to lead.setdefault(...).
-   If replace_id:
-     Set replaced to ListComp.
-     Set record[...] to a boolean condition.

**Calls →**
1. `features.prospects.str`
2. `entry.get`
3. `features.prospects.str`
4. `entry.get`
5. `features.prospects.str`
6. `entry.get`
7. `features.prospects.str`
8. `entry.get`
9. `features.prospects.str`
10. `entry.get`
11. `features.prospects.int`
12. `entry.get`
13. `features.prospects.int`
14. `entry.get`
15. `features.prospects.isinstance`
16. `entry.get`
17. `entry.get`
18. `entry.get`
19. `features.prospects.ProspectStore.backend.leads_locked`
20. `features.prospects._copy_of`
21. `lead.setdefault`
22. `item.get`
23. `features.prospects.str`
24. `features.prospects.next`
25. `item.get`
26. `item.get`
27. `item.get`
28. `features.prospects.str`
29. `features.prospects.any`
30. `item.get`

### `repair_total_dials_callbacks` (line 491)
_Fix prospects still marked New while they have Total dials rows._

**Pseudocode:**
- Set updated to 0.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   For each lead in leads:
-     If lead.get(...):
-     If canonical_status(...) compared to ...:
-     Set patched to _copy_of(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects.ProspectStore.backend.expire_locked`
3. `lead.get`
4. `shared.vocabulary.canonical_status`
5. `lead.get`
6. `features.prospects._copy_of`
7. `shared.dial_policy.apply_total_dials_callback_status`
8. `features.prospects.ProspectStore.backend.save_locked`

### `migrate_nov5_2026_static_callbacks` (line 508)
_One-time: Nov 5 Total dials + New (or timed Callback) → static Callback (pipeline Dialed)._

**Pseudocode:**
- Set updated to 0.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Call self.backend.expire_locked(...).
-   Set dialed_ids to lead_ids_with_dial_on_local_date(...).
-   For each lead in leads:
-     If lead.get(...) compared to ...:
-     Set status to canonical_status(...).

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects.ProspectStore.backend.expire_locked`
3. `shared.dial_policy.lead_ids_with_dial_on_local_date`
4. `lead.get`
5. `shared.vocabulary.canonical_status`
6. `lead.get`
7. `lead.get`
8. `features.prospects._copy_of`
9. `shared.dial_policy.apply_static_callback_status`
10. `features.prospects.ProspectStore.backend.save_locked`

### `set_call_outcome` (line 533)
_Tag the call-log entry stored under any of call_ids. Returns False when no entry has been written yet._

**Pseudocode:**
- If outcome compared to ...:
-   Raise an error.
- Set wanted to SetComp.
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   Set entries to ListComp.
-   If entries:

**Calls →**
1. `features.prospects.ValueError`
2. `features.prospects.str`
3. `features.prospects.ProspectStore.backend.leads_locked`
4. `features.prospects._copy_of`
5. `lead.get`
6. `item.get`
7. `features.prospects.ProspectStore.backend.save_locked`

### `set_booked_at` (line 549)
_Date a booked prospect that has no booking date. A dated booking is never moved,_

**Pseudocode:**
- With self.lock:
-   Set leads to self.backend.leads_locked(...).
-   Set lead to _copy_of(...).
-   If lead.get(...) compared to ...:
-     Raise an error.
-   If a boolean condition:
-     Raise an error.
-   Set lead[...] to booked_at.

**Calls →**
1. `features.prospects.ProspectStore.backend.leads_locked`
2. `features.prospects._copy_of`
3. `lead.get`
4. `features.prospects.ValueError`
5. `lead.get`
6. `features.prospects.ValueError`
7. `features.prospects.ProspectStore.backend.save_locked`
8. `features.prospects.dict`

### `_copy_of` (line 564)

**Pseudocode:**
- Set lead to next(...).
- If lead compared to ...:
-   Raise an error.
- Return deepcopy(...).

**Calls →**
1. `features.prospects.next`
2. `features.prospects.KeyError`
3. `copy.deepcopy`

**Called by ←**
- `fn:features/prospects.py:agent_finalize_status`
- `fn:features/prospects.py:append_call_log`
- `fn:features/prospects.py:append_transcript`
- `fn:features/prospects.py:defer`
- `fn:features/prospects.py:migrate_nov5_2026_static_callbacks`
- `fn:features/prospects.py:remap_pipeline_after_deletion`
- `fn:features/prospects.py:repair_total_dials_callbacks`
- `fn:features/prospects.py:reserve_for_agent`
- `fn:features/prospects.py:set_booked_at`
- `fn:features/prospects.py:set_call_outcome`
- `fn:features/prospects.py:set_pipeline_schema`
- `fn:features/prospects.py:set_pipeline_step`
- `fn:features/prospects.py:set_status`
- `fn:features/prospects.py:update_fields`

### `post_lead` (line 571)

**Pseudocode:**
- Set lead to request.account.crm.add_lead(...).
- Call request.send_json(...).

**Calls →**
1. `request.account.crm.add_lead`
2. `request.send_json`
3. `request.ctx.state`

### `post_fields` (line 576)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Set lead to request.account.crm.update_fields(...).
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `request.account.crm.update_fields`
4. `request.send_json`
5. `request.ctx.state`

### `post_pipeline_step` (line 582)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Set step to data.get(...).
- Set lead to request.account.crm.set_pipeline_step(...).
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `data.get`
4. `request.account.crm.set_pipeline_step`
5. `request.send_json`
6. `request.ctx.state`

### `post_save_pipeline_settings` (line 589)

**Pseudocode:**
- Set steps to data.get(...).
- Set migrate_leads to bool(...).
- If isinstance(...):
-   Raise an error.
- Set dialer to request.account.dialer.
- Set crm to request.account.crm.
- Set json_text to json.dumps(...).
- Set touched to crm.set_pipeline_tail(...).

**Calls →**
1. `data.get`
2. `features.prospects.bool`
3. `data.get`
4. `features.prospects.isinstance`
5. `features.prospects.ValueError`
6. `json.dumps`
7. `crm.set_pipeline_tail`
8. `features.prospects.getattr`
9. `features.prospects.getattr`
10. `features.prospects.saver`
11. `shared.config.write_env`
12. `dialer.account_values.update`
13. `shared.config.read_env`
14. `request.send_json`
15. `crm.pipeline_steps_for_catalog`
16. `request.ctx.state`

### `post_import` (line 614)

**Pseudocode:**
- Set result to request.account.crm.add_csv(...).
- Call request.account.dialer.maintain_crm(...).
- Try:
-   Set state to request.ctx.state(...).
- On <ast.Name object at 0x000001E0F9072C90>:
-   Call request.ctx.log(...).
-   Set state to a dict.
- Call request.send_json(...).

**Calls →**
1. `request.account.crm.add_csv`
2. `request.account.dialer.maintain_crm`
3. `request.ctx.state`
4. `request.ctx.log`
5. `request.account.crm.snapshot`
6. `request.send_json`

### `get_export` (line 625)

**Pseudocode:**
- Try:
-   Set content to request.account.crm.csv_bytes(...).
-   Call request.send_bytes(...).
- On <ast.Name object at 0x000001E0F9078ED0>:
-   Call request.report_storage_error(...).

**Calls →**
1. `request.account.crm.csv_bytes`
2. `request.send_bytes`
3. `request.report_storage_error`

### `delete_lead` (line 635)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Try:
-   Set crm to request.account.crm.
-   Set archive to request.account.dial_archive.
-   Set lead to next(...).
-   If lead compared to ...:
-     Raise an error.
-   Call archive.archive_lead(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `features.prospects.next`
4. `crm.snapshot`
5. `item.get`
6. `features.prospects.KeyError`
7. `archive.archive_lead`
8. `crm.remove`
9. `request.send_json`
10. `request.ctx.state`
11. `features.prospects.str`
12. `request.send_json`
13. `features.prospects.str`
14. `features.prospects.str`
15. `request.send_json`

**Called by ←**
- `fn:web.py:do_DELETE`
