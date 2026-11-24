# `features/_prospects/dial_archive.py`

**Purpose:** Persist Total dials rows after CRM deletes and restore them from CSV.

## Routes
- `GET` `prospects` → `self`
- `DELETE` `dial_archive` → `self`

## Functions
### `is_dial_archive_storage_lead` (line 17)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `features._prospects.dial_archive.isinstance`
2. `lead.get`

**Called by ←**
- `fn:features/prospects.py:snapshot`

### `dial_archive_path` (line 21)

**Pseudocode:**
- Set path to Path(...).
- If a boolean condition:
-   Return path op 'dial_archive.json'.
- Return path.with_name(...).

**Calls →**
1. `pathlib.Path`
2. `path.is_dir`
3. `path.with_name`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:__init__`

### `_record_id` (line 28)

**Pseudocode:**
- Set dial_id to str(...).strip(...).
- If a boolean condition:
-   Return JoinedStr.
- Set started to str(...).strip(...).
- If a boolean condition:
-   Return JoinedStr.
- Return str(...).

**Calls →**
1. `features._prospects.dial_archive.str`
2. `features._prospects.dial_archive.str`
3. `features._prospects.dial_archive.str`
4. `uuid.uuid4`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:archive_record_from_csv_row`
- `fn:features/_prospects/dial_archive.py:archive_record_from_lead`

### `_normalize_entry` (line 38)

**Pseudocode:**
- Set item to a boolean condition.
- Set connected to item.get(...).
- If connected compared to ...:
-   Set connected to None.
- Set outcome to IfExp.
- Set duration to item.get(...).
- Set transcript_lines to item.get(...).
- Return a dict.

**Calls →**
1. `item.get`
2. `item.get`
3. `item.get`
4. `item.get`
5. `item.get`
6. `features._prospects.dial_archive.str`
7. `item.get`
8. `features._prospects.dial_archive.str`
9. `item.get`
10. `features._prospects.dial_archive.str`
11. `item.get`
12. `features._prospects.dial_archive.str`
13. `item.get`
14. `features._prospects.dial_archive.str`
15. `item.get`
16. `features._prospects.dial_archive.int`
17. `features._prospects.dial_archive.int`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:_entry_from_csv_row`
- `fn:features/_prospects/dial_archive.py:archive_record_from_lead`

### `archive_record_from_lead` (line 59)

**Pseudocode:**
- Set lead_id to a boolean condition.
- Set normalized to _normalize_entry(...).
- Return a dict.

**Calls →**
1. `lead.get`
2. `features._prospects.dial_archive._normalize_entry`
3. `features._prospects.dial_archive._record_id`
4. `lead.get`
5. `lead.get`
6. `lead.get`
7. `lead.get`
8. `lead.get`
9. `shared.vocabulary.canonical_status`
10. `lead.get`
11. `features._prospects.dial_archive.dict`
12. `lead.get`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:archive_lead`
- `fn:features/_prospects/dial_records.py:collect_active_dial_records`

### `_parse_transcript_cell` (line 76)

**Pseudocode:**
- Set segments to a list.
- For each line in a boolean condition.splitlines(...):
-   Set stripped to line.strip(...).
-   If stripped:
-   Set match to re.match(...).
-   If match:
-   Set speaker to match.group(...).
- Return segments.

**Calls →**
1. `line.strip`
2. `re.match`
3. `match.group`
4. `segments.append`
5. `match.group`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:archive_record_from_csv_row`

### `_connected_from_csv` (line 97)

**Pseudocode:**
- If value compared to ...:
-   Return True.
- If value compared to ...:
-   Return False.
- Return None.

**Called by ←**
- `fn:features/_prospects/dial_archive.py:_entry_from_csv_row`

### `_entry_from_csv_row` (line 105)

**Pseudocode:**
- Set duration to row.get(...).
- Set transcript_lines to row.get(...).
- Set outcome to a boolean condition.
- If a boolean condition:
-   Set outcome to None.
- Return _normalize_entry(...).

**Calls →**
1. `row.get`
2. `row.get`
3. `row.get`
4. `features._prospects.dial_archive._normalize_entry`
5. `row.get`
6. `row.get`
7. `row.get`
8. `row.get`
9. `row.get`
10. `row.get`
11. `features._prospects.dial_archive._connected_from_csv`
12. `row.get`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:_import_csv_bytes`
- `fn:features/_prospects/dial_archive.py:archive_record_from_csv_row`

### `archive_record_from_csv_row` (line 124)

**Pseudocode:**
- Set lead_id to a boolean condition.
- Set entry to _entry_from_csv_row(...).
- Set reviews to row.get(...).
- Set review_count to IfExp.
- Set transcript to _parse_transcript_cell(...).
- Return a dict.

**Calls →**
1. `features._prospects.dial_archive.str`
2. `row.get`
3. `uuid.uuid4`
4. `features._prospects.dial_archive._entry_from_csv_row`
5. `row.get`
6. `features._prospects.dial_archive.int`
7. `features._prospects.dial_archive._parse_transcript_cell`
8. `row.get`
9. `entry.get`
10. `features._prospects.dial_archive._record_id`
11. `row.get`
12. `row.get`
13. `row.get`
14. `row.get`
15. `shared.vocabulary.canonical_status`
16. `row.get`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:_import_csv_bytes`

### `pseudo_lead_from_archive` (line 144)

**Pseudocode:**
- Return a dict.

**Calls →**
1. `record.get`
2. `record.get`
3. `record.get`
4. `record.get`
5. `record.get`
6. `record.get`
7. `record.get`
8. `record.get`
9. `features._prospects.dial_archive.dict`
10. `record.get`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:dials_export_rows`

### `__init__` (line 160)

**Pseudocode:**
- Set self.path to dial_archive_path(...).
- Set self.lock to threading.RLock(...).
- Set self.records to a list.
- Set self.revision to 0.
- Call self.load(...).

**Calls →**
1. `features._prospects.dial_archive.dial_archive_path`
2. `threading.RLock`
3. `features._prospects.dial_archive.LocalDialArchiveStore.load`

### `load` (line 167)

**Pseudocode:**
- With self.lock:
-   Try:
-     If self.path.is_file(...):
-       Set data to json.loads(...).
-       Set self.records to IfExp.
-     Else:
-       Set self.records to a list.
-   On <ast.Tuple object at 0x000001E0F8E87DD0>:

**Calls →**
1. `features._prospects.dial_archive.LocalDialArchiveStore.path.is_file`
2. `json.loads`
3. `features._prospects.dial_archive.LocalDialArchiveStore.path.read_text`
4. `features._prospects.dial_archive.isinstance`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:__init__`

### `save` (line 178)

**Pseudocode:**
- With self.lock:
-   Call self.path.parent.mkdir(...).
-   Set temp_path to self.path.with_suffix(...).
-   Call temp_path.write_text(...).
-   Call temp_path.replace(...).
-   Update self.revision with Add 1.

**Calls →**
1. `features._prospects.dial_archive.LocalDialArchiveStore.path.parent.mkdir`
2. `features._prospects.dial_archive.LocalDialArchiveStore.path.with_suffix`
3. `temp_path.write_text`
4. `json.dumps`
5. `temp_path.replace`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:replace_all`
- `fn:features/_prospects/dial_archive.py:upsert_many`

### `snapshot` (line 186)

**Pseudocode:**
- With self.lock:
-   Return ListComp.

**Calls →**
1. `features._prospects.dial_archive.dict`

### `upsert_many` (line 190)

**Pseudocode:**
- If records:
-   Return 0.
- Set added to 0.
- With self.lock:
-   Set by_id to DictComp.
-   For each record in records:
-     If record[...] compared to ...:
-     Set by_id[...] to dict(...).

**Calls →**
1. `features._prospects.dial_archive.dict`
2. `features._prospects.dial_archive.list`
3. `by_id.values`
4. `features._prospects.dial_archive.LocalDialArchiveStore.save`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:archive_lead`
- `fn:features/_prospects/dial_archive.py:upsert_many`

### `replace_all` (line 206)

**Pseudocode:**
- With self.lock:
-   Set self.records to ListComp.
-   Call self.save(...).

**Calls →**
1. `features._prospects.dial_archive.dict`
2. `features._prospects.dial_archive.LocalDialArchiveStore.save`

### `archive_lead` (line 211)

**Pseudocode:**
- Set records to a list.
- Set log to a boolean condition.
- For each entry in log:
-   Call records.append(...).
- If a boolean condition:
-   Set stamps to sorted(...).
-   Set stub to a dict.
-   Call records.append(...).

**Calls →**
1. `lead.get`
2. `records.append`
3. `features._prospects.dial_archive.archive_record_from_lead`
4. `lead.get`
5. `features._prospects.dial_archive.sorted`
6. `line.get`
7. `line.get`
8. `records.append`
9. `features._prospects.dial_archive.archive_record_from_lead`
10. `features._prospects.dial_archive.LocalDialArchiveStore.upsert_many`

### `import_csv_bytes` (line 222)

**Pseudocode:**
- Return _import_csv_bytes(...).

**Calls →**
1. `features._prospects.dial_archive._import_csv_bytes`

### `__init__` (line 227)

**Pseudocode:**
- Set self.client to client.
- Set self.user_id to user_id.
- Set self.lock to threading.RLock(...).
- Set self._cache to None.
- Set self.revision to 0.
- Set self._use_blob to None.

**Calls →**
1. `threading.RLock`

### `snapshot` (line 311)

**Pseudocode:**
- With self.lock:
-   Return ListComp.

**Calls →**
1. `features._prospects.dial_archive.dict`
2. `features._prospects.dial_archive.SupabaseDialArchiveStore._all`

### `upsert_many` (line 315)

**Pseudocode:**
- If records:
-   Return 0.
- With self.lock:
-   Set existing to SetComp.
-   Set additions to ListComp.
-   If additions:
-     Return 0.
-   If self._use_blob:

**Calls →**
1. `features._prospects.dial_archive.SupabaseDialArchiveStore._all`
2. `features._prospects.dial_archive.dict`
3. `features._prospects.dial_archive.list`
4. `features._prospects.dial_archive.SupabaseDialArchiveStore._all`
5. `merged.extend`
6. `features._prospects.dial_archive.SupabaseDialArchiveStore._save_blob`
7. `features._prospects.dial_archive.SupabaseDialArchiveStore._touch`
8. `features._prospects.dial_archive.len`
9. `features._prospects.dial_archive.range`
10. `features._prospects.dial_archive.len`
11. `features._prospects.dial_archive.SupabaseDialArchiveStore.client.request`
12. `features._prospects.dial_archive.SupabaseDialArchiveStore._table_missing`
13. `features._prospects.dial_archive.SupabaseDialArchiveStore.upsert_many`
14. `features._prospects.dial_archive.SupabaseDialArchiveStore._touch`
15. `features._prospects.dial_archive.len`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:archive_lead`
- `fn:features/_prospects/dial_archive.py:upsert_many`

### `replace_all` (line 354)

**Pseudocode:**
- With self.lock:
-   Set cleaned to ListComp.
-   If self._use_blob:
-     Call self._save_blob(...).
-     Set self._cache to cleaned.
-     Call self._touch(...).
-     Return nothing.
-   Try:

**Calls →**
1. `features._prospects.dial_archive.dict`
2. `features._prospects.dial_archive.SupabaseDialArchiveStore._save_blob`
3. `features._prospects.dial_archive.SupabaseDialArchiveStore._touch`
4. `features._prospects.dial_archive.SupabaseDialArchiveStore.client.select_all`
5. `features._prospects.dial_archive.SupabaseDialArchiveStore._scope`
6. `row.get`
7. `features._prospects.dial_archive.SupabaseDialArchiveStore.client.request`
8. `features._prospects.dial_archive.SupabaseDialArchiveStore._scope`
9. `features._prospects.dial_archive.range`
10. `features._prospects.dial_archive.len`
11. `features._prospects.dial_archive.SupabaseDialArchiveStore.client.request`
12. `features._prospects.dial_archive.SupabaseDialArchiveStore._touch`
13. `features._prospects.dial_archive.SupabaseDialArchiveStore._table_missing`
14. `features._prospects.dial_archive.SupabaseDialArchiveStore._save_blob`
15. `features._prospects.dial_archive.SupabaseDialArchiveStore._touch`

### `archive_lead` (line 396)

**Pseudocode:**
- Set records to a list.
- Set log to a boolean condition.
- For each entry in log:
-   Call records.append(...).
- If a boolean condition:
-   Set stamps to sorted(...).
-   Set stub to a dict.
-   Call records.append(...).

**Calls →**
1. `lead.get`
2. `records.append`
3. `features._prospects.dial_archive.archive_record_from_lead`
4. `lead.get`
5. `features._prospects.dial_archive.sorted`
6. `line.get`
7. `line.get`
8. `records.append`
9. `features._prospects.dial_archive.archive_record_from_lead`
10. `features._prospects.dial_archive.SupabaseDialArchiveStore.upsert_many`

### `import_csv_bytes` (line 407)

**Pseudocode:**
- Return _import_csv_bytes(...).

**Calls →**
1. `features._prospects.dial_archive._import_csv_bytes`

### `_import_csv_bytes` (line 411)

**Pseudocode:**
- Set text to IfExp.
- Set reader to csv.DictReader(...).
- If reader.fieldnames:
-   Raise an error.
- If a boolean condition:
-   Raise an error.
- Set archived to a list.
- Set added_to_crm to 0.

**Calls →**
1. `features._prospects.dial_archive.isinstance`
2. `data.decode`
3. `features._prospects.dial_archive.str`
4. `csv.DictReader`
5. `io.StringIO`
6. `features._prospects.dial_archive.ValueError`
7. `features._prospects.dial_archive.ValueError`
8. `crm.snapshot`
9. `features._prospects.dial_archive.str`
10. `row.get`
11. `features._prospects.dial_archive._entry_from_csv_row`
12. `leads_by_id.get`
13. `entry.get`
14. `features._prospects.dial_archive.any`
15. `item.get`
16. `lead.get`
17. `crm.append_call_log`
18. `archived.append`
19. `features._prospects.dial_archive.archive_record_from_csv_row`
20. `store.upsert_many`
21. `features._prospects.dial_archive.len`
22. `store.snapshot`

**Called by ←**
- `fn:features/_prospects/dial_archive.py:import_csv_bytes`

### `DialArchiveStore` (line 450)

**Pseudocode:**
- If client compared to ...:
-   Return SupabaseDialArchiveStore(...).
- If a boolean condition:
-   Set crm_path to args[...].
- Return LocalDialArchiveStore(...).

**Calls →**
1. `features._prospects.dial_archive.SupabaseDialArchiveStore`
2. `features._prospects.dial_archive.LocalDialArchiveStore`

**Called by ←**
- `fn:features/accounts.py:configure`
- `fn:features/accounts.py:session_for`

### `dials_export_rows` (line 458)

**Pseudocode:**
- Set rows to _rows_for_leads(...).
- For each record in a boolean condition:
-   Call rows.append(...).
- Call rows.sort(...).
- Return rows.

**Calls →**
1. `features._prospects.dial_archive._rows_for_leads`
2. `rows.append`
3. `features._prospects.dial_archive._row`
4. `features._prospects.dial_archive.pseudo_lead_from_archive`
5. `record.get`
6. `rows.sort`
