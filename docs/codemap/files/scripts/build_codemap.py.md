# `scripts/build_codemap.py`

**Purpose:** Build docs/codemap graph, per-file pseudocode, and bundle JSON. Does not read .env values.

## Functions
### `rel_posix` (line 59)

**Pseudocode:**
- Return path.relative_to(...).as_posix(...).

**Calls →**
1. `path.relative_to`

**Called by ←**
- `fn:scripts/build_codemap.py:build`
- `fn:scripts/build_codemap.py:parse_js`
- `fn:scripts/build_codemap.py:parse_python`
- `fn:scripts/build_codemap.py:path_for_module`
- `fn:scripts/build_codemap.py:resolve_js_import`

### `file_layer` (line 63)

**Pseudocode:**
- If rel.startswith(...):
-   Return 'browser'.
- If rel compared to ...:
-   Return 'entry'.
- If a boolean condition:
-   Return 'http'.
- If rel.startswith(...):
-   Return 'features'.

**Calls →**
1. `rel.startswith`
2. `rel.startswith`
3. `rel.startswith`
4. `rel.startswith`
5. `rel.startswith`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_js`
- `fn:scripts/build_codemap.py:parse_python`

### `collect_python_files` (line 79)

**Pseudocode:**
- Set found to a list.
- For each name in PY_ROOT_FILES:
-   Set path to ROOT op name.
-   If path.is_file(...):
-     Call found.append(...).
- For each pkg in PY_PACKAGES:
-   Set base to ROOT op pkg.
-   If base.is_dir(...):

**Calls →**
1. `path.is_file`
2. `found.append`
3. `base.is_dir`
4. `scripts.build_codemap.sorted`
5. `base.rglob`
6. `scripts.build_codemap.any`
7. `found.append`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `collect_js_files` (line 98)

**Pseudocode:**
- If JS_ROOT.is_dir(...):
-   Return a list.
- Set files to a list.
- For each path in sorted(...):
-   If any(...):
-   Call files.append(...).
- Return files.

**Calls →**
1. `JS_ROOT.is_dir`
2. `scripts.build_codemap.sorted`
3. `JS_ROOT.rglob`
4. `scripts.build_codemap.any`
5. `files.append`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `module_name_for_path` (line 109)

**Pseudocode:**
- Set rel to path.relative_to(...).
- Set parts to list(...).
- If parts[...].endswith(...):
-   Set parts[...] to parts[...][...].
- Return '.'.join(...).

**Calls →**
1. `path.relative_to`
2. `scripts.build_codemap.list`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`

### `path_for_module` (line 117)

**Pseudocode:**
- Set mod to mod.strip(...).
- If mod:
-   Return None.
- Set candidate to ROOT op Path(...).
- Set py to candidate.with_suffix(...).
- If py.is_file(...):
-   Return rel_posix(...).
- Set init_py to candidate op '__init__.py'.

**Calls →**
1. `mod.strip`
2. `pathlib.Path`
3. `mod.replace`
4. `candidate.with_suffix`
5. `py.is_file`
6. `scripts.build_codemap.rel_posix`
7. `init_py.is_file`
8. `scripts.build_codemap.rel_posix`

**Called by ←**
- `fn:scripts/build_codemap.py:build`
- `fn:scripts/build_codemap.py:parse_python`

### `stmt_pseudo` (line 158)

**Pseudocode:**
- Set pad to '  ' op depth.
- Set lines to a list.
- If isinstance(...):
-   Set val to IfExp.
-   Call lines.append(...).
- Else:
-   If isinstance(...):
-     Call lines.append(...).

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `scripts.build_codemap.describe_expr`
3. `lines.append`
4. `scripts.build_codemap.isinstance`
5. `lines.append`
6. `scripts.build_codemap.isinstance`
7. `scripts.build_codemap.describe_expr`
8. `lines.append`
9. `scripts.build_codemap.describe_expr`
10. `scripts.build_codemap.isinstance`
11. `lines.append`
12. `scripts.build_codemap.describe_expr`
13. `scripts.build_codemap.describe_expr`
14. `scripts.build_codemap.isinstance`
15. `lines.append`
16. `scripts.build_codemap.describe_expr`
17. `scripts.build_codemap.describe_expr`
18. `scripts.build_codemap.describe_expr`
19. `scripts.build_codemap.isinstance`
20. `lines.append`
21. `scripts.build_codemap.describe_expr`
22. `lines.extend`
23. `scripts.build_codemap.stmt_pseudo`
24. `lines.append`
25. `lines.extend`
26. `scripts.build_codemap.stmt_pseudo`
27. `scripts.build_codemap.isinstance`
28. `lines.append`
29. `scripts.build_codemap.describe_expr`
30. `scripts.build_codemap.describe_expr`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`
- `fn:scripts/build_codemap.py:stmt_pseudo`

### `describe_expr` (line 209)

**Pseudocode:**
- If node compared to ...:
-   Return '...'.
- If isinstance(...):
-   If a boolean condition:
-     Return repr(...).
-   Return repr(...).
- If isinstance(...):
-   Return node.id.

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `scripts.build_codemap.isinstance`
3. `scripts.build_codemap.len`
4. `scripts.build_codemap.repr`
5. `scripts.build_codemap.repr`
6. `scripts.build_codemap.isinstance`
7. `scripts.build_codemap.isinstance`
8. `scripts.build_codemap.describe_expr`
9. `scripts.build_codemap.isinstance`
10. `scripts.build_codemap.describe_call`
11. `scripts.build_codemap.isinstance`
12. `scripts.build_codemap.describe_expr`
13. `scripts.build_codemap.isinstance`
14. `scripts.build_codemap.isinstance`
15. `scripts.build_codemap.isinstance`
16. `scripts.build_codemap.describe_expr`
17. `scripts.build_codemap.isinstance`
18. `scripts.build_codemap.isinstance`
19. `scripts.build_codemap.describe_expr`
20. `scripts.build_codemap.isinstance`
21. `scripts.build_codemap.describe_expr`
22. `scripts.build_codemap.describe_expr`
23. `scripts.build_codemap.type`

**Called by ←**
- `fn:scripts/build_codemap.py:describe_call`
- `fn:scripts/build_codemap.py:describe_expr`
- `fn:scripts/build_codemap.py:stmt_pseudo`

### `describe_call` (line 239)

**Pseudocode:**
- Set func to describe_expr(...).
- Return JoinedStr.

**Calls →**
1. `scripts.build_codemap.describe_expr`

**Called by ←**
- `fn:scripts/build_codemap.py:describe_expr`
- `fn:scripts/build_codemap.py:stmt_pseudo`

### `collect_calls_in_body` (line 244)

**Pseudocode:**
- Set ordered to a list.
- For each stmt in body:
-   Call Visitor(...).visit(...).
- Return ordered.

**Calls →**
1. `scripts.build_codemap.resolve_call_target`
2. `ordered.append`
3. `self.generic_visit`
4. `scripts.build_codemap.Visitor`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`

### `resolve_call_target` (line 259)

**Pseudocode:**
- If isinstance(...):
-   Set local to func.id.
-   If local compared to ...:
-     Return imports[...].
-   Return JoinedStr.
- If isinstance(...):
-   Set chain to attr_chain(...).
-   If chain:

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `scripts.build_codemap.isinstance`
3. `scripts.build_codemap.attr_chain`
4. `scripts.build_codemap.len`

**Called by ←**
- `fn:scripts/build_codemap.py:collect_calls_in_body`

### `attr_chain` (line 279)

**Pseudocode:**
- Set parts to a list.
- Set cur to node.
- While isinstance(...):
-   Call parts.append(...).
-   Set cur to cur.value.
- If isinstance(...):
-   Call parts.append(...).
-   Call parts.reverse(...).

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `parts.append`
3. `scripts.build_codemap.isinstance`
4. `parts.append`
5. `parts.reverse`

**Called by ←**
- `fn:scripts/build_codemap.py:resolve_call_target`

### `parse_imports` (line 292)

**Pseudocode:**
- Set mapping to a dict.
- For each node in tree.body:
-   If isinstance(...):
-     For each alias in node.names:
-       Set name to a boolean condition.
-       Set mapping[...] to alias.name.
-   Else:
-     If isinstance(...):

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `alias.name.split`
3. `scripts.build_codemap.isinstance`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`

### `function_doc` (line 309)

**Pseudocode:**
- If isinstance(...):
-   Set doc to a boolean condition.
-   Return IfExp.
- Return ''.

**Calls →**
1. `scripts.build_codemap.isinstance`
2. `ast.get_docstring`
3. `doc.strip`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`

### `extract_routes_from_source` (line 316)

**Pseudocode:**
- Set routes to a list.
- For each match in ROUTE_TUPLE_RE.finditer(...):
-   Set Tuple to match.groups(...).
-   Call routes.append(...).
- Return routes.

**Calls →**
1. `ROUTE_TUPLE_RE.finditer`
2. `match.groups`
3. `routes.append`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_python`

### `parse_python` (line 331)

**Pseudocode:**
- Set rel to rel_posix(...).
- Try:
-   Set source to path.read_text(...).
- On <ast.Name object at 0x00000242BC1C21D0>:
-   Return None.
- Try:
-   Set tree to ast.parse(...).
- On <ast.Name object at 0x00000242BC1DE250>:

**Calls →**
1. `scripts.build_codemap.rel_posix`
2. `path.read_text`
3. `ast.parse`
4. `scripts.build_codemap.module_name_for_path`
5. `scripts.build_codemap.parse_imports`
6. `scripts.build_codemap.FileRecord`
7. `scripts.build_codemap.file_layer`
8. `ast.get_docstring`
9. `ast.get_docstring`
10. `imports_map.items`
11. `scripts.build_codemap.path_for_module`
12. `target.split`
13. `scripts.build_codemap.path_for_module`
14. `target.rsplit`
15. `rec.imports.append`
16. `scripts.build_codemap.extract_routes_from_source`
17. `scripts.build_codemap.isinstance`
18. `class_stack.append`
19. `scripts.build_codemap.isinstance`
20. `item.name.startswith`
21. `scripts.build_codemap.collect_calls_in_body`
22. `pseudo.extend`
23. `scripts.build_codemap.stmt_pseudo`
24. `scripts.build_codemap.len`
25. `scripts.build_codemap.FunctionInfo`
26. `scripts.build_codemap.getattr`
27. `scripts.build_codemap.function_doc`
28. `class_stack.pop`
29. `scripts.build_codemap.isinstance`
30. `scripts.build_codemap.collect_calls_in_body`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `parse_js` (line 403)

**Pseudocode:**
- Set rel to rel_posix(...).
- Try:
-   Set text to path.read_text(...).
- On <ast.Name object at 0x00000242BC3B64D0>:
-   Set text to ''.
- Set rec to FileRecord(...).
- Set m to re.search(...).
- If m:

**Calls →**
1. `scripts.build_codemap.rel_posix`
2. `path.read_text`
3. `scripts.build_codemap.FileRecord`
4. `scripts.build_codemap.file_layer`
5. `re.search`
6. `re.sub`
7. `m.group`
8. `doc.split`
9. `re.finditer`
10. `im.group`
11. `scripts.build_codemap.resolve_js_import`
12. `rec.imports.append`
13. `re.finditer`
14. `rec.exports.append`
15. `em.group`
16. `re.finditer`
17. `em.group`
18. `rec.exports.append`
19. `em.group`
20. `scripts.build_codemap.enumerate`
21. `HTTP_PATH_RE.finditer`
22. `match.group`
23. `p.startswith`
24. `rec.http_calls.append`
25. `match.start`
26. `EVENT_RE.finditer`
27. `rec.events.append`
28. `match.group`
29. `match.group`
30. `match.start`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `resolve_js_import` (line 441)

**Pseudocode:**
- Set base to ROOT op Path(...).parent.
- If spec.startswith(...):
-   Set target to base op spec.resolve(...).
-   For each ext in Tuple:
-     Set p to IfExp.
-     If p.suffix compared to ...:
-       Set p to p.with_suffix(...).
-     If a boolean condition:

**Calls →**
1. `pathlib.Path`
2. `spec.startswith`
3. `pathlib.Path`
4. `scripts.build_codemap.str`
5. `p.with_suffix`
6. `p.is_file`
7. `scripts.build_codemap.rel_posix`

**Called by ←**
- `fn:scripts/build_codemap.py:parse_js`

### `fn_node_id` (line 457)

**Pseudocode:**
- Set short to qual.split(...)[...].
- Return JoinedStr.

**Calls →**
1. `qual.split`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `build` (line 462)

**Pseudocode:**
- Set py_files to collect_python_files(...).
- Set js_files to collect_js_files(...).
- Set records to a dict.
- For each path in py_files:
-   Set rec to parse_python(...).
-   If rec:
-     Set records[...] to rec.
- For each path in js_files:

**Calls →**
1. `scripts.build_codemap.collect_python_files`
2. `scripts.build_codemap.collect_js_files`
3. `scripts.build_codemap.parse_python`
4. `scripts.build_codemap.rel_posix`
5. `scripts.build_codemap.parse_js`
6. `records.items`
7. `nodes.append`
8. `rec.functions.items`
9. `scripts.build_codemap.fn_node_id`
10. `nodes.append`
11. `edges.append`
12. `imp.get`
13. `edges.append`
14. `imp.get`
15. `imp.get`
16. `edges.append`
17. `imp.get`
18. `scripts.build_codemap.str`
19. `imp.get`
20. `scripts.build_codemap.str`
21. `imp.get`
22. `edges.append`
23. `rec.functions.items`
24. `scripts.build_codemap.fn_node_id`
25. `callee.split`
26. `scripts.build_codemap.path_for_module`
27. `scripts.build_codemap.len`
28. `scripts.build_codemap.path_for_module`
29. `edges.append`
30. `unresolved.append`

**Called by ←**
- `fn:scripts/build_codemap.py:main`

### `_pattern_match` (line 662)

**Pseudocode:**
- If '{' compared to ...:
-   Set pp to pattern.split(...).
-   Set cp to path.split(...).
-   If len(...) compared to ...:
-     Return False.
-   Return all(...).
- Return pattern compared to ....

**Calls →**
1. `pattern.split`
2. `path.split`
3. `scripts.build_codemap.len`
4. `scripts.build_codemap.len`
5. `scripts.build_codemap.all`
6. `a.startswith`
7. `a.endswith`
8. `scripts.build_codemap.zip`

**Called by ←**
- `fn:scripts/build_codemap.py:build`

### `write_file_markdown` (line 675)

**Pseudocode:**
- Call FILES_MD.mkdir(...).
- Set called_by to defaultdict(...).
- For each edge in graph[...]:
-   If edge[...] compared to ...:
-     Call called_by[...].append(...).
- For each Tuple in sorted(...):
-   Set out_path to FILES_MD op rel.
-   Call out_path.parent.mkdir(...).

**Calls →**
1. `FILES_MD.mkdir`
2. `collections.defaultdict`
3. `scripts.build_codemap.sorted`
4. `out_path.parent.mkdir`
5. `out_path.with_suffix`
6. `data.get`
7. `data.get`
8. `lines.append`
9. `lines.append`
10. `lines.append`
11. `data.get`
12. `lines.append`
13. `lines.append`
14. `lines.append`
15. `data.get`
16. `lines.append`
17. `e.get`
18. `e.get`
19. `lines.append`
20. `e.get`
21. `lines.append`
22. `lines.append`
23. `scripts.build_codemap.sorted`
24. `data.get`
25. `lines.append`
26. `fn.get`
27. `lines.append`
28. `lines.append`
29. `lines.append`
30. `fn.get`

**Called by ←**
- `fn:scripts/build_codemap.py:main`

### `main` (line 728)

**Pseudocode:**
- Set graph to build(...).
- Call OUT.mkdir(...).
- Call OUT op 'graph.json'.write_text(...).
- Set pseudocode to DictComp.
- Call OUT op 'pseudocode.json'.write_text(...).
- Call write_file_markdown(...).
- Set meta to graph[...].
- Call print(...).

**Calls →**
1. `scripts.build_codemap.build`
2. `OUT.mkdir`
3. `json.dumps`
4. `json.dumps`
5. `scripts.build_codemap.write_file_markdown`
6. `scripts.build_codemap.print`
7. `scripts.build_codemap.print`
8. `scripts.build_codemap.print`
9. `scripts.build_codemap.print`
10. `scripts.build_codemap.print`
11. `scripts.build_codemap.print`
