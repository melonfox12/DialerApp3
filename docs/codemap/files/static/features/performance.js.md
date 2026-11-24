# `static/features/performance.js`

**Purpose:** Wire UI events and API calls (bindPerformance).

## HTTP calls (browser)
- `/api/performance?range=${encodeURIComponent(range)}&tz=${encodeURIComponent(timezone)}` (line 160)
- `/api/performance/goal` (line 220)

## DOM events
- `#$performanceTabButton` / handler `performanceTabButton` — `click` (line 246)
- `#$dailyConversationGoalButton` / handler `dailyConversationGoalButton` — `click` (line 250)
- `#$dailyTalkGoalButton` / handler `dailyTalkGoalButton` — `click` (line 251)

## Functions