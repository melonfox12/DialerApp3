# `static/features/_ai_dialer/playbook-editor.js`

**Purpose:** Wire UI events and API calls (bindPlaybookEditor).

## HTTP calls (browser)
- `/api/ai-agents/playbook?agent_id=${encodeURIComponent(id)}` (line 68)
- `/api/ai-agents/playbook` (line 108)

## DOM events
- `#$onPromptInput` / handler `onPromptInput` — `input` (line 152)

## Functions