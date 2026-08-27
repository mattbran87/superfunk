# Finish Bookkeeping Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the missing Recommendation-checkbox instruction and a three-part mechanical verification gate to `subagent-driven-development/SKILL.md`'s Finish section, per `docs/superpowers/specs/2026-08-27-finish-bookkeeping-gate-design.md`.

**Architecture:** One new paragraph (find-and-check-off the Recommendation) plus one verification block (three `grep -c` checks), inserted between the existing tracker-append paragraph and the Lessons-learned paragraph in Finish.

**Tech Stack:** Markdown skill file, no code, no test framework. Verification is a direct read-through plus two disposable `--plugin-dir` scratch trials.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds the Recommendation-checkbox paragraph and verification gate to Finish.

No other file in `plugin/skills/subagent-driven-development/` (`re-review-prompt.md`, `implementer-prompt.md`, `task-reviewer-prompt.md`) mentions Finish, spec Status, the tracker, or Recommendation checkboxes — confirmed by grep before writing this plan — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits a markdown skill file only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add the Recommendation-checkbox paragraph and verification gate to Finish

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the new paragraph and gate between the tracker paragraph and the Lessons-learned paragraph**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
If you updated a spec's Status to `Shipped`, also append its filename
to `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped
since" list, and commit that change in the same commit. If the list
now holds 3 or more filenames, offer to run superpowers:process-review
right now — the same ask-don't-force pattern as any other checkpoint
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.

Capture a notable learning in `docs/lessons-learned.md`, or record
```

Replace with:
```
If you updated a spec's Status to `Shipped`, also append its filename
to `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped
since" list, and commit that change in the same commit. If the list
now holds 3 or more filenames, offer to run superpowers:process-review
right now — the same ask-don't-force pattern as any other checkpoint
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.

If the spec's Context section names a
`docs/superpowers/process-reviews/review-after-*.md` file, that file
holds the Recommendation this spec closes. Open it, find the matching
`- [ ]` Recommendation by content, and check it off: change it to
`- [x]` and append `(Shipped as <what shipped>, commit <sha>.)` naming
this spec and its key implementing commit. Commit this change in the
same commit as the Status and tracker updates above. No review file
named: skip this step.

Before moving on, verify this Finish pass's own bookkeeping landed:

```bash
grep -c "^\*\*Status:\*\* Shipped" <spec-file>
grep -c "<spec filename>" docs/superpowers/process-reviews/tracker.md
grep -c "\[x\].*<a few distinctive words from the Recommendation's own original text>" <review-file>
```

Run the third check only when a review file was named above. Each
check that applies should return at least 1. A 0 means that action
never happened — do it now, before starting the Lessons-learned
capture below, not left for a later final review to notice.

Capture a notable learning in `docs/lessons-learned.md`, or record
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "that file" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Before moving on, verify this Finish pass" plugin/skills/subagent-driven-development/SKILL.md
grep -c "grep -c" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match for the first two, and the third count includes the 3 new grep lines plus every pre-existing `grep -c` instance already in the file (the notes.md gate uses one) — confirm the count increased by exactly 3 versus the pre-edit file.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): add Recommendation-checkbox step and Finish bookkeeping gate

Finish never instructed the controller to check off a process-review
Recommendation at all -- only the spec Status flip and tracker append
existed as written steps. The checkbox omission recurred across two
specs because nothing told the controller to do it, not because a
written step got skipped. Adds the missing instruction plus a
three-part mechanical gate confirming all three bookkeeping actions
landed before moving on.

Part of docs/superpowers/specs/2026-08-27-finish-bookkeeping-gate-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Live trial — the missing-bookkeeping case

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a spec, tracker, and review file all missing their Finish bookkeeping**

```bash
mkdir -p /c/sf-finish-gate-missing-test/docs/superpowers/specs
mkdir -p /c/sf-finish-gate-missing-test/docs/superpowers/plans
mkdir -p /c/sf-finish-gate-missing-test/docs/superpowers/process-reviews
cd /c/sf-finish-gate-missing-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/process-reviews/review-after-2026-08-01-fixture-base-design.md <<'EOF'
# Process Review — after 2026-08-01-fixture-base-design.md

**Date:** 2026-08-01

## Recommendations

- [ ] Add a widget-cache timeout to config.md, since the cache never expires today and stale widgets have been reported in the fixture app.
EOF

cat > docs/superpowers/specs/2026-08-05-widget-cache-timeout-design.md <<'EOF'
# Widget Cache Timeout — Design

**Date:** 2026-08-05
**Status:** Approved

## Context

The process review docs/superpowers/process-reviews/review-after-2026-08-01-fixture-base-design.md left one open Recommendation: add a widget-cache timeout. This spec closes it.

## Decision

config.md gains a `cache_timeout_seconds: 300` setting.
EOF

cat > docs/superpowers/process-reviews/tracker.md <<'EOF'
# Process Review Tracker

**Last review:** 2026-08-01-fixture-base-design.md — 2026-08-01
**Specs shipped since:** (none)
EOF

cat > docs/superpowers/plans/2026-08-05-widget-cache-timeout.md <<'EOF'
# Widget Cache Timeout Implementation Plan

**Goal:** Add a widget-cache timeout. Part of docs/superpowers/specs/2026-08-05-widget-cache-timeout-design.md.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Add the timeout setting

Add `cache_timeout_seconds: 300` to config.md (fixture task; already implemented and reviewed clean for this trial).
EOF

git add -A
git commit -q -m "initial scratch fixture: spec/tracker/review-file all missing Finish bookkeeping"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising Finish's new paragraph and gate**

```bash
cd /c/sf-finish-gate-missing-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-finish-gate-missing-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current Finish section loaded. Treat Task 1 of docs/superpowers/plans/2026-08-05-widget-cache-timeout.md as already implemented and reviewed clean (a final whole-branch review already passed with no findings) -- you are now running the Finish step only. Follow Finish's instructions exactly, including the new Recommendation-checkbox paragraph and its verification gate. Make all real edits and commits this step calls for. Report back in exactly 3 numbered sections with literal headers: SECTION 1/3: what you changed in the spec file, the tracker, and the review file. SECTION 2/3: the exact output of the three verification greps you ran. SECTION 3/3: quote the exact text you appended to the Recommendation line." > /c/sf-finish-gate-missing-test/trial.txt 2>&1
cat /c/sf-finish-gate-missing-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-finish-gate-missing-test/trial.txt`. Confirm SECTION 1/3 reports flipping the spec's `Status` to `Shipped`, appending the spec's filename to the tracker, and checking off the Recommendation in the review file. Confirm SECTION 2/3 shows all three greps returning at least 1. Confirm SECTION 3/3 quotes a `(Shipped as ..., commit ...)`-shaped annotation.

Then independently verify against the actual fixture files (don't just trust the trial's report):

```bash
cat /c/sf-finish-gate-missing-test/docs/superpowers/specs/2026-08-05-widget-cache-timeout-design.md
cat /c/sf-finish-gate-missing-test/docs/superpowers/process-reviews/tracker.md
cat /c/sf-finish-gate-missing-test/docs/superpowers/process-reviews/review-after-2026-08-01-fixture-base-design.md
```

Confirm the spec's `Status` line reads `Shipped`, the tracker's "Specs shipped since" list includes `2026-08-05-widget-cache-timeout-design.md`, and the review file's Recommendation line changed from `- [ ]` to `- [x]` with a shipped-as annotation appended.

If any of the three actions didn't actually happen in the fixture files (regardless of what the trial's report claimed), treat this as DONE_WITH_CONCERNS and report exactly what the fixture files contain versus what the trial claimed.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-finish-gate-missing-test
```

No commit for this task.

---

## Task 3: Live trial — the already-compliant case

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build the same fixture shape, but with all three bookkeeping actions already done**

```bash
mkdir -p /c/sf-finish-gate-compliant-test/docs/superpowers/specs
mkdir -p /c/sf-finish-gate-compliant-test/docs/superpowers/plans
mkdir -p /c/sf-finish-gate-compliant-test/docs/superpowers/process-reviews
cd /c/sf-finish-gate-compliant-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/process-reviews/review-after-2026-08-01-fixture-base-design.md <<'EOF'
# Process Review — after 2026-08-01-fixture-base-design.md

**Date:** 2026-08-01

## Recommendations

- [x] Add a widget-cache timeout to config.md, since the cache never expires today and stale widgets have been reported in the fixture app. (Shipped as a 300-second cache_timeout_seconds setting in config.md, commit abc1234.)
EOF

cat > docs/superpowers/specs/2026-08-05-widget-cache-timeout-design.md <<'EOF'
# Widget Cache Timeout — Design

**Date:** 2026-08-05
**Status:** Shipped

## Context

The process review docs/superpowers/process-reviews/review-after-2026-08-01-fixture-base-design.md left one open Recommendation: add a widget-cache timeout. This spec closes it.

## Decision

config.md gains a `cache_timeout_seconds: 300` setting.
EOF

cat > docs/superpowers/process-reviews/tracker.md <<'EOF'
# Process Review Tracker

**Last review:** 2026-08-01-fixture-base-design.md — 2026-08-01
**Specs shipped since:** 2026-08-05-widget-cache-timeout-design.md
EOF

cat > docs/superpowers/plans/2026-08-05-widget-cache-timeout.md <<'EOF'
# Widget Cache Timeout Implementation Plan

**Goal:** Add a widget-cache timeout. Part of docs/superpowers/specs/2026-08-05-widget-cache-timeout-design.md.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Add the timeout setting

Add `cache_timeout_seconds: 300` to config.md (fixture task; already implemented, reviewed clean, and already Finished once for this trial).
EOF

git add -A
git commit -q -m "initial scratch fixture: spec/tracker/review-file already Finish-compliant"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising Finish's verification gate against the already-compliant fixture**

```bash
cd /c/sf-finish-gate-compliant-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-finish-gate-compliant-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current Finish section loaded. Task 1 of docs/superpowers/plans/2026-08-05-widget-cache-timeout.md is already implemented, reviewed clean, and Finish's bookkeeping has already run once successfully (check the current state of the spec file, tracker, and review file yourself to confirm this before doing anything). You are re-running Finish's verification gate now, as if resuming after a compaction or a second look. Follow Finish's instructions exactly, including the new Recommendation-checkbox paragraph and its verification gate. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: what your own check of the spec/tracker/review file found already in place, before running the gate. SECTION 2/2: the exact output of the three verification greps, and whether you made any edit or commit as a result." > /c/sf-finish-gate-compliant-test/trial.txt 2>&1
cat /c/sf-finish-gate-compliant-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-finish-gate-compliant-test/trial.txt`. Confirm SECTION 1/2 reports finding the spec already `Shipped`, the tracker already listing the spec, and the Recommendation already `- [x]`. Confirm SECTION 2/2 shows all three greps returning at least 1, and explicitly reports making no edit and no commit.

Then independently verify no new commit landed:

```bash
cd /c/sf-finish-gate-compliant-test && git log --oneline
```

Confirm exactly one commit exists (the fixture's own initial commit) — no second commit from the trial session.

If the trial made any edit, created a duplicate annotation, or committed anything, treat this as DONE_WITH_CONCERNS and report exactly what changed.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-finish-gate-compliant-test
```

No commit for this task.
