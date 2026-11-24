# `features/ai_agent_playbook.py`

**Purpose:** Per-seat AI call playbooks — single freeform prompt per agent.

## Functions
### `default_prompt_text` (line 45)

**Pseudocode:**
- Return DEFAULT_PROMPT_TEMPLATE.format(...).strip(...).

**Calls →**
1. `DEFAULT_PROMPT_TEMPLATE.format`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_extract_prompt`
- `fn:features/ai_agent_playbook.py:compile_playbook`
- `fn:features/ai_agent_playbook.py:default_playbook`

### `legacy_dict_to_prompt` (line 49)
_Flatten older structured playbooks into one prompt block._

**Pseudocode:**
- Set lines to a list.
- Set title to str(...).strip(...).
- If title:
-   Call lines.append(...).
- For each Tuple in Tuple:
-   Set value to str(...).strip(...).
-   If value:
-     Call lines.extend(...).

**Calls →**
1. `features.ai_agent_playbook.str`
2. `data.get`
3. `lines.append`
4. `features.ai_agent_playbook.str`
5. `data.get`
6. `lines.extend`
7. `features.ai_agent_playbook.str`
8. `data.get`
9. `lines.extend`
10. `target.replace`
11. `features.ai_agent_playbook.isinstance`
12. `data.get`
13. `data.get`
14. `features.ai_agent_playbook.str`
15. `guard.get`
16. `features.ai_agent_playbook.str`
17. `features.ai_agent_playbook.str`
18. `guard.get`
19. `features.ai_agent_playbook.str`
20. `lines.extend`
21. `lines.extend`
22. `features.ai_agent_playbook.isinstance`
23. `data.get`
24. `data.get`
25. `lines.extend`
26. `features.ai_agent_playbook.enumerate`
27. `features.ai_agent_playbook.isinstance`
28. `step.get`
29. `step.get`
30. `lines.append`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_extract_prompt`
- `fn:features/ai_agent_playbook.py:save_playbook`

### `_load_blob` (line 89)

**Pseudocode:**
- Set raw to str(...).
- Try:
-   Set parsed to json.loads(...).
- On <ast.Attribute object at 0x00000242BC224450>:
-   Set parsed to a dict.
- If isinstance(...):
-   Set parsed to a dict.
- Set playbooks to parsed.get(...).

**Calls →**
1. `features.ai_agent_playbook.str`
2. `state.read_settings`
3. `json.loads`
4. `features.ai_agent_playbook.isinstance`
5. `parsed.get`
6. `features.ai_agent_playbook.isinstance`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_persist_playbook`
- `fn:features/ai_agent_playbook.py:get_playbook`
- `fn:features/ai_agent_playbook.py:remove_playbook`

### `_save_blob` (line 103)

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
3. `features.ai_agent_playbook.hasattr`
4. `features.ai_agent_playbook.getattr`
5. `features.ai_agent_playbook.saver`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_persist_playbook`
- `fn:features/ai_agent_playbook.py:remove_playbook`

### `_extract_prompt` (line 114)

**Pseudocode:**
- If isinstance(...):
-   Set text to raw.strip(...).
-   Return a boolean condition.
- If isinstance(...):
-   Return default_prompt_text(...).
- Set prompt to str(...).strip(...).
- If prompt:
-   Return prompt.

**Calls →**
1. `features.ai_agent_playbook.isinstance`
2. `raw.strip`
3. `features.ai_agent_playbook.default_prompt_text`
4. `features.ai_agent_playbook.isinstance`
5. `features.ai_agent_playbook.default_prompt_text`
6. `features.ai_agent_playbook.str`
7. `raw.get`
8. `features.ai_agent_playbook.legacy_dict_to_prompt`
9. `features.ai_agent_playbook.default_prompt_text`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_playbook_view`
- `fn:features/ai_agent_playbook.py:normalize_playbook`

### `_prompt_digest` (line 127)

**Pseudocode:**
- Return hashlib.sha256(...).hexdigest(...)[...].

**Calls →**
1. `hashlib.sha256`
2. `features.ai_agent_playbook.str`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_playbook_view`
- `fn:features/ai_agent_playbook.py:compile_playbook`

### `_resolve_placeholders` (line 131)

**Pseudocode:**
- Set text to str(...).
- Return text.replace(...).

**Calls →**
1. `features.ai_agent_playbook.str`
2. `text.replace`

**Called by ←**
- `fn:features/ai_agent_playbook.py:compile_playbook`

### `_step_ids_from_prompt` (line 136)

**Pseudocode:**
- Set ids to a list.
- For each line in str(...).splitlines(...):
-   Set stripped to line.strip(...).
-   Set match to re.match(...).
-   If match:
-     Call ids.append(...).
- Return ids.

**Calls →**
1. `features.ai_agent_playbook.str`
2. `line.strip`
3. `re.match`
4. `ids.append`
5. `match.group`

**Called by ←**
- `fn:features/ai_agent_playbook.py:compile_playbook`

### `compile_playbook` (line 146)

**Pseudocode:**
- Set prompt to _resolve_placeholders(...).
- If prompt:
-   Set prompt to default_prompt_text(...).strip(...).
- Set system_prompt to JoinedStr.strip(...).
- Set digest to _prompt_digest(...).
- Return a dict.

**Calls →**
1. `features.ai_agent_playbook._resolve_placeholders`
2. `features.ai_agent_playbook.str`
3. `features.ai_agent_playbook.default_prompt_text`
4. `features.ai_agent_playbook._prompt_digest`
5. `features.ai_agent_playbook._step_ids_from_prompt`
6. `datetime.datetime.now`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_playbook_view`
- `fn:features/ai_agent_playbook.py:normalize_playbook`

### `normalize_playbook` (line 160)

**Pseudocode:**
- Set prompt to _extract_prompt(...).
- Set playbook to a dict.
- Set playbook[...] to compile_playbook(...).
- Set playbook[...] to True.
- Return playbook.

**Calls →**
1. `features.ai_agent_playbook._extract_prompt`
2. `features.ai_agent_playbook.compile_playbook`

**Called by ←**
- `fn:features/ai_agent_playbook.py:default_playbook`
- `fn:features/ai_agent_playbook.py:get_playbook`
- `fn:features/ai_agent_playbook.py:save_playbook`

### `_stored_record` (line 168)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `features.ai_agent_playbook.dict`

**Called by ←**
- `fn:features/ai_agent_playbook.py:_persist_playbook`

### `_playbook_view` (line 175)

**Pseudocode:**
- Set prompt to _extract_prompt(...).
- Set stored_compiled to IfExp.
- Set digest to _prompt_digest(...).
- Set ready to a boolean condition.
- If ready:
-   Set compiled to a dict.
- Else:
-   Set compiled to compile_playbook(...).

**Calls →**
1. `features.ai_agent_playbook._extract_prompt`
2. `features.ai_agent_playbook.isinstance`
3. `raw.get`
4. `features.ai_agent_playbook._prompt_digest`
5. `features.ai_agent_playbook.isinstance`
6. `features.ai_agent_playbook.str`
7. `stored_compiled.get`
8. `stored_compiled.get`
9. `features.ai_agent_playbook.str`
10. `features.ai_agent_playbook.list`
11. `stored_compiled.get`
12. `stored_compiled.get`
13. `stored_compiled.get`
14. `features.ai_agent_playbook.compile_playbook`

**Called by ←**
- `fn:features/ai_agent_playbook.py:get_playbook`

### `_persist_playbook` (line 200)

**Pseudocode:**
- Set blob to _load_blob(...).
- Set blob.setdefault(...)[...] to _stored_record(...).
- Call _save_blob(...).

**Calls →**
1. `features.ai_agent_playbook._load_blob`
2. `blob.setdefault`
3. `features.ai_agent_playbook._stored_record`
4. `features.ai_agent_playbook._save_blob`

**Called by ←**
- `fn:features/ai_agent_playbook.py:get_playbook`
- `fn:features/ai_agent_playbook.py:save_playbook`

### `_legacy_missing_compiled` (line 206)

**Pseudocode:**
- If isinstance(...):
-   Return False.
- If str(...).strip(...):
-   Return False.
- Set compiled to raw.get(...).
- Return a boolean condition.

**Calls →**
1. `features.ai_agent_playbook.isinstance`
2. `features.ai_agent_playbook.str`
3. `raw.get`
4. `raw.get`
5. `features.ai_agent_playbook.isinstance`
6. `features.ai_agent_playbook.str`
7. `compiled.get`

**Called by ←**
- `fn:features/ai_agent_playbook.py:get_playbook`

### `default_playbook` (line 215)

**Pseudocode:**
- Return normalize_playbook(...).

**Calls →**
1. `features.ai_agent_playbook.normalize_playbook`
2. `features.ai_agent_playbook.default_prompt_text`

**Called by ←**
- `fn:features/ai_agent_playbook.py:get_playbook`

### `get_playbook` (line 219)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set blob to _load_blob(...).
- Set raw to blob.get(...).get(...).
- If raw:
-   Set playbook to default_playbook(...).
-   Call _persist_playbook(...).
-   Return playbook.
- If _legacy_missing_compiled(...):

**Calls →**
1. `features.ai_agent_playbook.str`
2. `features.ai_agent_playbook._load_blob`
3. `blob.get`
4. `features.ai_agent_playbook.default_playbook`
5. `features.ai_agent_playbook._persist_playbook`
6. `features.ai_agent_playbook._legacy_missing_compiled`
7. `features.ai_agent_playbook.normalize_playbook`
8. `features.ai_agent_playbook._persist_playbook`
9. `features.ai_agent_playbook._playbook_view`
10. `features.ai_agent_playbook.ValueError`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_system_prompt`
- `fn:features/ai_agents.py:create_agent`
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/ai_voice_runtime.py:start_call_session`
- `fn:features/dialer.py:ai_agent_playbook`

### `remove_playbook` (line 240)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If agent_id:
-   Return nothing.
- Set blob to _load_blob(...).
- Set playbooks to blob.get(...).
- If a boolean condition:
-   Call _save_blob(...).

**Calls →**
1. `features.ai_agent_playbook.str`
2. `features.ai_agent_playbook._load_blob`
3. `blob.get`
4. `features.ai_agent_playbook.isinstance`
5. `features.ai_agent_playbook._save_blob`

**Called by ←**
- `fn:features/ai_agents.py:delete_agent`

### `save_playbook` (line 251)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- If agent_id:
-   Raise an error.
- If a boolean condition:
-   Set payload to payload.get(...).
- If a boolean condition:
-   Set payload to a dict.
- Else:

**Calls →**
1. `features.ai_agent_playbook.str`
2. `features.ai_agent_playbook.ValueError`
3. `features.ai_agent_playbook.isinstance`
4. `payload.get`
5. `features.ai_agent_playbook.isinstance`
6. `payload.get`
7. `features.ai_agent_playbook.len`
8. `features.ai_agent_playbook.legacy_dict_to_prompt`
9. `features.ai_agent_playbook.isinstance`
10. `features.ai_agent_playbook.isinstance`
11. `payload.get`
12. `features.ai_agent_playbook.normalize_playbook`
13. `features.ai_agent_playbook.isinstance`
14. `features.ai_agent_playbook._persist_playbook`

**Called by ←**
- `fn:features/ai_agents.py:duplicate_agent`
- `fn:features/dialer.py:save_ai_agent_playbook`
