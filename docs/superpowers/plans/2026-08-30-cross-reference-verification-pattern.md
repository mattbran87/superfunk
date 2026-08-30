# Cross-Reference Verification Pattern Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cross-reference `docs/patterns/verify-plan-commands-against-real-content.md` directly from writing-plans' Self-Review item 10 and brainstorming's Spec Self-Review item 6, and record both Recommendation dispositions in the review file that named them.

**Architecture:** Two small, independent text additions to two existing skill files, followed by checking off both Recommendations in the review file with their respective outcomes. No code, no tests in the software sense — every task verifies via direct read-back or `grep`.

**Tech Stack:** Markdown, `grep`.

## Global Constraints

- Both added sentences must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criteria 1, 2).
- `review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md`'s first Recommendation gets a `(Shipped...)` note; its second gets a `(Deferred: ...)` note, worded per the spec's Decision block — not both shipped, since the second Recommendation's outcome is a documented non-build decision, not a shipped mechanism (per spec Falsifiable Criterion 3).
- No file outside `plugin/skills/writing-plans/SKILL.md`, `plugin/skills/brainstorming/SKILL.md`, and `docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md` gets modified.

---

## File Structure

Directories touched: `plugin/skills/writing-plans/`, `plugin/skills/brainstorming/`, `docs/superpowers/process-reviews/`. Checked the first two for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`). `docs/superpowers/process-reviews/` has no `.context.md` either (checked directly).

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/writing-plans/SKILL.md` — append one sentence to Self-Review item 10
- `plugin/skills/brainstorming/SKILL.md` — append the same sentence to Spec Self-Review item 6
- `docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md` — check off both Recommendations with their dispositions

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds a sentence of Markdown text or checks off a list item.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add the cross-reference sentence to item 10 and item 6

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the two Self-Review items every future plan and spec checks against, now pointing at the known failure-mode catalog. Task 2's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm item 10's exact current closing text**

Run: `grep -n "Verified numeric expectations" -A 7 plugin/skills/writing-plans/SKILL.md`
Expected: text ending in "placeholder." — confirmed via direct read this session.

- [ ] **Step 2: Append the cross-reference sentence to item 10**

Change:
```markdown
**10. Verified numeric expectations:** For each step whose `Expected:`
value states a specific count (a test count, a grep match count, a
line count), confirm you ran the actual command during plan-writing
and copied its real output — not an estimate, and not carried over
from an earlier draft after other steps changed. An estimated count
nobody actually ran counts as a plan failure, the same as a
placeholder.
```
To:
```markdown
**10. Verified numeric expectations:** For each step whose `Expected:`
value states a specific count (a test count, a grep match count, a
line count), confirm you ran the actual command during plan-writing
and copied its real output — not an estimate, and not carried over
from an earlier draft after other steps changed. An estimated count
nobody actually ran counts as a plan failure, the same as a
placeholder. See docs/patterns/verify-plan-commands-against-real-content.md
for the specific failure shapes a plausible-looking prediction has
actually hit before — checking it against a known list beats
re-discovering the same trap.
```

- [ ] **Step 3: Append the same sentence to item 6**

Change:
```markdown
6. **Numeric-claim verification:** Does any Context or Decision
section state a specific count (occurrences, files, lines) about the
existing codebase? If so, confirm you ran the actual command and
copied its real output — not an estimate — before finalizing the
spec.
```
To:
```markdown
6. **Numeric-claim verification:** Does any Context or Decision
section state a specific count (occurrences, files, lines) about the
existing codebase? If so, confirm you ran the actual command and
copied its real output — not an estimate — before finalizing the
spec. See docs/patterns/verify-plan-commands-against-real-content.md
for the specific failure shapes a plausible-looking prediction has
actually hit before — checking it against a known list beats
re-discovering the same trap.
```

- [ ] **Step 4: Verify both additions landed**

Run: `grep -c "verify-plan-commands-against-real-content.md" plugin/skills/writing-plans/SKILL.md`
Expected: `1`

Run: `grep -c "verify-plan-commands-against-real-content.md" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): cross-reference verify-plan-commands-against-real-content.md from item 10 and item 6"
```

---

### Task 2: Check off both Recommendations and verify

**Files:**
- Modify: `docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md`

**Interfaces:**
- Consumes: Task 1's committed changes (the shipped cross-references), to cite their commit SHA in the first Recommendation's disposition note.
- Produces: the closed-out review file. Nothing later depends on this task.

- [ ] **Step 1: Get Task 1's commit SHA**

Run: `git log -1 --format=%H -- plugin/skills/writing-plans/SKILL.md`
(Use the printed SHA in Step 2 below, in place of `<task-1-sha>`.)

- [ ] **Step 2: Check off both Recommendations**

Change:
```markdown
- [ ] Add a direct cross-reference from `writing-plans/SKILL.md`'s Self-Review items 10 and 12, and `brainstorming/SKILL.md`'s Spec Self-Review item 6, to `docs/patterns/verify-plan-commands-against-real-content.md` — naming it as the place to check known failure-mode categories (line-vs-occurrence counting, anchored patterns against indented/fenced content, case sensitivity, a phrase's other appearances in the same file, a substring legitimately retained elsewhere) before trusting a verification command's predicted output. Addresses G1.
- [ ] Revisit `2026-08-30-doc-timing-and-mutation-check-design.md`'s Deferred item — "Making the mutation check itself automatic/scripted... no evidence yet that manual execution proves insufficient" — against this review's own evidence: 7 manual-verification misses in one review period. A small script that takes a pattern and a file and reports the real count (or confirms a substitution's real effect) would remove the class of error this review's Catches all share, not just the mutation-check's own narrower case. Addresses M1 and F1 at the tooling level rather than the instruction level.
```
To:
```markdown
- [x] Add a direct cross-reference from `writing-plans/SKILL.md`'s Self-Review items 10 and 12, and `brainstorming/SKILL.md`'s Spec Self-Review item 6, to `docs/patterns/verify-plan-commands-against-real-content.md` — naming it as the place to check known failure-mode categories (line-vs-occurrence counting, anchored patterns against indented/fenced content, case sensitivity, a phrase's other appearances in the same file, a substring legitimately retained elsewhere) before trusting a verification command's predicted output. Addresses G1. (Shipped as a cross-reference sentence added to item 10 and item 6 — item 12 doesn't itself state a numeric or pattern-matching claim, so it needed no addition — commit `<task-1-sha>`.)
- [x] Revisit `2026-08-30-doc-timing-and-mutation-check-design.md`'s Deferred item — "Making the mutation check itself automatic/scripted... no evidence yet that manual execution proves insufficient" — against this review's own evidence: 7 manual-verification misses in one review period. A small script that takes a pattern and a file and reports the real count (or confirms a substitution's real effect) would remove the class of error this review's Catches all share, not just the mutation-check's own narrower case. Addresses M1 and F1 at the tooling level rather than the instruction level. (Deferred: reconsidered directly in `2026-08-30-cross-reference-verification-pattern-design.md` — every miss this review found already got caught by the existing "run the command" step; a scripted helper would speed up the easy case without addressing the case that actually took effort. Revisit only if a future miss escapes the existing manual step undetected.)
```

- [ ] **Step 3: Verify both checkboxes landed correctly**

Run: `grep -c "\[x\]" docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md`
Expected: `2`

Run: `grep -c "(Deferred: reconsidered directly" docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/process-reviews/review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md
git commit -m "docs(process-reviews): check off both Recommendations for cross-reference-verification-pattern"
```

---

## Self-Review

**1. Spec coverage:** Task 1 covers the spec's Decision ¶1–2 (the two cross-reference additions). Task 2 covers Decision ¶3 (the Recommendation dispositions). No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command. `<task-1-sha>` is a documented placeholder filled from Task 2 Step 1's own output within the same task, not a plan failure.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** The added sentence is identical in both item 10 and item 6, matching the spec's own Decision block exactly rather than adapting wording per file — checked that both target items already end their own paragraph with a period before appending, so the new sentence reads as a natural continuation in both places.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into both Task 1 steps and both Recommendation disposition notes in Task 2 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` and `docs/patterns/verify-plan-commands-against-real-content.md` before writing this plan — every numeric claim in this plan (the `1`, `1`, `2`, and `1` counts in Task 1 Step 4 and Task 2 Step 3) got verified by running the actual grep against real file content before being written down. This plan is itself the vehicle shipping the very cross-reference these items describe, so applying the discipline here directly demonstrates the fix.

**8. Cross-section mechanism consistency:** Task 1 edits two Self-Review items that both describe the same underlying verification requirement across two different skill files (`writing-plans` and `brainstorming`). Grepped both files for every other mention of "verify-plan-commands-against-real-content" and "Numeric-claim verification"/"Verified numeric expectations" beyond the two target items, plus the design spec, to confirm no third description of this mechanism exists that would need the same addition. Found none — item 12 (checked explicitly, per the spec's own Decision) doesn't state a numeric or pattern-matching claim itself, so it correctly needs no addition. This plan traces to a design spec; the spec's own Decision block already states this reasoning for item 12, which is exactly what this check confirms holds true.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — both edits append a sentence to an existing item without changing any process's step sequence. No worked example needs a currency check.

**10. Verified numeric expectations:** Every `Expected:` count in this plan was confirmed by running the actual grep against real file content before being written down — not estimated. See docs/patterns/verify-plan-commands-against-real-content.md, applied directly here, in the very plan that ships the cross-reference to it.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-cross-reference-verification-pattern.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
