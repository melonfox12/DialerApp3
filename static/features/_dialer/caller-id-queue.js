import { state } from "../../_core/state.js";
import { dialerEl, dialerEls } from "../../_core/format.js";

function lastFour(phone) {
  const digits = String(phone || "").replace(/\D/g, "");
  return digits.slice(-4) || "????";
}

function formatPhone(phone) {
  const digits = String(phone || "").replace(/\D/g, "");
  if (digits.length === 11 && digits.startsWith("1")) {
    return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
  }
  return phone || "";
}

function summaryLabels(view) {
  const dialing = Boolean(view?.dialing_active);
  const primary = dialing && view.in_use?.length ? view.in_use : view.up_next || [];
  if (!primary.length) return "Caller IDs";
  return primary.map((phone) => lastFour(phone)).join(", ");
}

function renderList(listEl, view) {
  listEl.replaceChildren(...(view.rows || []).map((row) => {
    const item = document.createElement("li");
    item.className = `caller-id-queue-item caller-id-queue-${row.status || "waiting"}`;
    item.textContent = formatPhone(row.phone);
    return item;
  }));
}

let menuBound = false;
let documentCloseBound = false;

export function renderCallerIdQueueMenu() {
  const view = state.caller_id_queue || {};
  for (const summary of dialerEls("dialerCallerIdQueueSummary")) {
    summary.textContent = summaryLabels(view);
  }
  for (const list of dialerEls("dialerCallerIdQueueList")) {
    renderList(list, view);
  }
  for (const menu of dialerEls("dialerCallerIdQueueMenu")) {
    menu.classList.toggle("is-live", Boolean(view.dialing_active && view.in_use?.length));
  }
}

function closePanel(panel, button) {
  if (!panel) return;
  panel.hidden = true;
  button?.setAttribute("aria-expanded", "false");
}

function openPanel(panel, button) {
  if (!panel) return;
  panel.hidden = false;
  button?.setAttribute("aria-expanded", "true");
}

export function bindCallerIdQueueMenu() {
  if (menuBound) return;
  menuBound = true;
  const roots = dialerEls("dialerCallerIdQueueMenu");
  if (!roots.length) return;
  if (!documentCloseBound) {
    documentCloseBound = true;
    document.addEventListener("click", (event) => {
      if (event.target.closest(".caller-id-queue-menu")) return;
      for (const root of dialerEls("dialerCallerIdQueueMenu")) {
        const button = root.querySelector(".caller-id-queue-button");
        const panel = root.querySelector(".caller-id-queue-panel");
        closePanel(panel, button);
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      for (const root of dialerEls("dialerCallerIdQueueMenu")) {
        const panel = root.querySelector(".caller-id-queue-panel");
        if (panel && !panel.hidden) {
          const button = root.querySelector(".caller-id-queue-button");
          closePanel(panel, button);
          button?.focus();
        }
      }
    });
  }
  for (const root of roots) {
    const button = root.querySelector(".caller-id-queue-button");
    const panel = root.querySelector(".caller-id-queue-panel");
    button?.addEventListener("click", (event) => {
      event.stopPropagation();
      if (!panel) return;
      const open = panel.hidden;
      if (open) openPanel(panel, button);
      else closePanel(panel, button);
    });
  }
}

export function dialerCallerIdQueueRoot() {
  return dialerEl("dialerCallerIdQueueMenu");
}