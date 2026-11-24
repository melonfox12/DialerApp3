# `static/features/settings.js`

**Purpose:** Wire UI events and API calls (bindSettings).

## HTTP calls (browser)
- `/api/settings` (line 79)
- `/api/settings` (line 161)

## DOM events
- `#$openSettings` / handler `openSettings` — `click` (line 124)
- `#$unlockAuthToken` / handler `unlockAuthToken` — `pointerdown` (line 132)
- `#$unlockAuthToken` / handler `unlockAuthToken` — `focus` (line 133)
- `#$async` / handler `async` — `submit` (line 156)
- `#$settingsButton` / handler `settingsButton` — `click` (line 124)
- `#$apiKeyInput` / handler `apiKeyInput` — `focus` (line 125)
- `#$settingsDialog` / handler `settingsDialog` — `close` (line 149)
- `#$closeSettings` / handler `closeSettings` — `click` (line 154)
- `#$cancelSettings` / handler `cancelSettings` — `click` (line 155)
- `#$settingsForm` / handler `settingsForm` — `submit` (line 156)
- `#$soundVolumeInput` / handler `soundVolumeInput` — `input` (line 180)

## Functions