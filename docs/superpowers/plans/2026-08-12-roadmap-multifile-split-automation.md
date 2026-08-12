# Roadmap Multi-File Split Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the multi-file roadmap split automation from `docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md`: a new `split_roadmap.py` script, plus split-awareness in `rebuild_index.py` and `add_feature.py`, so a module's `roadmap.md` can split into an index + per-bundle files once it grows large, and stay fully usable afterward.

**Architecture:** `rebuild_index.py` gains four small helper functions (`is_split`, `parse_bundles_table`, `build_bundles_table`, `patch_bundles_table`) plus a rewritten Pass 3 that branches on split state — unsplit modules keep today's exact behavior (plus a new line-count warning), split modules aggregate across every discovered `roadmap-<bundle-slug>.md` file. `split_roadmap.py` is a new, separate script that performs the one-time rewrite, reusing `rebuild_index.py`'s parsing functions and `add_feature.py`'s `slugify()`. `add_feature.py` gains a split-aware branch in its bundle-linking function, reusing the same `is_split` check.

**Tech Stack:** Python 3 standard library only (`re`, `sqlite3`, `argparse`, `pathlib`) — matches the existing two scripts exactly. No test framework exists in this repo; verification happens by running the real scripts against disposable scratch fixtures outside the repo, per the design's Testing section.

---

## File Structure

- **Modify:** `.superfunk/rebuild_index.py` — new constants (`BUNDLES_START`/`END`/`BLOCK_RE`, `BUNDLE_ROW_RE`, `LINE_THRESHOLD`), four new functions, and a rewritten Pass 3 inside `rebuild()`.
- **Create:** `.superfunk/split_roadmap.py` — the one-time split command. Imports `rebuild_index` and `add_feature` as modules (the same `sys.path.insert` trick `add_feature.py` already uses to import `rebuild_index`).
- **Modify:** `.superfunk/add_feature.py` — moves the `rebuild_index` import to module level (currently lazy, inside `main()`), and gives `ensure_bundle_and_link` a split-aware branch via a new helper function `_ensure_bundle_and_link_split`.

One deliberate deviation from the approved design: the design's CLI sketch showed `split_roadmap.py --module <module> [--rebuild-index]`, an optional flag mirroring `add_feature.py`. This plan drops the flag and makes the rebuild **unconditional** at the end of `split_roadmap.py` instead. Reason found during planning: without an immediate rebuild, the freshly-split file's Bundles table would show a placeholder `0/N Done` for every bundle — not just stale (like a newly-filed `Planned` feature's status, which `add_feature.py`'s optional flag reasonably leaves stale), but actively misleading, since the split doesn't know real completion counts on its own. Always rebuilding closes that gap for a small, clearly-justified cost.

---

## Task 1: Split-awareness helpers and a rewritten Pass 3 in `rebuild_index.py`

**Files:**
- Modify: `.superfunk/rebuild_index.py`

- [ ] **Step 1: Add the new constants**

Find:
```python
STATUS_START = "<!-- status:start -->"
STATUS_END = "<!-- status:end -->"
STATUS_BLOCK_RE = re.compile(re.escape(STATUS_START) + r".*?" + re.escape(STATUS_END), re.DOTALL)
```

Replace with:
```python
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
```

- [ ] **Step 2: Write a scratch script exercising the four new functions (they don't exist yet — this must fail)**

```bash
mkdir -p /c/sf-split-unit-test
cat > /c/sf-split-unit-test/check.py <<'EOF'
import sys
sys.path.insert(0, r"C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk")
from pathlib import Path
import rebuild_index as ri

fixture = Path(r"/c/sf-split-unit-test/roadmap.md")
fixture.write_text(
    "# Widgets\n\n"
    "<!-- status:start -->\n## Status Summary\n\n_placeholder_\n<!-- status:end -->\n\n"
    "<!-- bundles:start -->\n## Bundles\n\n"
    "| Bundle | Features | Status | File |\n|---|---|---|---|\n"
    "| Core | 2 | 0/2 Done | [roadmap-core.md](./roadmap-core.md) |\n"
    "<!-- bundles:end -->\n",
    encoding="utf-8",
)

assert ri.is_split(fixture) is True, "is_split should detect the bundles markers"

entries = ri.parse_bundles_table(fixture)
assert entries == [("Core", "roadmap-core.md")], f"unexpected: {entries}"

table = ri.build_bundles_table([("Core", "roadmap-core.md", 1, 2)])
assert "| Core | 2 | 1/2 Done | [roadmap-core.md](./roadmap-core.md) |" in table, table

changed = ri.patch_bundles_table(fixture, table)
assert changed is True
assert "1/2 Done" in fixture.read_text(encoding="utf-8")

changed_again = ri.patch_bundles_table(fixture, table)
assert changed_again is False, "patching with identical content must be a no-op"

print("ALL CHECKS PASSED")
EOF
python /c/sf-split-unit-test/check.py
```

Expected: `AttributeError: module 'rebuild_index' has no attribute 'is_split'` (the functions don't exist yet).

- [ ] **Step 3: Implement the four functions**

Find:
```python
def parse_roadmap_links(roadmap_path: Path):
```

Replace with:
```python
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
```

- [ ] **Step 4: Run the scratch script again to verify it passes**

```bash
python /c/sf-split-unit-test/check.py
```

Expected: `ALL CHECKS PASSED`

- [ ] **Step 5: Rewrite Pass 3 to branch on split state**

Find:
```python
    # Pass 3: patch each module's roadmap.md with a generated status-summary block.
    path_index = {record["path"]: record for record in records}
    modules = sorted({record["module"] for record in records})
    if specs_root.is_dir():
        for module_dir in sorted(specs_root.iterdir()):
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            roadmap_path = module_dir / "roadmap.md"
            if not roadmap_path.is_file():
                continue
            entries = parse_roadmap_links(roadmap_path)
            table = build_status_table(entries, path_index, module_dir.name)
            changed = patch_roadmap_status(roadmap_path, table)
            if changed:
                print(f"Updated status summary in {roadmap_path}")
```

Replace with:
```python
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

                entries = []
                bundle_stats = []
                for bundle_name, bundle_file in bundles:
                    bundle_path = module_dir / bundle_file
                    bundle_entries = parse_roadmap_links(bundle_path) if bundle_path.is_file() else []
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
```

(This also drops the old `modules = sorted(...)` line — it was computed but never used anywhere in the original code.)

- [ ] **Step 6: Verify the existing (unsplit) behavior is unchanged, using the real repo's own dogfood module**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
python .superfunk/rebuild_index.py
```

Expected: output identical in shape to before this change — `Rebuilt .superfunk/tracking.db with 1 feature(s).` and no warnings (the real `specs/feature-tracking/roadmap.md` is nowhere near 150 lines). Confirm with:

```bash
git diff specs/feature-tracking/roadmap.md
```

Expected: no diff (Task 1 must not change the real repo's tracked files — `tracking.db` is gitignored, so only `git diff` on tracked files matters here).

- [ ] **Step 7: Clean up the scratch fixture and commit**

```bash
rm -rf /c/sf-split-unit-test
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
git add .superfunk/rebuild_index.py
git commit -m "feat: add split-awareness helpers and split-aware Pass 3 to rebuild_index.py

Adds is_split, parse_bundles_table, build_bundles_table, and
patch_bundles_table, plus a rewritten Pass 3 that branches on split
state. An unsplit module keeps today's exact behavior, plus a new
warning once its roadmap.md exceeds 150 lines. A split module
aggregates status across every discovered roadmap-<bundle-slug>.md
file and regenerates the Bundles table fresh every run -- including
self-healing any bundle file that exists on disk but isn't in the
table yet.

Part of docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md."
```

---

## Task 2: Create `.superfunk/split_roadmap.py`

**Files:**
- Create: `.superfunk/split_roadmap.py`

- [ ] **Step 1: Write a scratch script exercising the split against a synthetic unsplit module (the script doesn't exist yet — this must fail)**

```bash
mkdir -p /c/sf-split-e2e-test/specs/widgets/2026-01-01-feature-a
mkdir -p /c/sf-split-e2e-test/specs/widgets/2026-01-01-feature-b
mkdir -p /c/sf-split-e2e-test/specs/widgets/2026-01-01-feature-c
cat > /c/sf-split-e2e-test/specs/widgets/roadmap.md <<'EOF'
# Widgets

## Bundle: Core

- [Feature A](./2026-01-01-feature-a/)
- [Feature B](./2026-01-01-feature-b/)

## Bundle: Extras

- [Feature C](./2026-01-01-feature-c/)
EOF
for f in feature-a feature-b feature-c; do
cat > "/c/sf-split-e2e-test/specs/widgets/2026-01-01-$f/spec.md" <<EOF
# $(echo $f | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')

**Module:** widgets
**Bundle:** Core
**Status:** Planned
**Dependencies:** None
EOF
done
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\split_roadmap.py" --module widgets /c/sf-split-e2e-test
```

Expected: `python: can't open file '...split_roadmap.py': [Errno 2] No such file or directory` (the script doesn't exist yet).

- [ ] **Step 2: Create the script**

Write `.superfunk/split_roadmap.py`:
```python
#!/usr/bin/env python3
"""Split a module's roadmap.md into an index file plus one file per bundle.

Reads the module's existing roadmap.md, writes one
specs/<module>/roadmap-<bundle-slug>.md per bundle (holding that
bundle's heading and feature links), then rewrites roadmap.md itself
as a pure index: the H1, the generated Status Summary block, and a
new generated Bundles table. Always finishes by running
rebuild_index.py's full rebuild, so the newly-split file never shows
a misleading placeholder status/count.

Running this against an already-split module does nothing and prints
a message saying so -- safe to run more than once.

Usage: python .superfunk/split_roadmap.py --module <module> [repo_root]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import add_feature
import rebuild_index


def split_module(repo_root: Path, specs_root: Path, module: str) -> None:
    roadmap_path = specs_root / module / "roadmap.md"
    if not roadmap_path.is_file():
        raise SystemExit(f"Error: no roadmap.md found for module '{module}' at {roadmap_path}")

    if rebuild_index.is_split(roadmap_path):
        print(f"Module '{module}' is already split. Nothing to do.")
        return

    entries = rebuild_index.parse_roadmap_links(roadmap_path)
    if not entries:
        raise SystemExit(f"Error: no bundles/features found in {roadmap_path} -- nothing to split.")

    # Real feature names come from each spec.md, the same source rebuild_index.py
    # already trusts -- not from the roadmap.md link text, which could in
    # principle have drifted from the spec's actual title.
    path_index = {}
    for spec_path in rebuild_index.find_specs(specs_root):
        rel_path = str(spec_path.parent.relative_to(repo_root)).replace("\\", "/")
        name, _fields = rebuild_index.parse_spec(spec_path)
        path_index[rel_path] = name or spec_path.parent.name

    # Group entries by bundle, preserving first-seen bundle order.
    bundles_order = []
    bundles_map = {}
    for bundle, feature_dir in entries:
        if bundle not in bundles_map:
            bundles_map[bundle] = []
            bundles_order.append(bundle)
        bundles_map[bundle].append(feature_dir)

    # Slug each bundle, guarding against two different names colliding.
    slug_to_bundle = {}
    bundle_files = {}
    for bundle in bundles_order:
        slug = add_feature.slugify(bundle)
        filename = f"roadmap-{slug}.md"
        if slug in slug_to_bundle and slug_to_bundle[slug] != bundle:
            raise SystemExit(
                f"Error: bundles '{slug_to_bundle[slug]}' and '{bundle}' both slugify to "
                f"'{slug}' -- cannot split with colliding file names."
            )
        slug_to_bundle[slug] = bundle
        bundle_files[bundle] = filename

    module_dir = specs_root / module
    for bundle in bundles_order:
        lines = [f"## Bundle: {bundle}", ""]
        for feature_dir in bundles_map[bundle]:
            rel_path = f"specs/{module}/{feature_dir}"
            name = path_index.get(rel_path, feature_dir)
            lines.append(f"- [{name}](./{feature_dir}/)")
        bundle_path = module_dir / bundle_files[bundle]
        bundle_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Created {bundle_path}")

    title_line = f"# {add_feature.title_case(module)}"
    for line in roadmap_path.read_text(encoding="utf-8").splitlines():
        if rebuild_index.H1_RE.match(line):
            title_line = line
            break

    # Placeholder counts -- the unconditional rebuild below overwrites both
    # blocks with real numbers before this function returns.
    bundles_rows = "\n".join(
        f"| {bundle} | {len(bundles_map[bundle])} | 0/{len(bundles_map[bundle])} Done | "
        f"[{bundle_files[bundle]}](./{bundle_files[bundle]}) |"
        for bundle in bundles_order
    )
    new_index_content = (
        f"{title_line}\n\n"
        f"{rebuild_index.STATUS_START}\n## Status Summary\n\n_placeholder_\n{rebuild_index.STATUS_END}\n\n"
        f"{rebuild_index.BUNDLES_START}\n## Bundles\n\n"
        "| Bundle | Features | Status | File |\n|---|---|---|---|\n"
        f"{bundles_rows}\n"
        f"{rebuild_index.BUNDLES_END}\n"
    )
    roadmap_path.write_text(new_index_content, encoding="utf-8")
    print(f"Rewrote {roadmap_path} as a split index.")

    rebuild_index.rebuild(repo_root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True)
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    specs_root = repo_root / "specs"
    split_module(repo_root, specs_root, args.module)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the scratch script again to verify the split works**

```bash
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\split_roadmap.py" --module widgets /c/sf-split-e2e-test
cat /c/sf-split-e2e-test/specs/widgets/roadmap.md
cat /c/sf-split-e2e-test/specs/widgets/roadmap-core.md
cat /c/sf-split-e2e-test/specs/widgets/roadmap-extras.md
```

Expected:
- `roadmap-core.md` contains `## Bundle: Core` plus links to Feature A and Feature B.
- `roadmap-extras.md` contains `## Bundle: Extras` plus a link to Feature C.
- `roadmap.md` contains the H1, a Status Summary table showing all 3 features with status `Planned`, and a Bundles table with two rows: `Core | 2 | 0/2 Done | [roadmap-core.md](./roadmap-core.md)` and `Extras | 1 | 0/1 Done | [roadmap-extras.md](./roadmap-extras.md)` (0 Done is correct here — all three features are `Planned`, not `Done`).

- [ ] **Step 4: Verify running it again on the now-split module is a safe no-op**

```bash
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\split_roadmap.py" --module widgets /c/sf-split-e2e-test
```

Expected: `Module 'widgets' is already split. Nothing to do.` — and no files change (confirm with `git status` if you initialize the scratch dir as a git repo, or just re-`cat` the files and compare).

- [ ] **Step 5: Clean up the scratch fixture and commit**

```bash
rm -rf /c/sf-split-e2e-test
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
git add .superfunk/split_roadmap.py
git commit -m "feat: add .superfunk/split_roadmap.py

The explicit, one-time command that performs the actual roadmap
split: writes one roadmap-<bundle-slug>.md per bundle (real feature
names sourced from each spec.md, not the roadmap.md link text), then
rewrites roadmap.md as a pure index. Always finishes with a full
rebuild_index.py run so the split never leaves a misleading
placeholder status behind. Re-running against an already-split module
is a safe no-op.

Part of docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md."
```

---

## Task 3: Make `add_feature.py` split-aware

**Files:**
- Modify: `.superfunk/add_feature.py`

- [ ] **Step 1: Write a scratch script exercising add_feature.py against an already-split module (the split-aware branch doesn't exist yet — this must fail or misbehave)**

```bash
mkdir -p /c/sf-addfeature-split-test/specs/_template
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template\spec.md" /c/sf-addfeature-split-test/specs/_template/
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template\tasks.md" /c/sf-addfeature-split-test/specs/_template/
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template\decisions.md" /c/sf-addfeature-split-test/specs/_template/
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template\notes.md" /c/sf-addfeature-split-test/specs/_template/
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template\roadmap.md" /c/sf-addfeature-split-test/specs/_template/

mkdir -p /c/sf-addfeature-split-test/specs/widgets
cat > /c/sf-addfeature-split-test/specs/widgets/roadmap.md <<'EOF'
# Widgets

<!-- status:start -->
## Status Summary

_placeholder_
<!-- status:end -->

<!-- bundles:start -->
## Bundles

| Bundle | Features | Status | File |
|---|---|---|---|
| Core | 0 | 0/0 Done | [roadmap-core.md](./roadmap-core.md) |
<!-- bundles:end -->
EOF
cat > /c/sf-addfeature-split-test/specs/widgets/roadmap-core.md <<'EOF'
## Bundle: Core

EOF

python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module widgets --bundle Core --feature "Existing Bundle Feature" /c/sf-addfeature-split-test
cat /c/sf-addfeature-split-test/specs/widgets/roadmap-core.md
cat /c/sf-addfeature-split-test/specs/widgets/roadmap.md
```

Expected (current, unmodified `add_feature.py`): the link gets written into `roadmap.md` itself (wrong — it should go into `roadmap-core.md`), because `ensure_bundle_and_link` doesn't know this module is split yet.

- [ ] **Step 2: Move the `rebuild_index` import to module level**

Find:
```python
import argparse
import datetime
import re
import sys
from pathlib import Path

TEMPLATE_FILES = ["spec.md", "tasks.md", "decisions.md", "notes.md"]
```

Replace with:
```python
import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rebuild_index

TEMPLATE_FILES = ["spec.md", "tasks.md", "decisions.md", "notes.md"]
```

- [ ] **Step 3: Simplify the now-redundant lazy import in `main()`**

Find:
```python
    if args.rebuild_index:
        sys.path.insert(0, str(Path(__file__).parent))
        import rebuild_index
        rebuild_index.rebuild(repo_root)
```

Replace with:
```python
    if args.rebuild_index:
        rebuild_index.rebuild(repo_root)
```

- [ ] **Step 4: Add the split-aware branch to `ensure_bundle_and_link`**

Find:
```python
def ensure_bundle_and_link(roadmap_path: Path, bundle: str, feature_name: str, feature_dir_name: str) -> None:
    lines = roadmap_path.read_text(encoding="utf-8").splitlines(keepends=True)
```

Replace with:
```python
def ensure_bundle_and_link(roadmap_path: Path, bundle: str, feature_name: str, feature_dir_name: str) -> None:
    if rebuild_index.is_split(roadmap_path):
        _ensure_bundle_and_link_split(roadmap_path, bundle, feature_name, feature_dir_name)
        return

    lines = roadmap_path.read_text(encoding="utf-8").splitlines(keepends=True)
```

- [ ] **Step 5: Add the new `_ensure_bundle_and_link_split` helper**

Find:
```python
def scaffold_feature(specs_root: Path, template_root: Path, module: str, bundle: str, feature_name: str, depends_on: str) -> str:
```

Replace with:
```python
def _ensure_bundle_and_link_split(roadmap_path: Path, bundle: str, feature_name: str, feature_dir_name: str) -> None:
    module_dir = roadmap_path.parent
    bundles = rebuild_index.parse_bundles_table(roadmap_path)
    bundle_file = next((f for name, f in bundles if name == bundle), None)
    link_line = f"- [{feature_name}](./{feature_dir_name}/)\n"

    if bundle_file is None:
        slug = slugify(bundle)
        bundle_file = f"roadmap-{slug}.md"
        bundle_path = module_dir / bundle_file
        if bundle_path.exists():
            raise SystemExit(
                f"Error: {bundle_path} already exists but isn't listed in {roadmap_path}'s "
                f"Bundles table. Run rebuild_index.py to sync the table first, then retry."
            )
        bundle_path.write_text(f"## Bundle: {bundle}\n\n{link_line}", encoding="utf-8")
        print(f"Created new bundle file: {bundle_path} (run rebuild_index.py to add it to the Bundles table)")
        return

    bundle_path = module_dir / bundle_file
    lines = bundle_path.read_text(encoding="utf-8").splitlines(keepends=True)
    insert_at = len(lines)
    while insert_at > 0 and lines[insert_at - 1].strip() == "":
        insert_at -= 1
    lines.insert(insert_at, link_line)
    bundle_path.write_text("".join(lines), encoding="utf-8")
    print(f"Linked feature under '## Bundle: {bundle}' in {bundle_path}")


def scaffold_feature(specs_root: Path, template_root: Path, module: str, bundle: str, feature_name: str, depends_on: str) -> str:
```

- [ ] **Step 6: Run the scratch script again to verify the existing-bundle path now works**

```bash
rm -f /c/sf-addfeature-split-test/specs/widgets/2026-*/spec.md 2>/dev/null
rm -rf /c/sf-addfeature-split-test/specs/widgets/2026-*-existing-bundle-feature 2>/dev/null
cat > /c/sf-addfeature-split-test/specs/widgets/roadmap-core.md <<'EOF'
## Bundle: Core

EOF
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module widgets --bundle Core --feature "Existing Bundle Feature" /c/sf-addfeature-split-test
cat /c/sf-addfeature-split-test/specs/widgets/roadmap-core.md
cat /c/sf-addfeature-split-test/specs/widgets/roadmap.md
```

Expected: `roadmap-core.md` now contains the new link under `## Bundle: Core`; `roadmap.md` (the index) is untouched by this step.

- [ ] **Step 7: Verify the brand-new-bundle path**

```bash
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module widgets --bundle Extras --feature "Brand New Bundle Feature" /c/sf-addfeature-split-test
cat /c/sf-addfeature-split-test/specs/widgets/roadmap-extras.md
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module widgets --bundle Extras --feature "Second Extras Feature" --rebuild-index /c/sf-addfeature-split-test
cat /c/sf-addfeature-split-test/specs/widgets/roadmap.md
```

Expected: the first command creates `roadmap-extras.md` with `## Bundle: Extras` and the new link, and prints the "run rebuild_index.py to add it to the Bundles table" message. The second command (with `--rebuild-index`) files a second feature into the same now-known-on-disk bundle, then rebuilds — `roadmap.md`'s Bundles table should now show 3 rows total (Core, Extras with 2 features), confirming Task 1's filesystem self-healing discovered `roadmap-extras.md` even though it was never in the table.

- [ ] **Step 8: Verify the unsplit path is still completely unaffected, using the real repo's dogfood module**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
python .superfunk/add_feature.py --module feature-tracking --bundle "Roadmap Scaling" --feature "Scratch Verification Feature Do Not Keep"
git status --short specs/feature-tracking/
```

Expected: a new feature directory and a new link appear under `specs/feature-tracking/roadmap.md`'s existing `## Bundle: Roadmap Scaling` heading, exactly like before this task — proving the unsplit path is untouched. Then remove this scratch verification feature (it isn't real work):

```bash
git status --short specs/feature-tracking/
```

Note the new paths from the command's own output, then:

```bash
rm -rf "specs/feature-tracking/<the-new-feature-dir-printed-above>"
git checkout -- specs/feature-tracking/roadmap.md
```

- [ ] **Step 9: Clean up the scratch fixture and commit**

```bash
rm -rf /c/sf-addfeature-split-test
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
git add .superfunk/add_feature.py
git commit -m "feat: make add_feature.py split-aware

ensure_bundle_and_link now checks rebuild_index.is_split() and, for a
split module, writes the new link into that bundle's own
roadmap-<slug>.md file (creating it for a brand-new bundle) instead of
the index. Never touches the Bundles table itself -- that stays
rebuild_index.py's job, regenerated fresh (including self-healing a
brand-new bundle file that isn't in the table yet, per Task 1). The
unsplit path is completely unchanged.

Part of docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md."
```

---

## Task 4: End-to-end verification against the design's three Testing scenarios

**Files:** none (verification only; touches no repo files)

- [ ] **Step 1: Build a synthetic module big enough to actually trigger the warning**

```bash
mkdir -p /c/sf-split-final-test/specs/_template
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\specs\_template"/*.md /c/sf-split-final-test/specs/_template/

for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module bignode --bundle "Bundle $(( (n-1) / 4 + 1 ))" --feature "Feature $n" /c/sf-split-final-test
done
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\rebuild_index.py" /c/sf-split-final-test
wc -l /c/sf-split-final-test/specs/bignode/roadmap.md
```

Expected: 12 features across 3 bundles generate enough Status Summary rows to push `roadmap.md` over 150 lines (if not, add more features with a similar loop until `wc -l` reports over 150), and the `rebuild_index.py` output includes the warning line naming `bignode` and pointing at `split_roadmap.py`.

- [ ] **Step 2: Split it, and verify scenario 1 (correctness + idempotency)**

```bash
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\split_roadmap.py" --module bignode /c/sf-split-final-test
md5sum /c/sf-split-final-test/specs/bignode/roadmap.md /c/sf-split-final-test/specs/bignode/roadmap-*.md > /c/sf-split-final-test/hashes-1.txt
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\split_roadmap.py" --module bignode /c/sf-split-final-test
md5sum /c/sf-split-final-test/specs/bignode/roadmap.md /c/sf-split-final-test/specs/bignode/roadmap-*.md > /c/sf-split-final-test/hashes-2.txt
diff /c/sf-split-final-test/hashes-1.txt /c/sf-split-final-test/hashes-2.txt
```

Expected: no diff between the two hash files (the second split run is a genuine no-op, since `split_module` returns immediately on `is_split`). Also manually check no feature link is missing or duplicated across the three `roadmap-bundle-N.md` files versus the original 12.

- [ ] **Step 3: Verify scenario 2 (add_feature.py into an existing and a brand-new bundle)**

```bash
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module bignode --bundle "Bundle 1" --feature "Added To Existing Bundle" /c/sf-split-final-test
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\add_feature.py" --module bignode --bundle "Bundle 4" --feature "Added To New Bundle" --rebuild-index /c/sf-split-final-test
grep -l "Added To Existing Bundle" /c/sf-split-final-test/specs/bignode/roadmap-*.md
grep -l "Added To New Bundle" /c/sf-split-final-test/specs/bignode/roadmap-*.md
cat /c/sf-split-final-test/specs/bignode/roadmap.md
```

Expected: "Added To Existing Bundle" lands in `roadmap-bundle-1.md`; "Added To New Bundle" lands in a fresh `roadmap-bundle-4.md`; the index's Bundles table shows 4 rows total after the `--rebuild-index` run.

- [ ] **Step 4: Verify scenario 3 (status changes propagate correctly)**

```bash
FEATURE_DIR=$(grep -rl "Added To Existing Bundle" /c/sf-split-final-test/specs/bignode/*/spec.md | head -1 | xargs dirname)
sed -i 's/\*\*Status:\*\* Planned/\*\*Status:\*\* Done/' "$FEATURE_DIR/spec.md"
python "C:\Users\marko\IdeaProjects\personal_products\superfunk\.superfunk\rebuild_index.py" /c/sf-split-final-test
grep "Added To Existing Bundle" /c/sf-split-final-test/specs/bignode/roadmap.md
grep -A5 "Bundle 1" /c/sf-split-final-test/specs/bignode/roadmap.md | grep "Done"
```

Expected: the Status Summary table shows "Added To Existing Bundle" with status `Done`; the Bundles table's "Bundle 1" row shows an incremented Done count (e.g. `1/5 Done` instead of `0/5 Done`, depending on how many features that bundle ended up with).

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-split-final-test
```

No commit for this task — it verifies Tasks 1-3 together and touches no repository files.
