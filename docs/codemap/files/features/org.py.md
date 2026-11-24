# `features/org.py`

**Purpose:** Organization membership rules: roles, login hooks, and access checks.

## Functions
### `_empty_membership` (line 14)

**Pseudocode:**
- Return a dict.

**Called by ←**
- `fn:features/org.py:attach_membership_to_dialer`
- `fn:features/org.py:load_membership`
- `fn:features/org.py:membership_for_auth`
- `fn:features/org.py:sync_user_on_login`

### `can_manage_team` (line 24)

**Pseudocode:**
- Return str(...).strip(...).lower(...) compared to ....

**Calls →**
1. `features.org.str`

**Called by ←**
- `fn:features/org.py:assert_can_view_member`
- `fn:features/org.py:load_membership`
- `fn:features/team.py:post_invite`
- `fn:features/team.py:roster_payload`

### `_cache_key` (line 28)

**Pseudocode:**
- Return str(...).

**Calls →**
1. `features.org.str`

**Called by ←**
- `fn:features/org.py:clear_membership_cache`
- `fn:features/org.py:load_membership`

### `load_membership` (line 32)

**Pseudocode:**
- Set key to _cache_key(...).
- Set now to time.time(...).
- With _membership_lock:
-   Set entry to _membership_cache.get(...).
-   If a boolean condition:
-     Return dict(...).
- If a boolean condition:
-   Return _empty_membership(...).

**Calls →**
1. `features.org._cache_key`
2. `time.time`
3. `_membership_cache.get`
4. `features.org.dict`
5. `features.org._empty_membership`
6. `features.org_storage.get_active_membership`
7. `features.org._empty_membership`
8. `features.org_storage.get_organization`
9. `features.org.str`
10. `member.get`
11. `features.org.str`
12. `org.get`
13. `features.org.str`
14. `member.get`
15. `features.org.str`
16. `member.get`
17. `features.org.can_manage_team`
18. `member.get`
19. `features.org.dict`
20. `features.org.len`
21. `features.org.list`

**Called by ←**
- `fn:features/accounts.py:session_for`
- `fn:features/org.py:sync_user_on_login`

### `clear_membership_cache` (line 62)

**Pseudocode:**
- With _membership_lock:
-   If user_id compared to ...:
-     Call _membership_cache.clear(...).
-     Return nothing.
-   Call _membership_cache.pop(...).

**Calls →**
1. `_membership_cache.clear`
2. `_membership_cache.pop`
3. `features.org._cache_key`

**Called by ←**
- `fn:features/org.py:sync_user_on_login`
- `fn:features/team.py:post_invite`

### `sync_user_on_login` (line 70)

**Pseudocode:**
- If client:
-   Return _empty_membership(...).
- Set user_id to str(...).
- Set email to str(...).strip(...).
- If user_id:
-   Return _empty_membership(...).
- Call org_storage.upsert_profile(...).
- Set invite to org_storage.find_invite_for_email(...).

**Calls →**
1. `features.org._empty_membership`
2. `features.org.str`
3. `user.get`
4. `features.org.str`
5. `user.get`
6. `features.org._empty_membership`
7. `features.org_storage.upsert_profile`
8. `features.org_storage.find_invite_for_email`
9. `invite.get`
10. `features.org_storage.activate_invite`
11. `features.org.clear_membership_cache`
12. `features.org.load_membership`

**Called by ←**
- `fn:features/accounts.py:session_for`

### `attach_membership_to_dialer` (line 85)

**Pseudocode:**
- Set dialer.org_membership to dict(...).

**Calls →**
1. `features.org.dict`
2. `features.org._empty_membership`

**Called by ←**
- `fn:features/accounts.py:session_for`

### `membership_for_auth` (line 89)

**Pseudocode:**
- Set base to a boolean condition.
- Return a dict.

**Calls →**
1. `features.org.getattr`
2. `features.org._empty_membership`
3. `base.get`
4. `base.get`
5. `base.get`
6. `features.org.bool`
7. `base.get`

**Called by ←**
- `fn:web.py:get_auth_me`

### `assert_can_view_member` (line 99)

**Pseudocode:**
- If can_manage_team(...):
-   Raise an error.
- Set org_id to str(...).
- If org_id:
-   Raise an error.
- Set target to str(...).
- If target:
-   Raise an error.

**Calls →**
1. `features.org.can_manage_team`
2. `viewer_membership.get`
3. `features.org.PermissionError`
4. `features.org.str`
5. `viewer_membership.get`
6. `features.org.PermissionError`
7. `features.org.str`
8. `features.org.ValueError`
9. `features.org.str`
10. `features.org_storage.get_active_membership`
11. `features.org.str`
12. `member.get`
13. `features.org.PermissionError`

**Called by ←**
- `fn:features/team.py:member_live_payload`
- `fn:features/team.py:member_metrics_payload`

### `presence_is_online` (line 116)

**Pseudocode:**
- If last_seen_at:
-   Return False.
- If now compared to ...:
-   Set now to datetime.now(...).
- Try:
-   Set seen to datetime.fromisoformat(...).
- On <ast.Name object at 0x00000242BC1DC950>:
-   Return False.

**Calls →**
1. `datetime.now`
2. `datetime.fromisoformat`
3. `features.org.str`
4. `seen.replace`

**Called by ←**
- `fn:features/team.py:_roster_row`
- `fn:features/team.py:member_live_payload`
