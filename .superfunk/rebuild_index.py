#!/usr/bin/env python3
"""Rebuild .superfunk/tracking.db from every specs/<module>/<feature>/spec.md.

Usage: python .superfunk/rebuild_index.py [repo_root]
"""

import re
import sqlite3
import sys
from pathlib import Path

FIELD_RE = re.compile(r"^\*\*(?P<key>[A-Za-z]+):\*\*\s*(?P<value>.*)$")
H1_RE = re.compile(r"^#\s+(?P<name>.+)$")
DONE_STATUS = "Done"
VALID_STATUSES = {"Planned", "In Progress", "Done", "Deferred", "Dropped"}


def parse_spec(spec_path: Path):
    name = None
    fields = {}
    for line in spec_path.read_text(encoding="utf-8").splitlines():
        if name is None:
            h1 = H1_RE.match(line)
            if h1:
                name = h1.group("name").strip()
                continue
        m = FIELD_RE.match(line)
        if m:
            fields[m.group("key").lower()] = m.group("value").strip()
    return name, fields


def find_specs(specs_root: Path):
    for spec_path in specs_root.glob("*/*/spec.md"):
        # specs/<module>/<feature-dir>/spec.md ; skip the _template scaffold
        module_dir = spec_path.parent.parent
        if module_dir.name.startswith("_"):
            continue
        yield spec_path


def parse_dependencies(raw: str):
    if not raw or raw.strip().lower() == "none":
        return []
    return [title.strip() for title in raw.split(",") if title.strip()]


def resolve_dependency(title: str, name_index: dict):
    matches = name_index.get(title, [])
    if len(matches) == 0:
        return "unfiled", f'"{title}" is not filed yet'
    if len(matches) > 1:
        return "ambiguous", f'"{title}" matches {len(matches)} features -- ambiguous'
    status = matches[0]["status"]
    if status == DONE_STATUS:
        return "done", None
    return "not_done", f'"{title}" is not Done yet (status: {status or "unset"})'


def rebuild(repo_root: Path):
    specs_root = repo_root / "specs"
    db_dir = repo_root / ".superfunk"
    db_dir.mkdir(exist_ok=True)
    db_path = db_dir / "tracking.db"

    # Pass 1: read every spec.
    records = []
    if specs_root.is_dir():
        for spec_path in find_specs(specs_root):
            module = spec_path.parent.parent.name
            feature_dir = spec_path.parent.name
            rel_path = str(spec_path.parent.relative_to(repo_root)).replace("\\", "/")
            name, fields = parse_spec(spec_path)
            records.append(
                {
                    "path": rel_path,
                    "module": module,
                    "bundle": fields.get("bundle"),
                    "name": name or feature_dir,
                    "status": fields.get("status"),
                    "dependencies_raw": fields.get("dependencies", "None"),
                }
            )

    # Build a name -> [records] index for dependency resolution (spans every module).
    name_index = {}
    for record in records:
        name_index.setdefault(record["name"], []).append(record)

    # Pass 2: resolve dependencies and compute the derived blocked state per feature.
    for record in records:
        dep_titles = parse_dependencies(record["dependencies_raw"])
        reasons = []
        for title in dep_titles:
            outcome, reason = resolve_dependency(title, name_index)
            if outcome != "done":
                reasons.append(reason)
        record["blocked"] = 1 if reasons else 0
        record["blocked_reason"] = "; ".join(reasons) if reasons else None

    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS features")
    conn.execute(
        """
        CREATE TABLE features (
            path TEXT PRIMARY KEY,
            module TEXT NOT NULL,
            bundle TEXT,
            name TEXT,
            status TEXT,
            dependencies TEXT,
            blocked INTEGER NOT NULL DEFAULT 0,
            blocked_reason TEXT
        )
        """
    )
    for record in records:
        conn.execute(
            """
            INSERT INTO features (path, module, bundle, name, status, dependencies, blocked, blocked_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["path"],
                record["module"],
                record["bundle"],
                record["name"],
                record["status"],
                record["dependencies_raw"],
                record["blocked"],
                record["blocked_reason"],
            ),
        )

    conn.commit()
    conn.close()

    for record in records:
        status = record["status"]
        if status not in VALID_STATUSES:
            print(f'Warning: {record["path"]} has an unrecognized Status: "{status}" (expected one of {sorted(VALID_STATUSES)})')

    print(f"Rebuilt {db_path} with {len(records)} feature(s).")


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    rebuild(root)
