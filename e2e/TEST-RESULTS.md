# Playwright E2E results

- **Date:** 2026-11-26
- **Commit range:** `7392c7c` (dialer page changes) → `09e796e` (HEAD), plus **uncommitted** working-tree changes
- **Runner:** `npx playwright test e2e/<spec>.spec.ts` (Chromium, `scripts/e2e_server.py` local JSON mode unless `E2E_SERVER=existing`)
- **Env vars:** `E2E_ACCESS_TOKEN` / `E2E_MANAGER_ACCESS_TOKEN` (Supabase manager UI tests), `E2E_SERVER=existing` (optional, uses `python dialer.py`)

## Changes tested (grouped)

| # | User-facing change | Primary files |
|---|-------------------|---------------|
| 1 | **No-answer** disposition button on dialer CRM row | `static/features/_dialer/crm-status.js`, `static/css/linear/controls.css` (commit `09e796e`) |
| 2 | **Auto org bootstrap** + **`GET /api/account/setup`** | `features/org.py`, `web.py`, `tests/test_org.py` (uncommitted) |
| 3 | **Team live member detail** (faster poll, session stats, 7-day metrics) | `static/features/team.js`, `shared/vocabulary.py` (uncommitted) |
| 4 | **Usage events** + team activity timeline + tab focus API | `features/usage_events.py`, `org_storage.py`, `navigation.js`, `team.js`, migration SQL (uncommitted) |

## Results table

| Change | Test file | Tests run | Passed | Failed | Skipped | Status |
|--------|-----------|-----------|--------|--------|---------|--------|
| 1 No-answer button | `e2e/no-answer-disposition.spec.ts` | 4 | 4 | 0 | 0 | **Pass** |
| 2 Account setup API | `e2e/account-setup.spec.ts` | 3 | 2 | 0 | 1 | **Pass** (1 skipped: Supabase-only) |
| 3 Team live detail | `e2e/team-live-detail.spec.ts` | 3 | 2 | 0 | 1 | **Pass** (1 skipped: needs token) |
| 4 Usage events | `e2e/usage-events.spec.ts` | 4 | 0 | 4 | 0 | **Fail** (APP BUG) |

## Failure details

### Change 4 — `POST /api/usage/tab` (all usage specs that hit this route)

| Field | Detail |
|-------|--------|
| **Tested** | Tab focus beacon returns HTTP 204 in local mode |
| **Expected** | `204 No Content` |
| **Actual** | `502` with body `post_tab_focus() missing 1 required positional argument: 'data'` |
| **Classification** | **APP BUG** |
| **Cause** | `web.py` `do_POST` only passes JSON body to handlers in an explicit allowlist; `usage_events.post_tab_focus(request, data)` is invoked as `handler(self)` |
| **Suspected fix** | Add `usage_events.post_tab_focus` to the `handler(self, self.read_json(body))` group in `web.py` `do_POST` |

Affected tests: all four cases in `usage-events.spec.ts` (POST 502; GET member usage drops connection).

Initial run of change 1 failed because Playwright started the real Supabase-backed `dialer.py` (login gate). **TEST FIX:** `scripts/e2e_server.py` + `openAppShell()` auth-config stub for local mode.

Initial failure on change 1 (`Qualified` vs `Disqualified`): **TEST FIX** — `exact: true` on button roles.

## Issues found

### Critical

_None._

### High

1. **`GET /api/team/members/{user_id}/*` path params not passed**
   - **Description:** `get_member_metrics`, `get_member_live`, and `get_member_usage` crash; team member detail API calls fail.
   - **Repro:** `GET /api/team/members/<uuid>/live` (or `/metrics`, `/usage`).
   - **Cause:** `web.py` `do_GET` calls `handler(self)` and discards `_params` from `match_route`.
   - **Suggested fix:** For `profile == "GET reads"`, call `handler(self, **params)` when params are non-empty (e.g. `user_id`).

2. **`POST /api/usage/tab` route dispatch**
   - **Description:** Server returns 502; tab-focus telemetry never runs from the browser.
   - **Repro:** `POST /api/usage/tab` with `{"tab":"dialer"}` and `Content-Type: application/json`.
   - **Cause:** `web.py` `do_POST` (~line 248) omitting `usage_events.post_tab_focus` from JSON-body handlers.
   - **Suggested fix:** Register handler in the same tuple as `team.post_invite`, etc.

### Medium

1. **Supabase E2E not exercised in CI by default**
   - **Description:** Org bootstrap, team timeline with real rows, and manager UI require `E2E_SERVER=existing` + `E2E_ACCESS_TOKEN`.
   - **Repro:** Run default Playwright without env vars.
   - **Cause:** Test harness uses isolated local JSON server by design.
   - **Suggested fix:** Add documented CI job with secrets; optional `e2e/supabase/` project in config.

2. **`usage_events` table missing until migration applied**
   - **Description:** After fixing POST dispatch, timeline may stay empty until `202611261800_usage_events.sql` is applied on Supabase.
   - **Repro:** Manager opens member detail on live Supabase without migration.
   - **Cause:** `org_storage.insert_usage_event` fails silently in `usage_events.record`.
   - **Suggested fix:** Run migration; optional health check in setup API.

### Low

1. **Playwright example spec removed**
   - **Description:** `e2e/example.spec.ts` targeted playwright.dev, not this app.
   - **Action taken:** Deleted; replaced by feature specs above.

## How to re-run

```bash
# Default: isolated local server on :8000
npx playwright test e2e/no-answer-disposition.spec.ts

# Against your real Supabase-backed server (must already listen on :8000)
$env:E2E_SERVER='existing'
$env:E2E_ACCESS_TOKEN='<supabase access jwt>'
npx playwright test e2e/team-live-detail.spec.ts
```