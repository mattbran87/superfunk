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
