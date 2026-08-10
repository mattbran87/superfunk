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


def rebuild(repo_root: Path):
    specs_root = repo_root / "specs"
    db_dir = repo_root / ".superfunk"
    db_dir.mkdir(exist_ok=True)
    db_path = db_dir / "tracking.db"

    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS features")
    conn.execute(
        """
        CREATE TABLE features (
            path TEXT PRIMARY KEY,
            module TEXT NOT NULL,
            bundle TEXT,
            name TEXT,
            status TEXT
        )
        """
    )

    count = 0
    if specs_root.is_dir():
        for spec_path in find_specs(specs_root):
            module = spec_path.parent.parent.name
            feature_dir = spec_path.parent.name
            rel_path = str(spec_path.parent.relative_to(repo_root)).replace("\\", "/")
            name, fields = parse_spec(spec_path)
            conn.execute(
                "INSERT INTO features (path, module, bundle, name, status) VALUES (?, ?, ?, ?, ?)",
                (rel_path, module, fields.get("bundle"), name or feature_dir, fields.get("status")),
            )
            count += 1

    conn.commit()
    conn.close()
    print(f"Rebuilt {db_path} with {count} feature(s).")


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    rebuild(root)
