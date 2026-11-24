# `static/features/workflow.js`

**Purpose:** /** Max viewport pan speed (px/s) when pushing a node past the screen edge */

## DOM events
- `#$onPointerMove` / handler `onPointerMove` — `pointermove` (line 710)
- `#$endInteraction` / handler `endInteraction` — `pointerup` (line 711)
- `#$endInteraction` / handler `endInteraction` — `pointercancel` (line 712)
- `#$onPointerMove` / handler `onPointerMove` — `pointermove` (line 741)
- `#$endInteraction` / handler `endInteraction` — `pointerup` (line 742)
- `#$endInteraction` / handler `endInteraction` — `pointercancel` (line 743)
- `#$startDrag` / handler `startDrag` — `pointerdown` (line 784)
- `#$startPan` / handler `startPan` — `pointerdown` (line 785)
- `#$onWheel` / handler `onWheel` — `wheel` (line 786)
- `#$suppressMiddleAutoScroll` / handler `suppressMiddleAutoScroll` — `auxclick` (line 787)
- `#$refreshWorkflowCanvas` / handler `refreshWorkflowCanvas` — `resize` (line 791)

## Functions