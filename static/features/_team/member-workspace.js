import { byId, postJson, request, setText, showToast } from "../../core.js";
import { renderBarChart, renderDispositionChart, renderLineChart } from "./member-charts.js";
import { applyMemberSettings, buildMemberSettingsForm, saveMemberSettings } from "./member-settings-form.js";

const CHART_SPANS = [
  { value: "session", label: "Current session" },
  { value: "today", label: "Today" },
  { value: "week", label: "This week" },
  { value: "month", label: "This month" },
];

const LINE_TIMELINES = [
  { value: "8h", label: "Last 8 hours" },
  { value: "week", label: "Last week" },
  { value: "month", label: "Last month" },
];

let chartView = "activity";
let rangeBar = "today";
let rangeLine = "week";
let settingsFields = null;
let settingsUserId = null;
let workspaceBound = false;
let lastMemberContext = null;
let onWorkspaceClose = null;
let onWorkspaceAfterClose = null;

export function setWorkspaceCloseHandler(handler) {
  onWorkspaceClose = handler;
}

export function setWorkspaceAfterClose(handler) {
  onWorkspaceAfterClose = handler;
}

function showRosterView(show) {
  const roster = byId("teamRosterView");
  if (roster) roster.hidden = !show;
}

export function closeMemberWorkspace() {
  settingsUserId = null;
  const panel = byId("teamMemberDetail");
  if (panel) panel.hidden = true;
  showRosterView(true);
  if (onWorkspaceAfterClose) onWorkspaceAfterClose();
  else {
    void import("../team.js").then((module) => module.syncTeamPageHeading?.());
  }
}

function formatUsageMinutes(value) {
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return "0";
  const rounded = Math.round(n * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

function usageCard(label, value, unit) {
  const card = document.createElement("article");
  card.className = "team-usage-card";
  const dt = document.createElement("p");
  dt.className = "team-usage-card-label";
  dt.textContent = label;
  const dd = document.createElement("p");
  dd.className = "team-usage-card-value";
  dd.textContent = `${formatUsageMinutes(value)}${unit ? ` ${unit}` : ""}`;
  card.append(dt, dd);
  return card;
}

function usageSummaryPreferringStored(apiSummary, member, live) {
  const fromApi = apiSummary || {};
  const fromMember = usageSummaryFromMember(member, live);
  const storedKeys = ["today_minutes", "week_minutes", "month_minutes"];
  const merged = { ...fromApi };
  for (const key of storedKeys) {
    const apiVal = Number(fromApi[key]);
    const rosterVal = Number(fromMember[key]);
    if (!Number.isFinite(apiVal) || apiVal <= 0) {
      if (Number.isFinite(rosterVal) && rosterVal > 0) merged[key] = rosterVal;
      continue;
    }
    if (Number.isFinite(rosterVal) && rosterVal > apiVal + 0.05) merged[key] = rosterVal;
  }
  const liveApi = Number(fromApi.live_session_minutes);
  const liveRoster = Number(fromMember.live_session_minutes);
  if (!Number.isFinite(liveApi) || liveApi <= 0) {
    if (Number.isFinite(liveRoster) && liveRoster > 0) merged.live_session_minutes = liveRoster;
  }
  return merged;
}

function renderUsageRow(summary) {
  const row = byId("teamMemberUsageRow");
  if (!row) return;
  row.replaceChildren(
    usageCard("Live session", summary?.live_session_minutes ?? 0, "min"),
    usageCard("Today", summary?.today_minutes ?? 0, "min"),
    usageCard("This week", summary?.week_minutes ?? 0, "min"),
    usageCard("This month", summary?.month_minutes ?? 0, "min"),
  );
}

function rangeOptionsForView(view) {
  return view === "timeline" ? LINE_TIMELINES : CHART_SPANS;
}

function syncRangeSelect(preserve = true) {
  const select = byId("teamMemberChartRange");
  if (!select) return;
  const options = rangeOptionsForView(chartView);
  const previous = preserve ? select.value : "";
  const remembered = chartView === "timeline" ? rangeLine : rangeBar;
  select.replaceChildren();
  for (const item of options) {
    const opt = document.createElement("option");
    opt.value = item.value;
    opt.textContent = item.label;
    select.append(opt);
  }
  const values = options.map((item) => item.value);
  const pick = values.includes(previous) ? previous : values.includes(remembered) ? remembered : values[0];
  select.value = pick;
  if (chartView === "timeline") rangeLine = pick;
  else rangeBar = pick;
}

function currentRangeQuery() {
  const value = byId("teamMemberChartRange")?.value || (chartView === "timeline" ? rangeLine : rangeBar);
  if (chartView === "timeline") {
    rangeLine = value;
    return { span: "today", timeline: value };
  }
  rangeBar = value;
  return { span: value, timeline: "week" };
}

function renderChart(analytics) {
  const host = byId("teamMemberChartHost");
  if (!host || !analytics) return;
  if (chartView === "activity") {
    const bars = analytics.activity_bars || {};
    renderBarChart(host, [bars.dials, bars.connected, bars.conversations_30s], [
      "Total dials",
      "Live connects",
      "Convos 30s+",
    ]);
    return;
  }
  if (chartView === "dispositions") {
    renderDispositionChart(host, analytics.dispositions || []);
    return;
  }
  renderLineChart(host, analytics.activity_line || []);
}

function bindWorkspaceChrome() {
  if (workspaceBound) return;
  workspaceBound = true;
  syncRangeSelect(false);
  for (const tab of document.querySelectorAll(".team-chart-view-tab")) {
    tab.addEventListener("click", () => {
      chartView = tab.dataset.chartView || "activity";
      for (const peer of document.querySelectorAll(".team-chart-view-tab")) {
        const active = peer === tab;
        peer.classList.toggle("is-active", active);
        peer.classList.toggle("active", active);
        peer.setAttribute("aria-selected", active ? "true" : "false");
      }
      syncRangeSelect();
      refreshWorkspaceCharts();
    });
  }
  byId("teamMemberChartRange")?.addEventListener("change", () => refreshWorkspaceCharts());
  byId("teamMemberTabAnalytics")?.addEventListener("click", () => setWorkspaceTab("analytics"));
  byId("teamMemberTabSettings")?.addEventListener("click", () => setWorkspaceTab("settings"));
  const settingsBody = byId("teamMemberSettingsBody");
  if (settingsBody && !settingsFields) {
    settingsFields = buildMemberSettingsForm(settingsBody);
  }
  byId("teamMemberSettingsForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!settingsUserId || !settingsFields) return;
    try {
      await saveMemberSettings(settingsUserId, settingsFields);
    } catch (error) {
      showToast(error.message || "Could not save member settings.", true);
    }
  });
}

export function setWorkspaceTab(which) {
  const analytics = which === "analytics";
  byId("teamMemberAnalyticsPanel").hidden = !analytics;
  byId("teamMemberSettingsPanel").hidden = analytics;
  const tabAnalytics = byId("teamMemberTabAnalytics");
  const tabSettings = byId("teamMemberTabSettings");
  tabAnalytics?.setAttribute("aria-selected", analytics ? "true" : "false");
  tabSettings?.setAttribute("aria-selected", analytics ? "false" : "true");
  tabAnalytics?.classList.toggle("active", analytics);
  tabSettings?.classList.toggle("active", !analytics);
  if (!analytics && settingsUserId) {
    loadMemberSettings(settingsUserId);
  }
}

function fallbackAnalytics() {
  const today = lastMemberContext?.member?.today || {};
  const session = lastMemberContext?.live?.session_stats || {};
  return {
    usage_summary: usageSummaryFromMember(lastMemberContext?.member, lastMemberContext?.live),
    activity_bars: {
      dials: Number(today.dials ?? session.dials ?? 0),
      connected: Number(today.connected ?? session.connects ?? 0),
      conversations_30s: Number(session.conversations ?? 0),
    },
    dispositions: [],
    activity_line: [],
  };
}

async function refreshWorkspaceCharts() {
  if (!settingsUserId) return;
  const { span, timeline } = currentRangeQuery();
  try {
    const analytics = await request(
      `/api/team/members/${encodeURIComponent(settingsUserId)}/analytics?span=${encodeURIComponent(span)}&timeline=${encodeURIComponent(timeline)}`,
    );
    const summary = usageSummaryPreferringStored(
      analytics.usage_summary,
      lastMemberContext?.member,
      lastMemberContext?.live,
    );
    renderUsageRow(summary);
    renderChart(analytics);
  } catch (error) {
    const fallback = fallbackAnalytics();
    renderUsageRow(fallback.usage_summary);
    renderChart(fallback);
    showToast(error.message || "Analytics are limited — showing roster data only.", true);
  }
}

async function loadMemberSettings(userId) {
  if (!settingsFields) return;
  try {
    const settings = await request(`/api/team/members/${encodeURIComponent(userId)}/settings`);
    applyMemberSettings(settingsFields, settings);
  } catch (error) {
    showToast(error.message || "Could not load member settings.", true);
  }
}

export async function refreshMemberWorkspace(userId, live, extrasRenderer, member) {
  if (!userId || userId !== settingsUserId) return;
  lastMemberContext = {
    member: member ?? lastMemberContext?.member,
    live: live ?? lastMemberContext?.live,
  };
  const liveLine = byId("teamMemberLiveLine");
  if (liveLine && live) {
    const parts = live.online ? ["Live", live.stage || "idle"] : ["Offline"];
    if (live.active_lead_name) parts.push(live.active_lead_name);
    liveLine.textContent = parts.join(" · ");
  }
  const extras = byId("teamMemberDetailExtras");
  if (extras && extrasRenderer) {
    extras.replaceChildren();
    extras.append(extrasRenderer());
  }
  await refreshWorkspaceCharts();
}

function usageSummaryFromMember(member, live) {
  const app = live?.app_usage || member?.app_usage || {};
  const today = member?.today || {};
  return {
    live_session_minutes: Number(app.app_minutes_session ?? 0),
    today_minutes: Number(app.app_minutes_today ?? 0),
    week_minutes: Number(app.app_minutes_week ?? 0),
    month_minutes: Number(app.app_minutes_month ?? 0),
    today_dials: Number(today.dials ?? 0),
  };
}

export async function openMemberWorkspace(userId, member, live, extrasRenderer) {
  bindWorkspaceChrome();
  settingsUserId = userId;
  lastMemberContext = { member, live };
  const panel = byId("teamMemberDetail");
  showRosterView(false);
  panel.hidden = false;
  renderUsageRow(usageSummaryFromMember(member, live));
  setText("teamMemberDetailTitle", member?.display_name || member?.email || "Member");
  const liveLine = byId("teamMemberLiveLine");
  if (liveLine) {
    const parts = [];
    if (live?.online) {
      parts.push("Live", live.stage || "idle");
      if (live.running) parts.push("dialing");
      if (live.in_flight_count) parts.push(`${live.in_flight_count} in flight`);
      if (live.active_lead_name) parts.push(live.active_lead_name);
    } else {
      parts.push("Offline");
    }
    liveLine.textContent = parts.join(" · ");
  }
  const extras = byId("teamMemberDetailExtras");
  if (extras && extrasRenderer) {
    extras.replaceChildren();
    const node = extrasRenderer();
    if (node) extras.append(node);
  }
  setWorkspaceTab("analytics");
  await refreshWorkspaceCharts();
}