# Twilio live dial Playwright (real Voice SDK + ngrok)

These tests exercise the same path a rep uses: **Settings → HTTPS public URL → Start dialing → Twilio Device → outbound to a prospect**.

They are **opt-in** (not CI default) because they need live Twilio, ngrok, and a signed-in Supabase user.

## Twilio test numbers

From [Twilio test credentials / magic inputs](https://www.twilio.com/docs/iam/test-credentials):

| Number | Role |
|--------|------|
| `+15005550006` | Valid (availability / From on **test** creds only) |
| `+15005550004` | **To**: queues with no error (“blocked”) — default `E2E_TWILIO_TO` |
| `+15005550001` | Invalid To (21217) |
| `+15005550002` | Unroutable (21214) |

**Important:** Browser Voice SDK uses **live** account credentials from Settings, not Twilio “test credentials”. Magic `+1500555` destinations are useful for cheap outbound attempts; for a real ring, set `E2E_TWILIO_TO` to a **verified** mobile on your Twilio trial.

## Setup

1. Run `server.py` / `dialer.py` on **:8000** with Supabase + Twilio in Settings (or `.env` for first load).
2. Start ngrok: `ngrok http 8000` (Twilio `/hooks/*` is served on the **same** port as the CRM app).
3. Set **Settings → Public webhook URL** to the ngrok `https://…` URL (must match the current tunnel — stale URLs are a common failure).
4. On start, the app sets TwiML App Voice URL = `{PUBLIC_BASE_URL}/hooks/voice` (POST). Restart `dialer.py` after pulling hook-routing fixes.
5. Caller ID queue must have at least one outbound number.
6. In repo `.env`: `E2E_ACCESS_TOKEN=<Supabase JWT>`, optional `E2E_TWILIO_TO=+1…`.

## Run

```powershell
$env:E2E_SERVER='existing'
$env:E2E_BASE_URL='http://127.0.0.1:8000'
$env:E2E_TWILIO_LIVE='1'
npx playwright test e2e/twilio-live-dial.spec.ts --reporter=list
```

Grant microphone in Chromium (Playwright grants `microphone` permission; you may still need OS mic access).

## What bugs this catches

- `PUBLIC_BASE_URL` not `https` or not matching ngrok → start fails or webhooks never hit.
- Missing Twilio / caller ID → `/api/start` or UI toast errors.
- Pool empty after seed → outbound never launches.
- Voice agent never reaches `agent_ready` → client/WebRTC or token issues.

## One-time setup scripts

```powershell
python scripts/mint_e2e_access_token.py   # writes E2E_ACCESS_TOKEN + E2E_REFRESH_TOKEN to .env
python scripts/sync_public_base_url.py      # aligns Settings with current ngrok https URL
python scripts/twilio_live_preflight.py
```

## Latest run (2026-11-28)

| Step | Result |
|------|--------|
| ngrok → `:8000` | OK (`https://quack-unboxed-unbeaten.ngrok-free.dev`) |
| `sync_public_base_url` | OK |
| Preflight Playwright | **Pass** |
| Rep flow (Start dialing) | **Fail** — activity log: *API Key Secret does not match the API Key SID* (fix Twilio API key + secret in **Settings**, Save, re-run) |

The harness reached **Start dialing** and Twilio caller ID rotation; browser Voice leg did not become `agent_ready` because token creation failed on the server.