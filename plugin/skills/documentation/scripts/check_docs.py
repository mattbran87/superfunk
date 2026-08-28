#!/usr/bin/env python3
"""Deterministic check: does a shipped user-facing spec need a README/CHANGELOG update?"""
import re
import subprocess
import sys


def read_user_facing(spec_text):
    match = re.search(r'\*\*User-Facing:\*\*\s*(Yes|No)', spec_text)
    if not match:
        return None
    return match.group(1)


def extract_section(spec_text, heading):
    pattern = r'^## ' + re.escape(heading) + r'\n(.*?)(?=^## |\Z)'
    match = re.search(pattern, spec_text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def changed_files(base_sha, head_sha):
    result = subprocess.run(
        ["git", "diff", "--name-only", base_sha, head_sha],
        capture_output=True, text=True, check=True
    )
    return result.stdout.splitlines()


def main():
    if len(sys.argv) != 4:
        print("Usage: check_docs.py <spec_file> <base_sha> <head_sha>")
        sys.exit(2)

    spec_file, base_sha, head_sha = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(spec_file, "r", encoding="utf-8") as f:
        spec_text = f.read()

    user_facing = read_user_facing(spec_text)
    if user_facing != "Yes":
        print("NOT_APPLICABLE: User-Facing field is {!r}, not 'Yes'".format(user_facing))
        sys.exit(0)

    files = changed_files(base_sha, head_sha)
    doc_files = [f for f in files if f in ("README.md", "CHANGELOG.md")]
    if doc_files:
        print("ALREADY_UPDATED: {}".format(", ".join(doc_files)))
        sys.exit(0)

    context = extract_section(spec_text, "Context")
    decision = extract_section(spec_text, "Decision")
    consequences = extract_section(spec_text, "Consequences")

    print("ACTION_NEEDED")
    print("## Context")
    print(context)
    print("## Decision")
    print(decision)
    print("## Consequences")
    print(consequences)
    sys.exit(1)


if __name__ == "__main__":
    main()
