import { state } from "../../_core/state.js";
import { byId } from "../../_core/format.js";

export const LEAD_COLUMNS = [
  { label: "Company", key: "company", kind: "text" },
  { label: "Contact", key: "contact_name", kind: "text" },
  { label: "Office manager", key: "office_manager", kind: "text" },
  { label: "Phone", key: "phone", kind: "text" },
  { label: "City", key: "city", kind: "text" },
  { label: "Tier", key: "lead_tier", kind: "text" },
  { label: "Score", key: "lead_score", kind: "number" },
  { label: "Signal", key: "signal", kind: "text" },
  { label: "Days since signal", key: "days_since_signal", kind: "number" },
  { label: "Call status", key: "status", kind: "text" },
];

export const TRAILING_COLUMNS = [
  { label: "Notes", key: "notes", kind: "text" },
  { label: "Call transcript", key: "transcript", kind: "number" },
];

const TIER_RANK = { A: 0, B: 1, C: 2, D: 3 };

let columnSort = { key: "lead_tier", direction: "asc", kind: "text" };

export function currentColumnSort() {
  return columnSort;
}

export function setColumnSort(key, direction) {
  columnSort = { key, direction, kind: columnKind(key) };
}

export function toggleColumnSort(key) {
  const kind = columnKind(key);
  if (columnSort?.key === key) {
    columnSort = { key, kind, direction: columnSort.direction === "desc" ? "asc" : "desc" };
    return;
  }
  columnSort = { key, kind, direction: kind === "number" ? "desc" : "asc" };
}

export function locationText(lead, key) {
  return String(lead?.[key] || "").trim();
}

export function importedColumns() {
  return [];
}

export function syncStateFilter() {
  const select = byId("stateFilter");
  if (!select) return;
  const current = select.value;
  const states = [...new Set(state.leads.map((lead) => locationText(lead, "state")).filter(Boolean))];
  states.sort((left, right) => left.localeCompare(right, undefined, { sensitivity: "base" }));
  const wanted = ["", ...states];
  const existing = [...select.options].map((option) => option.value);
  if (existing.join("\0") === wanted.join("\0")) return;
  select.replaceChildren();
  const all = document.createElement("option");
  all.value = "";
  all.textContent = "All states";
  select.append(all);
  for (const code of states) {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = code;
    select.append(option);
  }
  select.value = wanted.includes(current) ? current : "";
}

export function filteredLeads() {
  const query = byId("searchInput").value.trim().toLocaleLowerCase();
  const filter = byId("statusFilter").value;
  const stateFilter = (byId("stateFilter")?.value || "").trim().toUpperCase();
  const leads = state.leads.filter((lead) => {
    if (filter !== "all" && lead.status !== filter) return false;
    if (stateFilter && locationText(lead, "state").trim().toUpperCase() !== stateFilter) return false;
    if (!query) return true;
    const values = [
      lead.company,
      lead.contact_name,
      lead.office_manager,
      lead.phone,
      lead.city,
      lead.lead_tier,
      lead.lead_score,
      lead.signal,
      lead.days_since_signal,
      lead.category,
      lead.website,
      lead.score_reasons,
      lead.status,
    ];
    return values.some((value) => String(value ?? "").toLocaleLowerCase().includes(query));
  });
  if (!columnSort) return leads;
  return leads.sort(compareLeads);
}

export function crmTableSignature() {
  return JSON.stringify([
    columnSort,
    byId("stateFilter")?.value || "",
    state.pending_outcome?.id || null,
    state.leads.map((lead) => [
      lead.id,
      lead.company,
      lead.contact_name,
      lead.office_manager,
      lead.phone,
      lead.city,
      lead.lead_tier,
      lead.lead_score,
      lead.signal,
      lead.days_since_signal,
      lead.status,
      lead.scheduled_until,
      lead.score_reasons,
      lead.transcript?.length || 0,
    ]),
  ]);
}

function columnKind(key) {
  const column = [...LEAD_COLUMNS, ...TRAILING_COLUMNS].find((item) => item.key === key);
  return column?.kind || "text";
}

function numberOrNull(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function compareLeads(left, right) {
  const direction = columnSort.direction === "desc" ? -1 : 1;
  const leftValue = sortValue(left);
  const rightValue = sortValue(right);
  if (leftValue == null && rightValue == null) return tieBreak(left, right);
  if (leftValue == null) return 1;
  if (rightValue == null) return -1;
  if (typeof leftValue === "number" && typeof rightValue === "number") {
    return leftValue === rightValue ? tieBreak(left, right) : (leftValue - rightValue) * direction;
  }
  const compared = String(leftValue).localeCompare(String(rightValue), undefined, { numeric: true, sensitivity: "base" });
  return compared ? compared * direction : tieBreak(left, right);
}

function sortValue(lead) {
  const key = columnSort.key;
  if (columnSort.kind === "number") {
    if (key === "transcript") return lead.transcript?.length || 0;
    return numberOrNull(lead[key]);
  }
  if (key === "notes") {
    return String(lead.score_reasons || "").trim() || null;
  }
  return String(lead[key] || "").trim() || null;
}

function tieBreak(left, right) {
  const leftTier = TIER_RANK[String(left.lead_tier || "C").toUpperCase()] ?? 9;
  const rightTier = TIER_RANK[String(right.lead_tier || "C").toUpperCase()] ?? 9;
  if (leftTier !== rightTier) return leftTier - rightTier;
  const leftScore = numberOrNull(left.lead_score) ?? -Infinity;
  const rightScore = numberOrNull(right.lead_score) ?? -Infinity;
  if (leftScore !== rightScore) return rightScore - leftScore;
  return String(right.signal_date || "").localeCompare(String(left.signal_date || ""));
}