import { selectedLeadIds, selection } from "./selection.js";
import { createCrmStatusSelect } from "../../_core/format.js";
import { prospectDisplayName } from "../../_core/format.js";
import { formatPhoneNumber } from "../../_core/phone.js";
import { LEAD_COLUMNS } from "./query.js";
import { appendNotesCell } from "../../_core/notes.js";
import { openTranscript } from "./transcript.js";

const EDITABLE_TEXT_KEYS = new Set([
  "company",
  "contact_name",
  "office_manager",
  "city",
  "lead_tier",
  "signal",
  "category",
  "website",
]);

export function appendLeadRows(body, leads, onSelection) {
  for (const lead of leads) {
    const row = document.createElement("tr");
    row.dataset.leadId = lead.id;
    const blocked = lead.status === "closed";
    const label = prospectDisplayName(lead);
    row.title = blocked ? "Will not be dialed" : lead.phone ? "Right-click to dial" : "No phone number";
    row.classList.toggle("selected", selectedLeadIds.has(lead.id));
    const selectionCell = document.createElement("td");
    selectionCell.className = "selection-cell";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "prospect-checkbox";
    checkbox.checked = selectedLeadIds.has(lead.id);
    checkbox.setAttribute("aria-label", `Select ${label}`);
    checkbox.addEventListener("click", (event) => {
      const targetIndex = leads.findIndex((item) => item.id === lead.id);
      const anchorIndex = leads.findIndex((item) => item.id === selection.anchorId);
      if (event.shiftKey && anchorIndex >= 0 && targetIndex >= 0) {
        const start = Math.min(anchorIndex, targetIndex);
        const end = Math.max(anchorIndex, targetIndex);
        for (const item of leads.slice(start, end + 1)) {
          if (checkbox.checked) selectedLeadIds.add(item.id);
          else selectedLeadIds.delete(item.id);
        }
      } else if (checkbox.checked) {
        selectedLeadIds.add(lead.id);
      } else {
        selectedLeadIds.delete(lead.id);
      }
      selection.anchorId = lead.id;
      onSelection();
    });
    selectionCell.append(checkbox);
    row.append(selectionCell);

    for (const column of LEAD_COLUMNS) appendLeadColumn(row, lead, column);

    appendNotesCell(row, lead, { compact: true });

    const transcriptCell = document.createElement("td");
    const transcriptButton = document.createElement("button");
    const transcriptCount = lead.transcript?.length || 0;
    transcriptButton.type = "button";
    transcriptButton.className = "transcript-view-button";
    transcriptButton.textContent = transcriptCount ? `View · ${transcriptCount}` : "No transcript";
    transcriptButton.disabled = transcriptCount === 0;
    transcriptButton.setAttribute(
      "aria-label",
      transcriptCount ? `View ${transcriptCount} transcript utterances for ${label}` : `No transcript for ${label}`,
    );
    transcriptButton.addEventListener("click", () => openTranscript(lead));
    transcriptCell.append(transcriptButton);
    row.append(transcriptCell);
    body.append(row);
  }
}

function statusCell(lead) {
  const cell = document.createElement("td");
  cell.className = "status-cell";
  cell.append(createCrmStatusSelect(lead));
  return cell;
}

function appendLeadColumn(row, lead, column) {
  if (column.key === "status") {
    row.append(statusCell(lead));
    return;
  }
  if (column.key === "phone") {
    row.append(phoneCell(lead));
    return;
  }
  if (column.kind === "number") {
    row.append(metricCell(formatCount(lead[column.key])));
    return;
  }
  if (EDITABLE_TEXT_KEYS.has(column.key)) {
    row.append(dataCell(fieldInput(lead, column.key, lead[column.key] || "", column.label)));
    return;
  }
  row.append(metricCell(String(lead[column.key] || "").trim() || "—"));
}

function phoneCell(lead) {
  const cell = document.createElement("td");
  cell.className = "phone-cell";
  if (!lead.phone) {
    cell.textContent = "—";
    return cell;
  }
  const link = document.createElement("a");
  link.className = "phone-link";
  link.href = `tel:${lead.phone}`;
  link.textContent = formatPhoneNumber(lead.phone);
  cell.title = link.textContent;
  cell.append(link);
  return cell;
}

function metricCell(text) {
  const cell = document.createElement("td");
  cell.className = "metric-cell";
  cell.textContent = text;
  return cell;
}

function formatCount(value) {
  if (value === null || value === undefined || value === "") return "—";
  const number = Number(value);
  return Number.isFinite(number) ? String(number) : "—";
}

function dataCell(control) {
  const cell = document.createElement("td");
  cell.append(control);
  return cell;
}

function fieldInput(lead, field, value, label) {
  const input = document.createElement("input");
  input.type = "text";
  input.className = "cell-editor";
  input.value = value;
  input.placeholder = "—";
  input.autocomplete = "off";
  input.setAttribute("aria-label", `${label} for ${prospectDisplayName(lead)}`);
  bindFieldEditor(input, { lead, field });
  return input;
}

function bindFieldEditor(input, detail) {
  input.dataset.savedValue = input.value;
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      input.value = input.dataset.savedValue;
      event.preventDefault();
      input.blur();
    } else if (event.key === "Enter") {
      event.preventDefault();
      input.blur();
    }
  });
  input.addEventListener("change", () => {
    const value = input.value.trim();
    if (value === input.dataset.savedValue) {
      input.value = input.dataset.savedValue;
      return;
    }
    document.dispatchEvent(new CustomEvent("prospect-field", {
      detail: { ...detail, value, previous: input.dataset.savedValue, input },
    }));
  });
  input.addEventListener("blur", () => {
    document.dispatchEvent(new CustomEvent("prospect-field-blur"));
  });
}