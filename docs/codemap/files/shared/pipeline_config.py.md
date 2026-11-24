# `shared/pipeline_config.py`

**Purpose:** Configurable CRM pipeline steps: Dialed + Contacted (engaged) (call_1) are fixed; the rest are user-defined.

## Functions
### `normalize_pipeline_step_key` (line 20)
_Turn user input into a valid step key: lowercase, letters/digits, underscores between words._

**Pseudocode:**
- Set s to str(...).strip(...).lower(...).
- Set parts to a list.
- Set buf to a list.
- For each ch in s:
-   If a boolean condition:
-     Call buf.append(...).
-   Else:
-     If buf:

**Calls →**
1. `shared.pipeline_config.str`
2. `ch.isdigit`
3. `buf.append`
4. `parts.append`
5. `parts.append`
6. `key.strip`
7. `shared.pipeline_config.len`

**Called by ←**
- `fn:shared/pipeline_config.py:_as_step_dict`

### `_as_step_dict` (line 53)

**Pseudocode:**
- If isinstance(...):
-   Return None.
- Set key to normalize_pipeline_step_key(...).
- Set label to str(...).strip(...).
- Try:
-   Set wait_hours to int(...).
- On <ast.Tuple object at 0x00000242BC179650>:
-   Return None.

**Calls →**
1. `shared.pipeline_config.isinstance`
2. `shared.pipeline_config.normalize_pipeline_step_key`
3. `raw.get`
4. `shared.pipeline_config.str`
5. `raw.get`
6. `shared.pipeline_config.int`
7. `shared.pipeline_config.float`
8. `raw.get`
9. `_PIPELINE_STEP_KEY_RE.match`
10. `shared.pipeline_config.len`

**Called by ←**
- `fn:shared/pipeline_config.py:parse_custom_pipeline_steps_json`
- `fn:shared/pipeline_config.py:validate_pipeline_tail_payload`

### `parse_custom_pipeline_steps_json` (line 75)
_Parse stored JSON list of custom tail steps. Returns (steps, error_message)._

**Pseudocode:**
- Set stripped to str(...).strip(...).
- If stripped:
-   Return Tuple.
- Try:
-   Set data to json.loads(...).
- On <ast.Attribute object at 0x00000242BC13B150>:
-   Return Tuple.
- If isinstance(...):

**Calls →**
1. `shared.pipeline_config.str`
2. `json.loads`
3. `shared.pipeline_config.isinstance`
4. `shared.pipeline_config.set`
5. `shared.pipeline_config._as_step_dict`
6. `seen.add`
7. `out.append`

**Called by ←**
- `fn:features/prospects.py:apply_pipeline_tail_from_settings`
- `fn:features/prospects.py:sync_pipeline_from_merged_values`
- `fn:features/settings.py:preferences`
- `fn:features/settings.py:settings_state`
- `fn:shared/pipeline_config.py:resolve_pipeline_steps`

### `merge_pipeline_steps` (line 99)
_Full ordered step list: locked head + custom tail (defaults when custom empty)._

**Pseudocode:**
- Set head to a list.
- If custom_tail:
-   Set tail to ListComp.
- Else:
-   Set tail to ListComp.
- Return head op tail.

**Calls →**
1. `shared.pipeline_config.dict`
2. `shared.pipeline_config.dict`
3. `shared.pipeline_config.dict`
4. `shared.pipeline_config.dict`

**Called by ←**
- `fn:features/prospects.py:__init__`
- `fn:features/prospects.py:apply_pipeline_tail_from_settings`
- `fn:features/prospects.py:set_pipeline_tail`
- `fn:features/prospects.py:sync_pipeline_from_merged_values`
- `fn:shared/pipeline_config.py:resolve_pipeline_steps`

### `resolve_pipeline_steps` (line 112)
_Steps for API/catalog from env/account settings._

**Pseudocode:**
- Set raw to ''.
- If account_values:
-   Set raw to str(...).strip(...).
- Set Tuple to parse_custom_pipeline_steps_json(...).
- Return merge_pipeline_steps(...).

**Calls →**
1. `shared.pipeline_config.str`
2. `account_values.get`
3. `shared.pipeline_config.parse_custom_pipeline_steps_json`
4. `shared.pipeline_config.merge_pipeline_steps`

### `validate_pipeline_tail_payload` (line 121)
_Validate user POST body steps (tail only). Returns (normalized_list, error_message)._

**Pseudocode:**
- If isinstance(...):
-   Return Tuple.
- If len(...) compared to ...:
-   Return Tuple.
- Set seen to set(...).
- Set out to a list.
- For each item in steps:
-   If isinstance(...):

**Calls →**
1. `shared.pipeline_config.isinstance`
2. `shared.pipeline_config.len`
3. `shared.pipeline_config.set`
4. `shared.pipeline_config.isinstance`
5. `shared.pipeline_config._as_step_dict`
6. `seen.add`
7. `out.append`

**Called by ←**
- `fn:features/prospects.py:set_pipeline_tail`

### `migrate_leads_pipeline_keys` (line 142)
_Remap pipeline_step / pipeline_history when step keys disappear. Returns lead ids touched._

**Pseudocode:**
- Set old_keys to set(...).
- Set new_keys to set(...).
- Set removed to old_keys op new_keys.
- If removed:
-   Return a list.
- Set fallback_send to send_info_step.
- Set touched to a list.
- For each lead in leads:

**Calls →**
1. `shared.pipeline_config.set`
2. `shared.pipeline_config.set`
3. `shared.pipeline_config.str`
4. `shared.pipeline_config.str`
5. `lead.get`
6. `shared.pipeline_config.str`
7. `lead.get`
8. `shared.pipeline_config.map_step`
9. `lead.get`
10. `shared.pipeline_config.isinstance`
11. `shared.pipeline_config.isinstance`
12. `shared.pipeline_config.str`
13. `entry.get`
14. `shared.pipeline_config.map_step`
15. `touched.append`

**Called by ←**
- `fn:features/prospects.py:remap_pipeline_after_deletion`
- `fn:features/prospects.py:set_pipeline_schema`
