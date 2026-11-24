#!/usr/bin/env python3
"""Build docs/codemap graph, per-file pseudocode, and bundle JSON. Does not read .env values."""

from __future__ import annotations

import ast
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "codemap"
FILES_MD = OUT / "files"

IGNORED_DIR_NAMES = {
    "tests",
    ".pytest_cache",
    "crm_data",
    "linear-design-system",
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv",
}

IGNORED_FILE_MARKERS = ["__init__.py"]

PY_ROOT_FILES = ("server.py", "web.py", "dialer.py")
PY_PACKAGES = ("_web", "shared", "features", "scripts")
JS_ROOT = ROOT / "static"

HTTP_PATH_RE = re.compile(
    r"""(?:request|postJson|fetch)\s*\(\s*['"`]([^'"`]+)['"`]""",
    re.MULTILINE,
)
IMPORT_EXPORT_RE = re.compile(
    r"^\s*(?:import\s+.+?\s+from\s+['\"]([^'\"]+)['\"]|export\s+(?:async\s+)?function\s+(\w+)|export\s*\{([^}]+)\})",
    re.MULTILINE,
)
EVENT_RE = re.compile(
    r"""addEventListener\s*\(\s*['"](\w+)['"]\s*,\s*(\w+)""",
)
BYID_EVENT_RE = re.compile(
    r"""byId\s*\(\s*['"]([^'"]+)['"]\s*\)\s*\.addEventListener\s*\(\s*['"](\w+)['"]""",
)
DIALER_EL_EVENT_RE = re.compile(
    r"""dialerEl\s*\(\s*['"]([^'"]+)['"]\s*\)\??\.addEventListener\s*\(\s*['"](\w+)['"]""",
)
ROUTE_TUPLE_RE = re.compile(
    r'\(\s*["\'](GET|POST|PUT|DELETE|PATCH)["\']\s*,\s*["\']([^"\']+)["\']\s*,\s*(\w+)',
)


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def file_layer(rel: str) -> str:
    if rel.startswith("static/"):
        return "browser"
    if rel in ("server.py", "dialer.py"):
        return "entry"
    if rel == "web.py" or rel.startswith("_web/"):
        return "http"
    if rel.startswith("features/"):
        return "features"
    if rel.startswith("shared/"):
        return "shared"
    if rel.startswith("scripts/"):
        return "scripts"
    return "other"


def collect_python_files() -> list[Path]:
    found: list[Path] = []
    for name in PY_ROOT_FILES:
        path = ROOT / name
        if path.is_file():
            found.append(path)
    for pkg in PY_PACKAGES:
        base = ROOT / pkg
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            if any(part in IGNORED_DIR_NAMES for part in path.parts):
                continue
            if path.name in IGNORED_FILE_MARKERS:
                continue
            found.append(path)
    return found


def collect_js_files() -> list[Path]:
    if not JS_ROOT.is_dir():
        return []
    files: list[Path] = []
    for path in sorted(JS_ROOT.rglob("*.js")):
        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return files


def module_name_for_path(path: Path) -> str:
    rel = path.relative_to(ROOT)
    parts = list(rel.parts)
    if parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def path_for_module(mod: str) -> str | None:
    mod = mod.strip()
    if not mod:
        return None
    candidate = ROOT / Path(mod.replace(".", "/"))
    py = candidate.with_suffix(".py")
    if py.is_file():
        return rel_posix(py)
    init_py = candidate / "__init__.py"
    if init_py.is_file():
        return rel_posix(init_py)
    return None


@dataclass
class FunctionInfo:
    qualified: str
    name: str
    line: int
    end_line: int
    doc: str
    kind: str  # function | method
    class_name: str | None = None
    pseudocode: list[str] = field(default_factory=list)
    call_order: list[str] = field(default_factory=list)


@dataclass
class FileRecord:
    rel: str
    layer: str
    language: str
    imports: list[dict] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    functions: dict[str, FunctionInfo] = field(default_factory=dict)
    routes: list[dict] = field(default_factory=list)
    http_calls: list[dict] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)
    purpose: str = ""


def stmt_pseudo(node: ast.AST, depth: int = 0) -> list[str]:
    pad = "  " * depth
    lines: list[str] = []
    if isinstance(node, ast.Return):
        val = describe_expr(node.value) if node.value else "nothing"
        lines.append(f"{pad}Return {val}.")
    elif isinstance(node, ast.Raise):
        lines.append(f"{pad}Raise an error.")
    elif isinstance(node, ast.Assign):
        targets = ", ".join(describe_expr(t) for t in node.targets)
        lines.append(f"{pad}Set {targets} to {describe_expr(node.value)}.")
    elif isinstance(node, ast.AnnAssign) and node.value:
        lines.append(f"{pad}Set {describe_expr(node.target)} to {describe_expr(node.value)}.")
    elif isinstance(node, ast.AugAssign):
        lines.append(f"{pad}Update {describe_expr(node.target)} with {describe_expr(node.op)} {describe_expr(node.value)}.")
    elif isinstance(node, ast.If):
        lines.append(f"{pad}If {describe_expr(node.test)}:")
        for child in node.body[:6]:
            lines.extend(stmt_pseudo(child, depth + 1))
        if node.orelse:
            lines.append(f"{pad}Else:")
            for child in node.orelse[:4]:
                lines.extend(stmt_pseudo(child, depth + 1))
    elif isinstance(node, ast.For):
        lines.append(f"{pad}For each {describe_expr(node.target)} in {describe_expr(node.iter)}:")
        for child in node.body[:5]:
            lines.extend(stmt_pseudo(child, depth + 1))
    elif isinstance(node, ast.While):
        lines.append(f"{pad}While {describe_expr(node.test)}:")
        for child in node.body[:5]:
            lines.extend(stmt_pseudo(child, depth + 1))
    elif isinstance(node, ast.With):
        items = ", ".join(describe_expr(it.context_expr) for it in node.items)
        lines.append(f"{pad}With {items}:")
        for child in node.body[:5]:
            lines.extend(stmt_pseudo(child, depth + 1))
    elif isinstance(node, ast.Try):
        lines.append(f"{pad}Try:")
        for child in node.body[:5]:
            lines.extend(stmt_pseudo(child, depth + 1))
        for handler in node.handlers[:2]:
            lines.append(f"{pad}On {handler.type or 'exception'}:")
            for child in handler.body[:3]:
                lines.extend(stmt_pseudo(child, depth + 1))
    elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        lines.append(f"{pad}Call {describe_call(node.value)}.")
    elif isinstance(node, ast.Pass):
        lines.append(f"{pad}No-op.")
    return lines


def describe_expr(node: ast.AST | None) -> str:
    if node is None:
        return "..."
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str) and len(node.value) > 48:
            return repr(node.value[:45] + "...")
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{describe_expr(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return describe_call(node)
    if isinstance(node, ast.Subscript):
        return f"{describe_expr(node.value)}[...]"
    if isinstance(node, ast.List):
        return "a list"
    if isinstance(node, ast.Dict):
        return "a dict"
    if isinstance(node, ast.Compare):
        return f"{describe_expr(node.left)} compared to ..."
    if isinstance(node, ast.BoolOp):
        return "a boolean condition"
    if isinstance(node, ast.UnaryOp):
        return describe_expr(node.operand)
    if isinstance(node, ast.BinOp):
        return f"{describe_expr(node.left)} op {describe_expr(node.right)}"
    return type(node).__name__


def describe_call(node: ast.Call) -> str:
    func = describe_expr(node.func)
    return f"{func}(...)"


def collect_calls_in_body(body: list[ast.stmt], imports: dict[str, str], module: str, current_class: str | None) -> list[tuple[int, str]]:
    ordered: list[tuple[int, str]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            name = resolve_call_target(node.func, imports, module, current_class)
            if name:
                ordered.append((node.lineno, name))
            self.generic_visit(node)

    for stmt in body:
        Visitor().visit(stmt)
    return ordered


def resolve_call_target(func: ast.AST, imports: dict[str, str], module: str, class_name: str | None) -> str | None:
    if isinstance(func, ast.Name):
        local = func.id
        if local in imports:
            return imports[local]
        return f"{module}.{local}"
    if isinstance(func, ast.Attribute):
        chain = attr_chain(func)
        if not chain:
            return None
        head, rest = chain[0], chain[1:]
        if head == "self" and class_name and rest:
            return f"{module}.{class_name}.{rest[0]}" + (f".{'.'.join(rest[1:])}" if len(rest) > 1 else "")
        if head in imports:
            base = imports[head]
            return base + "." + ".".join(rest) if rest else base
        return ".".join(chain)
    return None


def attr_chain(node: ast.AST) -> list[str]:
    parts: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def parse_imports(tree: ast.Module) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                mapping[name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                mapping[name] = f"{mod}.{alias.name}" if mod else alias.name
    return mapping


def function_doc(node: ast.AST) -> str:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        doc = ast.get_docstring(node) or ""
        return doc.strip().split("\n")[0] if doc else ""
    return ""


def extract_routes_from_source(source: str, rel: str) -> list[dict]:
    routes: list[dict] = []
    for match in ROUTE_TUPLE_RE.finditer(source):
        method, path, handler = match.groups()
        routes.append(
            {
                "method": method,
                "path": path,
                "handler_name": handler,
                "file": rel,
            }
        )
    return routes


def parse_python(path: Path) -> FileRecord | None:
    rel = rel_posix(path)
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        tree = ast.parse(source, filename=rel)
    except SyntaxError:
        return None
    module = module_name_for_path(path)
    imports_map = parse_imports(tree)
    rec = FileRecord(rel=rel, layer=file_layer(rel), language="python")
    rec.purpose = (ast.get_docstring(tree) or "").strip().split("\n")[0] if ast.get_docstring(tree) else ""
    for alias, target in imports_map.items():
        to_path = path_for_module(target.split(".")[0]) or path_for_module(target.rsplit(".", 1)[0] if "." in target else target)
        rec.imports.append({"alias": alias, "module": target, "to_file": to_path})
    rec.routes = extract_routes_from_source(source, rel)

    class_stack: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_stack.append(node.name)
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if item.name.startswith("_") and item.name not in ("__init__",):
                        continue
                    qual = f"{module}.{node.name}.{item.name}"
                    calls = collect_calls_in_body(item.body, imports_map, module, node.name)
                    pseudo: list[str] = []
                    for stmt in item.body:
                        pseudo.extend(stmt_pseudo(stmt))
                        if len(pseudo) >= 8:
                            break
                    if not pseudo:
                        pseudo = ["Run method logic for this class."]
                    rec.functions[qual] = FunctionInfo(
                        qualified=qual,
                        name=item.name,
                        line=item.lineno,
                        end_line=getattr(item, "end_lineno", item.lineno),
                        doc=function_doc(item),
                        kind="method",
                        class_name=node.name,
                        pseudocode=pseudo[:8],
                        call_order=[c[1] for c in calls],
                    )
            class_stack.pop()
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            qual = f"{module}.{node.name}"
            calls = collect_calls_in_body(node.body, imports_map, module, None)
            pseudo = []
            for stmt in node.body:
                pseudo.extend(stmt_pseudo(stmt))
                if len(pseudo) >= 8:
                    break
            if not pseudo:
                pseudo = ["Execute top-level function logic."]
            rec.functions[qual] = FunctionInfo(
                qualified=qual,
                name=node.name,
                line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                doc=function_doc(node),
                kind="function",
                pseudocode=pseudo[:8],
                call_order=[c[1] for c in calls],
            )
    return rec


def parse_js(path: Path) -> FileRecord:
    rel = rel_posix(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        text = ""
    rec = FileRecord(rel=rel, layer=file_layer(rel), language="javascript")
    m = re.search(r"/\*\*([^*]|\*(?!/))*\*/", text)
    if m:
        doc = re.sub(r"^\s*\*\s?", "", m.group(0), flags=re.MULTILINE).strip()
        rec.purpose = doc.split("\n")[0][:200]
    for im in re.finditer(r"from\s+['\"]([^'\"]+)['\"]", text):
        target = im.group(1)
        resolved = resolve_js_import(rel, target)
        rec.imports.append({"module": target, "to_file": resolved})
    for em in re.finditer(r"export\s+(?:async\s+)?function\s+(\w+)", text):
        rec.exports.append(em.group(1))
    for em in re.finditer(r"export\s+function\s+(\w+)", text):
        if em.group(1) not in rec.exports:
            rec.exports.append(em.group(1))
    for idx, match in enumerate(HTTP_PATH_RE.finditer(text)):
        p = match.group(1)
        if p.startswith("/"):
            rec.http_calls.append({"path": p, "line": text[: match.start()].count("\n") + 1, "order": idx})
    for match in EVENT_RE.finditer(text):
        rec.events.append({"event": match.group(1), "handler": match.group(2), "line": text[: match.start()].count("\n") + 1})
    for match in BYID_EVENT_RE.finditer(text):
        rec.events.append({"element_id": match.group(1), "event": match.group(2), "line": text[: match.start()].count("\n") + 1})
    for match in DIALER_EL_EVENT_RE.finditer(text):
        rec.events.append({"element_id": match.group(1), "event": match.group(2), "line": text[: match.start()].count("\n") + 1})
    export_fn_pattern = re.compile(r"export\s+function\s+(\w+)")
    for match in export_fn_pattern.finditer(text):
        fn = match.group(1)
        if fn.startswith("bind"):
            rec.purpose = rec.purpose or f"Wire UI events and API calls ({fn})."
    return rec


def resolve_js_import(from_rel: str, spec: str) -> str | None:
    base = (ROOT / Path(from_rel)).parent
    if spec.startswith("."):
        target = (base / spec).resolve()
        for ext in (".js", ""):
            p = Path(str(target) + ext) if ext else target
            if p.suffix != ".js":
                p = p.with_suffix(".js")
            if p.is_file() and ROOT in p.parents or p == ROOT:
                try:
                    return rel_posix(p)
                except ValueError:
                    pass
    return None


def fn_node_id(qual: str, file_rel: str) -> str:
    short = qual.split(".")[-1]
    return f"fn:{file_rel}:{short}"


def build() -> dict:
    py_files = collect_python_files()
    js_files = collect_js_files()
    records: dict[str, FileRecord] = {}
    for path in py_files:
        rec = parse_python(path)
        if rec:
            records[rec.rel] = rec
    for path in js_files:
        records[rel_posix(path)] = parse_js(path)

    nodes: list[dict] = []
    edges: list[dict] = []
    unresolved: list[dict] = []
    route_index: dict[str, dict] = {}

    for rel, rec in records.items():
        nodes.append({"id": f"file:{rel}", "type": "file", "layer": rec.layer, "language": rec.language})
        for qual, fn in rec.functions.items():
            nid = fn_node_id(qual, rel)
            nodes.append(
                {
                    "id": nid,
                    "type": "function",
                    "layer": rec.layer,
                    "file": rel,
                    "name": fn.name,
                    "line": fn.line,
                    "doc": fn.doc,
                    "kind": fn.kind,
                }
            )
            edges.append({"from": f"file:{rel}", "to": nid, "type": "contains", "line": fn.line})
        imp_order = 0
        for imp in rec.imports:
            to_file = imp.get("to_file")
            if to_file and to_file in records:
                imp_order += 1
                edges.append(
                    {
                        "from": f"file:{rel}",
                        "to": f"file:{to_file}",
                        "type": "import",
                        "line": 0,
                        "order": imp_order,
                        "detail": imp.get("module", ""),
                    }
                )
            elif imp.get("module", "").startswith(("twilio", "http", "urllib", "json", "threading")):
                edges.append(
                    {
                        "from": f"file:{rel}",
                        "to": "external:stdlib",
                        "type": "import",
                        "line": 0,
                        "detail": imp.get("module"),
                    }
                )
            elif "supabase" in str(imp.get("module", "")).lower() or "Supabase" in str(imp.get("to_file", "")):
                edges.append({"from": f"file:{rel}", "to": "external:supabase", "type": "import", "line": 0})

        call_order = 0
        for qual, fn in rec.functions.items():
            from_id = fn_node_id(qual, rel)
            for callee in fn.call_order:
                target_file = None
                target_fn = None
                if "." in callee:
                    parts = callee.split(".")
                    target_fn = parts[-1]
                    mod = ".".join(parts[:-1])
                    target_file = path_for_module(mod)
                    if not target_file and len(parts) >= 2:
                        target_file = path_for_module(".".join(parts[:-2]))
                if target_file and target_file in records:
                    to_id = f"fn:{target_file}:{target_fn}"
                    call_order += 1
                    edges.append(
                        {
                            "from": from_id,
                            "to": to_id,
                            "type": "call",
                            "line": fn.line,
                            "order": call_order,
                        }
                    )
                else:
                    unresolved.append({"from": from_id, "call": callee, "line": fn.line})

        if rec.language == "javascript":
            for http in rec.http_calls:
                path_key = f"{http['path']}"
                edges.append(
                    {
                        "from": f"file:{rel}",
                        "to": f"http:{path_key}",
                        "type": "http",
                        "line": http["line"],
                        "order": http.get("order", 0),
                    }
                )
            for ev in rec.events:
                edges.append(
                    {
                        "from": f"file:{rel}",
                        "to": f"dom:{ev.get('element_id') or ev.get('handler', '?')}",
                        "type": "event",
                        "line": ev["line"],
                        "detail": ev.get("event"),
                    }
                )

        for route in rec.routes:
            handler = route["handler_name"]
            handler_id = f"fn:{rel}:{handler}"
            key = f"{route['method']} {route['path']}"
            route_index[key] = {
                **route,
                "handler_id": handler_id,
            }
            edges.append(
                {
                    "from": f"http:{route['path']}",
                    "to": handler_id,
                    "type": "route",
                    "line": 0,
                    "detail": route["method"],
                }
            )
            nodes.append(
                {
                    "id": f"http:{route['path']}",
                    "type": "http",
                    "layer": "http",
                    "method": route["method"],
                    "path": route["path"],
                }
            )

    for rel, rec in records.items():
        if rec.language != "javascript":
            continue
        for http in rec.http_calls:
            p = http["path"]
            for key, route in route_index.items():
                if route["path"] == p or (_pattern_match(route["path"], p)):
                    route.setdefault("js_files", []).append(rel)
                    for ev in rec.events:
                        route.setdefault("events", []).append({"file": rel, **ev})

    nodes.append({"id": "external:supabase", "type": "external", "layer": "external"})
    nodes.append({"id": "external:twilio", "type": "external", "layer": "external"})
    nodes.append({"id": "external:stdlib", "type": "external", "layer": "external"})

    seen_ids = {n["id"] for n in nodes}
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "python_files": len(py_files),
            "javascript_files": len(js_files),
            "nodes": len(seen_ids),
            "edges": len(edges),
            "routes": len(route_index),
            "unresolved_calls": len(unresolved),
        },
        "ignored": {
            "dirs": sorted(IGNORED_DIR_NAMES),
            "file_markers": list(IGNORED_FILE_MARKERS),
            "skipped_init_files": "Listed as markers; not analyzed as code units.",
        },
        "nodes": nodes,
        "edges": edges,
        "routes": list(route_index.values()),
        "unresolved": unresolved[:500],
        "files": {
            rel: {
                "layer": rec.layer,
                "language": rec.language,
                "purpose": rec.purpose,
                "functions": {
                    k: {
                        "name": v.name,
                        "line": v.line,
                        "doc": v.doc,
                        "pseudocode": v.pseudocode,
                        "calls": v.call_order,
                    }
                    for k, v in rec.functions.items()
                },
                "imports": rec.imports,
                "exports": rec.exports,
                "http_calls": rec.http_calls,
                "events": rec.events,
                "routes": rec.routes,
            }
            for rel, rec in records.items()
        },
    }


def _pattern_match(pattern: str, path: str) -> bool:
    if "{" in pattern:
        pp = pattern.split("/")
        cp = path.split("/")
        if len(pp) != len(cp):
            return False
        return all(
            a == b or (a.startswith("{") and a.endswith("}"))
            for a, b in zip(pp, cp)
        )
    return pattern == path


def write_file_markdown(graph: dict) -> None:
    FILES_MD.mkdir(parents=True, exist_ok=True)
    called_by: dict[str, list[str]] = defaultdict(list)
    for edge in graph["edges"]:
        if edge["type"] == "call":
            called_by[edge["to"]].append(edge["from"])
    for rel, data in sorted(graph["files"].items()):
        out_path = FILES_MD / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path = out_path.with_suffix(out_path.suffix + ".md")
        lines = [f"# `{rel}`", "", f"**Purpose:** {data.get('purpose') or '(no module docstring)'}", ""]
        if data.get("routes"):
            lines.append("## Routes")
            for r in data["routes"]:
                lines.append(f"- `{r['method']}` `{r['path']}` → `{r['handler_name']}`")
            lines.append("")
        if data.get("http_calls"):
            lines.append("## HTTP calls (browser)")
            for h in data["http_calls"]:
                lines.append(f"- `{h['path']}` (line {h['line']})")
            lines.append("")
        if data.get("events"):
            lines.append("## DOM events")
            for e in data["events"][:40]:
                el = e.get("element_id") or e.get("handler") or "?"
                lines.append(f"- `#${el}` / handler `{el}` — `{e.get('event')}` (line {e['line']})")
            lines.append("")
        lines.append("## Functions")
        for qual, fn in sorted(data.get("functions", {}).items(), key=lambda x: x[1]["line"]):
            fid = f"fn:{rel}:{fn['name']}"
            lines.append(f"### `{fn['name']}` (line {fn['line']})")
            if fn.get("doc"):
                lines.append(f"_{fn['doc']}_")
            lines.append("")
            lines.append("**Pseudocode:**")
            for row in fn.get("pseudocode") or ["(no body parsed)"]:
                lines.append(f"- {row}")
            lines.append("")
            calls = fn.get("calls") or []
            if calls:
                lines.append("**Calls →**")
                for i, c in enumerate(calls[:30], 1):
                    lines.append(f"{i}. `{c}`")
                lines.append("")
            callers = called_by.get(fid, [])
            if callers:
                lines.append("**Called by ←**")
                for c in sorted(set(callers)):
                    lines.append(f"- `{c}`")
                lines.append("")
        out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    graph = build()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    pseudocode = {rel: graph["files"][rel] for rel in graph["files"]}
    (OUT / "pseudocode.json").write_text(json.dumps(pseudocode, indent=2), encoding="utf-8")
    write_file_markdown(graph)
    meta = graph["meta"]
    print(f"Python files: {meta['python_files']}")
    print(f"JavaScript files: {meta['javascript_files']}")
    print(f"Nodes: {meta['nodes']}, Edges: {meta['edges']}, Routes: {meta['routes']}")
    print(f"Unresolved calls (capped in JSON): {meta['unresolved_calls']}")
    print(f"Wrote {OUT / 'graph.json'}")
    print(f"Wrote per-file markdown under {FILES_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())