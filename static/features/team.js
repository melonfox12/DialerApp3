import { byId, postJson, registerRenderer, request, setText, showToast, S, state } from "../core.js";
import { setAnalyticsSubject } from "./analytics.js";
import {
  closeMemberWorkspace,
  openMemberWorkspace,
  refreshMemberWorkspace,
  setWorkspaceAfterClose,
  setWorkspaceCloseHandler,
} from "./_team/member-workspace.js";

const TEAM_MEMBER_KEY = "prospect-desk-team-member";

function rememberTeamMember(userId) {
  try {
    if (userId) localStorage.setItem(TEAM_MEMBER_KEY, userId);
    else localStorage.removeItem(TEAM_MEMBER_KEY);
  } catch {
    // ignore quota / private mode
  }
}

function savedTeamMember() {
  try {
    return localStorage.getItem(TEAM_MEMBER_KEY) || "";
  } catch {
    return "";
  }
}

export function dismissMemberWorkspace() {
  memberDetailEpoch += 1;
  rememberTeamMember(null);
  selectedUserId = null;
  stopLivePolling();
  closeMemberWorkspace();
  renderTeamTable();
  syncTeamPageHeading();
  requestAnimationFrame(() => syncTeamPageHeading());
}

export function clearTeamMemberSelection() {
  dismissMemberWorkspace();
}

export function syncTeamPageHeading() {
  const el = byId("pageTitle");
  if (!el) return;
  if (S.dashboardTab !== "team") return;
  const detailHidden = byId("teamMemberDetail")?.hidden !== false;
  el.replaceChildren();
  el.classList.add("page-title");
  if (detailHidden || !selectedUserId) {
    el.textContent = "Team";
    el.removeAttribute("aria-label");
    return;
  }
  const member = (roster?.members || []).find((item) => item.user_id === selectedUserId);
  const name =
    member?.display_name ||
    member?.email ||
    byId("teamMemberDetailTitle")?.textContent?.trim() ||
    "Member";
  const link = document.createElement("button");
  link.type = "button";
  link.className = "page-title-link";
  link.textContent = "Team";
  link.addEventListener("click", () => dismissMemberWorkspace());
  const sep = document.createElement("span");
  sep.className = "page-title-sep";
  sep.setAttribute("aria-hidden", "true");
  sep.textContent = " / ";
  const trail = document.createElement("span");
  trail.className = "page-title-trail";
  trail.textContent = `${name} info`;
  el.append(link, sep, trail);
  el.setAttribute("aria-label", `Team, ${name} info`);
}

const ROSTER_REFRESH_MS = 5000;
const LIVE_REFRESH_MS = 1500;
const USAGE_REFRESH_MS = 10_000;
let roster = null;
let selectedUserId = null;
let memberDetailEpoch = 0;
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
    const savedMember = !selectedUserId ? savedTeamMember() : "";
    if (!selectedUserId && savedMember) {
      const exists = (roster?.members || []).some((item) => item.user_id === savedMember);
      if (exists && savedTeamMember() === savedMember) {
        memberDetailEpoch += 1;
        const epoch = memberDetailEpoch;
        selectedUserId = savedMember;
        syncLivePolling();
        await loadMemberDetail(savedMember, true, epoch);
        if (selectedUserId === savedMember) syncTeamPageHeading();
        return;
      }
      rememberTeamMember(null);
    }
    if (selectedUserId && !byId("teamMemberDetail")?.hidden) {
      await loadMemberDetail(selectedUserId, false, memberDetailEpoch);
    }
    syncTeamPageHeading();
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
    if (member.user_id === selectedUserId) row.classList.add("is-selected");
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
    appCell.title = "App minutes today and this week (UTC); live session = continuous tab open (2 min gap starts a new session)";
    const todayCell = document.createElement("td");
    const today = member.today || {};
    todayCell.textContent = `${today.dials ?? 0} dials · ${today.connected ?? 0} connects · ${today.booked ?? 0} booked`;
    row.append(nameCell, roleCell, statusCell, activityCell, appCell, todayCell);
    row.addEventListener("click", () => {
      if (!member.user_id) return;
      memberDetailEpoch += 1;
      const epoch = memberDetailEpoch;
      selectedUserId = member.user_id;
      rememberTeamMember(member.user_id);
      syncLivePolling();
      loadMemberDetail(member.user_id, true, epoch);
    });
    body.append(row);
  }
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

async function optionalRequest(path) {
  try {
    return await request(path);
  } catch {
    return null;
  }
}

async function loadMemberDetail(userId, showPanel, epoch = memberDetailEpoch) {
  if (!userId) {
    closeMemberWorkspace();
    stopLivePolling();
    return;
  }
  const stale = () => epoch !== memberDetailEpoch || selectedUserId !== userId;
  const now = Date.now();
  const usageStale = now - liveFetchAt > USAGE_REFRESH_MS;
  const needsUsage = showPanel || usageStale;
  const needsScripts = showPanel || now - liveFetchAt > LIVE_REFRESH_MS * 2;
  try {
    liveFetchAt = now;
    const tz = encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone || "");
    const live = await request(`/api/team/members/${encodeURIComponent(userId)}/live`);
    const usage = needsUsage
      ? await optionalRequest(`/api/team/members/${encodeURIComponent(userId)}/usage?minutes=60`)
      : null;
    const scripts = needsScripts
      ? await optionalRequest(`/api/team/members/${encodeURIComponent(userId)}/scripts/performance?days=7&tz=${tz}`)
      : null;
    if (stale()) return;
    const member = (roster?.members || []).find((item) => item.user_id === userId);
    const extrasRenderer = () => {
      const wrap = document.createDocumentFragment();
      if (usage) wrap.append(renderUsageTimeline(usage.events, usage.minutes || 60));
      if (scripts) wrap.append(renderMemberScriptAnalytics(scripts));
      const updated = document.createElement("p");
      updated.className = "team-detail-updated";
      updated.textContent = `Updated ${new Date().toLocaleTimeString()}`;
      wrap.append(updated);
      const shell = document.createElement("div");
      shell.append(wrap);
      return shell;
    };
    if (showPanel) {
      if (stale()) return;
      rememberTeamMember(userId);
      await openMemberWorkspace(userId, member, live, extrasRenderer);
      if (stale()) {
        closeMemberWorkspace();
        syncTeamPageHeading();
        return;
      }
      syncTeamPageHeading();
    } else if (!byId("teamMemberDetail")?.hidden) {
      if (stale()) return;
      await refreshMemberWorkspace(userId, live, extrasRenderer, member);
    }
    if (!stale()) renderTeamTable();
  } catch (error) {
    showToast(error.message || "Could not load member detail.");
  }
}

export function renderTeam() {
  if (S.dashboardTab !== "team" || !teamReady()) {
    stopLivePolling();
    if (S.dashboardTab !== "team") {
      closeMemberWorkspace();
      selectedUserId = null;
    }
    return;
  }
  syncLivePolling();
  void refreshRoster(false);
}

export function bindTeam() {
  setWorkspaceCloseHandler(dismissMemberWorkspace);
  setWorkspaceAfterClose(syncTeamPageHeading);
  byId("teamMemberDetailClose")?.addEventListener("click", (event) => {
    event.preventDefault();
    dismissMemberWorkspace();
  });
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