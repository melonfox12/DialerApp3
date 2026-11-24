# `static/features/_prospects/csv.js`

**Purpose:** Wire UI events and API calls (bindCsv).

## HTTP calls (browser)
- `/api/import` (line 15)
- `/api/export.csv` (line 54)

## DOM events
- `#$exportCsv` / handler `exportCsv` — `click` (line 74)
- `#$deleteSelectedProspects` / handler `deleteSelectedProspects` — `click` (line 75)
- `#$importButton` / handler `importButton` — `click` (line 72)
- `#$headingImportButton` / handler `headingImportButton` — `click` (line 73)
- `#$exportButton` / handler `exportButton` — `click` (line 74)
- `#$deleteSelectedButton` / handler `deleteSelectedButton` — `click` (line 75)
- `#$csvInput` / handler `csvInput` — `change` (line 76)

## Functions