import { byId, postJson, registerRenderer, request, setText, showToast, S, state } from "../core.js";

const REFRESH_MS = 8000;
let roster = null;
let selectedUserId = null;
let fetchAt = 0;

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

async function refreshRoster(force = false) {
  if (!teamReady()) return;
  const now = Date.now();
  if (!force && roster && now - fetchAt < REFRESH_MS) return;
  try {
    roster = await request("/api/team/roster");
    fetchAt = now;
    state.team_roster = roster;
    if (roster?.org_name) {
      setText("teamOrgSubtitle", `${roster.org_name} · roster and live activity`);
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
    const todayCell = document.createElement("td");
    const today = member.today || {};
    todayCell.textContent = `${today.dials ?? 0} dials · ${today.connected ?? 0} connects · ${today.booked ?? 0} booked`;
    row.append(nameCell, roleCell, statusCell, activityCell, todayCell);
    row.addEventListener("click", () => {
      if (!member.user_id) return;
      selectedUserId = member.user_id;
      loadMemberDetail(member.user_id, true);
    });
    body.append(row);
  }
}

async function loadMemberDetail(userId, showPanel) {
  const detail = byId("teamMemberDetail");
  const body = byId("teamMemberDetailBody");
  if (!userId) {
    detail.hidden = true;
    return;
  }
  try {
    const [metrics, live] = await Promise.all([
      request(`/api/team/members/${encodeURIComponent(userId)}/metrics?days=7`),
      request(`/api/team/members/${encodeURIComponent(userId)}/live`),
    ]);
    const member = (roster?.members || []).find((item) => item.user_id === userId);
    setText("teamMemberDetailTitle", member?.display_name || member?.email || "Member detail");
  body.replaceChildren();
    const liveLine = document.createElement("p");
    liveLine.textContent = live.online
      ? `Live · ${live.stage || "idle"}${live.active_lead_name ? ` · ${live.active_lead_name}` : ""}`
      : `Last seen · ${live.last_seen_at || "unknown"}`;
    const stats = document.createElement("p");
    const allTime = metrics.metrics?.all_time || {};
    stats.textContent = `7-day metrics · ${allTime.dials ?? 0} dials · ${allTime.connected ?? 0} connects · ${allTime.booked ?? 0} booked`;
    body.append(liveLine, stats);
    if (showPanel) detail.hidden = false;
  } catch (error) {
    showToast(error.message || "Could not load member detail.");
  }
}

export function renderTeam() {
  if (S.dashboardTab !== "team" || !teamReady()) return;
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