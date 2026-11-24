# `features/ai_voice_stt.py`

**Purpose:** Prospect audio → text (8 kHz mulaw buffer → Whisper).

## Functions
### `_mulaw_decode` (line 15)

**Pseudocode:**
- Set byte to byte op 255.
- Set sign to byte op 128.
- Set exponent to byte op 4 op 7.
- Set mantissa to byte op 15.
- Set sample to mantissa op 3 op _MULAW_BIAS op exponent.
- Update sample with Sub _MULAW_BIAS.
- If sign:
-   Set sample to sample.

**Calls →**
1. `features.ai_voice_stt.max`
2. `features.ai_voice_stt.min`

**Called by ←**
- `fn:features/ai_voice_stt.py:mulaw_rms`
- `fn:features/ai_voice_stt.py:mulaw_to_wav`

### `mulaw_rms` (line 27)

**Pseudocode:**
- If mulaw_chunk:
-   Return 0.
- Set total to 0.
- For each byte in mulaw_chunk:
-   Set sample to _mulaw_decode(...).
-   Update total with Add sample op sample.
- Return total op len(...) op 0.5.

**Calls →**
1. `features.ai_voice_stt._mulaw_decode`
2. `features.ai_voice_stt.len`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_collect_utterances`
- `fn:features/ai_voice_inbound.py:ingest_mulaw`
- `fn:features/ai_voice_stt.py:transcribe_mulaw`

### `mulaw_to_wav` (line 37)

**Pseudocode:**
- Set pcm to bytearray(...).
- For each byte in mulaw_bytes:
-   Set sample to _mulaw_decode(...).
-   Call pcm.extend(...).
- Set buf to io.BytesIO(...).
- With wave.open(...):
-   Call handle.setnchannels(...).
-   Call handle.setsampwidth(...).

**Calls →**
1. `features.ai_voice_stt.bytearray`
2. `features.ai_voice_stt._mulaw_decode`
3. `pcm.extend`
4. `struct.pack`
5. `io.BytesIO`
6. `wave.open`
7. `handle.setnchannels`
8. `handle.setsampwidth`
9. `handle.setframerate`
10. `handle.writeframes`
11. `buf.getvalue`

**Called by ←**
- `fn:features/ai_voice_stt.py:transcribe_mulaw`

### `transcribe_mulaw` (line 51)

**Pseudocode:**
- If len(...) compared to ...:
-   Return ''.
- If mulaw_rms(...) compared to ...:
-   Return ''.
- Set key to str(...).strip(...).
- If key:
-   Return ''.
- Set wav to mulaw_to_wav(...).

**Calls →**
1. `features.ai_voice_stt.len`
2. `features.ai_voice_stt.mulaw_rms`
3. `features.ai_voice_stt.str`
4. `features.ai_voice_stt.mulaw_to_wav`
5. `urllib.request.request.Request`
6. `urllib.request.request.urlopen`
7. `json.loads`
8. `response.read`
9. `features.ai_voice_stt.str`
10. `data.get`

**Called by ←**
- `fn:features/ai_agent_sandbox.py:_transcribe_and_turn`
- `fn:features/ai_voice_inbound.py:_transcribe_and_reply`
