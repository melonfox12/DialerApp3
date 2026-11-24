# `scripts/gen_ai_dialer_partial.py`

**Purpose:** One-off: build static/features/ai-dialer-agent.html from dialer.html with prefixed ids.

## Functions
### `prefix_id` (line 27)

**Pseudocode:**
- Set val to match.group(...).
- If val compared to ...:
-   Return match.group(...).
- If val.startswith(...):
-   Return match.group(...).
- Return JoinedStr.

**Calls →**
1. `match.group`
2. `match.group`
3. `val.startswith`
4. `match.group`
