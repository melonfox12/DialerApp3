# `features/ai_voice_disposition.py`

**Purpose:** Map conversation to a CRM status at end of AI call.

## Functions
### `suggest_status` (line 8)

**Pseudocode:**
- If messages:
-   Return 'dialed'.
- Set prompt to 'Given this call transcript as JSON messages, ...'.
- Try:
-   Set raw to ai_voice_llm.chat_reply(...).
- On <ast.Attribute object at 0x00000242BC2AC290>:
-   Return 'contact_engaged'.
- Set key to IfExp.

**Calls →**
1. `features.ai_voice_llm.chat_reply`
2. `features.ai_voice_disposition.str`
3. `raw.strip`
4. `raw.strip`

**Called by ←**
- `fn:features/ai_voice_runtime.py:finish_session`
