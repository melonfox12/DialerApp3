# `_web/hooks.py`

**Purpose:** Twilio callback routes on port 8765.

## Functions
### `make_hook_handler` (line 12)

**Pseudocode:**
- Return HookHandler.

**Calls →**
1. `self.dispatch`
2. `_web.hooks.int`
3. `self.headers.get`
4. `self.send_response`
5. `self.end_headers`
6. `self.rfile.read`
7. `urllib.parse.parse.parse_qs`
8. `self.dispatch`
9. `urllib.parse.parse.urlsplit`
10. `params.get`
11. `params.get`
12. `_web.hooks.len`
13. `runtime.tokens.lookup`
14. `urllib.parse.parse.urlsplit`
15. `urllib.parse.parse.parse_qs`
16. `query.items`
17. `params.update`
18. `parsed.path.strip`
19. `time.perf_counter`
20. `self.resolve_dialer`
21. `dialer.validate_webhook`
22. `self.headers.get`
23. `dialer.record_activity`
24. `dialer.record_activity`
25. `dialer.handle_client_voice`
26. `_web.hooks.len`
27. `dialer.handle_webhook`
28. `shared.infra.debug_event`
29. `traceback.format_exc`
30. `_web.hooks.int`

**Called by ←**
- `fn:server.py:serve`
