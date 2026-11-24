# `static/features/_dialer/_voice/connect.js`

**Purpose:** Wire UI events and API calls (bindVoice).

## HTTP calls (browser)
- `/api/voice-token` (line 48)
- `/api/voice-token` (line 61)

## DOM events
- `#$async` / handler `async` — `click` (line 86)
- `#$async` / handler `async` — `change` (line 95)
- `#$async` / handler `async` — `change` (line 104)
- `#$startMicrophoneTest` / handler `startMicrophoneTest` — `click` (line 113)
- `#$testAudioOutput` / handler `testAudioOutput` — `click` (line 115)
- `#$refreshAudioDevices` / handler `refreshAudioDevices` — `click` (line 86)
- `#$audioInputSelect` / handler `audioInputSelect` — `change` (line 95)
- `#$audioOutputSelect` / handler `audioOutputSelect` — `change` (line 104)
- `#$startMicTest` / handler `startMicTest` — `click` (line 113)
- `#$stopMicTest` / handler `stopMicTest` — `click` (line 114)
- `#$outputTestButton` / handler `outputTestButton` — `click` (line 115)
- `#$testVolumeInput` / handler `testVolumeInput` — `input` (line 116)

## Functions