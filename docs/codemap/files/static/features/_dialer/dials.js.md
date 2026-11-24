# `static/features/_dialer/dials.js`

**Purpose:** /** Reload CRM catalog and repaint Total dials (matches each row to live CRM status). */

## HTTP calls (browser)
- `/api/dials/import` (line 87)
- `/api/dials/records/${encodeURIComponent(recordId)}` (line 165)
- `/api/dials/backfill-new-callbacks` (line 180)
- `/api/dials/backfill-nov5-static-callbacks` (line 200)
- `/api/dials/records/snapshot` (line 229)

## DOM events
- `#$exportDialsCsv` / handler `exportDialsCsv` — `click` (line 305)

## Functions