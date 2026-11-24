# `shared/_infra/files.py`

**Purpose:** Debug log, UTC clock, and atomic JSON writes.

## Functions
### `utc_now` (line 19)

**Pseudocode:**
- Return datetime.now(...).

**Calls →**
1. `datetime.datetime.now`

### `enable` (line 23)

**Pseudocode:**
- Set _enabled to True.
- With _lock:
-   With open(...):
-     Call handle.write(...).
- Call debug_event(...).

**Calls →**
1. `shared._infra.files.open`
2. `handle.write`
3. `shared._infra.files.debug_event`

### `debug_event` (line 32)

**Pseudocode:**
- If _enabled:
-   Return nothing.
- Set stamp to datetime.now(...).strftime(...)[...].
- Set text to _redact(...).
- Set extra to _redact(...).
- Set line to JoinedStr.
- If extra:
-   Update line with Add JoinedStr.

**Calls →**
1. `datetime.datetime.now`
2. `shared._infra.files._redact`
3. `shared._infra.files._redact`
4. `shared._infra.files.str`
5. `shared._infra.files.print`
6. `shared._infra.files.open`
7. `handle.write`

**Called by ←**
- `fn:shared/_infra/files.py:enable`

### `_redact` (line 47)

**Pseudocode:**
- Set text to _SECRET.sub(...).
- Set text to _BEARER.sub(...).
- Set text to _SUPABASE_KEY.sub(...).
- Return ' '.join(...)[...].

**Calls →**
1. `_SECRET.sub`
2. `match.group`
3. `shared._infra.files.str`
4. `_BEARER.sub`
5. `_SUPABASE_KEY.sub`
6. `text.split`

**Called by ←**
- `fn:shared/_infra/files.py:debug_event`

### `write_json_atomic` (line 54)

**Pseudocode:**
- Call path.parent.mkdir(...).
- Set temp_path to path.with_suffix(...).
- Call temp_path.write_text(...).
- Call temp_path.replace(...).

**Calls →**
1. `path.parent.mkdir`
2. `path.with_suffix`
3. `temp_path.write_text`
4. `temp_path.replace`
