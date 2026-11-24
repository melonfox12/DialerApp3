# `static/features/team.js`

**Purpose:** Wire UI events and API calls (bindTeam).

## HTTP calls (browser)
- `/api/team/roster` (line 28)
- `/api/team/members/${encodeURIComponent(userId)}/metrics?days=7` (line 104)
- `/api/team/members/${encodeURIComponent(userId)}/live` (line 105)
- `/api/team/invites` (line 137)

## DOM events
- `#$async` / handler `async` — `submit` (line 131)

## Functions