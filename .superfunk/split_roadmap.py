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


def _validate_only_recognized_content(roadmap_path: Path) -> None:
    in_status_block = False
    for line in roadmap_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == rebuild_index.STATUS_START:
            in_status_block = True
            continue
        if stripped == rebuild_index.STATUS_END:
            in_status_block = False
            continue
        if in_status_block:
            continue
        if rebuild_index.H1_RE.match(stripped):
            continue
        if rebuild_index.BUNDLE_HEADING_RE.match(stripped):
            continue
        if rebuild_index.LINK_RE.match(stripped):
            continue
        raise SystemExit(
            f"Error: {roadmap_path} has content this script doesn't recognize "
            f"(\"{stripped}\") -- refusing to split, since rewriting the file would "
            f"silently discard it. Remove or relocate that content first, then retry."
        )


def split_module(repo_root: Path, specs_root: Path, module: str) -> None:
    roadmap_path = specs_root / module / "roadmap.md"
    if not roadmap_path.is_file():
        raise SystemExit(f"Error: no roadmap.md found for module '{module}' at {roadmap_path}")

    if rebuild_index.is_split(roadmap_path):
        print(f"Module '{module}' is already split. Nothing to do.")
        rebuild_index.rebuild(repo_root)
        return

    entries = rebuild_index.parse_roadmap_links(roadmap_path)
    if not entries:
        raise SystemExit(f"Error: no bundles/features found in {roadmap_path} -- nothing to split.")

    _validate_only_recognized_content(roadmap_path)

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
        if bundle is None:
            raise SystemExit(
                f"Error: {roadmap_path} has a feature link that appears before any "
                f"'## Bundle:' heading -- fix the file's structure before splitting."
            )
        slug = add_feature.slugify(bundle)
        if not slug:
            raise SystemExit(
                f"Error: bundle '{bundle}' slugifies to an empty string -- rename it "
                f"to include at least one letter or digit before splitting."
            )
        filename = f"roadmap-{slug}.md"
        if slug in slug_to_bundle:
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
