#!/usr/bin/env python3
"""File a new feature into the tracking structure.

Usage:
    python .superfunk/add_feature.py --module <module> --bundle <bundle> --feature "<Feature Name>" [--rebuild-index] [repo_root]
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rebuild_index

TEMPLATE_FILES = ["spec.md", "tasks.md", "decisions.md", "notes.md"]
BUNDLE_HEADING_RE = re.compile(r"^## Bundle: (?P<name>.+)$")
INSTRUCTIONAL_COMMENT_RE = re.compile(r"^<!--(?!\s*status:).*-->\s*\n?", re.MULTILINE)


def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def title_case(module: str) -> str:
    return module.replace("-", " ").replace("_", " ").title()


def ensure_module(specs_root: Path, template_root: Path, module: str) -> Path:
    module_dir = specs_root / module
    roadmap_path = module_dir / "roadmap.md"
    if not roadmap_path.is_file():
        module_dir.mkdir(parents=True, exist_ok=True)
        content = (template_root / "roadmap.md").read_text(encoding="utf-8")
        content = content.replace("<Module Name>", title_case(module))
        roadmap_path.write_text(content, encoding="utf-8")
        print(f"Created module: {roadmap_path}")
    return roadmap_path


def ensure_bundle_and_link(roadmap_path: Path, bundle: str, feature_name: str, feature_dir_name: str) -> None:
    if rebuild_index.is_split(roadmap_path):
        _ensure_bundle_and_link_split(roadmap_path, bundle, feature_name, feature_dir_name)
        return

    lines = roadmap_path.read_text(encoding="utf-8").splitlines(keepends=True)
    link_line = f"- [{feature_name}](./{feature_dir_name}/)\n"

    bundle_line_idx = None
    for i, line in enumerate(lines):
        m = BUNDLE_HEADING_RE.match(line.rstrip("\n"))
        if m and m.group("name") == bundle:
            bundle_line_idx = i
            break

    if bundle_line_idx is None:
        # Strip the template's own instructional comment on first real content.
        joined = "".join(lines)
        joined = INSTRUCTIONAL_COMMENT_RE.sub("", joined, count=1)
        lines = joined.splitlines(keepends=True)
        if lines and lines[-1].strip() != "":
            lines.append("\n")
        lines.append(f"## Bundle: {bundle}\n")
        lines.append("\n")
        lines.append(link_line)
    else:
        insert_at = len(lines)
        for j in range(bundle_line_idx + 1, len(lines)):
            if BUNDLE_HEADING_RE.match(lines[j].rstrip("\n")):
                insert_at = j
                break
        while insert_at > bundle_line_idx + 1 and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        lines.insert(insert_at, link_line)

    roadmap_path.write_text("".join(lines), encoding="utf-8")
    print(f"Linked feature under '## Bundle: {bundle}' in {roadmap_path}")


def _append_link_to_bundle_file(bundle_path: Path, bundle: str, link_line: str) -> None:
    lines = bundle_path.read_text(encoding="utf-8").splitlines(keepends=True)
    insert_at = len(lines)
    while insert_at > 0 and lines[insert_at - 1].strip() == "":
        insert_at -= 1
    lines.insert(insert_at, link_line)
    bundle_path.write_text("".join(lines), encoding="utf-8")
    print(f"Linked feature under '## Bundle: {bundle}' in {bundle_path}")


def _ensure_bundle_and_link_split(roadmap_path: Path, bundle: str, feature_name: str, feature_dir_name: str) -> None:
    module_dir = roadmap_path.parent
    bundles = rebuild_index.parse_bundles_table(roadmap_path)
    bundle_file = next((f for name, f in bundles if name == bundle), None)
    link_line = f"- [{feature_name}](./{feature_dir_name}/)\n"

    if bundle_file is not None:
        bundle_path = module_dir / bundle_file
        if not bundle_path.exists():
            raise SystemExit(
                f"Error: {roadmap_path}'s Bundles table lists '{bundle}' pointing at "
                f"{bundle_path}, but that file doesn't exist. Run rebuild_index.py to "
                f"sync the table first, then retry."
            )
        _append_link_to_bundle_file(bundle_path, bundle, link_line)
        return

    slug = slugify(bundle)
    if not slug:
        raise SystemExit(
            f"Error: bundle '{bundle}' slugifies to an empty string -- rename it "
            f"to include at least one letter or digit before filing a feature into it."
        )
    bundle_path = module_dir / f"roadmap-{slug}.md"

    if bundle_path.exists():
        existing_name = None
        for line in bundle_path.read_text(encoding="utf-8").splitlines():
            m = BUNDLE_HEADING_RE.match(line.strip())
            if m:
                existing_name = m.group("name").strip()
                break
        if existing_name == bundle:
            # The file already belongs to this exact bundle -- the Bundles table
            # just hasn't caught up yet (e.g. filed twice before a rebuild).
            _append_link_to_bundle_file(bundle_path, bundle, link_line)
            return
        if existing_name is not None:
            raise SystemExit(
                f"Error: {bundle_path} already exists for bundle '{existing_name}', but "
                f"'{bundle}' slugifies to the same file name -- rename one of the two "
                f"bundles so they don't collide."
            )
        raise SystemExit(
            f"Error: {bundle_path} already exists but isn't listed in {roadmap_path}'s "
            f"Bundles table. Run rebuild_index.py to sync the table first, then retry."
        )

    bundle_path.write_text(f"## Bundle: {bundle}\n\n{link_line}", encoding="utf-8")
    print(f"Created new bundle file: {bundle_path} (run rebuild_index.py to add it to the Bundles table)")


def scaffold_feature(specs_root: Path, template_root: Path, module: str, bundle: str, feature_name: str, depends_on: str) -> str:
    date_str = datetime.date.today().isoformat()
    slug = slugify(feature_name)
    feature_dir_name = f"{date_str}-{slug}"
    feature_dir = specs_root / module / feature_dir_name

    if feature_dir.exists():
        raise SystemExit(f"Error: {feature_dir} already exists. Refusing to overwrite.")

    feature_dir.mkdir(parents=True)
    for filename in TEMPLATE_FILES:
        content = (template_root / filename).read_text(encoding="utf-8")
        if filename == "spec.md":
            content = content.replace("<Feature Name>", feature_name)
            content = content.replace("**Module:** <module-slug>", f"**Module:** {module}")
            content = content.replace("**Bundle:** <bundle-name>", f"**Bundle:** {bundle}")
            content = content.replace("**Dependencies:** None", f"**Dependencies:** {depends_on}")
        else:
            content = content.replace("<Feature Name>", feature_name)
        (feature_dir / filename).write_text(content, encoding="utf-8")
    print(f"Scaffolded feature: {feature_dir}")
    return feature_dir_name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True)
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--depends-on", default="None", help='Comma-separated feature titles this feature depends on, or omit for "None"')
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    specs_root = repo_root / "specs"
    template_root = specs_root / "_template"

    if not template_root.is_dir():
        raise SystemExit(f"Error: template directory not found at {template_root}")

    roadmap_path = ensure_module(specs_root, template_root, args.module)
    feature_dir_name = scaffold_feature(specs_root, template_root, args.module, args.bundle, args.feature, args.depends_on)
    ensure_bundle_and_link(roadmap_path, args.bundle, args.feature, feature_dir_name)

    if args.rebuild_index:
        rebuild_index.rebuild(repo_root)


if __name__ == "__main__":
    main()
