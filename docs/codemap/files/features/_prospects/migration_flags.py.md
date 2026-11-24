# `features/_prospects/migration_flags.py`

**Purpose:** One-time CRM migration flags stored beside local CRM data.

## Functions
### `_flags_path` (line 7)

**Pseudocode:**
- Set path to Path(...).
- Set base to IfExp.
- Return base op '.crm_migrations.json'.

**Calls →**
1. `pathlib.Path`
2. `path.is_dir`

**Called by ←**
- `fn:features/_prospects/migration_flags.py:mark_migration_done`
- `fn:features/_prospects/migration_flags.py:migration_done`

### `migration_done` (line 13)

**Pseudocode:**
- Set flags_path to _flags_path(...).
- Try:
-   Set data to json.loads(...).
- On <ast.Tuple object at 0x000001E0F8E78890>:
-   Return False.
- Return bool(...).

**Calls →**
1. `features._prospects.migration_flags._flags_path`
2. `json.loads`
3. `flags_path.read_text`
4. `features._prospects.migration_flags.bool`
5. `data.get`

**Called by ←**
- `fn:features/_dialer/queue.py:_nov5_static_callback_migration_done`

### `mark_migration_done` (line 22)

**Pseudocode:**
- Set flags_path to _flags_path(...).
- Set data to a dict.
- Try:
-   If flags_path.is_file(...):
-     Set data to json.loads(...).
-     If isinstance(...):
-       Set data to a dict.
- On <ast.Tuple object at 0x000001E0F8E74150>:

**Calls →**
1. `features._prospects.migration_flags._flags_path`
2. `flags_path.is_file`
3. `json.loads`
4. `flags_path.read_text`
5. `features._prospects.migration_flags.isinstance`
6. `flags_path.parent.mkdir`
7. `flags_path.write_text`
8. `json.dumps`

**Called by ←**
- `fn:features/_dialer/queue.py:_mark_nov5_static_callback_migration_done`
