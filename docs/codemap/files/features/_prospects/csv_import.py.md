# `features/_prospects/csv_import.py`

**Purpose:** CSV import and manual prospect construction for the normalized prospect schema.

## Functions
### `_phone` (line 22)

**Pseudocode:**
- Set text to str(...).strip(...).
- Set text to re.sub(...).
- Set text to re.sub(...).
- Set scientific to SCIENTIFIC_NUMBER.match(...).
- If scientific:
-   If len(...) compared to ...:
-     Return None.
-   Try:

**Calls →**
1. `features._prospects.csv_import.str`
2. `re.sub`
3. `re.sub`
4. `SCIENTIFIC_NUMBER.match`
5. `features._prospects.csv_import.len`
6. `scientific.group`
7. `scientific.group`
8. `features._prospects.csv_import.int`
9. `scientific.group`
10. `features._prospects.csv_import.str`
11. `features._prospects.csv_import.int`
12. `decimal.Decimal`
13. `re.fullmatch`
14. `text.split`
15. `re.fullmatch`
16. `re.sub`
17. `text.startswith`
18. `features._prospects.csv_import.len`
19. `text.startswith`
20. `features._prospects.csv_import.len`
21. `features._prospects.csv_import.len`
22. `features._prospects.csv_import.len`
23. `digits.startswith`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`
- `fn:features/_prospects/csv_import.py:build_manual_lead`
- `fn:features/_prospects/csv_import.py:update_lead_fields`

### `_timezone` (line 50)

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   Return None.
- Set lower to text.lower(...).
- Set alias to a boolean condition.
- If alias:
-   Return alias.
- For each Tuple in Tuple:

**Calls →**
1. `features._prospects.csv_import.str`
2. `text.lower`
3. `shared.vocabulary.TIMEZONE_ALIASES.get`
4. `shared.vocabulary.TIMEZONE_ALIASES.get`
5. `lower.replace`
6. `TIMEZONE_ABBREVIATION.search`
7. `shared.vocabulary.TIMEZONE_ALIASES.get`
8. `abbrev.group`
9. `re.fullmatch`
10. `re.search`
11. `offset.group`
12. `features._prospects.csv_import.int`
13. `offset.group`
14. `shared.vocabulary.UTC_OFFSET_ZONES.get`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`
- `fn:features/_prospects/csv_import.py:build_manual_lead`

### `_text` (line 79)

**Pseudocode:**
- Set text to str(...).strip(...).
- If len(...) compared to ...:
-   Raise an error.
- Return text.

**Calls →**
1. `features._prospects.csv_import.str`
2. `features._prospects.csv_import.len`
3. `features._prospects.csv_import.ValueError`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`
- `fn:features/_prospects/csv_import.py:_state_code`
- `fn:features/_prospects/csv_import.py:build_manual_lead`

### `_state_code` (line 86)

**Pseudocode:**
- Set text to _text(...).upper(...).
- If text:
-   Return ''.
- If a boolean condition:
-   Return text.
- Return IfExp.

**Calls →**
1. `features._prospects.csv_import._text`
2. `features._prospects.csv_import.len`
3. `text.isalpha`
4. `features._prospects.csv_import.len`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`

### `_tier` (line 95)

**Pseudocode:**
- Set text to str(...).strip(...).upper(...).
- Return IfExp.

**Calls →**
1. `features._prospects.csv_import.str`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`

### `_score` (line 100)

**Pseudocode:**
- Set text to str(...).strip(...).replace(...).
- If text:
-   Return None.
- Try:
-   Set number to Decimal(...).
- On <ast.Name object at 0x00000242BC293950>:
-   Return None.
- If number.is_finite(...):

**Calls →**
1. `features._prospects.csv_import.str`
2. `decimal.Decimal`
3. `number.is_finite`
4. `features._prospects.csv_import.float`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`

### `_date` (line 113)

**Pseudocode:**
- Set text to str(...).strip(...).
- If text:
-   Return None.
- If a boolean condition:
-   Try:
-     Return date.fromisoformat(...).
-   On <ast.Name object at 0x00000242BC13A5D0>:
-     No-op.

**Calls →**
1. `features._prospects.csv_import.str`
2. `features._prospects.csv_import.len`
3. `datetime.date.fromisoformat`
4. `re.search`
5. `datetime.date`
6. `features._prospects.csv_import.int`
7. `match.group`
8. `features._prospects.csv_import.int`
9. `match.group`
10. `features._prospects.csv_import.int`
11. `match.group`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`

### `_choose_dialect` (line 131)

**Pseudocode:**
- Set sample to text[...].
- Try:
-   Set dialect to csv.Sniffer(...).sniff(...).
- On <ast.Attribute object at 0x00000242BC210D90>:
-   Return csv.excel.
- Set first to next(...).
- If a boolean condition:
-   Return csv.excel.

**Calls →**
1. `csv.Sniffer`
2. `features._prospects.csv_import.next`
3. `sample.splitlines`
4. `line.strip`
5. `first.count`
6. `first.count`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_read_csv`

### `_read_csv` (line 143)

**Pseudocode:**
- If isinstance(...):
-   Set text to data.
- Else:
-   Set payload to bytes(...).replace(...).
-   Set text to None.
-   For each encoding in Tuple:
-     Try:
-       Set text to payload.decode(...).

**Calls →**
1. `features._prospects.csv_import.isinstance`
2. `features._prospects.csv_import.bytes`
3. `payload.decode`
4. `payload.decode`
5. `text.replace`
6. `features._prospects.csv_import._choose_dialect`
7. `cell.strip`
8. `csv.reader`
9. `io.StringIO`
10. `features._prospects.csv_import.any`
11. `cell.strip`

**Called by ←**
- `fn:features/_prospects/csv_import.py:parse_csv`

### `_blank_lead` (line 164)

**Pseudocode:**
- Return a dict.

**Called by ←**
- `fn:features/_prospects/csv_import.py:build_manual_lead`
- `fn:features/_prospects/csv_import.py:parse_csv`

### `_assign_field` (line 212)

**Pseudocode:**
- If field compared to ...:
-   Set phone to _phone(...).
-   If a boolean condition:
-     Set lead[...] to phone.
-   Else:
-     If a boolean condition:
-       Set lead[...] to phone.
-   Return nothing.

**Calls →**
1. `features._prospects.csv_import._phone`
2. `lead.get`
3. `lead.get`
4. `lead.get`
5. `features._prospects.csv_import._text`
6. `lead.get`
7. `features._prospects.csv_import._score`
8. `lead.get`
9. `features._prospects.csv_import.str`
10. `features._prospects.csv_import._tier`
11. `features._prospects.csv_import._date`
12. `parsed.isoformat`
13. `features._prospects.csv_import._state_code`
14. `features._prospects.csv_import._timezone`
15. `features._prospects.csv_import._coerce_bool_field`
16. `features._prospects.csv_import._text`

**Called by ←**
- `fn:features/_prospects/csv_import.py:build_manual_lead`
- `fn:features/_prospects/csv_import.py:parse_csv`
- `fn:features/_prospects/csv_import.py:update_lead_fields`

### `_coerce_bool_field` (line 254)

**Pseudocode:**
- If a boolean condition:
-   Return None.
- Set text to str(...).strip(...).lower(...).
- If text compared to ...:
-   Return True.
- If text compared to ...:
-   Return False.
- Return None.

**Calls →**
1. `features._prospects.csv_import.str`

**Called by ←**
- `fn:features/_prospects/csv_import.py:_assign_field`

### `parse_csv` (line 265)

**Pseudocode:**
- Set rows to _read_csv(...).
- If rows:
-   Return Tuple.
- Set headers to rows[...].
- Set records to rows[...].
- Set columns to ListComp.
- Set mapped to a list.
- For each header in headers:

**Calls →**
1. `features._prospects.csv_import._read_csv`
2. `features._prospects.csv_import.str`
3. `shared.prospect_schema.map_csv_header`
4. `mapped.append`
5. `features._prospects.csv_import.set`
6. `features._prospects.csv_import._blank_lead`
7. `features._prospects.csv_import.enumerate`
8. `features._prospects.csv_import.len`
9. `features._prospects.csv_import.str`
10. `features._prospects.csv_import._assign_field`
11. `lead.get`
12. `features._prospects.csv_import._assign_field`
13. `lead.get`
14. `seen.add`
15. `lead.get`
16. `lead.get`
17. `shared.prospect_schema.display_name`
18. `lead.get`
19. `leads.append`

**Called by ←**
- `fn:features/_prospects/backend_local.py:add_csv`
- `fn:features/_prospects/backend_supabase.py:add_csv`

### `build_manual_lead` (line 309)

**Pseudocode:**
- If isinstance(...):
-   Raise an error.
- Set lead to _blank_lead(...).
- Set allowed to set(...) op Set.
- For each key in allowed:
-   If key compared to ...:
-     Call _assign_field(...).
- Set phone to _phone(...).

**Calls →**
1. `features._prospects.csv_import.isinstance`
2. `features._prospects.csv_import.ValueError`
3. `features._prospects.csv_import._blank_lead`
4. `features._prospects.csv_import.set`
5. `features._prospects.csv_import._blank_lead`
6. `features._prospects.csv_import._assign_field`
7. `features._prospects.csv_import._phone`
8. `payload.get`
9. `features._prospects.csv_import.ValueError`
10. `features._prospects.csv_import.set`
11. `features._prospects.csv_import.ValueError`
12. `shared.vocabulary.parse_prospect_status`
13. `features._prospects.csv_import.str`
14. `payload.get`
15. `features._prospects.csv_import.ValueError`
16. `features._prospects.csv_import._timezone`
17. `payload.get`
18. `lead.get`
19. `features._prospects.csv_import._text`
20. `payload.get`
21. `shared.prospect_schema.display_name`
22. `lead.get`
23. `features._prospects.csv_import._text`
24. `payload.get`
25. `shared.infra.utc_now`
26. `datetime.timedelta`
27. `shared.infra.utc_now`

**Called by ←**
- `fn:features/_prospects/backend_local.py:add_lead`
- `fn:features/_prospects/backend_supabase.py:add_lead`

### `update_lead_fields` (line 340)

**Pseudocode:**
- If isinstance(...):
-   Raise an error.
- Set changed to False.
- If 'phone' compared to ...:
-   Set phone to _phone(...).
-   If phone:
-     Raise an error.
-   If phone compared to ...:

**Calls →**
1. `features._prospects.csv_import.isinstance`
2. `features._prospects.csv_import.ValueError`
3. `features._prospects.csv_import._phone`
4. `payload.get`
5. `features._prospects.csv_import.ValueError`
6. `features._prospects.csv_import.set`
7. `features._prospects.csv_import.ValueError`
8. `lead.get`
9. `payload.items`
10. `lead.get`
11. `features._prospects.csv_import._assign_field`
12. `lead.get`
13. `features._prospects.csv_import.ValueError`

**Called by ←**
- `fn:features/prospects.py:update_fields`

### `apply_pitch_segment_from_fields` (line 368)

**Pseudocode:**
- Return False.

### `apply_business_type_default_to_lead` (line 372)

**Pseudocode:**
- Return False.
