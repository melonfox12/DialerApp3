# `features/_prospects/dials_csv_export.py`

**Purpose:** CSV export for the Total dials call log (one row per call_log entry).

## Functions
### `_dial_when` (line 33)

**Pseudocode:**
- Return str(...).

**Calls →**
1. `features._prospects.dials_csv_export.str`
2. `entry.get`
3. `entry.get`

**Called by ←**
- `fn:features/_prospects/dials_csv_export.py:_row`

### `_transcript_display_time` (line 37)

**Pseudocode:**
- If value:
-   Return 'Time unavailable'.
- Try:
-   Set moment to datetime.fromisoformat(...).
- On <ast.Tuple object at 0x000001E0F8E76110>:
-   Return 'Time unavailable'.
- If moment.tzinfo compared to ...:
-   Set moment to moment.replace(...).

**Calls →**
1. `datetime.datetime.fromisoformat`
2. `features._prospects.dials_csv_export.str`
3. `moment.replace`
4. `moment.astimezone`
5. `moment.strftime`

**Called by ←**
- `fn:features/_prospects/dials_csv_export.py:_transcript_csv_cell`

### `_transcript_csv_cell` (line 51)

**Pseudocode:**
- Set ordered to sorted(...).
- Set lines to a list.
- For each entry in ordered:
-   Set speaker to a boolean condition.
-   Set stamp to _transcript_display_time(...).
-   Set text to a boolean condition.
-   Call lines.append(...).
- Return '\n'.join(...).

**Calls →**
1. `features._prospects.dials_csv_export.sorted`
2. `features._prospects.dials_csv_export.str`
3. `item.get`
4. `entry.get`
5. `features._prospects.dials_csv_export._transcript_display_time`
6. `entry.get`
7. `entry.get`
8. `lines.append`

**Called by ←**
- `fn:features/_prospects/dials_csv_export.py:_row`

### `_rows_for_leads` (line 62)

**Pseudocode:**
- Set rows to a list.
- For each lead in a boolean condition:
-   Set lead_id to lead.get(...).
-   If lead_id:
-   Set log to a boolean condition.
-   For each entry in log:
-     Call rows.append(...).
-   If a boolean condition:

**Calls →**
1. `lead.get`
2. `lead.get`
3. `rows.append`
4. `features._prospects.dials_csv_export._row`
5. `lead.get`
6. `features._prospects.dials_csv_export.sorted`
7. `line.get`
8. `line.get`
9. `rows.append`
10. `features._prospects.dials_csv_export._row`
11. `rows.sort`

### `_row` (line 79)

**Pseudocode:**
- Set reviews to lead.get(...).
- Set connected to entry.get(...).
- If connected compared to ...:
-   Set connected_text to 'true'.
- Else:
-   If connected compared to ...:
-     Set connected_text to 'false'.
-   Else:

**Calls →**
1. `lead.get`
2. `entry.get`
3. `features._prospects.dials_csv_export._dial_when`
4. `lead.get`
5. `lead.get`
6. `lead.get`
7. `shared.prospect_schema.display_name`
8. `features._prospects.dials_csv_export._transcript_csv_cell`
9. `lead.get`
10. `shared.vocabulary.canonical_status`
11. `lead.get`
12. `lead.get`
13. `lead.get`
14. `features._prospects.dials_csv_export.str`
15. `entry.get`
16. `features._prospects.dials_csv_export.str`
17. `entry.get`
18. `features._prospects.dials_csv_export.str`
19. `entry.get`
20. `features._prospects.dials_csv_export.str`
21. `entry.get`
22. `features._prospects.dials_csv_export.str`
23. `entry.get`
24. `entry.get`
25. `entry.get`
26. `entry.get`
27. `entry.get`
28. `features._prospects.dials_csv_export.str`
29. `entry.get`

**Called by ←**
- `fn:features/_prospects/dials_csv_export.py:_rows_for_leads`

### `dials_csv_bytes_for` (line 110)

**Pseudocode:**
- Set output to StringIO(...).
- Set writer to csv.DictWriter(...).
- Call writer.writeheader(...).
- For each row in dials_export_rows(...):
-   Call writer.writerow(...).
- Return output.getvalue(...).encode(...).

**Calls →**
1. `io.StringIO`
2. `csv.DictWriter`
3. `writer.writeheader`
4. `features._prospects.dials_csv_export.dials_export_rows`
5. `writer.writerow`
6. `output.getvalue`
