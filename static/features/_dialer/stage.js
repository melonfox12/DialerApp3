import { stageEffects } from "./effects.js";
import { S, state } from "../../_core/state.js";
import {
  STATUS_LABELS,
  dialerEl,
  dialerEls,
  callbackStatusText,
  markCallback,
  setDialerText,
} from "../../_core/format.js";
import { formatPhoneNumber } from "../../_core/phone.js";
import { startCallTimer, stopCallTimer } from "./timer.js";

export function renderCallStage(stage, target) {
  const containers = dialerEls("callStage");
  if (!containers.length) return;

  const fragment = document.createDocumentFragment();
  const heading = document.createElement("strong");
  const detail = document.createElement("span");
  if (stage === "connected" && target) {
    heading.textContent = state.pickup_answered_by === "voicemail" ? "VOICEMAIL" : "LIVE";
    const name = target.contact_name || target.company || formatPhoneNumber(target.phone) || "Prospect";
    const nameElement = document.createElement("p");
    nameElement.className = "call-prospect-name";
    nameElement.textContent = name;
    fragment.append(nameElement);
    if (target.company && target.company !== name) {
      const business = document.createElement("span");
      business.className = "call-prospect-business";
      business.textContent = target.company;
      fragment.append(business);
    }
    if (target.signal) {
      const signal = document.createElement("p");
      signal.className = "call-prospect-signal";
      signal.textContent = `Signal: ${target.signal}`;
      fragment.append(signal);
    }
    const meta = document.createElement("span");
    meta.className = "call-prospect-meta";
    if (target.phone) {
      const phone = document.createElement("span");
      phone.textContent = formatPhoneNumber(target.phone);
      meta.append(phone);
    }
    const clock = localTimeLabel(target.timezone);
    if (clock) {
      const clockElement = document.createElement("span");
      clockElement.textContent = clock;
      meta.append(clockElement);
    }
    const timer = document.createElement("span");
    timer.id = "callTimer";
    timer.textContent = "0:00";
    meta.append(timer);
    fragment.append(meta);
    if (target.score_reasons) {
      const notes = document.createElement("span");
      notes.className = "call-prospect-notes";
      notes.textContent = String(target.score_reasons);
      fragment.append(notes);
    }
    const script = document.createElement("span");
    script.className = "call-stage-script";
    script.textContent = state.settings?.opening_script || "Introduce yourself, confirm you have the right person, then ask one clear question.";
    fragment.append(script);
    if (S.previousStage !== "connected") stageEffects.playCue("connect");
  } else if (stage === "paused") {
    heading.textContent = "Session paused";
    detail.textContent = "Resume when you’re ready to continue the queue.";
  } else if (stage === "wrapup" && target) {
    heading.textContent = "Call complete";
    detail.textContent = `Choose a disposition for ${target.company || target.contact_name || formatPhoneNumber(target.phone)}.`;
  } else if (stage === "dialing" || stage === "ringing") {
    const calls = state.in_flight || [];
    heading.textContent = stage === "ringing" ? "Ring in progress" : "Dialing next prospect";
    detail.textContent = calls.map((call) => `${call.lead?.company || call.lead?.contact_name || "Prospect"} · ${call.state === "ringing" ? "Ringing" : "Dialing"}`).join(" · ") || state.last_event || "Connecting to the next prospect…";
  } else if (stage !== "idle") {
    const next = state.next_lead;
    const clock = next ? localTimeLabel(next.timezone) : "";
    const context = next?.score_reasons;
    if (next) {
      detail.append(`Next up: ${next.company || next.contact_name || "Prospect"} · ${formatPhoneNumber(next.phone)} · ${clock || next.timezone || "Local time unavailable"} · `);
      const status = document.createElement("span");
      const countdown = next.status === "dialed" && next.scheduled_until;
      status.dataset.callbackPrefix = "Status: Dialed ";
      status.textContent = countdown ? `Status: ${callbackStatusText(next)}` : `Status: ${STATUS_LABELS[next.status] || "New"}`;
      if (countdown && !context) markCallback(status, next);
      detail.append(context ? `Context: ${context}` : status);
    } else {
      detail.textContent = "No prospects available in this queue.";
    }
  }

  function localTimeLabel(timezoneName) {
    const zones = {
      Eastern: "America/New_York",
      Central: "America/Chicago",
      Mountain: "America/Denver",
      Pacific: "America/Los_Angeles",
      Alaska: "America/Anchorage",
      Hawaii: "Pacific/Honolulu",
    };
    const zone = zones[timezoneName] || timezoneName;
    try {
      const timeText = new Intl.DateTimeFormat([], { hour: "numeric", minute: "2-digit", timeZone: zone }).format(new Date());
      return `${timeText} ${timezoneName}`;
    } catch (error) {
      if (error instanceof RangeError) return "";
      throw error;
    }
  }
  if (stage === "connected") fragment.prepend(heading);
  else if (stage !== "idle") fragment.append(heading, detail);

  const isLive = stage === "connected" && Boolean(target);
  for (const container of containers) {
    container.hidden = stage === "idle";
    container.dataset.stage = stage;
    container.classList.toggle("call-stage-live", isLive);
    container.replaceChildren(fragment.cloneNode(true));
  }

  stopCallTimer();
  if (stage === "connected") {
    const started = state.active_call_started_at ? Date.parse(state.active_call_started_at) : Date.now();
    startCallTimer(Number.isFinite(started) ? started : Date.now());
  }
  if (stage !== S.previousStage && stage !== "idle") {
    setDialerText("stageAnnouncer", stage === "connected"
      ? (state.pickup_answered_by === "voicemail" ? "Voicemail picked up." : "Prospect picked up.")
      : stage === "wrapup" ? "Call ended." : stage === "paused" ? "Dialing session paused." : stage === "ringing" ? "Prospect line is ringing." : "Dialing next prospect.");
    for (const container of containers) {
      container.classList.remove("stage-enter");
      void container.offsetWidth;
      container.classList.add("stage-enter");
    }
  }
  if (stage === "idle" && S.previousStage !== "idle") setDialerText("stageAnnouncer", "Dialing session stopped.");
  if (stage === "connected" && S.previousStage !== "connected") S.connectedAt = Date.now();
  if (stage === "connected" && S.previousStage !== "connected") stageEffects.match(state.active_lead);
  if (S.previousStage === "connected" && stage === "wrapup") stageEffects.reset(true);
  if (S.previousStage === "connected" && (stage === "ringing" || stage === "dialing")) stageEffects.reset(true);
  if (S.previousStage === "ringing" && stage === "dialing") stageEffects.reset();
  if ((stage === "idle" || stage === "paused") && stage !== S.previousStage) stageEffects.stop();
  if (stage === "dialing" || stage === "ringing") {
    const call = (state.in_flight || []).find((item) => ["creating", "ringing"].includes(item.state));
    const lead = call?.lead || state.next_lead;
    stageEffects.startSpin(lead?.id || call?.lead_id || "dialing");
  }
  if (stage !== "connected") S.connectedAt = null;
  S.previousStage = stage;
}
