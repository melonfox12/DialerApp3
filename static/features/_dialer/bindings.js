import { dialerEl, dialerEls } from "../../_core/format.js";
import { bindCallerIdQueueMenu } from "./caller-id-queue.js";
import { loadCallScriptPanel } from "./call-script-panel.js";
import { selectDialBusinessType, selectDialPoolStatus, selectTimezone } from "./pool.js";
import { startDialing, stopDialing } from "./session.js";
import { bindCrmStatus } from "./crm-status.js";
import { bindDialsExport } from "./dials.js";
import { bindNotesSidebar } from "./notes-sidebar.js";

export function bindDialer() {
  bindNotesSidebar();
  dialerEl("startButton")?.addEventListener("click", startDialing);
  bindDialsExport();
  bindCrmStatus();
  for (const stop of dialerEls("stopButton")) {
    stop.addEventListener("click", () => {
      stopDialing().catch(() => {});
    });
  }
  document.getElementById("poolTimezoneFilter")?.addEventListener("change", (event) => selectTimezone(event.target.value));
  const poolStatusSelectors = [dialerEl("dialerPoolStatusFilter"), document.getElementById("poolStatusFilter")].filter(Boolean);
  for (const selector of poolStatusSelectors) {
    selector?.addEventListener("change", (event) => selectDialPoolStatus(event.target.value));
  }
  dialerEl("dialerBusinessTypeFilter")?.addEventListener("change", (event) => selectDialBusinessType(event.target.value));
  bindCallerIdQueueMenu();
  loadCallScriptPanel();
  for (const panel of document.querySelectorAll(".dialer-run-panel")) {
    panel.addEventListener("click", (event) => {
      if (!event.target.closest("button, input, select, summary, a")) panel.focus();
    });
  }
}
