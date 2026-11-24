# `features/_prospects/backend_local.py`

**Purpose:** Local JSON prospect persistence. Rules live in features.prospects.

## Functions
### `json_line_count` (line 17)

**Pseudocode:**
- Return json.dumps(...) op '\n'.count(...).

**Calls →**
1. `json.dumps`

**Called by ←**
- `fn:features/_prospects/backend_local.py:lead_chunks`

### `lead_chunks` (line 21)

**Pseudocode:**
- Set chunks to a list.
- Set current to a list.
- For each lead in leads:
-   If a boolean condition:
-     Call chunks.append(...).
-     Set current to a list.
-   Else:
-     Call current.append(...).

**Calls →**
1. `features._prospects.backend_local.json_line_count`
2. `chunks.append`
3. `current.append`
4. `chunks.append`

**Called by ←**
- `fn:features/_prospects/backend_local.py:write_lead_parts`

### `read_lead_parts` (line 35)

**Pseudocode:**
- Set leads to a list.
- For each path in sorted(...):
-   Set data to json.loads(...).
-   If isinstance(...):
-     Call leads.extend(...).
-   Else:
-     If isinstance(...):
-       Call leads.append(...).

**Calls →**
1. `features._prospects.backend_local.sorted`
2. `pathlib.Path`
3. `json.loads`
4. `path.read_text`
5. `features._prospects.backend_local.isinstance`
6. `leads.extend`
7. `features._prospects.backend_local.isinstance`
8. `leads.append`

**Called by ←**
- `fn:features/_prospects/backend_local.py:load`

### `write_lead_parts` (line 46)

**Pseudocode:**
- Set directory to Path(...).
- Call directory.mkdir(...).
- Set chunks to lead_chunks(...).
- Set written to set(...).
- For each Tuple in enumerate(...):
-   Set name to JoinedStr.
-   Set path to directory op name.
-   Set temp_path to path.with_suffix(...).

**Calls →**
1. `pathlib.Path`
2. `directory.mkdir`
3. `features._prospects.backend_local.lead_chunks`
4. `features._prospects.backend_local.set`
5. `features._prospects.backend_local.enumerate`
6. `path.with_suffix`
7. `temp_path.write_text`
8. `json.dumps`
9. `temp_path.replace`
10. `written.add`
11. `directory.glob`
12. `path.unlink`

**Called by ←**
- `fn:features/_prospects/backend_local.py:save`

### `__init__` (line 63)

**Pseudocode:**
- Set self.path to Path(...).
- Set self.lock to threading.RLock(...).
- Set self.leads to a list.
- Set self.revision to 0.
- Call self.load(...).

**Calls →**
1. `pathlib.Path`
2. `threading.RLock`
3. `features._prospects.backend_local.LocalBackend.load`

### `load` (line 73)

**Pseudocode:**
- With self.lock:
-   Try:
-     If self.path.is_dir(...):
-       Set self.leads to read_lead_parts(...).
-     Else:
-       If self.path.is_file(...):
-         Set data to json.loads(...).
-         Set self.leads to IfExp.

**Calls →**
1. `features._prospects.backend_local.LocalBackend.path.is_dir`
2. `features._prospects.backend_local.read_lead_parts`
3. `features._prospects.backend_local.LocalBackend.path.is_file`
4. `json.loads`
5. `features._prospects.backend_local.LocalBackend.path.read_text`
6. `features._prospects.backend_local.isinstance`
7. `features._prospects.backend_local.LocalBackend.expire_due`

**Called by ←**
- `fn:features/_prospects/backend_local.py:__init__`

### `save` (line 85)

**Pseudocode:**
- With self.lock:
-   If self._stores_parts(...):
-     Call write_lead_parts(...).
-   Else:
-     Call self.path.parent.mkdir(...).
-     Set temp_path to self.path.with_suffix(...).
-     Call temp_path.write_text(...).
-     Call temp_path.replace(...).

**Calls →**
1. `features._prospects.backend_local.LocalBackend._stores_parts`
2. `features._prospects.backend_local.write_lead_parts`
3. `features._prospects.backend_local.LocalBackend.path.parent.mkdir`
4. `features._prospects.backend_local.LocalBackend.path.with_suffix`
5. `temp_path.write_text`
6. `json.dumps`
7. `temp_path.replace`

**Called by ←**
- `fn:features/_prospects/backend_local.py:add_csv`
- `fn:features/_prospects/backend_local.py:add_lead`
- `fn:features/_prospects/backend_local.py:expire_due`
- `fn:features/_prospects/backend_local.py:remove`
- `fn:features/_prospects/backend_local.py:save_locked`

### `expire_due` (line 96)

**Pseudocode:**
- Set now to utc_now(...).
- Set changed to False.
- With self.lock:
-   For each lead in self.leads:
-     Set deadline to lead.get(...).
-     If a boolean condition:
-       Try:
-         Set due to datetime.fromisoformat(...).

**Calls →**
1. `shared.infra.utc_now`
2. `lead.get`
3. `lead.get`
4. `datetime.datetime.fromisoformat`
5. `features._prospects.backend_local.LocalBackend.save`

**Called by ←**
- `fn:features/_prospects/backend_local.py:add_csv`
- `fn:features/_prospects/backend_local.py:add_lead`
- `fn:features/_prospects/backend_local.py:expire_locked`
- `fn:features/_prospects/backend_local.py:load`
- `fn:features/_prospects/backend_local.py:snapshot`

### `snapshot` (line 114)

**Pseudocode:**
- Call self.expire_due(...).
- With self.lock:
-   Return ListComp.

**Calls →**
1. `features._prospects.backend_local.LocalBackend.expire_due`
2. `features._prospects.backend_local.dict`

**Called by ←**
- `fn:features/_prospects/backend_local.py:csv_bytes`
- `fn:features/_prospects/backend_local.py:timezone_groups`

### `timezone_groups` (line 119)

**Pseudocode:**
- Set counts to a dict.
- For each lead in IfExp:
-   If lead[...] compared to ...:
-   Set tz to a boolean condition.
-   Set counts[...] to counts.get(...) op 1.
- Return sorted(...).

**Calls →**
1. `features._prospects.backend_local.LocalBackend.snapshot`
2. `lead.get`
3. `counts.get`
4. `features._prospects.backend_local.sorted`
5. `counts.items`

### `csv_bytes` (line 128)

**Pseudocode:**
- Return csv_bytes_for(...).

**Calls →**
1. `features._prospects.csv_export.csv_bytes_for`
2. `features._prospects.backend_local.LocalBackend.snapshot`

### `add_lead` (line 131)

**Pseudocode:**
- With self.lock:
-   Call self.expire_due(...).
-   Set lead to build_manual_lead(...).
-   If lead.get(...):
-     Set lead[...] to str(...).
-   Call self.leads.append(...).
-   Call self.save(...).

**Calls →**
1. `features._prospects.backend_local.LocalBackend.expire_due`
2. `features._prospects.csv_import.build_manual_lead`
3. `lead.get`
4. `features._prospects.backend_local.str`
5. `uuid.uuid4`
6. `features._prospects.backend_local.LocalBackend.leads.append`
7. `features._prospects.backend_local.LocalBackend.save`
8. `features._prospects.backend_local.dict`

### `add_csv` (line 141)

**Pseudocode:**
- With self.lock:
-   Call self.expire_due(...).
-   Set Tuple to parse_csv(...).
-   For each lead in leads:
-     If lead.get(...):
-       Set lead[...] to str(...).
-   Call self.leads.extend(...).
-   Call self.save(...).

**Calls →**
1. `features._prospects.backend_local.LocalBackend.expire_due`
2. `features._prospects.csv_import.parse_csv`
3. `lead.get`
4. `features._prospects.backend_local.str`
5. `uuid.uuid4`
6. `features._prospects.backend_local.LocalBackend.leads.extend`
7. `features._prospects.backend_local.LocalBackend.save`
8. `features._prospects.backend_local.len`
9. `features._prospects.backend_local.len`
10. `shared.prospect_schema.active_leads`

### `leads_locked` (line 156)

**Pseudocode:**
- Return self.leads.

### `expire_locked` (line 159)

**Pseudocode:**
- Call self.expire_due(...).

**Calls →**
1. `features._prospects.backend_local.LocalBackend.expire_due`

### `save_locked` (line 162)

**Pseudocode:**
- For each Tuple in enumerate(...):
-   If item[...] compared to ...:
-     Set self.leads[...] to lead.
- Call self.save(...).

**Calls →**
1. `features._prospects.backend_local.enumerate`
2. `features._prospects.backend_local.LocalBackend.save`

### `bump_revision` (line 168)

**Pseudocode:**
- Update self.revision with Add 1.

### `remove` (line 171)

**Pseudocode:**
- With self.lock:
-   Set lead to next(...).
-   If lead compared to ...:
-     Raise an error.
-   Set lead[...] to utc_now(...).isoformat(...).
-   Call self.save(...).

**Calls →**
1. `features._prospects.backend_local.next`
2. `features._prospects.backend_local.KeyError`
3. `shared.infra.utc_now`
4. `features._prospects.backend_local.LocalBackend.save`
