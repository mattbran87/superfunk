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
        sys.path.insert(0, str(Path(__file__).parent))
        import rebuild_index
        rebuild_index.rebuild(repo_root)


if __name__ == "__main__":
    main()
