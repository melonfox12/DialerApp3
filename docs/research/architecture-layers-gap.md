# Architecture layers — AGENTS.md vs repo

**Rule (AGENTS.md):** dependency direction is `web → dialer → leads/settings → storage → shared`. Lower layers never import higher ones.

**Enforcement:** `python scripts/check_layers.py` (also wired in `tests/test_check_layers.py`).

## How layers are mapped today

| Layer | Score | Paths |
|-------|-------|--------|
| web | 4 | `web.py`, `server.py`, `dialer.py`, `_web/`, `features/accounts.py` |
| dialer | 3 | `features/dialer.py`, `features/_dialer/**` |
| domain | 2 | Other `features/*.py` and `_prospects/` helpers (e.g. `prospects.py`, `team.py`, `script_analytics.py`) |
| storage | 1 | `org_storage.py`, `_prospects/backend_*.py`, `dial_records`, `dial_archive`, CSV IO |
| shared | 0 | `shared/**` |

This is a **pragmatic** map: `accounts.py` sits with web because it constructs `Dialer` sessions; CSV helpers sit with storage because backends import them.

## Known gap (allowlisted)

1. **`shared/dial_policy.py` → `features._prospects.dial_records`**  
   - **Why it’s a gap:** `shared` should not import `features`.  
   - **Risk:** Low for now (type/isolation checks only).  
   - **Fix (later):** Move dial-record shape checks to `shared/` or inject a callback from `features`.  

## Recent features vs rules

| Feature | Layer | Notes |
|---------|-------|--------|
| `script_analytics.py` | domain | Imports `performance`, `org`, `prospects` — OK |
| `usage_events.py` | domain | Called from `_dialer` — OK (dialer → domain) |
| `script` fields on `call_log` | domain + dialer | Stamped in `_dialer/calls.py` — OK |

## CI / local usage

```bash
python scripts/check_layers.py
python -m unittest tests.test_check_layers
```

New violations fail the test unless added to `ALLOWED_VIOLATIONS` in `scripts/check_layers.py` **and** documented in this file.