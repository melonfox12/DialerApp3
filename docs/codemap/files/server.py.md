# `server.py`

**Purpose:** Local web application and public Twilio callback servers.

## Functions
### `serve` (line 17)

**Pseudocode:**
- Call enable(...).
- Set runtime to AppRuntime(...).configure(...).
- Call maybe_start_embedded(...).
- Set app_server to QuietThreadingHTTPServer(...).
- Set hook_server to QuietThreadingHTTPServer(...).
- Call threading.Thread(...).start(...).
- Call print(...).
- Call print(...).

**Calls →**
1. `server.enable`
2. `features.accounts.AppRuntime`
3. `server.maybe_start_embedded`
4. `server.QuietThreadingHTTPServer`
5. `web.make_app_handler`
6. `server.QuietThreadingHTTPServer`
7. `_web.hooks.make_hook_handler`
8. `threading.Thread`
9. `server.print`
10. `server.print`
11. `server.print`
12. `server.print`
13. `app_server.serve_forever`
14. `accounts.append`
15. `accounts.extend`
16. `runtime.sessions.values`
17. `account.dialer.stop`
18. `app_server.shutdown`
19. `hook_server.shutdown`
20. `app_server.server_close`
21. `hook_server.server_close`
