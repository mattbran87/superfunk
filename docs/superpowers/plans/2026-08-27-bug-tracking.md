# Bug Tracking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `bug-tracking` skill and wire its Finish-time auto-ledger into `subagent-driven-development`, per `docs/superpowers/specs/2026-08-27-bug-tracking-design.md`.

**Architecture:** One new skill (`plugin/skills/bug-tracking/SKILL.md`) owns the schema, numbering, and file-creation process for both callers: on-demand reporting (Step 1) and Finish-time auto-ledgering of real-and-deferred parked findings (Step 2, invoked by `subagent-driven-development`).

**Tech Stack:** Markdown skill files, no code, no test framework. Verification uses two direct read-throughs plus two disposable `--plugin-dir` trials.

---

## File Structure

- **Create:** `plugin/skills/bug-tracking/SKILL.md` — the new skill: schema, numbering, and the two-step process.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds the Finish-time ledger-scan step, inserted between the concept-index paragraph and the workspace-deletion step.

No other file in `plugin/skills/subagent-driven-development/` mentions the ledger's `parked` line format or its deletion at Finish — confirmed by grep — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: the bug file's schema uses markdown prose, not a code data structure — no type to model.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Create the bug-tracking skill

**Files:**
- Create: `plugin/skills/bug-tracking/SKILL.md`

- [ ] **Step 1: Write the skill file**

```markdown
---
name: bug-tracking
description: Use when reporting a bug found in a project, or when subagent-driven-development's Finish step needs to durably record a real-and-deferred parked finding before deleting its workspace ledger. Maintains docs/bugs/, a platform-agnostic bug tracker — one file per bug plus a tracker.md index — ready to connect to an external tracker later without committing to one now.
---

# Bug Tracking

## Overview

Maintains `docs/bugs/` in the invoking project's own repository: one markdown file per bug (`docs/bugs/BUG-<NNNN>-<slug>.md`) plus an index table (`docs/bugs/tracker.md`) for at-a-glance triage. Every project adopting superfunk gets this same mechanism, operating on its own repo — the same pattern `writing-plans` and `brainstorming` already use.

Two entry points exist: reporting a bug directly (Step 1, for any defect found any time) and `subagent-driven-development`'s Finish step invoking Step 2 to durably record a real-and-deferred parked finding before deleting the workspace ledger that currently holds it (see that skill's Finish section, not this one, for the trigger logic).

## Schema

Every bug file uses this exact structure:

```markdown
# BUG-<NNNN>: <short title>

**Severity:** Critical | Important | Minor
**Status:** Open | Triaged | In Progress | Fixed | Won't Fix
**Origin:** <how it surfaced>
**External ID:** (blank until synced to an external tracker)

## Description

## Reproduction
(if applicable)

## Resolution
(filled in when Status becomes Fixed or Won't Fix — what changed, commit SHA)
```

`Severity` reuses this project's own Critical/Important/Minor vocabulary, already used throughout code review and process review — one severity language across the framework, not a second one invented for bugs specifically.

`External ID` stays blank and unused until a project connects its own external tracker (Jira, GitHub Issues, Linear, or otherwise) — this skill never populates it and never syncs to any external system. Its presence keeps the schema platform-agnostic: whatever key an external system assigns fits this one field without a schema change.

## Numbering

The next ID counts existing `docs/bugs/BUG-*.md` files and adds 1, zero-padded to 4 digits (`0001`, `0002`, ...). This stays deterministic and git-checkable — no separate counter file to drift out of sync with the files it counts.

## Process

### Step 1: Report a bug directly

Invoked by a human or a session reporting a defect found any time — post-ship, mid-development, wherever.

1. If `docs/bugs/` doesn't exist yet, create it along with `docs/bugs/tracker.md` using this header:

```markdown
# Bug Tracker

| ID | Title | Severity | Status | Link |
|---|---|---|---|---|
```

2. Determine the next ID per Numbering, above.
3. Ask (or infer from context) the bug's title, severity, and description. Write `docs/bugs/BUG-<NNNN>-<slug>.md` using the Schema above, with `Origin` reading `Reported <YYYY-MM-DD> by <name or session>`.
4. Append one row to `docs/bugs/tracker.md` naming the new bug.
5. Commit both files together: `git commit -m "docs(bugs): add BUG-<NNNN> - <short title>"`.

### Step 2: Auto-ledger a deferred finding

Triggered by `subagent-driven-development`'s Finish step — never run this step standalone; it needs a specific plan's ledger and a specific parked finding as input, not a fresh report. Given one `parked` ledger line whose ruling calls the finding real:

1. If `docs/bugs/` doesn't exist yet, create it the same way Step 1 does.
2. Determine the next ID per Numbering, above.
3. Write `docs/bugs/BUG-<NNNN>-<slug>.md` using the Schema above. `Origin` reads `Deferred finding, <ledger line> (plan: <plan-slug>)`. Derive `<slug>` from the finding's own one-line text — short, kebab-case, descriptive.
4. Append one row to `docs/bugs/tracker.md`.
5. Commit both files together, in their own commit separate from Finish's other bookkeeping commits: `git commit -m "docs(bugs): add BUG-<NNNN> - <short title>"`.

Repeat for each real-and-deferred parked line the ledger holds — a plan can defer more than one finding.

## Updating a Bug's Status

Edit the bug's file in place — change `Status`, and when it becomes `Fixed` or `Won't Fix`, fill in `Resolution` with what changed and the commit SHA. Update the matching `tracker.md` row's Status column in the same commit. A bug file holds a mutable record, not an append-only log — its git history, not its own text, shows how it changed over time.
```

- [ ] **Step 2: Verify the new file exists and reads correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
test -f plugin/skills/bug-tracking/SKILL.md && echo "EXISTS"
grep -c "^name: bug-tracking" plugin/skills/bug-tracking/SKILL.md
grep -c "### Step 2: Auto-ledger a deferred finding" plugin/skills/bug-tracking/SKILL.md
```

Expected: `EXISTS`, then one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/bug-tracking/SKILL.md
git commit -m "feat(skills): add the bug-tracking skill

Closes three gaps named in the brainstorm: deferred findings
disappearing with the deleted workspace ledger, no post-ship bug
reporting process, and no severity/priority triage mechanism.
Platform-agnostic foundation (an unused External ID field maps to
whatever external tracker a project later connects) with no sync
mechanism built yet.

Part of docs/superpowers/specs/2026-08-27-bug-tracking-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Wire the Finish-time auto-ledger into subagent-driven-development

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the ledger-scan step**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
If `docs/architecture/concept-index.md` exists, check this plan's own
File Structure section for whether it created, renamed, moved, or
deleted a `plugin/skills/<name>/`, a `specs/<module>/<feature>/`, or a
directory crossing `docs/ai-code-guidelines.md`'s significant-directory
threshold. If so, use superpowers:concept-index's Step 3 to add,
update, or remove that row, and commit the index change in its own
small commit. If the index file doesn't exist yet, or no File
Structure entry crosses one of those three boundaries, skip this step
— do not run a full rebuild here, and do not treat a missing index as
something this step must create. This keeps the index accurate the
same moment the rest of Finish's bookkeeping happens, rather than
letting it drift until someone notices.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

Replace with:
```
If `docs/architecture/concept-index.md` exists, check this plan's own
File Structure section for whether it created, renamed, moved, or
deleted a `plugin/skills/<name>/`, a `specs/<module>/<feature>/`, or a
directory crossing `docs/ai-code-guidelines.md`'s significant-directory
threshold. If so, use superpowers:concept-index's Step 3 to add,
update, or remove that row, and commit the index change in its own
small commit. If the index file doesn't exist yet, or no File
Structure entry crosses one of those three boundaries, skip this step
— do not run a full rebuild here, and do not treat a missing index as
something this step must create. This keeps the index accurate the
same moment the rest of Finish's bookkeeping happens, rather than
letting it drift until someone notices.

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

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "invoke superpowers:bug-tracking" plugin/skills/subagent-driven-development/SKILL.md
grep -n "No real-and-deferred parked findings: skip this step" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): wire bug-tracking into Finish's workspace-deletion step

The ledger's parked lines held the only record of a real-and-deferred
finding, and Finish deletes the workspace holding them — git history
never actually recorded these, only the commit SHAs the ledger
referenced. Inserted immediately before the deletion step so nothing
gets lost.

Part of docs/superpowers/specs/2026-08-27-bug-tracking-design.md."
```

Stage only this one file.

---

## Task 3: Live trial for on-demand bug reporting

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with no docs/bugs/ directory yet**

```bash
mkdir -p /c/sf-bug-tracking-report-test
cd /c/sf-bug-tracking-report-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Fixture Project" > README.md
git add -A
git commit -q -m "initial scratch fixture: empty project, no docs/bugs/ yet"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial invoking bug-tracking directly**

```bash
cd /c/sf-bug-tracking-report-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-bug-tracking-report-test with no docs/bugs/ directory yet. Use the Skill tool to invoke bug-tracking, Step 1 (report a bug directly). Report this bug: title 'Login form accepts empty password', severity Important, description 'Submitting the login form with an empty password field logs the user in anyway, bypassing authentication entirely.', origin 'Reported 2026-08-27 by QA'. Create and commit the files exactly as the skill instructs. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: the exact bug ID assigned and the full path of the file you created. SECTION 2/2: the exact content of docs/bugs/tracker.md after your edit, and the commit SHA." > /c/sf-bug-tracking-report-test/trial.txt 2>&1
cat /c/sf-bug-tracking-report-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-bug-tracking-report-test/trial.txt`. Confirm SECTION 1/2 reports `BUG-0001` and a file path matching `docs/bugs/BUG-0001-<slug>.md`. Confirm SECTION 2/2 shows a `tracker.md` row for the new bug.

Then independently verify against the actual fixture files (don't just trust the trial's report):

```bash
cat /c/sf-bug-tracking-report-test/docs/bugs/tracker.md
ls /c/sf-bug-tracking-report-test/docs/bugs/
cat /c/sf-bug-tracking-report-test/docs/bugs/BUG-0001-*.md
cd /c/sf-bug-tracking-report-test && git log --oneline
```

Confirm the bug file matches the Schema exactly (Severity: Important, Status: Open, Origin naming "Reported 2026-08-27 by QA", the Description text), the tracker row matches, and exactly one new commit landed beyond the fixture's initial commit.

If any of this doesn't match, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture files both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-bug-tracking-report-test
```

No commit for this task.

---

## Task 4: Live trial for the Finish-time auto-ledger

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with one existing bug and a fixture plan whose ledger has one real-and-deferred parked finding**

```bash
mkdir -p /c/sf-bug-tracking-finish-test/docs/bugs
mkdir -p /c/sf-bug-tracking-finish-test/docs/superpowers/plans
mkdir -p "/c/sf-bug-tracking-finish-test/.superpowers/sdd/fixture-finish-bugtest"
cd /c/sf-bug-tracking-finish-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/bugs/tracker.md <<'EOF'
# Bug Tracker

| ID | Title | Severity | Status | Link |
|---|---|---|---|---|
| BUG-0001 | Existing seeded bug | Minor | Open | BUG-0001-existing-seeded-bug.md |
EOF

cat > docs/bugs/BUG-0001-existing-seeded-bug.md <<'EOF'
# BUG-0001: Existing seeded bug

**Severity:** Minor
**Status:** Open
**Origin:** Reported 2026-08-20 by fixture setup
**External ID:** (blank until synced to an external tracker)

## Description

A pre-existing bug seeded into the fixture, to confirm numbering
doesn't collide with it.
EOF

cat > docs/superpowers/plans/2026-08-27-fixture-finish-bugtest.md <<'EOF'
# Fixture Finish Bugtest Implementation Plan

**Goal:** A trivial plan used only to exercise the Finish-time bug-tracking auto-ledger in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: A trivial task

Nothing real to implement; this plan exists only to carry a ledger with a parked finding through Finish.
EOF

cat > ".superpowers/sdd/fixture-finish-bugtest/progress.md" <<'EOF'
# SDD ledger — plan: docs/superpowers/plans/2026-08-27-fixture-finish-bugtest.md

Task 1: parked — Error messages use inconsistent capitalization across the login and signup forms — ruling: real and deferred, cosmetic-only, not load-bearing for this plan
Task 1: complete (commits a1b2c3d..e4f5a6b, 1 parked)
EOF

git add -A
git commit -q -m "initial scratch fixture: one existing bug, fixture plan, ledger with one real-and-deferred parked finding"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the Finish-time ledger scan**

```bash
cd /c/sf-bug-tracking-finish-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-bug-tracking-finish-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current Finish section loaded. The plan docs/superpowers/plans/2026-08-27-fixture-finish-bugtest.md has completed its final whole-branch review clean, and you are now running the Finish step. Its ledger lives at .superpowers/sdd/fixture-finish-bugtest/progress.md -- read it. Follow Finish's instructions exactly, including the new ledger-scan step before workspace deletion, invoking superpowers:bug-tracking's Step 2 as instructed for any real-and-deferred parked finding you find. Do not actually delete the workspace directory -- stop right after the bug-tracking step and report before proceeding further. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: which ledger line you identified as real-and-deferred, and the bug ID you assigned it. SECTION 2/2: the exact content of the new bug file you created, and confirm it does not collide with the existing BUG-0001." > /c/sf-bug-tracking-finish-test/trial.txt 2>&1
cat /c/sf-bug-tracking-finish-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-bug-tracking-finish-test/trial.txt`. Confirm SECTION 1/2 identifies the capitalization-inconsistency parked line and assigns it `BUG-0002` (not colliding with the existing `BUG-0001`). Confirm SECTION 2/2 shows a bug file whose `Origin` names the ledger finding and `plan: fixture-finish-bugtest`.

Then independently verify against the actual fixture files (don't just trust the trial's report):

```bash
ls /c/sf-bug-tracking-finish-test/docs/bugs/
cat /c/sf-bug-tracking-finish-test/docs/bugs/BUG-0002-*.md
cat /c/sf-bug-tracking-finish-test/docs/bugs/tracker.md
test -d "/c/sf-bug-tracking-finish-test/.superpowers/sdd/fixture-finish-bugtest" && echo "WORKSPACE STILL PRESENT (correct, deletion was skipped)"
```

Confirm `BUG-0002` exists with the correct `Origin`, the tracker now lists both `BUG-0001` and `BUG-0002`, and the workspace directory still exists (since the dispatch prompt told the trial to stop before deletion).

If the trial assigned a colliding ID, skipped the bug entirely, or the fixture files don't show the expected content, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture files both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-bug-tracking-finish-test
```

No commit for this task.
