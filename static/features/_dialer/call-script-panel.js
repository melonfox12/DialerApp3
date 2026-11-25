import { postJson, request } from "../../_core/api.js";
import { dialerEls, setDialerText } from "../../_core/format.js";
import { showToast } from "../../_core/notify.js";

const vocabulary = JSON.parse(document.getElementById("vocabulary").textContent);

function defaultPanelPayload() {
  return {
    industries: vocabulary.callScriptIndustries || [],
    prospect_types: vocabulary.callScriptProspectTypes || [],
    variations: vocabulary.callScriptVariations || [],
    industry: vocabulary.defaultCallScriptIndustry || "",
    prospect_type: vocabulary.defaultCallScriptProspectType || "",
    variation: vocabulary.defaultCallScriptVariation || 1,
    body: "",
  };
}

const panel = {
  industries: [],
  prospect_types: [],
  variations: [],
  industry: "",
  prospect_type: "",
  variation: 1,
  body: "",
  loaded: false,
  loading: false,
};

let bound = false;
let saveTimer = null;
let switching = false;

function scriptKey(industry, prospectType, variation) {
  return `${industry}|${prospectType}|${variation}`;
}

function selectionFromUi() {
  const industry = dialerEls("callScriptIndustry")[0]?.value;
  const prospectType = dialerEls("callScriptProspectType")[0]?.value;
  const variation = dialerEls("callScriptVariation")[0]?.value;
  return { industry, prospectType, variation };
}

function setSelectOptions(select, options, value) {
  if (!select) return;
  const normalizedValue = String(value ?? "");
  select.replaceChildren(...options.map((item) => {
    const option = document.createElement("option");
    option.value = String(item.key);
    option.textContent = item.label;
    return option;
  }));
  if (options.some((item) => String(item.key) === normalizedValue)) {
    select.value = normalizedValue;
  }
}

function syncEditorsFrom(source) {
  if (!source) return;
  for (const editor of dialerEls("callScriptEditor")) {
    if (editor === source) continue;
    editor.value = source.value;
    editor.dataset.scriptKey = source.dataset.scriptKey;
    editor.dataset.savedValue = source.dataset.savedValue;
  }
}

function syncSelectsFrom(source) {
  if (!source) return;
  const peerId = source.id;
  for (const peer of dialerEls(peerId)) {
    if (peer === source) continue;
    peer.value = source.value;
  }
}

async function flushSave(editor) {
  if (!editor || switching) return;
  const { industry, prospectType, variation } = selectionFromUi();
  if (!industry || !prospectType || !variation) return;
  const body = editor.value;
  if (body === editor.dataset.savedValue) return;
  setDialerText("callScriptSaveState", "Saving…");
  try {
    const payload = await postJson("/api/call-script", {
      industry,
      prospect_type: prospectType,
      variation: Number(variation) || variation,
      body,
    });
    applyPanelPayload(payload);
    setDialerText("callScriptSaveState", "Saved");
    syncEditorsFrom(editor);
  } catch (error) {
    setDialerText("callScriptSaveState", "Save failed");
    showToast(error.message, true);
  }
}

function applyPanelPayload(payload) {
  if (!payload) return;
  panel.industries = payload.industries || [];
  panel.prospect_types = payload.prospect_types || [];
  panel.variations = payload.variations || [];
  panel.industry = payload.industry || panel.industry;
  panel.prospect_type = payload.prospect_type || panel.prospect_type;
  panel.variation = payload.variation ?? panel.variation ?? 1;
  panel.body = payload.body ?? "";
  panel.loaded = true;
  for (const select of dialerEls("callScriptIndustry")) {
    setSelectOptions(select, panel.industries, panel.industry);
  }
  for (const select of dialerEls("callScriptProspectType")) {
    setSelectOptions(select, panel.prospect_types, panel.prospect_type);
  }
  for (const select of dialerEls("callScriptVariation")) {
    setSelectOptions(select, panel.variations, panel.variation);
  }
  const key = scriptKey(panel.industry, panel.prospect_type, panel.variation);
  for (const editor of dialerEls("callScriptEditor")) {
    if (document.activeElement === editor && !switching) continue;
    editor.value = panel.body;
    editor.dataset.scriptKey = key;
    editor.dataset.savedValue = panel.body;
  }
}

export async function loadCallScriptPanel() {
  if (panel.loading) return;
  panel.loading = true;
  try {
    const payload = await request("/api/call-script");
    applyPanelPayload(payload);
    setDialerText("callScriptSaveState", "");
  } catch (error) {
    if (!panel.loaded) applyPanelPayload(defaultPanelPayload());
    setDialerText("callScriptSaveState", "Could not load");
  } finally {
    panel.loading = false;
  }
}

async function changeScriptSelection(industry, prospectType, variation) {
  clearTimeout(saveTimer);
  switching = true;
  const editor = dialerEls("callScriptEditor")[0];
  if (editor) await flushSave(editor);
  setDialerText("callScriptSaveState", "Loading…");
  try {
    const payload = await postJson("/api/call-script", {
      industry,
      prospect_type: prospectType,
      variation: Number(variation) || variation,
    });
    applyPanelPayload(payload);
    setDialerText("callScriptSaveState", "");
  } catch (error) {
    showToast(error.message, true);
    setDialerText("callScriptSaveState", "");
  } finally {
    switching = false;
  }
}

function bindCallScriptPanelOnce() {
  if (bound) return;
  bound = true;
  for (const select of dialerEls("callScriptIndustry")) {
    select.addEventListener("change", () => {
      syncSelectsFrom(select);
      const { prospectType, variation } = selectionFromUi();
      if (!prospectType || !variation) return;
      changeScriptSelection(select.value, prospectType, variation);
    });
  }
  for (const select of dialerEls("callScriptProspectType")) {
    select.addEventListener("change", () => {
      syncSelectsFrom(select);
      const { industry, variation } = selectionFromUi();
      if (!industry || !variation) return;
      changeScriptSelection(industry, select.value, variation);
    });
  }
  for (const select of dialerEls("callScriptVariation")) {
    select.addEventListener("change", () => {
      syncSelectsFrom(select);
      const { industry, prospectType } = selectionFromUi();
      if (!industry || !prospectType) return;
      changeScriptSelection(industry, prospectType, select.value);
    });
  }
  for (const editor of dialerEls("callScriptEditor")) {
    editor.addEventListener("input", () => {
      syncEditorsFrom(editor);
      clearTimeout(saveTimer);
      setDialerText("callScriptSaveState", "Editing…");
      saveTimer = setTimeout(() => flushSave(editor), 700);
    });
    editor.addEventListener("blur", () => {
      clearTimeout(saveTimer);
      flushSave(editor);
    });
  }
}

export function renderCallScriptPanel() {
  bindCallScriptPanelOnce();
  if (!panel.loaded && !panel.loading) {
    loadCallScriptPanel();
    return;
  }
  applyPanelPayload(panel);
}

export function callScriptEditorFocused() {
  return dialerEls("callScriptEditor").some((editor) => editor === document.activeElement);
}