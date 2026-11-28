export function renderBarChart(host, bars, labels) {
  if (!host) return;
  host.replaceChildren();
  const values = (bars || []).map((n) => Number(n) || 0);
  if (!values.length || values.every((v) => v === 0)) {
    const empty = document.createElement("p");
    empty.className = "team-chart-empty";
    empty.textContent = "No outbound activity in this range yet.";
    host.append(empty);
    return;
  }
  const wrap = document.createElement("div");
  wrap.className = "team-bar-chart";
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 420 120");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Bar chart");
  const width = 420;
  const height = 120;
  const pad = { left: 24, right: 16, top: 14, bottom: 34 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const baselineY = pad.top + innerH;
  const max = Math.max(1, ...values);
  const slot = innerW / Math.max(values.length, 1);
  const barW = Math.min(40, slot * 0.34);
  const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  axis.setAttribute("x1", String(pad.left));
  axis.setAttribute("y1", String(baselineY));
  axis.setAttribute("x2", String(pad.left + innerW));
  axis.setAttribute("y2", String(baselineY));
  axis.setAttribute("class", "team-chart-axis");
  svg.append(axis);
  values.forEach((v, index) => {
    const h = v > 0 ? Math.max(3, (v / max) * innerH) : 2;
    const x = pad.left + slot * index + (slot - barW) / 2;
    const y = baselineY - h;
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", String(x));
    rect.setAttribute("y", String(y));
    rect.setAttribute("width", String(barW));
    rect.setAttribute("height", String(h));
    rect.setAttribute("rx", "3");
    rect.setAttribute("class", `team-chart-bar-${index % 3}${v === 0 ? " is-zero" : ""}`);
    svg.append(rect);
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", String(x + barW / 2));
    label.setAttribute("y", String(height - 8));
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("class", "team-chart-label");
    label.textContent = labels[index] || "";
    svg.append(label);
    const val = document.createElementNS("http://www.w3.org/2000/svg", "text");
    val.setAttribute("x", String(x + barW / 2));
    val.setAttribute("y", String(v > 0 ? Math.max(pad.top + 10, y - 5) : baselineY - 6));
    val.setAttribute("text-anchor", "middle");
    val.setAttribute("class", "team-chart-value");
    val.textContent = String(v);
    svg.append(val);
  });
  wrap.append(svg);
  host.append(wrap);
}

export function renderDispositionChart(host, rows) {
  const labels = (rows || []).map((row) => row.label || row.key);
  const values = (rows || []).map((row) => row.count || 0);
  renderBarChart(host, values, labels);
}

export function renderLineChart(host, points) {
  if (!host) return;
  host.replaceChildren();
  const wrap = document.createElement("div");
  wrap.className = "team-line-chart";
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 420 120");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Activity line chart");
  const width = 420;
  const height = 120;
  const pad = { left: 24, right: 16, top: 12, bottom: 22 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const series = (points || []).map((row) => Number(row.value) || 0);
  const max = Math.max(1, ...series);
  const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  axis.setAttribute("x1", String(pad.left));
  axis.setAttribute("y1", String(pad.top + innerH));
  axis.setAttribute("x2", String(pad.left + innerW));
  axis.setAttribute("y2", String(pad.top + innerH));
  axis.setAttribute("class", "team-chart-axis");
  svg.append(axis);
  if (!series.length) {
    wrap.append(svg);
    host.append(wrap);
    return;
  }
  const step = innerW / Math.max(series.length - 1, 1);
  const coords = series.map((value, index) => {
    const x = pad.left + step * index;
    const y = pad.top + innerH - (value / max) * innerH;
    return [x, y];
  });
  const path = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
  path.setAttribute(
    "points",
    coords.map(([x, y]) => `${x},${y}`).join(" "),
  );
  path.setAttribute("class", "team-chart-line");
  svg.append(path);
  wrap.append(svg);
  host.append(wrap);
}