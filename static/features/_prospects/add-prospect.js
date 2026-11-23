import { postJson } from "../../_core/api.js";
import { applyMutationPayload } from "../../_core/sync-state.js";
import { CRM_STATUS_KEYS, CRM_STATUS_LABELS, byId, fillTimezoneSelect, prospectDisplayName } from "../../_core/format.js";
import { showToast } from "../../_core/notify.js";
import { render } from "../../core.js";

const STANDARD_FIELDS = [
  ["company", "Company", "text", ""],
  ["contact_name", "Contact name", "text", ""],
  ["office_manager", "Office manager", "text", ""],
  ["category", "Category", "text", "pest control"],
  ["city", "City", "text", ""],
  ["state", "State", "text", ""],
  ["phone", "Phone number", "tel", ""],
  ["lead_tier", "Lead tier", "text", "C"],
  ["timezone", "Timezone", "timezone", ""],
];

export function bindAddProspect() {
  byId("addProspectButton").addEventListener("click", openAddProspectDialog);
  byId("closeAddProspect").addEventListener("click", closeAddProspectDialog);
  byId("cancelAddProspect").addEventListener("click", closeAddProspectDialog);
  byId("addProspectDialog").addEventListener("click", (event) => {
    if (event.target === byId("addProspectDialog")) closeAddProspectDialog();
  });
  byId("addProspectForm").addEventListener("submit", (event) => {
    event.preventDefault();
    saveProspect();
  });
}

function openAddProspectDialog() {
  const fields = byId("addProspectFields");
  fields.replaceChildren();
  for (const [name, label, type, placeholder] of STANDARD_FIELDS) {
    fields.append(type === "timezone" ? timezoneField() : textField(name, label, { type, placeholder, required: name === "phone" }));
  }
  fields.append(statusField());
  const error = byId("addProspectError");
  error.hidden = true;
  error.textContent = "";
  byId("addProspectDialog").showModal();
  fields.querySelector("input")?.focus();
}

function closeAddProspectDialog() {
  byId("addProspectDialog").close();
}

function textField(name, label, options = {}) {
  const wrap = document.createElement("label");
  wrap.className = "form-field";
  const title = document.createElement("span");
  title.textContent = label;
  const input = document.createElement("input");
  input.name = name;
  input.dataset.prospectField = name;
  input.type = options.type || "text";
  input.autocomplete = "off";
  if (options.placeholder) input.placeholder = options.placeholder;
  if (options.required) input.required = true;
  wrap.append(title, input);
  return wrap;
}

function timezoneField() {
  const wrap = document.createElement("label");
  wrap.className = "form-field";
  const title = document.createElement("span");
  title.textContent = "Timezone";
  const select = document.createElement("select");
  select.name = "timezone";
  select.dataset.prospectField = "timezone";
  fillTimezoneSelect(select, "Unknown");
  wrap.append(title, select);
  return wrap;
}

function statusField() {
  const wrap = document.createElement("label");
  wrap.className = "form-field";
  const title = document.createElement("span");
  title.textContent = "Call status";
  const select = document.createElement("select");
  select.name = "status";
  select.dataset.prospectField = "status";
  for (const value of CRM_STATUS_KEYS) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = CRM_STATUS_LABELS[value];
    option.selected = value === "new";
    select.append(option);
  }
  wrap.append(title, select);
  return wrap;
}

function fieldValue(name) {
  const input = byId("addProspectForm").elements.namedItem(name);
  return input ? String(input.value || "").trim() : "";
}

async function saveProspect() {
  const button = byId("saveAddProspect");
  const error = byId("addProspectError");
  button.disabled = true;
  error.hidden = true;
  try {
    const result = await postJson("/api/leads", {
      company: fieldValue("company"),
      contact_name: fieldValue("contact_name"),
      office_manager: fieldValue("office_manager"),
      category: fieldValue("category"),
      city: fieldValue("city"),
      state: fieldValue("state"),
      phone: fieldValue("phone"),
      lead_tier: fieldValue("lead_tier"),
      timezone: fieldValue("timezone"),
      status: fieldValue("status"),
    });
    await applyMutationPayload(result);
    closeAddProspectDialog();
    render();
    const lead = result.lead || {};
    showToast(`${prospectDisplayName(lead)} added`);
  } catch (saveError) {
    error.hidden = false;
    error.textContent = saveError?.message || "Could not add that prospect.";
  } finally {
    button.disabled = false;
  }
}