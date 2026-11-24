# `features/_prospects/dial_records.py`

**Purpose:** Saved Total dials snapshots (records) separate from the live call log.

## Functions
### `is_dial_records_storage_lead` (line 14)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `features._prospects.dial_records.isinstance`
2. `lead.get`

**Called by ←**
- `fn:features/prospects.py:snapshot`

### `dial_records_path` (line 18)

**Pseudocode:**
- Set path to Path(...).
- If a boolean condition:
-   Return path op 'dial_records.json'.
- Return path.with_name(...).

**Calls →**
1. `pathlib.Path`
2. `path.is_dir`
3. `path.with_name`

**Called by ←**
- `fn:features/_prospects/dial_records.py:__init__`

### `_default_title` (line 25)

**Pseudocode:**
- Set stamp to datetime.now(...).strftime(...).
- Return JoinedStr.

**Calls →**
1. `datetime.datetime.now`

**Called by ←**
- `fn:features/_prospects/dial_records.py:append_record`

### `collect_active_dial_records` (line 30)
_Every row currently shown on Total dials, in archive record shape._

**Pseudocode:**
- Set rows to a list.
- Set seen to set(...).
- For each lead in a boolean condition:
-   Set log to a boolean condition.
-   For each entry in log:
-     Set record to archive_record_from_lead(...).
-     If record[...] compared to ...:
-     Call seen.add(...).

**Calls →**
1. `features._prospects.dial_records.set`
2. `lead.get`
3. `features._prospects.dial_archive.archive_record_from_lead`
4. `seen.add`
5. `rows.append`
6. `lead.get`
7. `features._prospects.dial_records.sorted`
8. `line.get`
9. `line.get`
10. `features._prospects.dial_archive.archive_record_from_lead`
11. `seen.add`
12. `rows.append`
13. `record.get`
14. `seen.add`
15. `rows.append`
16. `features._prospects.dial_records.dict`
17. `rows.sort`
18. `item.get`
19. `item.get`

**Called by ←**
- `fn:features/_prospects/dial_records.py:snapshot_active_dials`

### `snapshot_active_dials` (line 65)

**Pseudocode:**
- Set leads to crm.snapshot(...).
- Set archived to dial_archive.snapshot(...).
- Set dial_rows to collect_active_dial_records(...).
- If dial_rows:
-   Raise an error.
- Set saved to records_store.append_record(...).
- Call crm.clear_all_call_logs(...).
- Call dial_archive.replace_all(...).

**Calls →**
1. `crm.snapshot`
2. `dial_archive.snapshot`
3. `features._prospects.dial_records.collect_active_dial_records`
4. `features._prospects.dial_records.ValueError`
5. `records_store.append_record`
6. `crm.clear_all_call_logs`
7. `dial_archive.replace_all`

### `__init__` (line 78)

**Pseudocode:**
- Set self.path to dial_records_path(...).
- Set self.lock to threading.RLock(...).
- Set self.saved to a list.
- Set self.revision to 0.
- Call self.load(...).

**Calls →**
1. `features._prospects.dial_records.dial_records_path`
2. `threading.RLock`
3. `features._prospects.dial_records.LocalDialRecordsStore.load`

### `load` (line 85)

**Pseudocode:**
- With self.lock:
-   Try:
-     If self.path.is_file(...):
-       Set data to json.loads(...).
-       Set self.saved to IfExp.
-     Else:
-       Set self.saved to a list.
-   On <ast.Tuple object at 0x000001E0F8DFCA10>:

**Calls →**
1. `features._prospects.dial_records.LocalDialRecordsStore.path.is_file`
2. `json.loads`
3. `features._prospects.dial_records.LocalDialRecordsStore.path.read_text`
4. `features._prospects.dial_records.isinstance`

**Called by ←**
- `fn:features/_prospects/dial_records.py:__init__`

### `save` (line 96)

**Pseudocode:**
- With self.lock:
-   Call self.path.parent.mkdir(...).
-   Set temp_path to self.path.with_suffix(...).
-   Call temp_path.write_text(...).
-   Call temp_path.replace(...).
-   Update self.revision with Add 1.

**Calls →**
1. `features._prospects.dial_records.LocalDialRecordsStore.path.parent.mkdir`
2. `features._prospects.dial_records.LocalDialRecordsStore.path.with_suffix`
3. `temp_path.write_text`
4. `json.dumps`
5. `temp_path.replace`

**Called by ←**
- `fn:features/_prospects/dial_records.py:append_record`

### `list_summaries` (line 104)

**Pseudocode:**
- With self.lock:
-   Return ListComp.

**Calls →**
1. `item.get`
2. `item.get`
3. `features._prospects.dial_records.len`
4. `item.get`

### `get_record` (line 116)

**Pseudocode:**
- With self.lock:
-   For each item in self.saved:
-     If item.get(...) compared to ...:
-       Return a dict.
- Return None.

**Calls →**
1. `item.get`
2. `item.get`
3. `item.get`
4. `features._prospects.dial_records.len`
5. `item.get`
6. `features._prospects.dial_records.dict`
7. `item.get`

### `append_record` (line 129)

**Pseudocode:**
- Set entry to a dict.
- With self.lock:
-   Call self.saved.insert(...).
-   Call self.save(...).
- Return a dict.

**Calls →**
1. `features._prospects.dial_records.str`
2. `uuid.uuid4`
3. `features._prospects.dial_records._default_title`
4. `datetime.datetime.now`
5. `features._prospects.dial_records.dict`
6. `features._prospects.dial_records.LocalDialRecordsStore.saved.insert`
7. `features._prospects.dial_records.LocalDialRecordsStore.save`
8. `features._prospects.dial_records.len`

### `__init__` (line 148)

**Pseudocode:**
- Set self.client to client.
- Set self.user_id to user_id.
- Set self.lock to threading.RLock(...).
- Set self._cache to None.
- Set self.revision to 0.

**Calls →**
1. `threading.RLock`

### `list_summaries` (line 216)

**Pseudocode:**
- With self.lock:
-   Return ListComp.

**Calls →**
1. `item.get`
2. `item.get`
3. `features._prospects.dial_records.len`
4. `item.get`
5. `features._prospects.dial_records.SupabaseDialRecordsStore._all`

### `get_record` (line 228)

**Pseudocode:**
- With self.lock:
-   For each item in self._all(...):
-     If item.get(...) compared to ...:
-       Return a dict.
- Return None.

**Calls →**
1. `features._prospects.dial_records.SupabaseDialRecordsStore._all`
2. `item.get`
3. `item.get`
4. `item.get`
5. `features._prospects.dial_records.len`
6. `item.get`
7. `features._prospects.dial_records.dict`
8. `item.get`

### `append_record` (line 241)

**Pseudocode:**
- Set entry to a dict.
- With self.lock:
-   Set merged to list(...).
-   Call merged.insert(...).
-   Call self._save(...).
-   Set self._cache to merged.
-   Call self._touch(...).
- Return a dict.

**Calls →**
1. `features._prospects.dial_records.str`
2. `uuid.uuid4`
3. `features._prospects.dial_records._default_title`
4. `datetime.datetime.now`
5. `features._prospects.dial_records.dict`
6. `features._prospects.dial_records.list`
7. `features._prospects.dial_records.SupabaseDialRecordsStore._all`
8. `merged.insert`
9. `features._prospects.dial_records.SupabaseDialRecordsStore._save`
10. `features._prospects.dial_records.SupabaseDialRecordsStore._touch`
11. `features._prospects.dial_records.len`

### `DialRecordsStore` (line 262)

**Pseudocode:**
- If client compared to ...:
-   Return SupabaseDialRecordsStore(...).
- If a boolean condition:
-   Set crm_path to args[...].
- Return LocalDialRecordsStore(...).

**Calls →**
1. `features._prospects.dial_records.SupabaseDialRecordsStore`
2. `features._prospects.dial_records.LocalDialRecordsStore`

**Called by ←**
- `fn:features/accounts.py:configure`
- `fn:features/accounts.py:session_for`
