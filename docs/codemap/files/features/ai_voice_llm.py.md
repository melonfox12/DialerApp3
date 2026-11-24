# `features/ai_voice_llm.py`

**Purpose:** LLM replies for AI voice (OpenAI-compatible chat API).

## Functions
### `chat_reply` (line 14)
_Return assistant text for one turn._

**Pseudocode:**
- Set key to str(...).strip(...).
- If key:
-   Return _fallback_reply(...).
- Set model to str(...).strip(...).
- Set payload to a dict.
- Set body to json.dumps(...).encode(...).
- Set request to urllib.request.Request(...).
- Try:

**Calls →**
1. `features.ai_voice_llm.str`
2. `features.ai_voice_llm._fallback_reply`
3. `features.ai_voice_llm.str`
4. `json.dumps`
5. `urllib.request.request.Request`
6. `urllib.request.request.urlopen`
7. `json.loads`
8. `response.read`
9. `exc.read`
10. `features.ai_voice_llm.LlmError`
11. `features.ai_voice_llm.LlmError`
12. `features.ai_voice_llm.str`
13. `shared.infra.debug_event`
14. `features.ai_voice_llm.str`
15. `features.ai_voice_llm.LlmError`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_opening_reply`
- `fn:features/ai_agent_sandbox.py:_prospect_turn`
- `fn:features/ai_voice_disposition.py:suggest_status`
- `fn:features/ai_voice_runtime.py:kickoff_conversation`
- `fn:features/ai_voice_runtime.py:on_prospect_text`

### `_fallback_reply` (line 50)
_Short reply when no API key — keeps calls from hanging silently in dev._

**Pseudocode:**
- Set last_user to ''.
- For each item in reversed(...):
-   If item.get(...) compared to ...:
-     Set last_user to str(...).
- If last_user:
-   Return 'Thanks for taking my call. I am still being c...'.
- Return 'Hi — thanks for picking up. I am calling for ...'.

**Calls →**
1. `features.ai_voice_llm.reversed`
2. `item.get`
3. `features.ai_voice_llm.str`
4. `item.get`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_opening_reply`
- `fn:features/ai_voice_llm.py:chat_reply`
- `fn:features/ai_voice_runtime.py:kickoff_conversation`
