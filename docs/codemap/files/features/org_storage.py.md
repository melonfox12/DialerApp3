# `features/org_storage.py`

**Purpose:** Supabase reads and writes for organizations, members, profiles, and presence.

## Routes
- `POST` `organizations` → `None`
- `POST` `org_members` → `None`

## Functions
### `_iso_now` (line 8)

**Pseudocode:**
- Return datetime.now(...).isoformat(...).

**Calls →**
1. `datetime.datetime.now`

**Called by ←**
- `fn:features/org_storage.py:activate_invite`
- `fn:features/org_storage.py:add_member`
- `fn:features/org_storage.py:upsert_presence`
- `fn:features/org_storage.py:upsert_profile`

### `_row` (line 12)

**Pseudocode:**
- If rows:
-   Return None.
- Return IfExp.

**Calls →**
1. `features.org_storage.isinstance`

**Called by ←**
- `fn:features/org_storage.py:add_member`
- `fn:features/org_storage.py:create_organization`
- `fn:features/org_storage.py:find_invite_for_email`
- `fn:features/org_storage.py:get_active_membership`
- `fn:features/org_storage.py:get_organization`

### `get_organization` (line 18)

**Pseudocode:**
- Set rows to a boolean condition.
- Return _row(...).

**Calls →**
1. `client.request`
2. `features.org_storage._row`

**Called by ←**
- `fn:features/org.py:load_membership`

### `get_active_membership` (line 27)

**Pseudocode:**
- Set rows to a boolean condition.
- Return _row(...).

**Calls →**
1. `client.request`
2. `features.org_storage._row`

**Called by ←**
- `fn:features/org.py:assert_can_view_member`
- `fn:features/org.py:load_membership`

### `list_org_members` (line 37)

**Pseudocode:**
- Set rows to a boolean condition.
- Return IfExp.

**Calls →**
1. `client.request`
2. `features.org_storage.isinstance`
3. `features.org_storage.list`

**Called by ←**
- `fn:features/team.py:roster_payload`

### `find_invite_for_email` (line 46)

**Pseudocode:**
- Set normalized to str(...).strip(...).lower(...).
- If normalized:
-   Return None.
- Set rows to a boolean condition.
- Set row to _row(...).
- If a boolean condition:
-   Return None.
- Return row.

**Calls →**
1. `features.org_storage.str`
2. `client.request`
3. `features.org_storage._row`
4. `features.org_storage.str`
5. `row.get`

**Called by ←**
- `fn:features/org.py:sync_user_on_login`

### `activate_invite` (line 62)

**Pseudocode:**
- Call client.request(...).

**Calls →**
1. `client.request`
2. `features.org_storage._iso_now`

**Called by ←**
- `fn:features/org.py:sync_user_on_login`

### `upsert_profile` (line 76)

**Pseudocode:**
- Set body to a dict.
- Call client.request(...).

**Calls →**
1. `features.org_storage.str`
2. `features.org_storage.str`
3. `features.org_storage._iso_now`
4. `client.request`

**Called by ←**
- `fn:features/org.py:sync_user_on_login`

### `get_profiles` (line 92)

**Pseudocode:**
- If user_ids:
-   Return a dict.
- Set ids to ','.join(...).
- Set rows to a boolean condition.
- Return DictComp.

**Calls →**
1. `client.request`
2. `features.org_storage.str`
3. `row.get`

**Called by ←**
- `fn:features/team.py:roster_payload`

### `create_organization` (line 103)

**Pseudocode:**
- Set rows to client.request(...).
- Return _row(...).

**Calls →**
1. `client.request`
2. `features.org_storage._row`

### `add_member` (line 108)

**Pseudocode:**
- If role compared to ...:
-   Raise an error.
- Set body to a dict.
- If user_id:
-   Set body[...] to user_id.
-   Set body[...] to _iso_now(...).
- Set rows to client.request(...).
- Return _row(...).

**Calls →**
1. `features.org_storage.ValueError`
2. `features.org_storage.str`
3. `features.org_storage._iso_now`
4. `client.request`
5. `features.org_storage._row`

**Called by ←**
- `fn:features/org_storage.py:invite_member`

### `upsert_presence` (line 124)

**Pseudocode:**
- Set body to a dict.
- Call client.request(...).

**Calls →**
1. `features.org_storage._iso_now`
2. `features.org_storage.bool`
3. `fields.get`
4. `features.org_storage.bool`
5. `fields.get`
6. `features.org_storage.str`
7. `fields.get`
8. `features.org_storage.str`
9. `fields.get`
10. `features.org_storage.int`
11. `fields.get`
12. `client.request`

**Called by ←**
- `fn:features/team.py:maybe_record_presence`

### `list_presence_for_org` (line 144)

**Pseudocode:**
- Set rows to a boolean condition.
- Return DictComp.

**Calls →**
1. `client.request`
2. `features.org_storage.str`
3. `row.get`

**Called by ←**
- `fn:features/team.py:member_live_payload`
- `fn:features/team.py:roster_payload`

### `invite_member` (line 152)

**Pseudocode:**
- If role compared to ...:
-   Raise an error.
- Set normalized to str(...).strip(...).lower(...).
- If a boolean condition:
-   Raise an error.
- Return add_member(...).

**Calls →**
1. `features.org_storage.ValueError`
2. `features.org_storage.str`
3. `features.org_storage.ValueError`
4. `features.org_storage.add_member`

**Called by ←**
- `fn:features/team.py:post_invite`
