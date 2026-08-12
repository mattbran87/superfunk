#!/usr/bin/env python3
"""Rebuild .superfunk/tracking.db from every specs/<module>/<feature>/spec.md.

Also patches a generated status-summary block into each module's roadmap.md,
between <!-- status:start --> and <!-- status:end --> markers. The markers get
inserted automatically, right after the H1 heading, if a roadmap.md doesn't
have them yet. Nothing outside the markers is ever touched.

Usage: python .superfunk/rebuild_index.py [repo_root]
"""

import re
import sqlite3
import sys
from pathlib import Path

FIELD_RE = re.compile(r"^\*\*(?P<key>[A-Za-z]+):\*\*\s*(?P<value>.*)$")
H1_RE = re.compile(r"^#\s+(?P<name>.+)$")
BUNDLE_HEADING_RE = re.compile(r"^##\s+Bundle:\s*(?P<name>.+)$")
LINK_RE = re.compile(r"^-\s*\[(?P<name>.+?)\]\(\./(?P<dir>[^/)]+)/?\)\s*$")
DONE_STATUS = "Done"
VALID_STATUSES = {"Planned", "In Progress", "Done", "Deferred", "Dropped"}

STATUS_START = "<!-- status:start -->"
STATUS_END = "<!-- status:end -->"
STATUS_BLOCK_RE = re.compile(re.escape(STATUS_START) + r".*?" + re.escape(STATUS_END), re.DOTALL)

BUNDLES_START = "<!-- bundles:start -->"
BUNDLES_END = "<!-- bundles:end -->"
BUNDLES_BLOCK_RE = re.compile(re.escape(BUNDLES_START) + r".*?" + re.escape(BUNDLES_END), re.DOTALL)
BUNDLE_ROW_RE = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*\d+\s*\|[^|]*\|\s*\[[^\]]*\]\(\./(?P<file>[^)]+)\)\s*\|\s*$"
)

LINE_THRESHOLD = 150


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


def is_split(roadmap_path: Path) -> bool:
    return BUNDLES_START in roadmap_path.read_text(encoding="utf-8")


def parse_bundles_table(roadmap_path: Path):
    """Ordered list of (bundle_name, bundle_filename) from the generated Bundles table."""
    text = roadmap_path.read_text(encoding="utf-8")
    match = BUNDLES_BLOCK_RE.search(text)
    if not match:
        return []
    entries = []
    for line in match.group(0).splitlines():
        row = BUNDLE_ROW_RE.match(line.strip())
        if row:
            entries.append((row.group("name").strip(), row.group("file").strip()))
    return entries


def build_bundles_table(bundle_stats):
    """bundle_stats: ordered list of (bundle_name, filename, done_count, total_count)."""
    lines = ["## Bundles", "", "| Bundle | Features | Status | File |", "|---|---|---|---|"]
    for bundle, filename, done, total in bundle_stats:
        lines.append(f"| {bundle} | {total} | {done}/{total} Done | [{filename}](./{filename}) |")
    return "\n".join(lines)


def patch_bundles_table(roadmap_path: Path, table_content: str) -> bool:
    text = roadmap_path.read_text(encoding="utf-8")
    new_block = f"{BUNDLES_START}\n{table_content}\n{BUNDLES_END}"
    new_text = BUNDLES_BLOCK_RE.sub(lambda _m: new_block, text, count=1)
    if new_text != text:
        roadmap_path.write_text(new_text, encoding="utf-8")
        return True
    return False


def parse_roadmap_links(roadmap_path: Path):
    """Ordered list of (bundle_name, feature_dir), walking the file top to bottom.

    Skips the generated status block itself, so re-parsing after a patch never
    picks up table rows as if they were hand-authored links.
    """
    entries = []
    current_bundle = None
    in_status_block = False
    for line in roadmap_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == STATUS_START:
            in_status_block = True
            continue
        if stripped == STATUS_END:
            in_status_block = False
            continue
        if in_status_block:
            continue
        bundle_match = BUNDLE_HEADING_RE.match(stripped)
        if bundle_match:
            current_bundle = bundle_match.group("name").strip()
            continue
        link_match = LINK_RE.match(stripped)
        if link_match:
            entries.append((current_bundle, link_match.group("dir")))
    return entries


def build_status_table(entries, path_index, module):
    lines = ["## Status Summary", ""]
    if not entries:
        lines.append("_No features filed yet._")
    else:
        lines.append("| Feature | Bundle | Status |")
        lines.append("|---|---|---|")
        for bundle, feature_dir in entries:
            path = f"specs/{module}/{feature_dir}"
            record = path_index.get(path)
            name = record["name"] if record else feature_dir
            status = record["status"] if record else "unknown"
            lines.append(f"| [{name}](./{feature_dir}/) | {bundle or ''} | {status or 'unset'} |")
    return "\n".join(lines)


def patch_roadmap_status(roadmap_path: Path, table_content: str) -> bool:
    text = roadmap_path.read_text(encoding="utf-8")
    new_block = f"{STATUS_START}\n{table_content}\n{STATUS_END}"

    if STATUS_BLOCK_RE.search(text):
        new_text = STATUS_BLOCK_RE.sub(lambda _m: new_block, text, count=1)
    else:
        lines = text.splitlines()
        h1_idx = 0
        for i, line in enumerate(lines):
            if H1_RE.match(line):
                h1_idx = i
                break
        insert_at = h1_idx + 1
        # Skip past any existing blank lines right after the H1, so we don't
        # stack our own separator blank line on top of one that's already there.
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        new_lines = lines[: h1_idx + 1] + ["", new_block, ""] + lines[insert_at:]
        new_text = "\n".join(new_lines) + "\n"

    if new_text != text:
        roadmap_path.write_text(new_text, encoding="utf-8")
        return True
    return False


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

    # Pass 3: patch each module's roadmap.md with generated status (and, for a
    # split module, Bundles) content.
    path_index = {record["path"]: record for record in records}
    if specs_root.is_dir():
        for module_dir in sorted(specs_root.iterdir()):
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            roadmap_path = module_dir / "roadmap.md"
            if not roadmap_path.is_file():
                continue

            if is_split(roadmap_path):
                # Trust the existing table's order for bundles it already knows
                # about, then append anything discovered on disk that isn't in
                # the table yet -- e.g. a bundle add_feature.py just created.
                known = parse_bundles_table(roadmap_path)
                known_files = {file for _, file in known}
                discovered = sorted(
                    p.name for p in module_dir.glob("roadmap-*.md") if p.name not in known_files
                )
                bundles = list(known)
                for filename in discovered:
                    bundle_path = module_dir / filename
                    name = None
                    for line in bundle_path.read_text(encoding="utf-8").splitlines():
                        m = BUNDLE_HEADING_RE.match(line.strip())
                        if m:
                            name = m.group("name").strip()
                            break
                    bundles.append((name or filename, filename))

                seen_names = set()
                deduped_bundles = []
                for name, file in bundles:
                    if name in seen_names:
                        print(f"Warning: module '{module_dir.name}' has two bundle files both named '{name}' -- keeping the first, ignoring {file}")
                        continue
                    seen_names.add(name)
                    deduped_bundles.append((name, file))
                bundles = deduped_bundles

                entries = []
                bundle_stats = []
                for bundle_name, bundle_file in bundles:
                    bundle_path = module_dir / bundle_file
                    if not bundle_path.is_file():
                        if bundle_file in known_files:
                            print(f"Warning: {roadmap_path} lists bundle '{bundle_name}' pointing at {bundle_file}, but that file doesn't exist")
                        bundle_entries = []
                    else:
                        bundle_entries = parse_roadmap_links(bundle_path)
                    entries.extend(bundle_entries)
                    done = 0
                    for _, feature_dir in bundle_entries:
                        record = path_index.get(f"specs/{module_dir.name}/{feature_dir}")
                        if record and record["status"] == DONE_STATUS:
                            done += 1
                    bundle_stats.append((bundle_name, bundle_file, done, len(bundle_entries)))

                table = build_status_table(entries, path_index, module_dir.name)
                status_changed = patch_roadmap_status(roadmap_path, table)
                bundles_table = build_bundles_table(bundle_stats)
                bundles_changed = patch_bundles_table(roadmap_path, bundles_table)
                if status_changed or bundles_changed:
                    print(f"Updated status summary and Bundles table in {roadmap_path}")
            else:
                entries = parse_roadmap_links(roadmap_path)
                table = build_status_table(entries, path_index, module_dir.name)
                changed = patch_roadmap_status(roadmap_path, table)
                if changed:
                    print(f"Updated status summary in {roadmap_path}")

                line_count = len(roadmap_path.read_text(encoding="utf-8").splitlines())
                if line_count > LINE_THRESHOLD:
                    print(
                        f"Warning: {roadmap_path} has {line_count} lines (over {LINE_THRESHOLD}) -- "
                        f"consider running: python .superfunk/split_roadmap.py --module {module_dir.name}"
                    )

    print(f"Rebuilt {db_path} with {len(records)} feature(s).")


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    rebuild(root)
