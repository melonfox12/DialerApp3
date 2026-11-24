# `scripts/check_static.py`

**Purpose:** Check that static JS imports resolve, named exports exist, DOM ids exist, and linked assets exist.

## Functions
### `resolve_specifier` (line 47)

**Pseudocode:**
- Set raw to source.parent op specifier.resolve(...).
- If raw.suffix:
-   Return raw.
- For each suffix in Tuple:
-   Set candidate to raw.with_suffix(...).
-   If candidate.is_file(...):
-     Return candidate.
- Return raw.

**Calls →**
1. `raw.with_suffix`
2. `candidate.is_file`

**Called by ←**
- `fn:scripts/check_static.py:main`

### `specifier_names` (line 58)

**Pseudocode:**
- Set names to a list.
- For each part in block.split(...):
-   Set part to part.strip(...).
-   If part:
-   If ' as ' compared to ...:
-     Set Tuple to GeneratorExp.
-   Else:
-     Set original, exported to part.

**Calls →**
1. `block.split`
2. `part.strip`
3. `piece.strip`
4. `part.split`
5. `names.append`

**Called by ←**
- `fn:scripts/check_static.py:local_exports`
- `fn:scripts/check_static.py:main`

### `local_exports` (line 72)

**Pseudocode:**
- Set names to set(...).
- Call names.update(...).
- For each block in EXPORT_LIST.findall(...):
-   For each Tuple in specifier_names(...):
-     Call names.add(...).
- Return names.

**Calls →**
1. `scripts.check_static.set`
2. `EXPORT_FUNCTION.findall`
3. `names.update`
4. `EXPORT_DECL.findall`
5. `EXPORT_LIST.findall`
6. `scripts.check_static.specifier_names`
7. `names.add`

**Called by ←**
- `fn:scripts/check_static.py:main`

### `main` (line 81)

**Pseudocode:**
- Set problems to a list.
- Set js_files to a list.
- For each folder in Tuple:
-   If folder.is_dir(...):
-     Call js_files.extend(...).
- For each name in Tuple:
-   Set candidate to STATIC op name.
-   If candidate.is_file(...):

**Calls →**
1. `folder.is_dir`
2. `js_files.extend`
3. `folder.rglob`
4. `candidate.is_file`
5. `js_files.append`
6. `scripts.check_static.sorted`
7. `scripts.check_static.set`
8. `path.read_text`
9. `problems.append`
10. `path.relative_to`
11. `scripts.check_static.set`
12. `path.is_file`
13. `scripts.check_static.set`
14. `texts.get`
15. `path.read_text`
16. `stack.add`
17. `scripts.check_static.local_exports`
18. `NAMED_REEXPORT.findall`
19. `scripts.check_static.resolve_specifier`
20. `scripts.check_static.exported`
21. `scripts.check_static.specifier_names`
22. `problems.append`
23. `path.relative_to`
24. `target.relative_to`
25. `names.add`
26. `stack.remove`
27. `texts.items`
28. `IMPORT_FROM.finditer`
29. `scripts.check_static.resolve_specifier`
30. `match.group`
