# Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `documentation` skill, its deterministic `check_docs.py` CLI tool, and wire both into `brainstorming` and `subagent-driven-development`, per `docs/superpowers/specs/2026-08-28-documentation-design.md`.

**Architecture:** A Python CLI tool (`check_docs.py`) does deterministic detection and spec-content extraction only. A new `documentation` skill owns the two entry points (bootstrap, Finish-time drafting) and does the creative drafting. `brainstorming` gains a required `User-Facing` spec field. `subagent-driven-development`'s Finish step and Example Workflow both get updated to include the new check.

**Tech Stack:** Python 3 (standard library only — `re`, `subprocess`, `sys` — no third-party dependencies) with `pytest` for the CLI tool's unit tests. Markdown skill files cover everything else. This marks the first real code (not just markdown instructions) this framework ships.

## Global Constraints

- Python 3, standard library only for `check_docs.py` itself (`re`, `subprocess`, `sys`) — no third-party runtime dependency. `pytest` stays a test-only dependency, never imported by the shipped tool.
- No LLM call, no credentials, no network access from `check_docs.py` — strictly deterministic (per the design spec's Decision: "extraction, diffing, reporting only").
- No Claude-Code-specific mechanism (hooks, etc.) — every check runs as a script a skill's own prose instructs the agent to invoke, portable across any harness that can run a shell command.

---

## File Structure

- **Create:** `plugin/skills/documentation/scripts/check_docs.py` — the deterministic CLI tool.
- **Create:** `plugin/skills/documentation/scripts/test_check_docs.py` — its unit tests.
- **Create:** `plugin/skills/documentation/SKILL.md` — the new skill: bootstrap (Step 1) and Finish-time drafting (Step 2).
- **Modify:** `plugin/skills/brainstorming/SKILL.md` — adds the required `User-Facing` field.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds the Finish-time documentation check, and updates the Example Workflow's bracket-line sequence to include it (applying `writing-plans`' own Self-Review item 9 to this addition).

No other file in any of the three touched skills' directories mentions the `User-Facing` field, `check_docs.py`, or the Example Workflow's content — confirmed by grep — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: `check_docs.py` shells out to `git diff --name-only`, a trivial CLI invocation (two positional arguments, plain-text output) — not an API call with a signature substantial enough to warrant pseudocode.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern beyond the tool's own three pure functions, each covered by its own TDD cycle below.
- **T3 — DTO/schema shape:** Skipped: the tool's input (a spec file's markdown) and output (stdout banners) use plain text, not a structured data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Build check_docs.py with real unit tests (TDD)

**Files:**
- Create: `plugin/skills/documentation/scripts/check_docs.py`
- Test: `plugin/skills/documentation/scripts/test_check_docs.py`

- [ ] **Step 1: Write failing tests for the two pure parsing functions**

```bash
mkdir -p "plugin/skills/documentation/scripts"
```

Create `plugin/skills/documentation/scripts/test_check_docs.py`:

```python
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_docs import read_user_facing, extract_section, changed_files


def test_read_user_facing_yes():
    spec = "**Date:** 2026-08-28\n**User-Facing:** Yes\n"
    assert read_user_facing(spec) == "Yes"


def test_read_user_facing_no():
    spec = "**Date:** 2026-08-28\n**User-Facing:** No\n"
    assert read_user_facing(spec) == "No"


def test_read_user_facing_missing():
    spec = "**Date:** 2026-08-28\n**Status:** Approved\n"
    assert read_user_facing(spec) is None


def test_extract_section_finds_content():
    spec = "## Context\n\nSome context here.\n\n## Decision\n\nSome decision here.\n"
    assert extract_section(spec, "Context") == "Some context here."
    assert extract_section(spec, "Decision") == "Some decision here."


def test_extract_section_missing_returns_empty():
    spec = "## Context\n\nSome context here.\n"
    assert extract_section(spec, "Decision") == ""


def test_extract_section_last_section_to_end_of_file():
    spec = "## Context\n\nFirst.\n\n## Consequences\n\nLast section, no trailing header.\n"
    assert extract_section(spec, "Consequences") == "Last section, no trailing header."
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\documentation\scripts"
python -m pytest test_check_docs.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'check_docs'` (the module doesn't exist yet).

- [ ] **Step 3: Write minimal implementation for the two pure functions**

Create `plugin/skills/documentation/scripts/check_docs.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\documentation\scripts"
python -m pytest test_check_docs.py -v
```

Expected: PASS, 6/6.

- [ ] **Step 5: Write a failing test for changed_files against a real git fixture**

Append to `plugin/skills/documentation/scripts/test_check_docs.py`:

```python
def test_changed_files_detects_readme(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "file.txt").write_text("v1")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    base_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    (repo / "README.md").write_text("# Test")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add readme"], cwd=repo, check=True)
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    original_cwd = os.getcwd()
    os.chdir(repo)
    try:
        result = changed_files(base_sha, head_sha)
    finally:
        os.chdir(original_cwd)

    assert "README.md" in result
```

- [ ] **Step 6: Run the test to verify it fails for the right reason, then verify it passes**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\documentation\scripts"
python -m pytest test_check_docs.py::test_changed_files_detects_readme -v
```

Expected on a fresh checkout with `changed_files` already implemented (Step 3 already wrote it): PASS immediately. This step confirms the fixture itself works correctly — if it fails, the fixture setup has a bug, not `changed_files`.

- [ ] **Step 7: Write failing end-to-end tests exercising all three branches via subprocess**

Append to `plugin/skills/documentation/scripts/test_check_docs.py`:

```python
CHECK_DOCS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_docs.py")


def _init_repo(repo):
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)


def _commit_all(repo, message):
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=repo, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


def test_end_to_end_not_applicable(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text("**Date:** 2026-08-28\n**User-Facing:** No\n\n## Context\n\nInternal only.\n")
    base_sha = _commit_all(repo, "base")
    (repo / "other.py").write_text("x = 1")
    head_sha = _commit_all(repo, "change")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "NOT_APPLICABLE" in result.stdout


def test_end_to_end_already_updated(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text("**Date:** 2026-08-28\n**User-Facing:** Yes\n\n## Context\n\nSomething.\n")
    base_sha = _commit_all(repo, "base")
    (repo / "README.md").write_text("# Updated")
    head_sha = _commit_all(repo, "update readme")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "ALREADY_UPDATED: README.md" in result.stdout


def test_end_to_end_action_needed(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text(
        "**Date:** 2026-08-28\n**User-Facing:** Yes\n\n"
        "## Context\n\nUsers hit a bug.\n\n"
        "## Decision\n\nFix the bug this way.\n\n"
        "## Consequences\n\nUsers see correct behavior now.\n"
    )
    base_sha = _commit_all(repo, "base")
    (repo / "fix.py").write_text("x = 2")
    head_sha = _commit_all(repo, "fix")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "ACTION_NEEDED" in result.stdout
    assert "Users hit a bug." in result.stdout
    assert "Fix the bug this way." in result.stdout
    assert "Users see correct behavior now." in result.stdout
```

- [ ] **Step 8: Run all tests to verify everything passes**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\documentation\scripts"
python -m pytest test_check_docs.py -v
```

Expected: PASS, 9/9. Since `check_docs.py`'s implementation already exists from Step 3 and needed no changes for the new tests to pass, this step confirms the end-to-end behavior matches the unit-level behavior already verified — not a case of writing code to make a test pass, since the new tests needed no new code.

- [ ] **Step 9: Commit**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
git add plugin/skills/documentation/scripts/check_docs.py plugin/skills/documentation/scripts/test_check_docs.py
git commit -m "feat(skills): add check_docs.py, the documentation skill's deterministic CLI tool

Strictly deterministic -- extraction, diffing, reporting only. No LLM
call, no credentials. The first real code (not markdown instructions)
this framework ships, built via test-driven-development with 9 unit
and end-to-end tests covering all three branches.

Part of docs/superpowers/specs/2026-08-28-documentation-design.md."
```

Stage only these two files — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Write the documentation skill

**Files:**
- Create: `plugin/skills/documentation/SKILL.md`

- [ ] **Step 1: Write the skill file**

```markdown
---
name: documentation
description: Use when a project needs an initial README/CHANGELOG scaffold, or when subagent-driven-development's Finish step needs to draft a user-facing doc update from a shipped spec. Maintains a project's README.md and CHANGELOG.md, translating a design spec's own Context/Decision/Consequences into the external-facing content a user needs, rather than starting from a blank page.
---

# Documentation

## Overview

Maintains `README.md` and `CHANGELOG.md` in the invoking project's own repository. Every project adopting superfunk gets this same mechanism, operating on its own repo — the same pattern `bug-tracking` and `writing-plans` already use.

Two entry points exist: bootstrapping initial docs for a project with none (Step 1) and drafting a doc update from a shipped, user-facing design spec (Step 2, invoked by `subagent-driven-development`'s Finish step — see that skill's Finish section, not this one, for the trigger logic).

## Step 1: Bootstrap

Invoked by a human or a session for a project with no `README.md` or `CHANGELOG.md` yet.

1. Create `README.md` with a minimal scaffold: a title, a one-paragraph description (ask the user, or infer from the project's existing files), and empty `## Installation` and `## Usage` headings for the user to fill in.
2. Create `CHANGELOG.md` with a minimal scaffold:

```markdown
# Changelog

<!-- entries below this line, newest first -->
```

3. Commit both files together: `git commit -m "docs: scaffold initial README and CHANGELOG"`.

## Step 2: Finish-time drafting

Triggered by `subagent-driven-development`'s Finish step — never run this step standalone; it needs a specific spec file and commit range as input, not a fresh scaffold.

1. Run `python plugin/skills/documentation/scripts/check_docs.py <spec_file> <base_sha> <head_sha>`.
2. If the output starts with `NOT_APPLICABLE` or `ALREADY_UPDATED`: nothing to do, skip the rest of this step.
3. If the output starts with `ACTION_NEEDED`: read the Context/Decision/Consequences content the script printed. Draft:
   - A `CHANGELOG.md` entry, newest-first, in plain language describing what changed and why a user would care — not the internal implementation detail, the user-facing effect.
   - A `README.md` update, only if the change affects something the README already documents (a new feature the Usage section should mention, a changed installation step). Skip the README if the change doesn't affect anything already documented there.
4. Commit both files together, in their own commit separate from Finish's other bookkeeping commits: `git commit -m "docs: update README/CHANGELOG for <short description>"`.

## When check_docs.py Reports ACTION_NEEDED But the Spec Stays Genuinely Unclear

If the spec's Context/Decision/Consequences don't give enough to draft honest user-facing content (e.g., a Consequences section that only discusses internal trade-offs), don't invent user-facing language that isn't grounded in the spec. Report DONE_WITH_CONCERNS instead of fabricating content.
```

- [ ] **Step 2: Verify the new file exists and reads correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
test -f plugin/skills/documentation/SKILL.md && echo "EXISTS"
grep -c "^name: documentation" plugin/skills/documentation/SKILL.md
grep -c "## Step 2: Finish-time drafting" plugin/skills/documentation/SKILL.md
```

Expected: `EXISTS`, then one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/documentation/SKILL.md
git commit -m "feat(skills): add the documentation skill

Closes the three gaps named in the brainstorm: docs drifting from
what shipped, no initial scaffold, and no translation from internal
spec content to external doc content. Step 2 explicitly refuses to
fabricate user-facing content when the spec doesn't ground it.

Part of docs/superpowers/specs/2026-08-28-documentation-design.md."
```

Stage only this one file.

---

## Task 3: Add the User-Facing field requirement to brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Insert the new field requirement**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
- Give it a `Status` line: `Proposed`, `Approved` (not yet implemented), or `Superseded by <filename>`. Never a free-text description — `subagent-driven-development`'s Finish step is what advances `Approved` to `Shipped` once the work actually ships.
- Include a `Consequences` section after Decision (and after Falsifiable Criteria or Testing, if either applies): what becomes easier or harder because of this decision, what assumptions must hold.
```

Replace with:
```
- Give it a `Status` line: `Proposed`, `Approved` (not yet implemented), or `Superseded by <filename>`. Never a free-text description — `subagent-driven-development`'s Finish step is what advances `Approved` to `Shipped` once the work actually ships.
- Give it a `User-Facing:` field: `Yes` or `No` — decided during
  brainstorming, not inferred later. `Yes` means a project's README
  or CHANGELOG needs updating once this ships;
  superpowers:documentation's Finish-time check reads this field to
  decide whether to fire.
- Include a `Consequences` section after Decision (and after Falsifiable Criteria or Testing, if either applies): what becomes easier or harder because of this decision, what assumptions must hold.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Give it a \`User-Facing:\` field" plugin/skills/brainstorming/SKILL.md
grep -c "superpowers:documentation's Finish-time check reads this field" plugin/skills/brainstorming/SKILL.md
```

Expected: one match, one count.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): require a User-Facing field on every design spec

Decided explicitly during brainstorming rather than inferred at
Finish time -- matches this session's own repeated lesson that a
gate needs a git-checkable precondition, not a last-second judgment
call. subagent-driven-development's new Finish-time documentation
check reads this field.

Part of docs/superpowers/specs/2026-08-28-documentation-design.md."
```

Stage only this one file.

---

## Task 4: Wire the Finish-time check into subagent-driven-development

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the documentation check into Finish, alongside the bug-tracking step**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
Before deleting the workspace below, check this plan's ledger
(`<workspace>/progress.md`) for any `parked` line whose ruling calls
the finding real rather than contestable — a "reviewer is wrong"
ruling needs no bug; it already resolved as correctly not one. For
each real-and-deferred parked finding, invoke superpowers:bug-tracking's
Step 2 to record it durably in `docs/bugs/` before its only record —
the ledger text itself — disappears with the workspace below. No
real-and-deferred parked findings: skip this step.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

Replace with:
```
Before deleting the workspace below, check this plan's ledger
(`<workspace>/progress.md`) for any `parked` line whose ruling calls
the finding real rather than contestable — a "reviewer is wrong"
ruling needs no bug; it already resolved as correctly not one. For
each real-and-deferred parked finding, invoke superpowers:bug-tracking's
Step 2 to record it durably in `docs/bugs/` before its only record —
the ledger text itself — disappears with the workspace below. No
real-and-deferred parked findings: skip this step.

If this plan traces to a design spec (per the Status-flip check
above), run `python plugin/skills/documentation/scripts/check_docs.py
<spec-file> <merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or
`ALREADY_UPDATED`: skip the rest of this step. `ACTION_NEEDED`:
invoke superpowers:documentation's Step 2 to draft the README/CHANGELOG
update from the printed spec content. No design spec: skip this step
entirely — nothing to read a `User-Facing` field from.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

- [ ] **Step 2: Update the Example Workflow's bracket-line sequence to include the new check**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
[Finish: no real-and-deferred parked findings -- bug-tracking step skipped]

[Delete this plan's workspace — the record now lives in git]
```

Replace with:
```
[Finish: no real-and-deferred parked findings -- bug-tracking step skipped]
[Finish: this plan's spec has no User-Facing field set to Yes -- documentation step skipped]

[Delete this plan's workspace — the record now lives in git]
```

- [ ] **Step 3: Verify both edits landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "invoke superpowers:documentation's Step 2" plugin/skills/subagent-driven-development/SKILL.md
grep -n "documentation step skipped" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): wire the documentation check into Finish

Positioned alongside the existing bug-tracking ledger scan, both
running as pre-workspace-deletion checks. Also updates the Example
Workflow's bracket-line sequence to include it -- applying
writing-plans' own Self-Review item 9 to this very addition, on the
first Finish addition after item 9 shipped.

Part of docs/superpowers/specs/2026-08-28-documentation-design.md."
```

Stage only this one file.

---

## Task 5: Live trial for the ACTION_NEEDED path

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a user-facing spec whose commit range never touched README/CHANGELOG**

```bash
mkdir -p /c/sf-documentation-actionneeded-test/docs/superpowers/specs
mkdir -p /c/sf-documentation-actionneeded-test/docs/superpowers/plans
cd /c/sf-documentation-actionneeded-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/specs/2026-08-28-fixture-login-timeout-design.md <<'EOF'
# Fixture Login Timeout — Design

**Date:** 2026-08-28
**Status:** Approved
**User-Facing:** Yes

## Context

Users reported getting logged out after only 5 minutes of inactivity, far shorter than expected, causing frequent re-logins during normal use.

## Decision

The session timeout increases from 5 minutes to 30 minutes of inactivity.

## Consequences

Users stay logged in through normal working sessions without needing to re-authenticate every few minutes.
EOF

cat > docs/superpowers/plans/2026-08-28-fixture-login-timeout.md <<'EOF'
# Fixture Login Timeout Implementation Plan

**Goal:** A trivial plan used only to exercise the documentation skill's Finish-time drafting in a disposable trial. Part of docs/superpowers/specs/2026-08-28-fixture-login-timeout-design.md.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Change the timeout constant

Change SESSION_TIMEOUT_MINUTES from 5 to 30 in config.py.
EOF

cat > README.md <<'EOF'
# Fixture App

A fixture application for testing.

## Usage

Log in with your credentials.
EOF

cat > CHANGELOG.md <<'EOF'
# Changelog

<!-- entries below this line, newest first -->
EOF

git add -A
git commit -q -m "initial scratch fixture: spec, plan, README, CHANGELOG (this is the review base)"
base_sha=$(git rev-parse HEAD)
echo "BASE_SHA=$base_sha" > /c/sf-documentation-actionneeded-test/.fixture-shas

cat > config.py <<'EOF'
SESSION_TIMEOUT_MINUTES = 30
EOF

git add -A
git commit -q -m "fix: increase session timeout to 30 minutes (fixture fix commit)"
head_sha=$(git rev-parse HEAD)
echo "HEAD_SHA=$head_sha" >> /c/sf-documentation-actionneeded-test/.fixture-shas

echo "FIXTURE READY"
cat /c/sf-documentation-actionneeded-test/.fixture-shas
```

- [ ] **Step 2: Run an isolated trial exercising the Finish-time documentation check**

```bash
cd /c/sf-documentation-actionneeded-test
source .fixture-shas
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-documentation-actionneeded-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current Finish section loaded. The plan docs/superpowers/plans/2026-08-28-fixture-login-timeout.md has completed its final whole-branch review clean, and you are now running the Finish step's documentation check specifically. The spec is docs/superpowers/specs/2026-08-28-fixture-login-timeout-design.md, the merge-base commit is $BASE_SHA, and the head commit is $HEAD_SHA. Run the check_docs.py invocation exactly as Finish instructs, and follow through on whatever it reports, including invoking superpowers:documentation's Step 2 if it reports ACTION_NEEDED. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: the exact check_docs.py output. SECTION 2/2: what you did as a result, including the exact content you wrote to README.md and/or CHANGELOG.md and the commit SHA." > trial.txt 2>&1
cat trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-documentation-actionneeded-test/trial.txt`. Confirm SECTION 1/2 shows `ACTION_NEEDED` with the Context/Decision/Consequences content. Confirm SECTION 2/2 describes a real CHANGELOG.md entry (and, if it judged the README's Usage section relevant, a README update) written in user-facing language about the timeout change, not internal implementation detail like "SESSION_TIMEOUT_MINUTES."

Then independently verify against the actual fixture files (don't just trust the trial's report):

```bash
cat /c/sf-documentation-actionneeded-test/CHANGELOG.md
cat /c/sf-documentation-actionneeded-test/README.md
cd /c/sf-documentation-actionneeded-test && git log --oneline
```

Confirm `CHANGELOG.md` has a real new entry, the entry describes the user-facing effect (staying logged in longer) rather than the variable name that changed, and a new commit landed separate from the fixture's own commits.

If the trial reports anything other than `ACTION_NEEDED`, fabricates content not grounded in the spec, or the fixture files don't show the expected update, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture files both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-documentation-actionneeded-test
```

No commit for this task.

---

## Task 6: Live trial for the NOT_APPLICABLE path

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build the same fixture shape with a non-user-facing spec**

```bash
mkdir -p /c/sf-documentation-notapplicable-test/docs/superpowers/specs
mkdir -p /c/sf-documentation-notapplicable-test/docs/superpowers/plans
cd /c/sf-documentation-notapplicable-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/specs/2026-08-28-fixture-internal-refactor-design.md <<'EOF'
# Fixture Internal Refactor — Design

**Date:** 2026-08-28
**Status:** Approved
**User-Facing:** No

## Context

The internal config-loading module has grown tangled, making it hard to maintain.

## Decision

Split config-loading into two smaller internal modules, no behavior change.

## Consequences

Future internal changes to config loading are easier to make. No user-visible effect.
EOF

cat > docs/superpowers/plans/2026-08-28-fixture-internal-refactor.md <<'EOF'
# Fixture Internal Refactor Implementation Plan

**Goal:** A trivial plan used only to exercise the documentation skill's NOT_APPLICABLE path in a disposable trial. Part of docs/superpowers/specs/2026-08-28-fixture-internal-refactor-design.md.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Split the module

Split config.py into config_loader.py and config_validator.py, no behavior change.
EOF

cat > README.md <<'EOF'
# Fixture App

A fixture application for testing.
EOF

git add -A
git commit -q -m "initial scratch fixture: spec, plan, README (this is the review base)"
base_sha=$(git rev-parse HEAD)
echo "BASE_SHA=$base_sha" > /c/sf-documentation-notapplicable-test/.fixture-shas

cat > config_loader.py <<'EOF'
# split from config.py
EOF
cat > config_validator.py <<'EOF'
# split from config.py
EOF

git add -A
git commit -q -m "refactor: split config.py into loader and validator (fixture fix commit)"
head_sha=$(git rev-parse HEAD)
echo "HEAD_SHA=$head_sha" >> /c/sf-documentation-notapplicable-test/.fixture-shas

echo "FIXTURE READY"
cat /c/sf-documentation-notapplicable-test/.fixture-shas
```

- [ ] **Step 2: Run an isolated trial exercising the Finish-time documentation check against the non-user-facing spec**

```bash
cd /c/sf-documentation-notapplicable-test
source .fixture-shas
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-documentation-notapplicable-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current Finish section loaded. The plan docs/superpowers/plans/2026-08-28-fixture-internal-refactor.md has completed its final whole-branch review clean, and you are now running the Finish step's documentation check specifically. The spec is docs/superpowers/specs/2026-08-28-fixture-internal-refactor-design.md, the merge-base commit is $BASE_SHA, and the head commit is $HEAD_SHA. Run the check_docs.py invocation exactly as Finish instructs, and follow through on whatever it reports. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: the exact check_docs.py output. SECTION 2/2: what you did as a result -- if it reported NOT_APPLICABLE, confirm you made no edit." > trial.txt 2>&1
cat trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-documentation-notapplicable-test/trial.txt`. Confirm SECTION 1/2 shows `NOT_APPLICABLE`. Confirm SECTION 2/2 reports making no edit.

Then independently verify against the actual fixture files:

```bash
cat /c/sf-documentation-notapplicable-test/README.md
cd /c/sf-documentation-notapplicable-test && git log --oneline
```

Confirm `README.md` remains unchanged from the fixture's own commit, and no new commit landed beyond the fixture's two setup commits.

If the trial reports anything other than `NOT_APPLICABLE`, or an edit landed anyway, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture files both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-documentation-notapplicable-test
```

No commit for this task.
