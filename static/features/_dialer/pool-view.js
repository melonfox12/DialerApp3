import { state } from "../../_core/state.js";
import {
  byId,
  CRM_STATUS_LABELS,
  DEFAULT_DIAL_POOL_STATUS,
  DIAL_POOL_STATUSES,
  DIAL_POOL_STATUS_LABELS,
  dialerEls,
  prospectDisplayName,
  setText,
} from "../../_core/format.js";
import { appendNotesCell, notesEditorFocused } from "../../_core/notes.js";
import { openTranscript } from "../../_core/transcript.js";

export function renderPoolStatusFilters() {
  const keys = DIAL_POOL_STATUSES;
  const labels = DIAL_POOL_STATUS_LABELS;
  const selected = state.dial_pool_status || DEFAULT_DIAL_POOL_STATUS;
  const options = keys.map((key) => new Option(labels[key] || key, key));
  for (const select of [...dialerEls("dialerPoolStatusFilter"), document.getElementById("poolStatusFilter")].filter(Boolean)) {
    select.replaceChildren(...options.map((option) => option.cloneNode(true)));
    select.value = keys.includes(selected) ? selected : "new";
  }
}

function industryFilterOptions() {
  const fromCatalog = state.business_type_options;
  if (Array.isArray(fromCatalog) && fromCatalog.length) {
    return fromCatalog.map((value) => String(value).trim()).filter(Boolean);
  }
  const seen = new Map();
  for (const lead of state.leads || []) {
    const value = String(lead.category || "").trim();
    if (!value) continue;
    const folded = value.toLowerCase();
    if (!seen.has(folded)) seen.set(folded, value);
  }
  return [...seen.values()].sort((left, right) => left.localeCompare(right, undefined, { sensitivity: "base" }));
}

export function renderBusinessTypeFilter() {
  const selects = dialerEls("dialerBusinessTypeFilter");
  if (!selects.length) return;
  const selected = state.selected_business_type || "";
  const industries = industryFilterOptions();
  const known = industries.map((value) => value.toLowerCase());
  const options = [new Option("All industries", "")];
  options.push(...industries.map((value) => new Option(value, value)));
  if (selected && !known.includes(selected.toLowerCase())) {
    options.push(new Option(selected, selected));
  }
  const value = selected && (known.includes(selected.toLowerCase()) || selected) ? selected : "";
  for (const select of selects) {
    select.replaceChildren(...options.map((o) => o.cloneNode(true)));
    select.value = value;
  }
}

export function renderPoolTimezoneFilter() {
  const poolSelect = document.getElementById("poolTimezoneFilter");
  if (!poolSelect) return;
  const groups = state.timezone_groups || [];
  const totalNew = groups.reduce((sum, group) => sum + group.count, 0);
  const selected = state.selected_timezone || "";
  const knownZones = groups.map((group) => group.name);
  const options = [new Option(`All time zones (${totalNew})`, "")];
  if (selected && !knownZones.includes(selected)) options.push(new Option(selected, selected));
  options.push(...groups.map((group) => new Option(`${group.name} (${group.count})`, group.name)));
  poolSelect.replaceChildren(...options.map((option) => option.cloneNode(true)));
  poolSelect.value = selected;
}

export function renderDialFilters() {
  renderPoolStatusFilters();
  renderBusinessTypeFilter();
  renderPoolTimezoneFilter();
}

export function syncDialFiltersFromState() {
  renderDialFilters();
}

export function renderCallerPool() {
  if (notesEditorFocused("poolTable")) return;
  const pool = state.pool || [];
  setText("poolTabCount", String(pool.length));
  const poolLabel = DIAL_POOL_STATUS_LABELS[state.dial_pool_status || DEFAULT_DIAL_POOL_STATUS] || "New";
  const typeSuffix = state.selected_business_type ? ` · ${state.selected_business_type}` : "";
  const zoneSuffix = state.selected_timezone ? ` · ${state.selected_timezone}` : "";
  setText("poolTableSummary", `${pool.length} ${poolLabel} prospect${pool.length === 1 ? "" : "s"}${typeSuffix}${zoneSuffix}`);
  const emptyHint = byId("poolTableEmptyHint");
  if (emptyHint) emptyHint.textContent = `Only prospects marked ${poolLabel} appear in this pool.`;
  const body = byId("poolTableBody");
  body.replaceChildren(...pool.map((lead) => {
    const row = document.createElement("tr");
    row.dataset.leadId = lead.id;
    row.title = lead.phone ? "Right-click to dial" : "No phone number";
    const prospect = document.createElement("td");
    const contact = document.createElement("div");
    contact.className = "contact-copy";
    const name = document.createElement("strong");
    name.textContent = lead.contact_name || "Unnamed prospect";
    const detail = document.createElement("span");
    detail.textContent = lead.company || prospectDisplayName(lead);
    contact.append(name, detail);
    prospect.append(contact);
    row.append(prospect);
    for (const value of [lead.company || "—", lead.phone || "—", lead.timezone || "Unknown"]) {
      const cell = document.createElement("td");
      cell.textContent = value;
      if (value === lead.phone) cell.className = "phone-cell";
      row.append(cell);
    }
    const status = document.createElement("td");
    const statusLabel = document.createElement("span");
    statusLabel.className = `pool-new-status pool-status-${lead.status || "new"}`;
    statusLabel.textContent = CRM_STATUS_LABELS[lead.status] || lead.status || "New";
    status.append(statusLabel);
    row.append(status);
    appendNotesCell(row, lead, { compact: true });
    const transcript = document.createElement("td");
    const button = document.createElement("button");
    const count = lead.transcript?.length || 0;
    button.type = "button";
    button.className = "transcript-view-button";
    button.textContent = count ? `View · ${count}` : "No transcript";
    button.disabled = count === 0;
    button.addEventListener("click", () => openTranscript(lead));
    transcript.append(button);
    row.append(transcript);
    return row;
  }));
  byId("poolTable").hidden = pool.length === 0;
  byId("poolTableEmpty").classList.toggle("visible", pool.length === 0);
}
