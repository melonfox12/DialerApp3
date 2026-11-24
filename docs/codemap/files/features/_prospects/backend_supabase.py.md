# `features/_prospects/backend_supabase.py`

**Purpose:** Supabase prospect persistence (normalized columns).

## Routes
- `PATCH` `prospects` → `self`
- `POST` `prospects` → `None`
- `PATCH` `prospects` → `self`

## Functions
### `__init__` (line 19)

**Pseudocode:**
- Set self.client to client.
- Set self.user_id to user_id.
- Set self.lock to threading.RLock(...).
- Set self._cache to None.
- Set self.revision to 0.

**Calls →**
1. `threading.RLock`

### `bump_revision` (line 35)

**Pseudocode:**
- Call self._touch(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._touch`

### `snapshot` (line 100)

**Pseudocode:**
- With self.lock:
-   Set leads to active_leads(...).
-   Call self._expire(...).
-   Return ListComp.

**Calls →**
1. `shared.prospect_schema.active_leads`
2. `features._prospects.backend_supabase.SupabaseBackend._all`
3. `features._prospects.backend_supabase.SupabaseBackend._expire`
4. `features._prospects.backend_supabase.dict`

**Called by ←**
- `fn:features/_prospects/backend_supabase.py:csv_bytes`
- `fn:features/_prospects/backend_supabase.py:timezone_groups`

### `timezone_groups` (line 106)

**Pseudocode:**
- Set counts to a dict.
- For each lead in IfExp:
-   If lead.get(...) compared to ...:
-   Set timezone to a boolean condition.
-   Set counts[...] to counts.get(...) op 1.
- Return sorted(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend.snapshot`
2. `lead.get`
3. `lead.get`
4. `counts.get`
5. `features._prospects.backend_supabase.sorted`
6. `counts.items`

### `csv_bytes` (line 115)

**Pseudocode:**
- Return csv_bytes_for(...).

**Calls →**
1. `features._prospects.csv_export.csv_bytes_for`
2. `features._prospects.backend_supabase.SupabaseBackend.snapshot`

### `add_lead` (line 118)

**Pseudocode:**
- With self.lock:
-   Set leads to self._all(...).
-   Call self._expire(...).
-   Set lead to build_manual_lead(...).
-   Set created to self._insert(...).
-   Call leads.append(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._all`
2. `features._prospects.backend_supabase.SupabaseBackend._expire`
3. `features._prospects.csv_import.build_manual_lead`
4. `features._prospects.backend_supabase.SupabaseBackend._insert`
5. `leads.append`
6. `features._prospects.backend_supabase.SupabaseBackend._touch`
7. `features._prospects.backend_supabase.dict`

### `add_csv` (line 128)

**Pseudocode:**
- With self.lock:
-   Set leads to self._all(...).
-   Call self._expire(...).
-   Set Tuple to parse_csv(...).
-   For each lead in additions:
-     Call self._insert(...).
-   Call leads.extend(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._all`
2. `features._prospects.backend_supabase.SupabaseBackend._expire`
3. `features._prospects.csv_import.parse_csv`
4. `features._prospects.backend_supabase.SupabaseBackend._insert`
5. `leads.extend`
6. `features._prospects.backend_supabase.len`
7. `features._prospects.backend_supabase.len`
8. `shared.prospect_schema.active_leads`
9. `features._prospects.backend_supabase.SupabaseBackend._touch`

### `leads_locked` (line 142)

**Pseudocode:**
- Return self._all(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._all`

### `expire_locked` (line 145)

**Pseudocode:**
- Call self._expire(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._expire`

### `save_locked` (line 148)

**Pseudocode:**
- Set updated to self._write(...).
- Call lead.update(...).
- Set leads to self._all(...).
- For each Tuple in enumerate(...):
-   If item[...] compared to ...:
-     Set leads[...] to lead.
- Call self._touch(...).

**Calls →**
1. `features._prospects.backend_supabase.SupabaseBackend._write`
2. `lead.update`
3. `features._prospects.backend_supabase.SupabaseBackend._all`
4. `features._prospects.backend_supabase.enumerate`
5. `features._prospects.backend_supabase.SupabaseBackend._touch`

### `remove` (line 157)

**Pseudocode:**
- With self.lock:
-   Set archived_at to utc_now(...).isoformat(...).
-   Set rows to self.client.request(...).
-   If rows:
-     Raise an error.
-   If self._cache compared to ...:
-     Set self._cache to ListComp.
-   Call self._touch(...).

**Calls →**
1. `shared.infra.utc_now`
2. `features._prospects.backend_supabase.SupabaseBackend.client.request`
3. `features._prospects.backend_supabase.SupabaseBackend._scope`
4. `features._prospects.backend_supabase.KeyError`
5. `features._prospects.backend_supabase.SupabaseBackend._touch`
