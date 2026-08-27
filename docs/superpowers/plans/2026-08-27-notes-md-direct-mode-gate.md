# Notes.md Direct-Mode Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Widen the notes.md logging gate to also fire when the controller implements a task directly, without subagent dispatch, and catches a real issue — per `docs/superpowers/specs/2026-08-27-notes-md-direct-mode-gate-design.md`.

**Architecture:** One OR-clause added to the gate's existing trigger condition, plus backfilling the two real notes.md entries this exact gap already caused.

**Tech Stack:** Markdown skill file, no code, no test framework. Verification is a direct read-through, confirming the two backfilled entries exist, and one disposable `--plugin-dir` trial.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — widens the notes.md gate's trigger condition.
- **Modify:** `docs/superpowers/process-reviews/notes.md` — backfills two missing entries.

No other currently-shipped skill file mentions this gate's trigger condition — confirmed by grep. The phrase also appears in historical plan/spec/review documents from when this gate first shipped (`2026-08-26-process-review-recommendations-batch-2.md` and its design spec, plus the two most recent process-review files discussing the gap this plan closes) — those are point-in-time records, not live instructions, and don't need reconciling.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Widen the notes.md gate's trigger condition

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the OR clause**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
If this task's fix loop ran at least one round, run
`grep -c "Task <N> (<plan-slug>)" docs/superpowers/process-reviews/notes.md`
to confirm at least one entry exists — a task whose review passed
clean on the first pass never entered the loop, so this check doesn't
apply to it. If the grep returns 0, append one entry now for each
finding the review reported, naming the specific finding (not
"review findings addressed"), using the findings you already have
from the review:
```

Replace with:
```
If this task's fix loop ran at least one round, or if you implemented
and reviewed this task directly — without dispatching an implementer
subagent — and caught a real issue during that direct review, run
`grep -c "Task <N> (<plan-slug>)" docs/superpowers/process-reviews/notes.md`
to confirm at least one entry exists — a task whose review passed
clean on the first pass, dispatched or direct, never triggers this
check. If the grep returns 0, append one entry now for each finding
you caught, naming the specific finding (not "review findings
addressed" or "issues fixed"), using the findings you already have:
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "without dispatching an implementer" plugin/skills/subagent-driven-development/SKILL.md
grep -n "dispatched or direct, never triggers" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "docs(skills): widen notes.md gate to cover direct implementation

The gate's trigger condition ('if this task's fix loop ran at least
one round') never fired when the controller implemented a task
directly without subagent dispatch, even when real findings occurred
-- as happened across all three specs the originating process review
covers. Does not encourage direct implementation as routine; closes
the logging gap for when it happens anyway.

Part of docs/superpowers/specs/2026-08-27-notes-md-direct-mode-gate-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Backfill the two missing notes.md entries

**Files:**
- Modify: `docs/superpowers/process-reviews/notes.md`

- [ ] **Step 1: Append both entries**

Read the file first to find the last line, then append these two entries after it:

```
- 2026-08-27 | Catch | Spec self-review (cross-section-negative-case-trials) | Falsifiable Criterion 3, as originally drafted, would have forbidden naming the mechanism under test at all ("item 8," "the carve-out") in either trial's dispatch prompt -- a misreading of Rule 2, which only forbids revealing the discriminating fact or the answer, not naming which check to run; caught before the implementation plan got built around the over-strict wording
- 2026-08-27 | Catch | Finish (cross-section-negative-case-trials) | The spec's own Context section never cited docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-sibling-scope-design.md, even though this spec closes that review's second Recommendation -- citing only the two intermediate specs that had deferred the gap instead; caught by re-reading the spec once more before running Finish
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -c "Spec self-review (cross-section-negative-case-trials)" docs/superpowers/process-reviews/notes.md
grep -c "Finish (cross-section-negative-case-trials)" docs/superpowers/process-reviews/notes.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/process-reviews/notes.md
git commit -m "docs(process-reviews): backfill two missing notes.md entries for cross-section-negative-case-trials

Both findings already appear in review-after-2026-08-27-cross-section-
recursion-boundary-design.md's Catches section, reconstructed from git
log since notes.md held no real-time entry for either at the time.

Part of docs/superpowers/specs/2026-08-27-notes-md-direct-mode-gate-design.md."
```

Stage only this one file.

---

## Task 3: Live trial for the widened trigger condition

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a fixture plan and an empty notes.md**

```bash
mkdir -p /c/sf-directmode-gate-test/docs/superpowers/process-reviews
mkdir -p /c/sf-directmode-gate-test/docs/superpowers/plans
cd /c/sf-directmode-gate-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/process-reviews/notes.md <<'EOF'
# Process Review — Running Notes

Append-only log. Each entry marks one finding a review catches on its
first pass.

<!-- entries below this line -->
EOF

cat > docs/superpowers/plans/2026-08-27-fixture-directmode-test.md <<'EOF'
# Fixture Directmode Test Implementation Plan

**Goal:** A trivial plan used only to exercise the notes.md direct-mode gate in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 3: Set the cache timeout config key

Add a cache_timeout_seconds setting to config.md.
EOF

git add -A
git commit -q -m "initial scratch fixture: fixture plan, empty notes.md"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the widened gate against a direct-implementation scenario**

```bash
cd /c/sf-directmode-gate-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-directmode-gate-test. Use the Skill tool to invoke subagent-driven-development, so you have its actual current Complete-the-task step loaded. Scenario: this session's Agent-tool subagent spawn limit was reached, so you implemented Task 3 of docs/superpowers/plans/2026-08-27-fixture-directmode-test.md directly yourself, without dispatching an implementer subagent and without any reviewer subagent involved. While reviewing your own direct implementation, you caught and fixed a real issue: your first attempt used the wrong config key name (cache_timeout instead of cache_timeout_seconds), which you corrected before considering the task done. Follow the Complete-the-task step now for Task 3, exactly as written. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether this scenario triggers the notes.md check, and explain why using the step's own wording. SECTION 2/2: report the exact grep command you ran, its output, and the exact notes.md entry you appended (if any)." > /c/sf-directmode-gate-test/trial.txt 2>&1
cat /c/sf-directmode-gate-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-directmode-gate-test/trial.txt`. Confirm SECTION 1/2 reports the scenario triggers the check — direct implementation, no subagent dispatch, and a real issue caught during that direct review — citing the widened condition's own wording. Confirm SECTION 2/2 reports the grep returned 0 (the fixture's `notes.md` starts empty) and shows a real appended entry naming the specific finding (the wrong config key name), not a vague "issues fixed" or "review findings addressed."

Then independently verify against the actual fixture file (don't just trust the trial's report):

```bash
cat /c/sf-directmode-gate-test/docs/superpowers/process-reviews/notes.md
```

Confirm a real entry now exists, naming the wrong-config-key finding specifically.

If the trial reports the scenario doesn't trigger the check, or the fixture file's `notes.md` still shows no new entry, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and the fixture file both contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-directmode-gate-test
```

No commit for this task.
