# `features/_prospects/csv_export.py`

**Purpose:** (no module docstring)

## Functions
### `_csv_number` (line 58)

**Pseudocode:**
- If a boolean condition:
-   Return ''.
- Return value.

**Called by ←**
- `fn:features/_prospects/csv_export.py:csv_bytes_for`

### `csv_bytes_for` (line 64)

**Pseudocode:**
- Set output to StringIO(...).
- Set writer to csv.DictWriter(...).
- Call writer.writeheader(...).
- For each lead in leads:
-   Set row to DictComp.
-   Set row[...] to _csv_number(...).
-   Set row[...] to canonical_status(...).
-   Set row[...] to a boolean condition.

**Calls →**
1. `io.StringIO`
2. `csv.DictWriter`
3. `writer.writeheader`
4. `features._prospects.csv_export._csv_number`
5. `lead.get`
6. `_HEADER_BY_KEY.items`
7. `features._prospects.csv_export._csv_number`
8. `shared.prospect_schema.days_since_signal`
9. `shared.vocabulary.canonical_status`
10. `lead.get`
11. `lead.get`
12. `lead.get`
13. `entry.get`
14. `entry.get`
15. `entry.get`
16. `lead.get`
17. `row.get`
18. `shared.prospect_schema.display_name`
19. `writer.writerow`
20. `output.getvalue`

**Called by ←**
- `fn:features/_prospects/backend_local.py:csv_bytes`
- `fn:features/_prospects/backend_supabase.py:csv_bytes`
