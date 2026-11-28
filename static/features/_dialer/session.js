import { postJson } from "../../_core/api.js";
import { loadAppState, mergeLiveState } from "../../_core/sync-state.js";
import { S, state } from "../../_core/state.js";
import { dialerEls } from "../../_core/format.js";
import { errorText, showToast } from "../../_core/notify.js";
import { render } from "../../core.js";
import { openSettings } from "../settings.js";
import { cancelVoiceRejoin, connectAndCleanup, tearDownVoice } from "./connect.js";
import { stopProspectWaveform } from "./card.js";
import { stageEffects } from "./effects.js";
import { stopCallTimer } from "./timer.js";
import { showSessionSummary } from "./summary.js";

function haltDialerUiImmediately() {
  cancelVoiceRejoin();
  S.expectVoiceDisconnect = true;
  S.voiceConnectBusy = false;
  state.running = false;
  state.paused = false;
  state.agent_ready = false;
  state.in_flight = [];
  state.active_lead = null;
  state.pending_outcome = null;
  state.stage = "idle";
  stageEffects.stop();
  stopProspectWaveform();
  stopCallTimer();
  render();
}

export async function startDialing() {
  for (const button of dialerEls("startButton")) button.disabled = true;
  S.voiceConnectBusy = true;
  let sessionStarted = false;
  try {
    const session = await postJson("/api/start");
    sessionStarted = true;
    const { client_call_token: clientCallToken, ...sessionState } = session;
    if (!clientCallToken) throw new Error("The browser call session could not be created.");
    const failure = await connectAndCleanup(clientCallToken, sessionState);
    if (failure) return;
  } catch (error) {
    if (sessionStarted) await postJson("/api/stop").catch(() => {});
    await tearDownVoice({ intentional: true });
    await loadAppState().catch(() => {});
    render();
    showToast(errorText(error, "Could not start dialing."), true);
    if (!sessionStarted) openSettings();
  } finally {
    S.voiceConnectBusy = false;
    for (const button of dialerEls("startButton")) button.disabled = state.running;
  }
}

export async function stopDialing() {
  if (S.stopDialingBusy || !state.running) return;
  S.stopDialingBusy = true;
  for (const button of dialerEls("stopButton")) button.disabled = true;

  haltDialerUiImmediately();

  try {
    const [result] = await Promise.all([
      postJson("/api/stop"),
      tearDownVoice({ intentional: true }),
    ]);
    mergeLiveState(result);
    render();
    showSessionSummary(result.session_summary, result.previous_session);
  } catch (error) {
    await loadAppState().catch(() => {});
    render();
    showToast(errorText(error, "Could not stop dialing."), true);
  } finally {
    S.stopDialingBusy = false;
    S.expectVoiceDisconnect = false;
    for (const button of dialerEls("stopButton")) button.disabled = state.running;
    for (const button of dialerEls("startButton")) button.disabled = state.running;
  }
}