# `_web/respond.py`

**Purpose:** Response helpers shared by the app server and the Twilio hook server.

## Functions
### `log_server_fault` (line 14)

**Pseudocode:**
- Set detail to traceback.format_exc(...).
- If detail.strip(...) compared to ...:
-   Set detail to IfExp.
- Call debug_event(...).

**Calls →**
1. `traceback.format_exc`
2. `detail.strip`
3. `_web.respond.str`
4. `shared.infra.debug_event`

**Called by ←**
- `fn:_web/hooks.py:make_hook_handler`
- `fn:_web/respond.py:log_error`

### `begin_trace` (line 22)

**Pseudocode:**
- Set self._trace_t0 to time.perf_counter(...).
- Set self._trace_path to urllib.parse.urlsplit(...).path.
- Set self._trace_logged to False.
- Set self._trace_error to ''.

**Calls →**
1. `time.perf_counter`
2. `urllib.parse.parse.urlsplit`

### `finish_trace` (line 28)

**Pseudocode:**
- If getattr(...):
-   Return nothing.
- Set self._trace_logged to True.
- Set path to getattr(...).
- Set error to getattr(...).
- Set quiet to a boolean condition.
- If a boolean condition:
-   Return nothing.

**Calls →**
1. `_web.respond.getattr`
2. `_web.respond.getattr`
3. `urllib.parse.parse.urlsplit`
4. `_web.respond.getattr`
5. `path.startswith`
6. `_web.respond.int`
7. `time.perf_counter`
8. `_web.respond.getattr`
9. `time.perf_counter`
10. `shared.infra.debug_event`

**Called by ←**
- `fn:_web/respond.py:send_bytes`

### `read_body` (line 43)

**Pseudocode:**
- Set length to int(...).
- If length compared to ...:
-   Raise an error.
- Return self.rfile.read(...).

**Calls →**
1. `_web.respond.int`
2. `_web.respond.HandlerMixin.headers.get`
3. `_web.respond.ValueError`
4. `_web.respond.HandlerMixin.rfile.read`

### `read_json` (line 50)

**Pseudocode:**
- If body:
-   Return a dict.
- Set result to json.loads(...).
- If isinstance(...):
-   Raise an error.
- Return result.

**Calls →**
1. `json.loads`
2. `body.decode`
3. `_web.respond.isinstance`
4. `_web.respond.ValueError`

### `send_app_page` (line 58)

**Pseudocode:**
- Set parts to Tuple.
- Try:
-   Set chunks to a list.
-   For each part in parts:
-     With open(...):
-       Call chunks.append(...).
-   Set body to b''.join(...).
-   Set script to b'<script type="application/json" id="vocabulary">' op vocabulary_json(...).encode(...) op b'</script>'.

**Calls →**
1. `os.path.join`
2. `os.path.join`
3. `os.path.join`
4. `os.path.join`
5. `os.path.join`
6. `os.path.join`
7. `os.path.join`
8. `os.path.join`
9. `os.path.join`
10. `os.path.join`
11. `os.path.join`
12. `_web.respond.open`
13. `chunks.append`
14. `source.read`
15. `shared.vocabulary.vocabulary_json`
16. `body.replace`
17. `_web.respond.HandlerMixin.send_json`
18. `_web.respond.HandlerMixin.send_bytes`

**Called by ←**
- `fn:_web/respond.py:serve_static`

### `send_file` (line 89)

**Pseudocode:**
- Set full_path to os.path.join(...).
- Try:
-   With open(...):
-     Set body to source.read(...).
- On <ast.Name object at 0x00000242BC1B4450>:
-   Call self.send_json(...).
-   Return nothing.
- If filename.endswith(...):

**Calls →**
1. `os.path.join`
2. `_web.respond.open`
3. `source.read`
4. `_web.respond.HandlerMixin.send_json`
5. `filename.endswith`
6. `filename.endswith`
7. `filename.endswith`
8. `mimetypes.guess_type`
9. `filename.endswith`
10. `_web.respond.HandlerMixin.send_bytes`

**Called by ←**
- `fn:_web/respond.py:serve_static`

### `send_json` (line 109)

**Pseudocode:**
- Call self.send_bytes(...).

**Calls →**
1. `_web.respond.HandlerMixin.send_bytes`
2. `json.dumps`

**Called by ←**
- `fn:_web/respond.py:send_app_page`
- `fn:_web/respond.py:send_file`

### `send_bytes` (line 113)

**Pseudocode:**
- Call self.send_response(...).
- Call self.send_header(...).
- Call self.send_header(...).
- Call self.send_header(...).
- For each Tuple in a boolean condition.items(...):
-   Call self.send_header(...).
- Call self.end_headers(...).
- Call self.wfile.write(...).

**Calls →**
1. `_web.respond.HandlerMixin.send_response`
2. `_web.respond.HandlerMixin.send_header`
3. `_web.respond.HandlerMixin.send_header`
4. `_web.respond.str`
5. `_web.respond.len`
6. `_web.respond.HandlerMixin.send_header`
7. `_web.respond.HandlerMixin.send_header`
8. `_web.respond.HandlerMixin.end_headers`
9. `_web.respond.HandlerMixin.wfile.write`
10. `_web.respond.HandlerMixin.finish_trace`

**Called by ←**
- `fn:_web/respond.py:send_app_page`
- `fn:_web/respond.py:send_file`
- `fn:_web/respond.py:send_json`

### `log_error` (line 124)

**Pseudocode:**
- Call log_server_fault(...).

**Calls →**
1. `_web.respond.log_server_fault`

### `log_message` (line 127)

**Pseudocode:**
- Return nothing.

### `serve_static` (line 130)

**Pseudocode:**
- If path compared to ...:
-   Call self.send_app_page(...).
-   Return True.
- Set rel to IfExp.
- If a boolean condition:
-   Return False.
- Set root to os.path.normpath(...).
- Set full to os.path.normpath(...).

**Calls →**
1. `_web.respond.HandlerMixin.send_app_page`
2. `path.startswith`
3. `_web.respond.len`
4. `path.lstrip`
5. `rel.endswith`
6. `rel.split`
7. `os.path.normpath`
8. `os.path.normpath`
9. `os.path.join`
10. `full.startswith`
11. `os.path.isfile`
12. `_web.respond.HandlerMixin.send_file`
