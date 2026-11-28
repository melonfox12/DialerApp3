# Playwright E2E results

- **Date:** 2026-11-27 (latest full `e2e/` run)
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
| 4 Usage events | `e2e/usage-events.spec.ts` | 4 | 4 | 0 | 0 | **Pass** (after `web.py` dispatch fix) |
| 5 Script analytics | `e2e/script-analytics.spec.ts` | 4 | 3 | 0 | 1 | **Pass** (1 skipped: Supabase-only) |

**Latest suite:** `E2E_PORT=8010` + `E2E_SERVER=local` → **16 tests, 14 passed, 2 skipped** (manager team + one account-setup skip).

## Failure details

### Change 4 — fixed in app (2026-11-27)

- `web.py`: `POST /api/usage/tab` passes JSON body; `GET /api/team/members/{user_id}/*` passes path params (`user_id` → `member_user_id`).

Initial run of change 1 failed because Playwright started the real Supabase-backed `dialer.py` (login gate). **TEST FIX:** `scripts/e2e_server.py` + `openAppShell()` auth-config stub for local mode.

Initial failure on change 1 (`Qualified` vs `Disqualified`): **TEST FIX** — `exact: true` on button roles.

## Issues found

### Critical

_None._

### High

_None (route dispatch fixed 2026-11-27)._

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
# Default: isolated local server (use :8010 if dialer.py already on :8000)
$env:E2E_PORT='8010'; $env:E2E_BASE_URL='http://127.0.0.1:8010'
npx playwright test e2e/no-answer-disposition.spec.ts

# Against your real Supabase-backed server (must already listen on :8000)
$env:E2E_SERVER='existing'
$env:E2E_ACCESS_TOKEN='<supabase access jwt>'
npx playwright test e2e/team-live-detail.spec.ts
```