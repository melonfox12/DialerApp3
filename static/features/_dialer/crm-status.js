import { postJson } from "../../_core/api.js";
import { applyMutationPayload } from "../../_core/sync-state.js";
import { state } from "../../_core/state.js";
import { CRM_STATUS_KEYS, dialerEls, leavesQueueForGood } from "../../_core/format.js";
import { errorText, showToast } from "../../_core/notify.js";
import { render } from "../../core.js";
import { nextProspectLabel, queueProspect } from "./queue.js";

const PRIMARY_OUTCOMES = [
  // dialed status keeps the 2-hour callback timer and pool re-queue behavior.
  { status: "dialed", label: "Engaged", className: "outcome-btn outcome-btn-engaged" },
  { disposition: "no_answer", label: "No answer", className: "outcome-btn outcome-btn-no-answer" },
  { status: "closed", label: "Disqualified", className: "outcome-btn outcome-btn-disqualified" },
  { status: "qualified", label: "Qualified", className: "outcome-btn outcome-btn-qualified" },
];

const BOOKED_OUTCOME = {
  status: "booked",
  label: "Booked",
  className: "outcome-btn outcome-btn-booked outcome-btn-booked-hero",
};

let saving = false;

function buildButton(item, lead) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = item.className;
  const outcomeStatus = item.status || "dialed";
  if (item.disposition) button.dataset.disposition = item.disposition;
  else button.dataset.status = item.status;
  button.textContent = item.label;
  button.disabled = !lead || saving || leavesQueueForGood(lead, outcomeStatus);
  button.setAttribute("aria-pressed", lead?.status === outcomeStatus ? "true" : "false");
  return button;
}

export function bindCrmStatus() {
  for (const root of dialerEls("crmStatusButtons")) {
    root.addEventListener("click", (event) => {
      const button = event.target.closest("[data-status], [data-disposition]");
      if (!button || saving) return;
      const lead = queueProspect();
      if (!lead) return;
      const disposition = String(button.dataset.disposition || "").trim();
      if (disposition) {
        saveDisposition(lead, disposition, button.textContent);
        return;
      }
      const status = String(button.dataset.status || "").trim();
      if (!CRM_STATUS_KEYS.includes(status)) return;
      if (status === "booked" && lead.status === "booked") return;
      saveCrmStatus(lead, status, button.textContent);
    });
  }
}

export function renderCrmStatus() {
  const lead = queueProspect();
  const label = lead ? nextProspectLabel(lead) : "No prospect in the queue";

  const primaryRow = document.createElement("div");
  primaryRow.className = "crm-outcome-buttons-primary";
  primaryRow.append(...PRIMARY_OUTCOMES.map((item) => buildButton(item, lead)));

  const bookedRow = document.createElement("div");
  bookedRow.className = "crm-outcome-buttons-booked";
  bookedRow.append(buildButton(BOOKED_OUTCOME, lead));

  for (const target of dialerEls("crmStatusTarget")) target.textContent = label;
  for (const root of dialerEls("crmStatusButtons")) {
    root.replaceChildren(primaryRow, bookedRow);
  }
}

async function saveCrmStatus(lead, status, label) {
  saving = true;
  renderCrmStatus();
  const name = nextProspectLabel(lead);
  try {
    const result = await postJson(`/api/leads/${encodeURIComponent(lead.id)}/status`, {
      status,
      crm_only: true,
    });
    await applyMutationPayload(result);
    if (status === "dialed") showToast(`Callback started for ${name}`);
    else if (status === "closed") showToast(`${name} marked disqualified`);
    else if (status === "qualified") showToast(`${name}: Qualified`);
    else if (status === "booked") showToast(`${name}: Meeting booked!`);
    else showToast(`${name}: ${label}`);
  } catch (error) {
    showToast(errorText(error, "Could not update the CRM status."), true);
  } finally {
    saving = false;
    render();
  }
}

async function saveDisposition(lead, disposition, label) {
  saving = true;
  renderCrmStatus();
  const name = nextProspectLabel(lead);
  try {
    const result = await postJson(`/api/leads/${encodeURIComponent(lead.id)}/status`, { disposition });
    await applyMutationPayload(result);
    if (disposition === "no_answer") showToast(`No answer — callback started for ${name}`);
    else showToast(`${name}: ${label}`);
  } catch (error) {
    showToast(errorText(error, "Could not save the call disposition."), true);
  } finally {
    saving = false;
    render();
  }
}