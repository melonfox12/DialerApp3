# DialerApp2 code map

Interactive graph and per-file pseudocode generated from the repo (not hand-waved). **Does not read or embed `.env`.**

## Regenerate

From the project root:

```powershell
python scripts/build_codemap.py
```

Outputs:

| Output | Purpose |
|--------|---------|
| `docs/codemap/graph.json` | Nodes (files, functions, HTTP paths) and edges (import, call, route, http, event) |
| `docs/codemap/pseudocode.json` | Per-file functions, pseudocode, routes, events (viewer + tooling) |
| `docs/codemap/files/**` | One markdown file per source file with pseudocode and call lists |

Latest generator stats are in `graph.json` → `meta` (file counts, edges, routes, unresolved calls).

## Open the viewer

Static files must be served over HTTP (browsers block `fetch` on `file://`).

```powershell
cd path\to\DialerApp2
python -m http.server 8001
```

Then open: [http://localhost:8001/docs/codemap/](http://localhost:8001/docs/codemap/)

Use the search box, edge-type toggles, and **Focus** mode (1–2 hops). Click a file node for a summary; full detail is in `files/<path>.md`.

## Start here (10-step reading order)

1. `server.py` — process entry, dual HTTP servers (app + Twilio hooks).
2. `web.py` — route table composition and `BaseHTTPRequestHandler` dispatch.
3. `_web/respond.py` — HTML shell stitch for `GET /`, JSON/static helpers.
4. `features/accounts.py` — `AppRuntime.configure`, Google session → `Dialer` per user.
5. `static/main.js` — browser boot order (auth, dialer bindings, polling).
6. `static/_core/api.js` + `poller.js` — Bearer token on `/api/*`, live poll loop.
7. `features/dialer.py` — largest REST surface (`/api/start`, live, leads, voice).
8. `_web/hooks.py` — Twilio callbacks on port **8765**.
9. `features/prospects.py` + `csv_import.py` — CRM import/export.
10. `features/org.py` + `team.py` — org membership and manager Team APIs.

Then read `flows.md` for numbered sequences across those files.

## Ignored paths (not analyzed)

The script skips:

- `tests/`, `.pytest_cache/`, `crm_data/`, `docs/linear-design-system/`, `__pycache__/`, virtualenvs
- `**/__init__.py` (listed as markers only)

Analyzed: root `server.py`, `web.py`, `dialer.py`; packages `_web/`, `shared/`, `features/`, `scripts/`; all `static/**/*.js`.

## Map uncertainty (unresolved calls)

`build_codemap.py` resolves many internal calls via `ast` + import aliases. It **does not** reliably link:

- Chained calls on locals (`foo().bar()`), `getattr`, dynamic imports
- Methods on variables typed at runtime only
- Twilio / Supabase SDK methods (counted toward `external:*` when obvious)
- JS minified patterns, template-string URLs, or non-literal `fetch(url)`

See `graph.json` → `unresolved` (capped at 500 entries; `meta.unresolved_calls` is the full count). Treat those edges as “something is invoked here” without a guaranteed target node.

## Layers (viewer colors)

| Layer | Paths |
|-------|--------|
| entry | `server.py`, `dialer.py` |
| http | `web.py`, `_web/` |
| features | `features/` |
| shared | `shared/` |
| browser | `static/` |
| scripts | `scripts/` (including `build_codemap.py`) |
| external | `external:supabase`, `external:twilio`, `external:stdlib` |

## Related docs

- `flows.md` — Mermaid sequence diagrams for seven critical user journeys.
- `files/` — exhaustive per-function pseudocode pulled from source bodies.