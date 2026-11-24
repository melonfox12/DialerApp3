# `shared/prospect_schema.py`

**Purpose:** Prospect row shape (DB snake_case), API JSON, and CSV header mapping.

## Functions
### `normalize_header` (line 164)

**Pseudocode:**
- Return re.sub(...).

**Calls →**
1. `re.sub`
2. `shared.prospect_schema.str`

**Called by ←**
- `fn:shared/prospect_schema.py:map_csv_header`

### `map_csv_header` (line 233)

**Pseudocode:**
- Set key to normalize_header(...).
- If key compared to ...:
-   Return None.
- If key compared to ...:
-   Return _HEADER_TO_FIELD[...].
- If key compared to ...:
-   Return '__score_fallback__'.
- Return None.

**Calls →**
1. `shared.prospect_schema.normalize_header`

**Called by ←**
- `fn:features/_prospects/csv_import.py:parse_csv`

### `display_name` (line 244)

**Pseudocode:**
- Return a boolean condition.

**Calls →**
1. `shared.prospect_schema.str`
2. `lead.get`
3. `shared.prospect_schema.str`
4. `lead.get`
5. `shared.prospect_schema.str`
6. `lead.get`

**Called by ←**
- `fn:features/_dialer/_call_events/pickup.py:_name`
- `fn:features/_dialer/calls.py:_create_call`
- `fn:features/_dialer/outcomes.py:end_call_with_status`
- `fn:features/_dialer/outcomes.py:log_booking`
- `fn:features/_dialer/outcomes.py:update_status`
- `fn:features/_dialer/projection.py:public_state`
- `fn:features/_dialer/queue.py:dial_lead`
- `fn:features/_dialer/queue.py:pass_next`
- `fn:features/_dialer/slots.py:_place_prospect_call`
- `fn:features/_prospects/csv_export.py:csv_bytes_for`
- `fn:features/_prospects/csv_import.py:build_manual_lead`
- `fn:features/_prospects/csv_import.py:parse_csv`
- `fn:features/_prospects/dials_csv_export.py:_row`
- `fn:features/ai_voice_runtime.py:_lead_context`

### `days_since_signal` (line 253)

**Pseudocode:**
- Set raw to lead.get(...).
- If raw:
-   Return None.
- Try:
-   If isinstance(...):
-     Set signal_day to raw.
-   Else:
-     Set signal_day to date.fromisoformat(...).

**Calls →**
1. `lead.get`
2. `shared.prospect_schema.isinstance`
3. `datetime.date.fromisoformat`
4. `shared.prospect_schema.str`
5. `datetime.datetime.now`
6. `shared.prospect_schema.max`

**Called by ←**
- `fn:features/_prospects/csv_export.py:csv_bytes_for`
- `fn:features/prospects.py:snapshot`
- `fn:shared/prospect_schema.py:row_from_db`

### `_coerce_bool` (line 268)

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
1. `shared.prospect_schema.str`

### `row_from_db` (line 279)
_Normalize a Supabase prospects row into an in-memory lead dict._

**Pseudocode:**
- If isinstance(...):
-   Raise an error.
- Set lead to DictComp.
- Set lead[...] to str(...).
- If record.get(...):
-   Set lead[...] to str(...).
- For each key in Tuple:
-   If lead.get(...) compared to ...:

**Calls →**
1. `shared.prospect_schema.isinstance`
2. `shared.prospect_schema.ValueError`
3. `record.get`
4. `shared.prospect_schema.str`
5. `record.get`
6. `record.get`
7. `shared.prospect_schema.str`
8. `lead.get`
9. `shared.prospect_schema.days_since_signal`

### `db_payload_from_lead` (line 297)

**Pseudocode:**
- Set payload to a dict.
- For each key in PROSPECT_DB_COLUMNS:
-   If key compared to ...:
-   If a boolean condition:
-   If key compared to ...:
-     If user_id:
-       Set payload[...] to user_id.
-   If key compared to ...:

**Calls →**
1. `lead.get`

### `is_archived` (line 315)

**Pseudocode:**
- Return bool(...).

**Calls →**
1. `shared.prospect_schema.bool`
2. `lead.get`

**Called by ←**
- `fn:shared/prospect_schema.py:active_leads`

### `active_leads` (line 319)

**Pseudocode:**
- Return ListComp.

**Calls →**
1. `shared.prospect_schema.is_archived`

**Called by ←**
- `fn:features/_prospects/backend_local.py:add_csv`
- `fn:features/_prospects/backend_supabase.py:add_csv`
- `fn:features/_prospects/backend_supabase.py:snapshot`
- `fn:features/prospects.py:snapshot`
