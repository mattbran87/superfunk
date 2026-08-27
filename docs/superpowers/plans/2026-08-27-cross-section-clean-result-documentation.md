# Cross-Section Clean-Result Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a clean-result documentation sentence to item 8, per `docs/superpowers/specs/2026-08-27-cross-section-clean-result-documentation-design.md`.

**Architecture:** One sentence appended to item 8's existing text — no new item, continuing the same check into its clean-result branch.

**Tech Stack:** Markdown skill file, no code, no test framework. Verification is a direct read-through plus one disposable `--plugin-dir` trial.

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — extends item 8.

No other file in `plugin/skills/writing-plans/` (`plan-document-reviewer-prompt.md`) mentions item 8 or cross-section mechanism consistency — confirmed by grep before writing this plan — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits a markdown skill file only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add the clean-result documentation sentence to item 8

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert the new sentence**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the target file lives in one, and the design spec,
if it also describes this mechanism — for every other mention of the
key terms involved, and read each hit. Confirm the edit doesn't leave
any of them contradicting the new content.
```

Replace with:
```
**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the target file lives in one, and the design spec,
if it also describes this mechanism — for every other mention of the
key terms involved, and read each hit. Confirm the edit doesn't leave
any of them contradicting the new content. If none of them
contradict, and this plan traces to a design spec, add one sentence
to that spec's Deferred or Consequences section explaining why the
checked file(s) needed no change.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "If none of them" plugin/skills/writing-plans/SKILL.md
grep -n "explaining why the" plugin/skills/writing-plans/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "docs(skills): document item 8's clean-result branch

The clean-result case (dog-fooding finds no contradiction) never
required documenting why, twice landing only reactively after a
final review asked for it. Fires only when item 8 both triggers
(rare) and finds nothing wrong (rarer still), keeping the added cost
low.

Part of docs/superpowers/specs/2026-08-27-cross-section-clean-result-documentation-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Live trial for the clean-result documentation sentence

**Files:** none (verification only; touches no repository files, except a real fixture spec file created and edited entirely within a disposable scratch repo)

- [ ] **Step 1: Build a scratch fixture with a target file, a consistent (non-contradicting) sibling, and a real fixture design spec to write into**

```bash
mkdir -p /c/sf-clean-result-test/plugin/skills/mock-skill
mkdir -p /c/sf-clean-result-test/docs/superpowers/specs
cd /c/sf-clean-result-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.
EOF

cat > plugin/skills/mock-skill/SKILL.md <<'EOF'
# Mock Skill

## Overview

This skill wraps routing.md's Apply Config step, which only runs
when triggered by the setup wizard -- it never runs standalone.
EOF

cat > docs/superpowers/specs/2026-08-27-fixture-cleanresult-design.md <<'EOF'
# Fixture Cleanresult — Design

**Date:** 2026-08-27
**Status:** Approved

## Context

Fixture spec for a disposable trial only.

## Decision

Reword plugin/skills/mock-skill/routing.md's Apply Config section for
clarity, no behavior change intended.

## Deferred

- Nothing yet.
EOF

git add -A
git commit -q -m "initial scratch fixture: mock-skill directory, fixture design spec"
echo "FIXTURE READY"
```

Note: the planned edit below restates Apply Config's meaning in different words without changing what it claims — SKILL.md's "only runs when triggered by the setup wizard... it never runs standalone" stays fully consistent with the reworded text. This is a genuine clean-result case: item 8 triggers (the edit still contains "triggered by" / "standalone" / lifecycle language) but finds no contradiction.

- [ ] **Step 2: Run an isolated trial exercising item 8's clean-result branch**

```bash
cd /c/sf-clean-result-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-clean-result-test. Use the Skill tool to invoke writing-plans. You are drafting a plan whose Goal line reads: 'Reword Apply Config for clarity. Part of docs/superpowers/specs/2026-08-27-fixture-cleanresult-design.md.' The plan has exactly one task: modify plugin/skills/mock-skill/routing.md's Apply Config section so it reads: 'Applies configuration to the target system. Runs only when triggered by the setup wizard, immediately after Step 2 completes; never runs as a standalone step.' Do not actually write the plan file to disk or make any edit to plugin/skills/mock-skill/routing.md -- this is a dry run of the Self-Review step only. However, if item 8's own instructions call for an edit to the fixture design spec file, make that edit for real. Run Self-Review item 8 (Cross-section mechanism consistency) against this one planned task. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether the edit triggers item 8, what you checked, and whether you found a contradiction. SECTION 2/2: report whatever action you took as a result, including the exact text of any edit made to docs/superpowers/specs/2026-08-27-fixture-cleanresult-design.md." > /c/sf-clean-result-test/trial.txt 2>&1
cat /c/sf-clean-result-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-clean-result-test/trial.txt`. Confirm SECTION 1/2 reports the edit triggers item 8 (via the "triggered by"/"standalone"/lifecycle language it still contains), reports checking `plugin/skills/mock-skill/SKILL.md`, and reports finding NO contradiction (the reworded text stays consistent with SKILL.md's claim). Confirm SECTION 2/2 reports adding a sentence to `docs/superpowers/specs/2026-08-27-fixture-cleanresult-design.md`'s Deferred or Consequences section explaining why `SKILL.md` needed no change.

Then independently verify against the actual fixture file (don't just trust the trial's report):

```bash
cat /c/sf-clean-result-test/docs/superpowers/specs/2026-08-27-fixture-cleanresult-design.md
```

Confirm the file's Deferred (or Consequences) section now contains a real sentence explaining why `SKILL.md` needed no change — not a placeholder, not an unrelated edit, and not still reading "Nothing yet."

If the trial reports item 8 didn't trigger, reports a false contradiction, or the fixture spec file's content doesn't actually contain the expected explanation, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture file both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-clean-result-test
```

No commit for this task.
