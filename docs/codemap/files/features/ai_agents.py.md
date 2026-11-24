# `features/ai_agents.py`

**Purpose:** AI agent seats: reserved dialer pools and session mode.

## Functions
### `_default_agents` (line 35)

**Pseudocode:**
- Return ListComp.

**Calls →**
1. `features.ai_agents.dict`

**Called by ←**
- `fn:features/ai_agents.py:_load_agents_data`
- `fn:features/ai_agents.py:agents_public_view`

### `_load_agents_data` (line 39)

**Pseudocode:**
- Set raw to str(...).
- Try:
-   Set parsed to json.loads(...).
- On <ast.Attribute object at 0x000001E0F8F0D950>:
-   Set parsed to a dict.
- If isinstance(...):
-   Set parsed to a dict.
- Set pools to parsed.get(...).

**Calls →**
1. `features.ai_agents.str`
2. `state.read_settings`
3. `json.loads`
4. `features.ai_agents.isinstance`
5. `parsed.get`
6. `features.ai_agents.isinstance`
7. `parsed.get`
8. `features.ai_agents.isinstance`
9. `features.ai_agents._default_agents`
10. `features.ai_agents.isinstance`
11. `features.ai_agents._normalize_agent_record`
12. `features.ai_agents._default_agents`

**Called by ←**
- `fn:features/ai_agents.py:_agent_records`
- `fn:features/ai_agents.py:agent_pool_lead_ids`
- `fn:features/ai_agents.py:agents_public_view`
- `fn:features/ai_agents.py:all_reserved_lead_ids`
- `fn:features/ai_agents.py:create_agent`
- `fn:features/ai_agents.py:delete_agent`
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/ai_agents.py:set_agent_pool_lead_ids`

### `_save_agents_data` (line 68)

**Pseudocode:**
- Set payload to json.dumps(...).
- Set values to a dict.
- Set state.settings to values.
- If hasattr(...):
-   Set state.account_values[...] to payload.
- Set saver to getattr(...).
- If saver:
-   Call saver(...).

**Calls →**
1. `json.dumps`
2. `state.read_settings`
3. `features.ai_agents.hasattr`
4. `features.ai_agents.getattr`
5. `features.ai_agents.saver`

**Called by ←**
- `fn:features/ai_agents.py:create_agent`
- `fn:features/ai_agents.py:delete_agent`
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/ai_agents.py:set_agent_pool_lead_ids`

### `_normalize_agent_record` (line 79)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set name to a boolean condition.
- Set title to a boolean condition.
- Set primary to bool(...).
- If agent_id:
-   Return None.
- Return a dict.

**Calls →**
1. `features.ai_agents.str`
2. `item.get`
3. `features.ai_agents.str`
4. `item.get`
5. `features.ai_agents.str`
6. `item.get`
7. `features.ai_agents.bool`
8. `item.get`

**Called by ←**
- `fn:features/ai_agents.py:_load_agents_data`

### `_agent_records` (line 89)

**Pseudocode:**
- Return list(...).

**Calls →**
1. `features.ai_agents.list`
2. `features.ai_agents._load_agents_data`

**Called by ←**
- `fn:features/ai_agents.py:_find_agent_record`

### `_find_agent_record` (line 93)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- For each record in _agent_records(...):
-   If record.get(...) compared to ...:
-     Return record.
- Return None.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents._agent_records`
3. `record.get`

**Called by ←**
- `fn:features/ai_agents.py:_agent_name`
- `fn:features/ai_agents.py:boot_agent_pool`
- `fn:features/ai_agents.py:delete_agent`
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/ai_agents.py:start_agent`

### `_slugify_name` (line 101)

**Pseudocode:**
- Set base to a boolean condition.
- If base compared to ...:
-   Return base.
- For each index in range(...):
-   Set candidate to JoinedStr.
-   If candidate compared to ...:
-     Return candidate.
- Return JoinedStr.

**Calls →**
1. `re.sub`
2. `features.ai_agents.str`
3. `features.ai_agents.range`
4. `uuid.uuid4`

**Called by ←**
- `fn:features/ai_agents.py:create_agent`
- `fn:features/ai_agents.py:duplicate_agent`

### `_primary_agent_id` (line 112)

**Pseudocode:**
- For each record in records:
-   If record.get(...):
-     Return record[...].
- Return IfExp.

**Calls →**
1. `record.get`

**Called by ←**
- `fn:features/ai_agents.py:agents_public_view`

### `_agent_name` (line 119)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If state compared to ...:
-   Set record to _find_agent_record(...).
-   If record:
-     Return record[...].
- For each seat in DEFAULT_AGENT_SEATS:
-   If seat[...] compared to ...:
-     Return seat[...].

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents._find_agent_record`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_agent_name`
- `fn:features/ai_agents.py:boot_agent_pool`
- `fn:features/ai_agents.py:release_agent_pool`
- `fn:features/ai_voice_runtime.py:start_call_session`
- `fn:features/dialer.py:ai_agent_playbook`
- `fn:features/dialer.py:save_ai_agent_playbook`

### `all_reserved_lead_ids` (line 131)

**Pseudocode:**
- Set blob to _load_agents_data(...).
- Set reserved to set(...).
- For each ids in blob.get(...).values(...):
-   For each lead_id in a boolean condition:
-     If lead_id:
-       Call reserved.add(...).
- Return reserved.

**Calls →**
1. `features.ai_agents._load_agents_data`
2. `features.ai_agents.set`
3. `blob.get`
4. `reserved.add`
5. `features.ai_agents.str`

**Called by ←**
- `fn:features/ai_agents.py:boot_agent_pool`

### `agent_pool_lead_ids` (line 141)

**Pseudocode:**
- Set blob to _load_agents_data(...).
- Set ids to a boolean condition.
- Return ListComp.

**Calls →**
1. `features.ai_agents._load_agents_data`
2. `blob.get`
3. `features.ai_agents.str`
4. `features.ai_agents.str`

**Called by ←**
- `fn:features/ai_agents.py:agent_lead_ids_for_queue`
- `fn:features/ai_agents.py:agent_pool_stats`
- `fn:features/ai_agents.py:boot_agent_pool`
- `fn:features/ai_agents.py:dialable_pool_for_agent`
- `fn:features/ai_agents.py:release_agent_pool`

### `set_agent_pool_lead_ids` (line 147)

**Pseudocode:**
- Set blob to _load_agents_data(...).
- Set pools to blob.setdefault(...).
- Set pools[...] to ListComp.
- Call _save_agents_data(...).

**Calls →**
1. `features.ai_agents._load_agents_data`
2. `blob.setdefault`
3. `features.ai_agents.str`
4. `features.ai_agents.str`
5. `features.ai_agents._save_agents_data`

**Called by ←**
- `fn:features/ai_agents.py:boot_agent_pool`
- `fn:features/ai_agents.py:release_agent_pool`

### `create_agent` (line 154)

**Pseudocode:**
- Set display to str(...).strip(...).
- If display:
-   Raise an error.
- If len(...) compared to ...:
-   Raise an error.
- Set role to a boolean condition.
- If len(...) compared to ...:
-   Raise an error.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.ValueError`
3. `features.ai_agents.len`
4. `features.ai_agents.ValueError`
5. `features.ai_agents.str`
6. `features.ai_agents.len`
7. `features.ai_agents.ValueError`
8. `features.ai_agents._load_agents_data`
9. `blob.setdefault`
10. `features.ai_agents.str`
11. `item.get`
12. `features.ai_agents._slugify_name`
13. `agents.append`
14. `blob.setdefault`
15. `features.ai_agents._save_agents_data`
16. `features.ai_agent_playbook.get_playbook`
17. `state.record_activity`
18. `features.ai_agents.agents_public_view`

**Called by ←**
- `fn:features/dialer.py:create_ai_agent`

### `duplicate_agent` (line 176)

**Pseudocode:**
- Set source_id to str(...).strip(...).
- Set source to _find_agent_record(...).
- If source:
-   Raise an error.
- Set blob to _load_agents_data(...).
- Set agents to blob.setdefault(...).
- Set existing_ids to SetComp.
- Set display to a boolean condition.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents._find_agent_record`
3. `features.ai_agents.ValueError`
4. `features.ai_agents._load_agents_data`
5. `blob.setdefault`
6. `features.ai_agents.str`
7. `item.get`
8. `features.ai_agents.str`
9. `features.ai_agents._slugify_name`
10. `source.get`
11. `agents.append`
12. `blob.setdefault`
13. `features.ai_agents._save_agents_data`
14. `features.ai_agent_playbook.get_playbook`
15. `features.ai_agent_playbook.save_playbook`
16. `source_playbook.get`
17. `state.record_activity`
18. `features.ai_agents.agents_public_view`

**Called by ←**
- `fn:features/dialer.py:duplicate_ai_agent`

### `delete_agent` (line 208)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set record to _find_agent_record(...).
- If record:
-   Raise an error.
- If a boolean condition:
-   Raise an error.
- Set blob to _load_agents_data(...).
- Set agents to a boolean condition.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents._find_agent_record`
3. `features.ai_agents.ValueError`
4. `features.ai_agents.getattr`
5. `features.ai_agents.getattr`
6. `features.ai_agents.ValueError`
7. `features.ai_agents._load_agents_data`
8. `blob.get`
9. `features.ai_agents.len`
10. `features.ai_agents.ValueError`
11. `features.ai_agents.release_agent_pool`
12. `features.ai_agent_playbook.remove_playbook`
13. `item.get`
14. `record.get`
15. `blob.get`
16. `features.ai_agents._save_agents_data`
17. `state.record_activity`
18. `features.ai_agents.agents_public_view`

**Called by ←**
- `fn:features/dialer.py:delete_ai_agent`

### `boot_agent_pool` (line 233)
_Claim up to AGENT_POOL_SIZE prospects from the global dialer pool for one seat._

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If agent_id:
-   Raise an error.
- If _find_agent_record(...):
-   Raise an error.
- Set existing to agent_pool_lead_ids(...).
- If existing:
-   Return a dict.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.ValueError`
3. `features.ai_agents._find_agent_record`
4. `features.ai_agents.ValueError`
5. `features.ai_agents.agent_pool_lead_ids`
6. `state.crm.snapshot`
7. `features._dialer.calls._busy_lead_ids`
8. `features.ai_agents.all_reserved_lead_ids`
9. `shared.dial_policy.pick_agent_pool_ids`
10. `features.ai_agents.getattr`
11. `features.ai_agents.ValueError`
12. `features.ai_agents._agent_name`
13. `state.crm.reserve_for_agent`
14. `features.ai_agents.set_agent_pool_lead_ids`
15. `state.record_activity`
16. `features.ai_agents.len`
17. `features.ai_agents.getattr`
18. `features.ai_agents.getattr`
19. `features.ai_agents.try_resume_agent_dial`

**Called by ←**
- `fn:features/ai_agents.py:start_agent`
- `fn:features/dialer.py:boot_ai_agent_pool`

### `release_agent_pool` (line 270)
_Remove every prospect from a seat pool and clear agent-use locks._

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set ids to agent_pool_lead_ids(...).
- If ids:
-   Call set_agent_pool_lead_ids(...).
-   Return a dict.
- Set count to 0.
- For each lead_id in ids:
-   Set lead to next(...).

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.agent_pool_lead_ids`
3. `features.ai_agents.set_agent_pool_lead_ids`
4. `features.ai_agents.next`
5. `state.crm.snapshot`
6. `item.get`
7. `shared.dial_policy.is_agent_reserved`
8. `state.crm.agent_finalize_status`
9. `features.ai_agents.set_agent_pool_lead_ids`
10. `state.record_activity`
11. `features.ai_agents._agent_name`

**Called by ←**
- `fn:features/ai_agents.py:delete_agent`
- `fn:features/dialer.py:release_ai_agent_pool`

### `dialable_pool_for_agent` (line 290)

**Pseudocode:**
- Set leads to IfExp.
- Set agent_id to getattr(...).
- If agent_id:
-   Return calls._pool_leads(...).
- Set ids to agent_pool_lead_ids(...).
- Set busy to calls._busy_lead_ids(...).
- Return agent_dial_queue(...).

**Calls →**
1. `state.crm.snapshot`
2. `features.ai_agents.getattr`
3. `features._dialer.calls._pool_leads`
4. `features.ai_agents.agent_pool_lead_ids`
5. `features._dialer.calls._busy_lead_ids`
6. `shared.dial_policy.agent_dial_queue`

**Called by ←**
- `fn:features/ai_agents.py:agent_pool_stats`
- `fn:features/ai_agents.py:try_resume_agent_dial`

### `global_pool_snapshot` (line 300)

**Pseudocode:**
- Set leads to state.crm.snapshot(...).
- Set busy to calls._busy_lead_ids(...).
- Set pool to global_dialer_pool(...).
- Return a dict.

**Calls →**
1. `state.crm.snapshot`
2. `features._dialer.calls._busy_lead_ids`
3. `shared.dial_policy.global_dialer_pool`
4. `features.ai_agents.getattr`
5. `features.ai_agents.len`

**Called by ←**
- `fn:features/ai_agents.py:agents_public_view`

### `agents_public_view` (line 315)

**Pseudocode:**
- Set blob to _load_agents_data(...).
- Set pools to blob.get(...).
- Set records to a boolean condition.
- Set running_id to getattr(...).
- Set primary_id to _primary_agent_id(...).
- Set agents to a list.
- Set leads to state.crm.snapshot(...).
- Set busy to calls._busy_lead_ids(...).

**Calls →**
1. `features.ai_agents._load_agents_data`
2. `blob.get`
3. `blob.get`
4. `features.ai_agents._default_agents`
5. `features.ai_agents.getattr`
6. `features.ai_agents._primary_agent_id`
7. `state.crm.snapshot`
8. `features._dialer.calls._busy_lead_ids`
9. `pools.get`
10. `features.ai_agents.len`
11. `shared.dial_policy.agent_dial_queue`
12. `agents.append`
13. `record.get`
14. `features.ai_agents.len`
15. `features.ai_agents.global_pool_snapshot`
16. `features.ai_agents.agent_pool_stats`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/ai_agents.py:create_agent`
- `fn:features/ai_agents.py:delete_agent`
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/ai_agents.py:start_agent`
- `fn:features/ai_agents.py:stop_agent`
- `fn:features/dialer.py:get_ai_agents`

### `agent_pool_stats` (line 349)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set ids to IfExp.
- Set dialable to IfExp.
- Return a dict.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.getattr`
3. `features.ai_agents.agent_pool_lead_ids`
4. `features.ai_agents.dialable_pool_for_agent`
5. `features.ai_agents.len`
6. `features.ai_agents.len`

**Called by ←**
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/ai_agents.py:agents_public_view`
- `fn:features/ai_agents.py:start_agent`

### `try_resume_agent_dial` (line 359)
_Refill lines when the agent pool gains dialable prospects and no live call is up._

**Pseudocode:**
- If getattr(...):
-   Return nothing.
- With state.lock:
-   If a boolean condition:
-     Return nothing.
-   If voice_session.slots_may_dial(...):
-     Return nothing.
- Set dialable to dialable_pool_for_agent(...).

**Calls →**
1. `features.ai_agents.getattr`
2. `voice_session.slots_may_dial`
3. `features.ai_agents.dialable_pool_for_agent`
4. `features.ai_agents.len`
5. `features._dialer.slots.fill_slots`

**Called by ←**
- `fn:features/ai_agents.py:boot_agent_pool`

### `start_agent` (line 379)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If agent_id:
-   Raise an error.
- If _find_agent_record(...):
-   Raise an error.
- With state.lock:
-   If state.running:
-     If getattr(...) compared to ...:

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.ValueError`
3. `features.ai_agents._find_agent_record`
4. `features.ai_agents.ValueError`
5. `features.ai_agents.getattr`
6. `features.ai_agents.ValueError`
7. `features.ai_agents.ValueError`
8. `features.ai_agents.boot_agent_pool`
9. `features.ai_agents.agent_pool_stats`
10. `features.ai_agents.ValueError`
11. `features.ai_agents.ValueError`
12. `features._dialer.queue.start`
13. `features.ai_agents.agents_public_view`

**Called by ←**
- `fn:features/dialer.py:start_ai_agent`

### `stop_agent` (line 405)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- With state.lock:
-   Set running_id to getattr(...).
- If a boolean condition:
-   Raise an error.
- Set view to queue.stop(...).
- With state.lock:
-   Set state.ai_agent_id to None.

**Calls →**
1. `features.ai_agents.str`
2. `features.ai_agents.getattr`
3. `features.ai_agents.ValueError`
4. `features._dialer.queue.stop`
5. `features.ai_agents.agents_public_view`

**Called by ←**
- `fn:features/dialer.py:stop_ai_agent`

### `finalize_agent_call` (line 419)
_Auto CRM updates for AI sessions — dialed or contact_engaged only._

**Pseudocode:**
- If getattr(...):
-   Return nothing.
- Set agent_id to getattr(...).
- Set lead to next(...).
- If a boolean condition:
-   Return nothing.
- If a boolean condition:
-   Call state.crm.agent_finalize_status(...).

**Calls →**
1. `features.ai_agents.getattr`
2. `features.ai_agents.getattr`
3. `features.ai_agents.next`
4. `state.crm.snapshot`
5. `item.get`
6. `shared.dial_policy.agent_reservation_blocks_other_apps`
7. `state.crm.agent_finalize_status`
8. `state.crm.agent_finalize_status`

### `assert_lead_mutable_by_user` (line 433)

**Pseudocode:**
- Set lead to next(...).
- If lead compared to ...:
-   Return nothing.
- If agent_reservation_blocks_other_apps(...):
-   Set name to agent_use_status_text(...).
-   Raise an error.

**Calls →**
1. `features.ai_agents.next`
2. `state.crm.snapshot`
3. `item.get`
4. `shared.dial_policy.agent_reservation_blocks_other_apps`
5. `shared.vocabulary.agent_use_status_text`
6. `features.ai_agents.ValueError`

### `agent_lead_ids_for_queue` (line 442)

**Pseudocode:**
- Return agent_pool_lead_ids(...).

**Calls →**
1. `features.ai_agents.agent_pool_lead_ids`
2. `features.ai_agents.getattr`
