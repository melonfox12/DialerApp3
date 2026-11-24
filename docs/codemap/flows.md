# End-to-end flow walkthroughs

Each step lists `file:function` (or DOM id → handler). Regenerate call edges with `python scripts/build_codemap.py`.

---

## 1. App startup (`python server.py` → ports open)

```mermaid
sequenceDiagram
  participant Op as Operator
  participant SP as server.py
  participant RT as features/accounts.py AppRuntime
  participant WH as _web/hooks.py
  participant WB as web.py

  Op->>SP: 1. python server.py / dialer.serve()
  SP->>SP: 2. shared/infra.enable()
  SP->>RT: 3. AppRuntime().configure()
  RT->>RT: 4. read_env + SupabaseClient.from_env (shared/_infra/supabase.py)
  RT->>RT: 5. _ping() → GET prospects (health check)
  SP->>SP: 6. maybe_start_embedded() (features/ai_media_bridge.py)
  SP->>SP: 7. ThreadingHTTPServer APP_HOST:APP_PORT → make_app_handler(runtime)
  SP->>SP: 8. ThreadingHTTPServer HOOK_HOST:HOOK_PORT → make_hook_handler(runtime)
  SP->>SP: 9. serve_forever() on app port; hook thread serve_forever()
  Note over WB: Incoming GET / handled by web.make_app_handler → respond.HandlerMixin
```

| Step | Location | What happens |
|------|----------|--------------|
| 1 | `dialer.py:serve` or `server.py` | Entry calls `serve()`. |
| 2 | `shared/infra.py:enable` | Debug logging setup. |
| 3–5 | `features/accounts.py:AppRuntime.configure` | Picks Supabase vs local JSON; stores `runtime.client`. |
| 6 | `features/ai_media_bridge.py:maybe_start_embedded` | Optional AI bridge WebSocket. |
| 7–9 | `server.py:serve` | Binds **8000** (app) and **8765** (Twilio hooks). |

---

## 2. Page load (GET `/` → `main.js` → auth → poller)

```mermaid
sequenceDiagram
  participant BR as Browser
  participant WB as web.py
  participant RS as _web/respond.py
  participant MJ as static/main.js
  participant AU as static/features/auth.js
  participant PL as static/features/_dialer/poller.js

  BR->>WB: 1. GET /
  WB->>RS: 2. send_app_page() stitches shell + feature partials
  RS->>BR: 3. HTML + vocabulary JSON inline
  BR->>MJ: 4. load main.js module graph
  MJ->>MJ: 5. bindNavigation, bindDialer, bindAuth, …
  MJ->>AU: 6. initAuth()
  AU->>WB: 7. GET /api/auth/config
  alt Google enabled
    AU->>AU: 8. supabase.createClient; getSession()
    AU->>WB: 9. GET /api/auth/me (Bearer token)
    AU->>AU: 10. refreshAccountContext → syncTeamChrome
    AU->>MJ: 11. bootApp() → refreshState
  else local mode
    AU->>MJ: bootApp without login gate
  end
  MJ->>PL: 12. startPolling()
  loop every ~1.5s
    PL->>WB: GET /api/live
    PL->>WB: GET /api/leads (if version changed)
    PL->>WB: GET /api/metrics (every 15s)
    PL->>PL: render() via registry
  end
```

| Step | Location | What happens |
|------|----------|--------------|
| 1–3 | `_web/respond.py:send_app_page` | Concatenates `static/shell.html` + feature HTML partials. |
| 7 | `web.py:get_auth_config` | Returns Supabase URL + anon key for browser auth. |
| 9 | `web.py:get_auth_me` + `features/org.py:membership_for_auth` | Org role for Team tab. |
| 12+ | `poller.js:refreshState` | Live dialer + CRM sync loop. |

---

## 3. Click Start dialing → Twilio browser leg

```mermaid
sequenceDiagram
  participant UI as #startButton
  participant BD as static/features/_dialer/bindings.js
  participant SS as static/features/_dialer/session.js
  participant CN as static/features/_dialer/connect.js
  participant WB as web.py
  participant DL as features/dialer.py

  UI->>BD: 1. click
  BD->>SS: 2. startDialing()
  SS->>WB: 3. POST /api/start
  WB->>DL: 4. post_start(request)
  DL->>DL: 5. Dialer.start_session / queue / voice token
  DL-->>SS: 6. JSON live snapshot + client_call_token
  SS->>CN: 7. connectAndCleanup(clientCallToken)
  CN->>CN: 8. Twilio.Device connect (browser SDK)
  SS->>SS: 9. render() on success
```

| Step | Location | What happens |
|------|----------|--------------|
| 1–2 | `bindings.js:bindDialer` | `dialerEl("startButton")` click → `startDialing`. |
| 3–6 | `features/dialer.py:post_start` | Starts server dialer session; issues desk token. |
| 7–8 | `connect.js` | Registers Twilio voice device with token from `/api/voice-token` path in session flow. |

---

## 4. Twilio webhook: answered → pickup → slots

```mermaid
sequenceDiagram
  participant TW as Twilio
  participant HK as _web/hooks.py HookHandler
  participant DL as features/_dialer/state.py Dialer
  participant CE as features/_dialer/call_events.py
  participant PU as features/_dialer/_call_events/pickup.py
  participant SL as features/_dialer/slots.py

  TW->>HK: 1. POST /hooks/{token}/answered (or amd)
  HK->>HK: 2. resolve_dialer + validate_webhook signature
  HK->>DL: 3. handle_webhook(token, event, params)
  DL->>CE: 4. dispatch event name
  CE->>PU: 5. pickup handler (AnsweredBy / AMD)
  PU->>PU: 6. _amd_should_connect / voicemail branch
  PU->>SL: 7. slot connect or drop line
  PU->>DL: 8. update call + CRM call_log via outcomes/calls
```

| Step | Location | What happens |
|------|----------|--------------|
| 1–2 | `_web/hooks.py:dispatch` | Separate **port 8765** hook server. |
| 3 | `Dialer.handle_webhook` | Routes Twilio status to internal handlers. |
| 5–7 | `pickup.py` | Machine/human detection; connects agent or drops. |

---

## 5. Disposition click → CRM + metrics

```mermaid
sequenceDiagram
  participant UI as crmStatusButtons
  participant CS as static/features/_dialer/crm-status.js
  participant WB as web.py
  participant DL as features/dialer.py
  participant OC as features/_dialer/outcomes.py
  participant PR as features/prospects.py
  participant MT as features/metrics.py

  UI->>CS: 1. click [data-status]
  CS->>CS: 2. saveCrmStatus(lead, status)
  CS->>WB: 3. POST /api/leads/{id}/call-outcome or /status
  WB->>DL: 4. post_call_outcome / post_status
  DL->>OC: 5. apply outcome rules
  DL->>PR: 6. ProspectStore persist lead status
  DL->>MT: 7. increment_metric (Supabase RPC)
```

| Step | Location | What happens |
|------|----------|--------------|
| 1–3 | `crm-status.js` | In-call disposition buttons on active lead. |
| 4–7 | `outcomes.py`, `metrics.py` | Status transitions + daily metric counters. |

---

## 6. Login → Team tab visibility

```mermaid
sequenceDiagram
  participant AU as static/features/auth.js
  participant WB as web.py
  participant AC as features/accounts.py
  participant OR as features/org.py
  participant OS as features/org_storage.py
  participant TM as static/features/team.js

  AU->>WB: 1. GET /api/auth/me
  WB->>AC: 2. session_for → sync_user_on_login
  AC->>OR: 3. sync_user_on_login
  OR->>OS: 4. get_active_membership(user_id)
  OR->>OR: 5. can_manage_team(role)
  WB-->>AU: 6. { can_manage_team, role, org_id }
  AU->>TM: 7. syncTeamChrome()
  TM->>TM: 8. #teamTabButton hidden = !canManageTeam
```

| Step | Location | What happens |
|------|----------|--------------|
| 4 | `org_storage.py:get_active_membership` | `org_members` row status=active. |
| 8 | `team.js:syncTeamChrome` | Side nav Team tab only for owner/manager. |

---

## 7. CSV import

```mermaid
sequenceDiagram
  participant UI as csv file input
  participant CV as static/features/_prospects/csv.js
  participant WB as web.py
  participant PR as features/prospects.py
  participant IM as features/_prospects/csv_import.py
  participant ST as features/_prospects/backend_supabase.py

  UI->>CV: 1. user picks file → submit handler
  CV->>WB: 2. POST /api/import (multipart or body per handler)
  WB->>PR: 3. post_import(request)
  PR->>IM: 4. parse + validate CSV rows
  PR->>ST: 5. upsert prospects for account user_id
  PR-->>CV: 6. counts + errors JSON
  CV->>CV: 7. toast + refreshState / renderTable
```

| Step | Location | What happens |
|------|----------|--------------|
| 2 | `csv.js` | `request("/api/import", { method: "POST", … })`. |
| 3–5 | `prospects.py:post_import` | Per-user CRM storage (not org-shared). |

---

See `graph.json` `routes` and `docs/codemap/files/**` for handlers and pseudocode on every step.