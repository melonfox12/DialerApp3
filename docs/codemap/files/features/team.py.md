# `features/team.py`

**Purpose:** Manager team roster, metrics, live snapshots, and presence.

## Routes
- `GET` `/api/team/roster` → `get_roster`
- `GET` `/api/team/members/{user_id}/metrics` → `get_member_metrics`
- `GET` `/api/team/members/{user_id}/live` → `get_member_live`
- `POST` `/api/team/invites` → `post_invite`

## Functions
### `maybe_record_presence` (line 11)

**Pseudocode:**
- Set client to getattr(...).
- Set user_id to getattr(...).
- Set membership to a boolean condition.
- Set org_id to membership.get(...).
- If a boolean condition:
-   Return nothing.
- Set now to time.monotonic(...).
- Set last to float(...).

**Calls →**
1. `features.team.getattr`
2. `features.team.getattr`
3. `features.team.getattr`
4. `membership.get`
5. `time.monotonic`
6. `features.team.float`
7. `features.team.getattr`
8. `features.team.isinstance`
9. `live_payload.get`
10. `features.org_storage.upsert_presence`
11. `features.team.bool`
12. `live_payload.get`
13. `features.team.bool`
14. `live_payload.get`
15. `live_payload.get`
16. `live_payload.get`
17. `features.team.isinstance`
18. `features.team.len`

### `_member_contact` (line 33)

**Pseudocode:**
- Set profile to a boolean condition.
- Set email to a boolean condition.
- Set display to IfExp.
- Return a dict.

**Calls →**
1. `profiles.get`
2. `features.team.str`
3. `profile.get`
4. `member_row.get`
5. `profile.get`
6. `email.split`

**Called by ←**
- `fn:features/team.py:_roster_row`

### `_today_metrics` (line 40)

**Pseudocode:**
- Set snap to metrics_store.snapshot(...).
- Set today to a boolean condition.
- Return a dict.

**Calls →**
1. `metrics_store.snapshot`
2. `snap.get`
3. `features.team.int`
4. `today.get`
5. `features.team.int`
6. `today.get`
7. `features.team.int`
8. `today.get`
9. `features.team.int`
10. `today.get`

**Called by ←**
- `fn:features/team.py:_roster_row`

### `_roster_row` (line 51)

**Pseudocode:**
- Set user_id to str(...).
- Set status to str(...).
- Set contact to _member_contact(...).
- Set presence to a boolean condition.
- Set online to IfExp.
- Set live to None.
- If a boolean condition:
-   Set account to runtime.sessions.get(...).

**Calls →**
1. `features.team.str`
2. `member_row.get`
3. `features.team.str`
4. `member_row.get`
5. `features.team._member_contact`
6. `presence_by_user.get`
7. `features.org.presence_is_online`
8. `presence.get`
9. `runtime.sessions.get`
10. `account.dialer.live_state`
11. `view.get`
12. `features.team.bool`
13. `view.get`
14. `features.team.bool`
15. `view.get`
16. `features.team.len`
17. `view.get`
18. `view.get`
19. `features.team.str`
20. `member_row.get`
21. `presence.get`
22. `presence.get`
23. `presence.get`
24. `presence.get`
25. `presence.get`
26. `features.metrics.SupabaseMetricsStore`
27. `features.team._today_metrics`

**Called by ←**
- `fn:features/team.py:roster_payload`

### `roster_payload` (line 93)

**Pseudocode:**
- Set client to runtime.client.
- Set membership to a boolean condition.
- If org.can_manage_team(...):
-   Raise an error.
- Set org_id to str(...).
- If org_id:
-   Raise an error.
- Set members to org_storage.list_org_members(...).

**Calls →**
1. `features.team.getattr`
2. `features.org.can_manage_team`
3. `membership.get`
4. `features.team.PermissionError`
5. `features.team.str`
6. `membership.get`
7. `features.team.PermissionError`
8. `features.org_storage.list_org_members`
9. `features.team.str`
10. `row.get`
11. `features.org_storage.get_profiles`
12. `features.org_storage.list_presence_for_org`
13. `features.team._roster_row`
14. `membership.get`

**Called by ←**
- `fn:features/team.py:get_roster`

### `member_metrics_payload` (line 113)

**Pseudocode:**
- Set client to runtime.client.
- Set membership to a boolean condition.
- Call org.assert_can_view_member(...).
- Try:
-   Set days to max(...).
- On <ast.Tuple object at 0x00000242BC2A8750>:
-   Set days to 7.
- Set metrics to SupabaseMetricsStore(...).

**Calls →**
1. `features.team.getattr`
2. `features.org.assert_can_view_member`
3. `features.team.max`
4. `features.team.min`
5. `features.team.int`
6. `features.metrics.SupabaseMetricsStore`
7. `features.team.str`
8. `features.team.str`
9. `metrics.snapshot`

**Called by ←**
- `fn:features/team.py:get_member_metrics`

### `member_live_payload` (line 125)

**Pseudocode:**
- Set client to runtime.client.
- Set membership to a boolean condition.
- Call org.assert_can_view_member(...).
- Set target to str(...).
- Set account to runtime.sessions.get(...).
- Set presence to a boolean condition.
- If account:
-   Set view to account.dialer.live_state(...).

**Calls →**
1. `features.team.getattr`
2. `features.org.assert_can_view_member`
3. `features.team.str`
4. `runtime.sessions.get`
5. `features.org_storage.list_presence_for_org`
6. `account.dialer.live_state`
7. `view.get`
8. `view.get`
9. `features.team.bool`
10. `view.get`
11. `features.team.bool`
12. `view.get`
13. `features.team.len`
14. `view.get`
15. `view.get`
16. `active.get`
17. `active.get`
18. `view.get`
19. `features.org.presence_is_online`
20. `presence.get`
21. `presence.get`
22. `features.team.bool`
23. `presence.get`
24. `features.team.bool`
25. `presence.get`
26. `features.team.int`
27. `presence.get`
28. `presence.get`
29. `presence.get`

**Called by ←**
- `fn:features/team.py:get_member_live`

### `get_roster` (line 162)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC13F3D0>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC2D8150>:
-   Call request.report_storage_error(...).

**Calls →**
1. `request.send_json`
2. `features.team.roster_payload`
3. `features.team.str`
4. `request.send_json`
5. `features.team.str`
6. `request.report_storage_error`

### `get_member_metrics` (line 172)

**Pseudocode:**
- Set query to urllib.parse.parse_qs(...).
- Set days to a boolean condition[...].
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC188590>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC36D250>:

**Calls →**
1. `urllib.parse.parse.parse_qs`
2. `urllib.parse.parse.urlsplit`
3. `query.get`
4. `request.send_json`
5. `features.team.member_metrics_payload`
6. `features.team.str`
7. `request.send_json`
8. `features.team.str`
9. `features.team.str`
10. `request.send_json`
11. `features.team.str`
12. `request.report_storage_error`

### `get_member_live` (line 187)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC36E150>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC36C410>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `features.team.member_live_payload`
3. `features.team.str`
4. `request.send_json`
5. `features.team.str`
6. `features.team.str`
7. `request.send_json`
8. `features.team.str`
9. `request.report_storage_error`

### `post_invite` (line 200)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set membership to a boolean condition.
- If org.can_manage_team(...):
-   Call request.send_json(...).
-   Return nothing.
- Set org_id to str(...).
- If org_id:
-   Call request.send_json(...).

**Calls →**
1. `features.team.getattr`
2. `features.org.can_manage_team`
3. `membership.get`
4. `request.send_json`
5. `features.team.str`
6. `membership.get`
7. `request.send_json`
8. `features.team.str`
9. `data.get`
10. `request.send_json`
11. `features.org_storage.invite_member`
12. `data.get`
13. `features.org.clear_membership_cache`
14. `request.send_json`
15. `features.team.str`
16. `row.get`
17. `row.get`
18. `row.get`
19. `row.get`
20. `features.team.str`
21. `request.send_json`
22. `features.team.str`
23. `request.report_storage_error`
