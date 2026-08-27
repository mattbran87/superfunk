# Refresh Example Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh `subagent-driven-development`'s stale Example Workflow and add a Self-Review check preventing the same staleness from recurring, per `docs/superpowers/specs/2026-08-27-refresh-example-workflow-design.md`.

**Architecture:** Two content additions to the Example Workflow (a fix-loop notes.md bracket, and the real Finish sequence) plus one new Self-Review item in `writing-plans/SKILL.md`.

**Tech Stack:** Markdown skill files, no code, no test framework. Verification uses two direct read-throughs plus one disposable `--plugin-dir` trial.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — refreshes the Example Workflow section.
- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds Self-Review item 9.

No other file in either skill's directory mentions the Example Workflow's content or a "Worked-example currency" check — confirmed by grep — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Refresh the Example Workflow

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the fix-loop notes.md bracket line**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
[Fix round 1: resume the implementer with both findings]
```

Replace with:
```
[notes.md: append Task 2 findings — Missing progress reporting; Magic number (100)]
[Fix round 1: resume the implementer with both findings]
```

- [ ] **Step 2: Replace the bare workspace-deletion ending with the real Finish sequence**

Find:
```
[After all tasks]
[Run review-package PLAN_FILE MERGE_BASE HEAD; dispatch final code-reviewer, most capable model]
Final reviewer: All requirements met. Deferred minors triaged: none block merge.

[Delete this plan's workspace — the record now lives in git]

Done! Using superpowers:finishing-a-development-branch.
```

Replace with:
```
[After all tasks]
[Run review-package PLAN_FILE MERGE_BASE HEAD; dispatch final code-reviewer, most capable model]
Final reviewer: All requirements met. Deferred minors triaged: none block merge.

[Finish: spec Status Approved -> Shipped, committed]
[Finish: appended feature-plan-design.md to tracker.md's Specs shipped since]
[Finish: no Recommendation to check off -- this plan didn't trace to a process review]
[Finish: notes.md gate -- Task 2's fix round already logged above, check passes]
[Finish: captured a Lesson in lessons-learned.md; no pattern promoted, one instance so far]
[Finish: no concept-index entry needed -- no skill/feature/significant directory created]
[Finish: no real-and-deferred parked findings -- bug-tracking step skipped]

[Delete this plan's workspace — the record now lives in git]

Done! Using superpowers:finishing-a-development-branch.
```

- [ ] **Step 3: Verify both edits landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "notes.md: append Task 2 findings" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Finish: spec Status Approved" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Finish: no real-and-deferred parked findings" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "docs(skills): refresh the stale Example Workflow

The example jumped straight from the final review to workspace
deletion, never showing the fix-loop's own notes.md bracket or any of
Finish's six bookkeeping steps -- one prior fix, five more additions
since that never revisited it. Adds both, including the skip cases,
which illustrate what 'correctly not applicable' looks like too.

Part of docs/superpowers/specs/2026-08-27-refresh-example-workflow-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Add Self-Review item 9 to writing-plans

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert item 9 after item 8**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below matches byte-for-byte without checking.

Find:
```
to that spec's Deferred or Consequences section explaining why the
checked file(s) needed no change.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

Replace with:
```
to that spec's Deferred or Consequences section explaining why the
checked file(s) needed no change.

**9. Worked-example currency:** Does any task add, remove, or reorder a
step in a documented multi-step process (e.g., Finish's bookkeeping
sequence, the fix loop)? If so, check whether a worked example
elsewhere in the same file demonstrates that process. If it does,
update it to reflect the change.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "9. Worked-example currency" plugin/skills/writing-plans/SKILL.md
grep -c "update it to reflect the change." plugin/skills/writing-plans/SKILL.md
```

Expected: one match, one count.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): add Worked-example currency to Self-Review

Prevents the exact staleness cross-section-mechanism-consistency's
own final review found in subagent-driven-development's Example
Workflow -- six Finish additions in a row skipped updating it,
because nothing asked whether a worked example needed the same
change the new step's own instructions just got.

Part of docs/superpowers/specs/2026-08-27-refresh-example-workflow-design.md."
```

Stage only this one file.

---

## Task 3: Live trial for Self-Review item 9

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a mock skill file containing a documented process and a worked example demonstrating it**

```bash
mkdir -p /c/sf-worked-example-currency-test/plugin/skills/mock-skill
cd /c/sf-worked-example-currency-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/SKILL.md <<'EOF'
# Mock Skill

## Process

When finishing a task, run these two checks in order:

1. Verify the tests pass.
2. Update the status file.

## Example Workflow

```
[Run tests: 5/5 passing]
[Update status file: marked complete]
Done!
```
EOF

git add -A
git commit -q -m "initial scratch fixture: mock-skill with a 2-step process and a matching worked example"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising item 9 against a plan task that adds a step to the process without touching the example**

```bash
cd /c/sf-worked-example-currency-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-worked-example-currency-test. Use the Skill tool to invoke writing-plans. You are drafting a plan with exactly one task: modify plugin/skills/mock-skill/SKILL.md's Process section to add a third step: '3. Notify the team channel.' Do not actually write the plan file to disk or make any edit to SKILL.md -- this is a dry run of the Self-Review step only. Run Self-Review item 9 (Worked-example currency) against this one planned task. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether this planned edit triggers item 9, and why. SECTION 2/2: if it triggers, name the specific worked example that needs updating and what change it needs." > /c/sf-worked-example-currency-test/trial.txt 2>&1
cat /c/sf-worked-example-currency-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-worked-example-currency-test/trial.txt`. Confirm SECTION 1/2 reports item 9 triggers, since the task adds a step to a documented multi-step process. Confirm SECTION 2/2 correctly identifies the "Example Workflow" section as needing an update to add the new "Notify the team channel" step, matching the new 3-step process.

If the trial reports item 9 doesn't trigger, or fails to identify the specific worked example needing an update, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-worked-example-currency-test
```

No commit for this task.
