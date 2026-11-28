import { S, byId, registerRenderer, request, setText } from "../core.js";

const REFRESH_MS = 5000;
const DAYS = 7;
const SUBJECT_KEY = "prospect-desk-analytics-subject";
let timer = null;
let lastFetchAt = 0;
let inflight = null;

function subjectUserId() {
  if (S.analyticsSubjectUserId) return S.analyticsSubjectUserId;
  try {
    const saved = sessionStorage.getItem(SUBJECT_KEY);
    if (saved && S.canManageTeam) return saved;
  } catch {
    /* ignore */
  }
  return "";
}

export function setAnalyticsSubject(userId) {
  S.analyticsSubjectUserId = userId || "";
  try {
    if (userId) sessionStorage.setItem(SUBJECT_KEY, userId);
    else sessionStorage.removeItem(SUBJECT_KEY);
  } catch {
    /* ignore */
  }
}

function formatRate(value) {
  if (value == null || Number.isNaN(value)) return "—";
  return `${Math.round(value * 1000) / 10}%`;
}

function renderPayload(data) {
  const body = byId("analyticsTableBody");
  const empty = byId("analyticsEmpty");
  const table = byId("analyticsTable");
  const totalsEl = byId("analyticsTotals");
  if (!body) return;
  body.replaceChildren();
  const segments = data?.segments || [];
  const subject = data?.subject_label || (data?.user_id && S.canManageTeam ? data.user_id : "You");
  setText("analyticsSubjectLine", subject ? `Showing: ${subject} · last ${data?.days || DAYS} days` : `Last ${data?.days || DAYS} days`);
  setText("analyticsUpdated", data?.updated_at ? `Updated ${new Date(data.updated_at).toLocaleTimeString()}` : "");
  if (!segments.length) {
    empty.hidden = false;
    table.hidden = true;
    totalsEl.hidden = true;
    return;
  }
  empty.hidden = true;
  table.hidden = false;
  totalsEl.hidden = false;
  const totals = data.totals || {};
  totalsEl.textContent = `All scripts · ${totals.dials ?? 0} dials · ${totals.connected ?? 0} connects · ${totals.conversations ?? 0} conversations · ${totals.booked ?? 0} booked`;
  for (const row of segments) {
    const tr = document.createElement("tr");
    const counts = row.counts || {};
    const cells = [
      row.industry_label || row.industry,
      row.prospect_type_label || row.prospect_type,
      row.variation_label || row.variation,
      counts.dials ?? 0,
      counts.connected ?? 0,
      counts.conversations ?? 0,
      counts.booked ?? 0,
      formatRate(row.rates?.connect_rate),
    ];
    for (const text of cells) {
      const td = document.createElement("td");
      td.textContent = String(text);
      tr.append(td);
    }
    body.append(tr);
  }
}

async function fetchAnalytics() {
  const uid = subjectUserId();
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
  const path = uid
    ? `/api/team/members/${encodeURIComponent(uid)}/scripts/performance?days=${DAYS}&tz=${encodeURIComponent(tz)}`
    : `/api/scripts/performance?days=${DAYS}&tz=${encodeURIComponent(tz)}`;
  return request(path);
}

export async function refreshAnalytics(force = false) {
  const now = Date.now();
  if (!force && now - lastFetchAt < REFRESH_MS && inflight) return inflight;
  lastFetchAt = now;
  inflight = fetchAnalytics()
    .then((data) => {
      renderPayload(data);
      return data;
    })
  .catch(() => {
      setText("analyticsUpdated", "Could not load analytics.");
    })
    .finally(() => {
      inflight = null;
    });
  return inflight;
}

function stopTimer() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
}

function startTimer() {
  stopTimer();
  timer = setInterval(() => refreshAnalytics(false), REFRESH_MS);
}

export function renderAnalytics() {
  if (S.dashboardTab !== "analytics") {
    stopTimer();
    return;
  }
  refreshAnalytics(true);
  startTimer();
}

export function bindAnalytics() {
  registerRenderer(renderAnalytics, "end", "analytics");
}