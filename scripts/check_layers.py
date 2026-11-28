#!/usr/bin/env python3
"""Smoke check for AGENTS.md dependency direction: web -> dialer -> domain -> storage -> shared."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Higher number = higher layer; may import same or lower only.
LAYER_SHARED = 0
LAYER_STORAGE = 1
LAYER_DOMAIN = 2
LAYER_DIALER = 3
LAYER_WEB = 4

LAYER_NAMES = {
    LAYER_SHARED: "shared",
    LAYER_STORAGE: "storage",
    LAYER_DOMAIN: "domain",
    LAYER_DIALER: "dialer",
    LAYER_WEB: "web",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "test-results",
    "playwright-report",
    "Claude outputs",
}

# Known edges to fix later (documented in docs/research/architecture-layers-gap.md).
ALLOWED_VIOLATIONS: set[tuple[str, str]] = {
    ("shared/dial_policy.py", "features._prospects.dial_records"),
}


def layer_for_path(path: Path) -> int | None:
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    if rel.startswith("tests/") or rel.startswith("e2e/"):
        return None
    if rel.startswith("scripts/") and rel != "scripts/check_layers.py":
        return None
    if rel.startswith("shared/"):
        return LAYER_SHARED
    if rel in ("server.py", "dialer.py", "web.py") or rel.startswith("_web/"):
        return LAYER_WEB
    if rel == "features/dialer.py" or rel.startswith("features/_dialer/"):
        return LAYER_DIALER
    if rel in ("features/accounts.py",):
        return LAYER_WEB
    if rel.startswith("features/_prospects/"):
        if rel.endswith(
            (
                "backend_local.py",
                "backend_supabase.py",
                "dial_records.py",
                "dial_archive.py",
                "csv_export.py",
                "csv_import.py",
                "dials_csv_export.py",
                "migration_flags.py",
            )
        ) or "/backend_" in rel:
            return LAYER_STORAGE
        return LAYER_DOMAIN
    if rel in ("features/org_storage.py",):
        return LAYER_STORAGE
    if rel.startswith("features/"):
        return LAYER_DOMAIN
    return None


def layer_for_module(module: str) -> int | None:
    if not module:
        return None
    if module.startswith("shared."):
        return LAYER_SHARED
    if module in ("shared",):
        return LAYER_SHARED
    if module.startswith("_web."):
        return LAYER_WEB
    if module in ("web", "server", "dialer"):
        return LAYER_WEB
    if module == "features.dialer" or module.startswith("features._dialer."):
        return LAYER_DIALER
    if module in (
        "features.org_storage",
        "features._prospects.backend_local",
        "features._prospects.backend_supabase",
        "features._prospects.dial_records",
        "features._prospects.dial_archive",
        "features._prospects.csv_export",
        "features._prospects.csv_import",
        "features._prospects.dials_csv_export",
        "features._prospects.migration_flags",
    ):
        return LAYER_STORAGE
    if module == "features.accounts":
        return LAYER_WEB
    if module.startswith("features."):
        return LAYER_DOMAIN
    return None


def iter_python_files():
    for path in ROOT.rglob("*.py"):
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_DIRS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        layer = layer_for_path(path)
        if layer is not None:
            yield path, layer


def imports_in_file(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return []
    mods: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.append(alias.name.split(".")[0] if alias.name else "")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.append(node.module)
    return mods


def main() -> int:
    violations: list[str] = []
    for path, source_layer in iter_python_files():
        rel = path.relative_to(ROOT).as_posix()
        for mod in imports_in_file(path):
            if not (mod.startswith("features") or mod.startswith("shared") or mod.startswith("_web")):
                continue
            target_layer = layer_for_module(mod)
            if target_layer is None:
                continue
            if source_layer < target_layer:
                pair = (rel, mod)
                if pair in ALLOWED_VIOLATIONS:
                    continue
                violations.append(
                    f"{rel} ({LAYER_NAMES[source_layer]}) imports {mod} ({LAYER_NAMES[target_layer]})"
                )
    if violations:
        sys.stderr.write("Layer violations (importer cannot import a higher layer):\n")
        for line in sorted(set(violations)):
            sys.stderr.write(f"  - {line}\n")
        return 1
    files = list(iter_python_files())
    print(f"OK: {len(files)} files checked, no layer violations ({len(ALLOWED_VIOLATIONS)} allowlisted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())