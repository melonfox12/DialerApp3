import { postJson, showToast } from "../../core.js";

function field(label, input) {
  const wrap = document.createElement("label");
  wrap.className = "form-field";
  const span = document.createElement("span");
  span.textContent = label;
  wrap.append(span, input);
  return wrap;
}

function section(title, eyebrow, fields) {
  const sec = document.createElement("section");
  sec.className = "team-settings-section";
  const head = document.createElement("div");
  head.className = "audio-section-heading";
  const e = document.createElement("div");
  e.className = "eyebrow";
  e.textContent = eyebrow;
  const h = document.createElement("h4");
  h.textContent = title;
  head.append(e, h);
  sec.append(head);
  for (const node of fields) {
    sec.append(node);
  }
  return sec;
}

export function buildMemberSettingsForm(container) {
  if (!container) return {};
  container.replaceChildren();
  const ids = {};
  const input = (id, type = "text", extra = {}) => {
    const el = document.createElement("input");
    el.id = id;
    el.name = id;
    el.type = type;
    Object.assign(el, extra);
    ids[id] = el;
    return el;
  };
  const textarea = (id, rows = 3) => {
    const el = document.createElement("textarea");
    el.id = id;
    el.rows = rows;
    ids[id] = el;
    return el;
  };
  container.append(
    section(
      "Session preferences",
      "CALL FLOW",
      [
        field("Session conversation goal", input("teamSetSessionGoal", "number", { min: 1, max: 1000 })),
        field("Conversation threshold (seconds)", input("teamSetConvo", "number", { min: 1, max: 3600 })),
        field("Auto-advance delay (seconds)", input("teamSetAdvance", "number", { min: 0, max: 60 })),
        field("Break nudge interval (minutes)", input("teamSetBreak", "number", { min: 1, max: 720 })),
        field("Opener / talking points", textarea("teamSetOpener", 3)),
      ],
    ),
    section(
      "Twilio & callbacks",
      "API — MANAGED",
      [
        field("Twilio Account SID", input("teamSetAccountSid")),
        field("Twilio Auth Token", input("teamSetAuthToken", "password")),
        field("Twilio API Key SID", input("teamSetApiKey")),
        field("Twilio API Key Secret", input("teamSetApiSecret", "password")),
        field("Twilio TwiML App SID", input("teamSetTwimlApp")),
        field("Public HTTPS callback URL", input("teamSetPublicUrl")),
      ],
    ),
    section(
      "AI bridge & keys",
      "INTEGRATIONS",
      [
        field("Bridge WSS URL", input("teamSetBridgeWss")),
        field("Bridge app URL", input("teamSetBridgeApp")),
        field("Bridge secret", input("teamSetBridgeSecret", "password")),
        field("OpenAI API key", input("teamSetOpenai", "password")),
        field("Cartesia API key", input("teamSetCartesia", "password")),
        field("Cartesia voice id", input("teamSetCartesiaVoice")),
      ],
    ),
  );
  return ids;
}

export function applyMemberSettings(fields, settings) {
  fields.teamSetSessionGoal.value = settings.session_goal ?? "";
  fields.teamSetConvo.value = settings.conversation_threshold ?? "";
  fields.teamSetAdvance.value = settings.auto_advance_delay ?? "";
  fields.teamSetBreak.value = settings.break_nudge_minutes ?? "";
  fields.teamSetOpener.value = settings.opening_script || "";
  fields.teamSetAccountSid.value = settings.account_sid || "";
  fields.teamSetAuthToken.value = "";
  fields.teamSetAuthToken.placeholder = settings.has_auth_token ? "Saved — leave blank to keep" : "";
  fields.teamSetApiKey.value = settings.api_key || "";
  fields.teamSetApiSecret.value = "";
  fields.teamSetApiSecret.placeholder = settings.has_api_secret ? "Saved — leave blank to keep" : "";
  fields.teamSetTwimlApp.value = settings.twiml_app_sid || "";
  fields.teamSetPublicUrl.value = settings.public_base_url || "";
  fields.teamSetBridgeWss.value = settings.ai_bridge_wss_url || "";
  fields.teamSetBridgeApp.value = settings.ai_bridge_app_url || "";
  fields.teamSetBridgeSecret.value = "";
  fields.teamSetBridgeSecret.placeholder = settings.has_ai_bridge_secret ? "Saved — leave blank to keep" : "";
  fields.teamSetOpenai.value = "";
  fields.teamSetOpenai.placeholder = settings.has_openai_api_key ? "Saved — leave blank to keep" : "";
  fields.teamSetCartesia.value = settings.cartesia_api_key || "";
  fields.teamSetCartesiaVoice.value = settings.cartesia_voice_id || "";
}

export function memberSettingsPayload(fields) {
  return {
    session_goal: fields.teamSetSessionGoal.value,
    conversation_threshold: fields.teamSetConvo.value,
    auto_advance_delay: fields.teamSetAdvance.value,
    break_nudge_minutes: fields.teamSetBreak.value,
    opening_script: fields.teamSetOpener.value,
    account_sid: fields.teamSetAccountSid.value,
    auth_token: fields.teamSetAuthToken.value,
    api_key: fields.teamSetApiKey.value,
    api_secret: fields.teamSetApiSecret.value,
    twiml_app_sid: fields.teamSetTwimlApp.value,
    public_base_url: fields.teamSetPublicUrl.value,
    ai_bridge_wss_url: fields.teamSetBridgeWss.value,
    ai_bridge_app_url: fields.teamSetBridgeApp.value,
    ai_bridge_secret: fields.teamSetBridgeSecret.value,
    openai_api_key: fields.teamSetOpenai.value,
    cartesia_api_key: fields.teamSetCartesia.value,
    cartesia_voice_id: fields.teamSetCartesiaVoice.value,
  };
}

export async function saveMemberSettings(userId, fields) {
  const payload = memberSettingsPayload(fields);
  const saved = await postJson(`/api/team/members/${encodeURIComponent(userId)}/settings`, payload);
  applyMemberSettings(fields, saved);
  showToast("Member settings saved.");
}