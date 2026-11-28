import { byId, postJson, registerRenderer, request, setText, showToast, S, state } from "../core.js";
import { setAnalyticsSubject } from "./analytics.js";

const ROSTER_REFRESH_MS = 5000;
const LIVE_REFRESH_MS = 1500;
const USAGE_REFRESH_MS = 10_000;
let roster = null;
let selectedUserId = null;
let rosterFetchAt = 0;
let liveTimer = null;
let liveFetchAt = 0;

function teamReady() {
  return Boolean(S.canManageTeam);
}

export function syncTeamChrome() {
  const button = byId("teamTabButton");
  const panel = byId("teamPanel");
  if (!button || !panel) return;
  const show = teamReady();
  button.hidden = !show;
  if (!show && S.dashboardTab === "team") {
    import("../_core/navigation.js").then(({ setDashboardTab }) => setDashboardTab("dialer"));
  }
}

function formatScriptRate(value) {
  if (value == null || Number.isNaN(value)) return "—";
  return `${Math.round(value * 1000) / 10}%`;
}

function renderMemberScriptAnalytics(payload) {
  const section = document.createElement("section");
  section.className = "team-script-analytics";
  const heading = document.createElement("h4");
  heading.textContent = "Script analytics (7 days, live)";
  section.append(heading);
  const segments = payload?.segments || [];
  if (!segments.length) {
    const empty = document.createElement("p");
    empty.className = "form-footnote";
    empty.textContent = "No script-tagged dials yet for this member.";
    section.append(empty);
  } else {
    const table = document.createElement("table");
    table.className = "team-script-table";
    const head = document.createElement("thead");
    head.innerHTML = "<tr><th>Script</th><th>Dials</th><th>Connect %</th></tr>";
    table.append(head);
    const body = document.createElement("tbody");
    for (const row of segments.slice(0, 8)) {
      const tr = document.createElement("tr");
      const label = `${row.industry_label || row.industry} · ${row.prospect_type_label || row.prospect_type} · v${row.variation}`;
      const counts = row.counts || {};
      tr.innerHTML = `<td>${label}</td><td>${counts.dials ?? 0}</td><td>${formatScriptRate(row.rates?.connect_rate)}</td>`;
      body.append(tr);
    }
    table.append(body);
    section.append(table);
  }
  const actions = document.createElement("div");
  actions.className = "team-script-actions";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "button-link";
  btn.textContent = "Open full Analytics page for this member";
  btn.addEventListener("click", () => {
    setAnalyticsSubject(payload?.user_id || selectedUserId || "");
    import("../_core/navigation.js").then(({ setDashboardTab }) => setDashboardTab("analytics"));
  });
  actions.append(btn);
  section.append(actions);
  return section;
}

function formatAppMinutes(usage, online) {
  const today = Number(usage?.app_minutes_today ?? 0);
  const week = Number(usage?.app_minutes_week ?? 0);
  const session = Number(usage?.app_minutes_session ?? 0);
  if (online && session > 0) {
    return `${today}m today · ${week}m wk · ${session}m live`;
  }
  return `${today}m today · ${week}m wk`;
}

function renderAppUsageBlock(app, online) {
  const section = document.createElement("section");
  section.className = "team-app-usage";
  const heading = document.createElement("h4");
  heading.className = "team-section-label";
  heading.textContent = "Browser app time (UTC)";
  section.append(heading);
  const rows = [
    ["This browser session", app?.app_minutes_session, online],
    ["Today", app?.app_minutes_today, true],
    ["This week (ISO)", app?.app_minutes_week, true],
    ["This month", app?.app_minutes_month, true],
  ];
  const list = document.createElement("dl");
  list.className = "team-app-usage-list";
  for (const [label, minutes, show] of rows) {
    if (!show && !Number(minutes)) continue;
    const dt = document.createElement("dt");
    dt.textContent = label;
    const dd = document.createElement("dd");
    dd.textContent = `${Number(minutes ?? 0)} min`;
    list.append(dt, dd);
  }
  section.append(list);
  const note = document.createElement("p");
  note.className = "form-footnote";
  note.textContent = "Session resets when they leave the app (~90s without heartbeats). Today, week, and month keep adding.";
  section.append(note);
  return section;
}

function formatSeen(iso) {
  if (!iso) return "unknown";
  const seen = Date.parse(iso);
  if (!Number.isFinite(seen)) return iso;
  const delta = Math.max(0, Date.now() - seen);
  if (delta < 60_000) return `${Math.floor(delta / 1000)}s ago`;
  if (delta < 3_600_000) return `${Math.floor(delta / 60_000)}m ago`;
  return new Date(seen).toLocaleString();
}

function stopLivePolling() {
  if (liveTimer) {
    clearInterval(liveTimer);
    liveTimer = null;
  }
}

function syncLivePolling() {
  stopLivePolling();
  if (S.dashboardTab !== "team" || !teamReady() || !selectedUserId) return;
  liveTimer = setInterval(() => {
    if (S.dashboardTab !== "team" || !selectedUserId) {
      stopLivePolling();
      return;
    }
    loadMemberDetail(selectedUserId, false);
  }, LIVE_REFRESH_MS);
}

async function refreshRoster(force = false) {
  if (!teamReady()) return;
  const now = Date.now();
  if (!force && roster && now - rosterFetchAt < ROSTER_REFRESH_MS) return;
  try {
    roster = await request("/api/team/roster");
    rosterFetchAt = now;
    state.team_roster = roster;
    if (roster?.org_name) {
      setText("teamOrgSubtitle", `${roster.org_name} · roster and live activity · updates every ${ROSTER_REFRESH_MS / 1000}s`);
    }
    renderTeamTable();
    if (selectedUserId) {
      loadMemberDetail(selectedUserId, false);
    }
  } catch (error) {
    showToast(error.message || "Could not load team roster.");
  }
}

function renderTeamTable() {
  const body = byId("teamTableBody");
  const empty = byId("teamEmpty");
  const members = roster?.members || [];
  body.replaceChildren();
  if (!members.length) {
    empty.hidden = false;
    return;
  }
  empty.hidden = true;
  for (const member of members) {
    const row = document.createElement("tr");
    row.dataset.userId = member.user_id || "";
    const nameCell = document.createElement("td");
    const strong = document.createElement("strong");
    strong.textContent = member.display_name || member.email || "—";
    nameCell.append(strong);
    if (member.email) {
      const span = document.createElement("span");
      span.className = "team-email";
      span.textContent = member.email;
      nameCell.append(document.createElement("br"), span);
    }
    const roleCell = document.createElement("td");
    roleCell.textContent = member.role || "";
    const statusCell = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = `team-status team-status--${member.online ? "online" : "offline"}`;
    badge.textContent = member.online ? "Online" : "Offline";
    statusCell.append(badge);
    if (member.status === "invited") {
      const invite = document.createElement("span");
      invite.className = "team-invited";
      invite.textContent = "Invited";
      statusCell.append(document.createTextNode(" "), invite);
    }
    const activityCell = document.createElement("td");
    const stage = member.presence?.stage || "idle";
    activityCell.textContent = member.online ? stage : (stage === "idle" ? "—" : stage);
    const appCell = document.createElement("td");
    appCell.textContent = formatAppMinutes(member.app_usage, member.online);
    appCell.title = "App minutes today and this week (UTC); live session when online";
    const todayCell = document.createElement("td");
    const today = member.today || {};
    todayCell.textContent = `${today.dials ?? 0} dials · ${today.connected ?? 0} connects · ${today.booked ?? 0} booked`;
    row.append(nameCell, roleCell, statusCell, activityCell, appCell, todayCell);
    row.addEventListener("click", () => {
      if (!member.user_id) return;
      selectedUserId = member.user_id;
      syncLivePolling();
      loadMemberDetail(member.user_id, true);
    });
    body.append(row);
  }
}

function sumMetricSeries(series, key) {
  return (series || []).reduce((total, day) => total + Number(day[key] || 0), 0);
}

const USAGE_KIND_LABELS = {
  session_start: "Session started",
  session_stop: "Session stopped",
  session_pause: "Paused",
  session_resume: "Resumed",
  stage_change: "Stage",
  connect: "Connected",
  disposition: "Disposition",
  tab_focus: "Tab",
};

function usageEventDetail(event) {
  const payload = event?.payload || {};
  if (event.kind === "stage_change") return payload.stage || "";
  if (event.kind === "tab_focus") return payload.tab || "";
  if (event.kind === "disposition") return payload.status || "";
  if (event.kind === "connect") return payload.lead_id ? "live call" : "";
  if (event.kind === "session_start" && payload.queue_total != null) {
    return `${payload.queue_total} in queue`;
  }
  return "";
}

function renderUsageTimeline(events, minutes) {
  const section = document.createElement("section");
  section.className = "team-usage-timeline";
  const heading = document.createElement("h4");
  heading.className = "team-section-label";
  heading.textContent = `Activity · last ${minutes} min`;
  section.append(heading);
  const list = document.createElement("ol");
  list.className = "team-usage-list";
  const items = [...(events || [])].reverse();
  if (!items.length) {
    const empty = document.createElement("li");
    empty.textContent = "No recorded events yet (run Supabase migration for usage_events).";
    list.append(empty);
  } else {
    for (const event of items) {
      const row = document.createElement("li");
      const stamp = document.createElement("time");
      const at = Date.parse(event.at);
      stamp.dateTime = event.at || "";
      stamp.textContent = Number.isFinite(at)
        ? new Date(at).toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit" })
        : event.at || "—";
      const label = USAGE_KIND_LABELS[event.kind] || event.kind || "Event";
      const detail = usageEventDetail(event);
      row.append(stamp, document.createTextNode(` ${label}${detail ? ` · ${detail}` : ""}`));
      list.append(row);
    }
  }
  section.append(list);
  return section;
}

async function loadMemberDetail(userId, showPanel) {
  const detail = byId("teamMemberDetail");
  const body = byId("teamMemberDetailBody");
  if (!userId) {
    detail.hidden = true;
    stopLivePolling();
    return;
  }
  const now = Date.now();
  const metricsStale = now - liveFetchAt > LIVE_REFRESH_MS * 2;
  const usageStale = now - liveFetchAt > USAGE_REFRESH_MS;
  try {
    const needsMetrics = showPanel || metricsStale || !body.childElementCount;
    const needsUsage = showPanel || usageStale || !body.childElementCount;
    const needsScripts = showPanel || metricsStale || !body.childElementCount;
    const tz = encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone || "");
    const requests = [
      request(`/api/team/members/${encodeURIComponent(userId)}/live`),
    ];
    if (needsMetrics) {
      requests.push(request(`/api/team/members/${encodeURIComponent(userId)}/metrics?days=7`));
    }
    if (needsUsage) {
      requests.push(request(`/api/team/members/${encodeURIComponent(userId)}/usage?minutes=60`));
    }
    if (needsScripts) {
      requests.push(request(`/api/team/members/${encodeURIComponent(userId)}/scripts/performance?days=7&tz=${tz}`));
    }
    liveFetchAt = now;
    const results = await Promise.all(requests);
    const live = results[0];
    let metrics = null;
    let usage = null;
    let scripts = null;
    let idx = 1;
    if (needsMetrics) metrics = results[idx++];
    if (needsUsage) usage = results[idx++];
    if (needsScripts) scripts = results[idx];
    const member = (roster?.members || []).find((item) => item.user_id === userId);
    setText("teamMemberDetailTitle", member?.display_name || member?.email || "Member detail");
    body.replaceChildren();
    const liveLine = document.createElement("p");
    liveLine.className = "team-detail-live";
    const parts = [];
    if (live.online) {
      parts.push(`Live (${live.source || "session"})`, live.stage || "idle");
      if (live.running) parts.push("dialing");
      if (live.paused) parts.push("paused");
      if (live.in_flight_count) parts.push(`${live.in_flight_count} in flight`);
      if (live.active_lead_name) parts.push(live.active_lead_name);
    } else {
      parts.push("Offline", live.stage && live.stage !== "idle" ? `last stage ${live.stage}` : null);
      parts.push(`last seen ${formatSeen(live.last_seen_at)}`);
    }
    liveLine.textContent = parts.filter(Boolean).join(" · ");
    body.append(liveLine);
    const app = live.app_usage || member?.app_usage;
    if (app) {
      body.append(renderAppUsageBlock(app, live.online));
    }
    const session = live.session_stats || {};
    if (live.online && (session.dials || session.conversations)) {
      const sessionLine = document.createElement("p");
      sessionLine.textContent = `This session · ${session.dials ?? 0} dials · ${session.conversations ?? 0} conversations`;
      body.append(sessionLine);
    }
    if (metrics) {
      const series = metrics.metrics?.series || [];
      const totals = {
        dials: sumMetricSeries(series, "dials"),
        connected: sumMetricSeries(series, "connected"),
        booked: sumMetricSeries(series, "booked"),
        talk_seconds: sumMetricSeries(series, "talk_seconds"),
      };
      const stats = document.createElement("p");
      const talkMin = Math.round((totals.talk_seconds || 0) / 60);
      stats.textContent = `Last 7 days · ${totals.dials} dials · ${totals.connected} connects · ${totals.booked} booked · ${talkMin} talk min`;
      body.append(stats);
    }
    if (usage) {
      body.append(renderUsageTimeline(usage.events, usage.minutes || 60));
    }
    if (scripts) {
      body.append(renderMemberScriptAnalytics(scripts));
    }
    const updated = document.createElement("p");
    updated.className = "team-detail-updated";
    updated.textContent = `Updated ${new Date().toLocaleTimeString()}`;
    body.append(updated);
    if (showPanel) detail.hidden = false;
  } catch (error) {
    showToast(error.message || "Could not load member detail.");
  }
}

export function renderTeam() {
  if (S.dashboardTab !== "team" || !teamReady()) {
    stopLivePolling();
    return;
  }
  syncLivePolling();
  refreshRoster(false);
}

export function bindTeam() {
  const form = byId("teamInviteForm");
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!teamReady()) return;
    const email = byId("teamInviteEmail")?.value?.trim();
    if (!email) return;
    try {
      await postJson("/api/team/invites", { email, role: "rep" });
      byId("teamInviteEmail").value = "";
      showToast("Invite recorded. They join when they sign in with that Google account.");
      await refreshRoster(true);
    } catch (error) {
      showToast(error.message || "Could not send invite.");
    }
  });
  registerRenderer(renderTeam, "end", "team");
}