# Quote Verification Self-Review Item Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Spec Self-Review item 7 to `brainstorming/SKILL.md`, cross-referencing `docs/patterns/re-verify-quotes-against-source-before-citing.md`, and check off the Recommendation that requested it.

**Architecture:** One small text addition to one existing skill file, followed by checking off the Recommendation in the review file that named it. No code, no tests in the software sense — every task verifies via direct read-back or `grep`.

**Tech Stack:** Markdown, `grep`.

## Global Constraints

- Item 7's wording must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criterion 1).
- No file outside `plugin/skills/brainstorming/SKILL.md` and `docs/superpowers/process-reviews/review-after-2026-08-30-fix-wave-regression-amendment-design.md` gets modified.

---

## File Structure

Directories touched: `plugin/skills/brainstorming/`, `docs/superpowers/process-reviews/`. Checked both for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`); `docs/superpowers/process-reviews/` has none either (checked directly).

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/brainstorming/SKILL.md` — append Spec Self-Review item 7
- `docs/superpowers/process-reviews/review-after-2026-08-30-fix-wave-regression-amendment-design.md` — check off the Recommendation

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds Markdown text or checks off a list item.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add Spec Self-Review item 7

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the new Spec Self-Review item every future spec checks against. Task 2's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm item 6's exact current closing text**

Run: `grep -n "re-discovering the same trap." plugin/skills/brainstorming/SKILL.md`
Expected: one match, at line 152 (confirmed via direct read this session).

- [ ] **Step 2: Append item 7**

Change:
```markdown
6. **Numeric-claim verification:** Does any Context or Decision
section state a specific count (occurrences, files, lines) about the
existing codebase? If so, confirm you ran the actual command and
copied its real output — not an estimate — before finalizing the
spec. See docs/patterns/verify-plan-commands-against-real-content.md
for the specific failure shapes a plausible-looking prediction has
actually hit before — checking it against a known list beats
re-discovering the same trap.

Fix any issues inline. No need to re-review — just fix and move on.
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
7. **Quote and source-freshness verification:** Does the spec cite an
external or previously-read document's content, or present anything
in quotation marks? If so, grep the source for the exact quoted
phrase, and re-read the full document fresh if it describes state (a
report, a tracker, a shipped file) that might have changed since you
last read it — not just what you recall it saying. See
docs/patterns/re-verify-quotes-against-source-before-citing.md for
the specific failure shapes a plausible-looking citation has actually
hit before.

Fix any issues inline. No need to re-review — just fix and move on.
```

- [ ] **Step 3: Verify the addition landed**

Run: `grep -c "Quote and source-freshness verification" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): add Spec Self-Review item 7 to brainstorming (quote and source-freshness verification)"
```

---

### Task 2: Check off the Recommendation and verify

**Files:**
- Modify: `docs/superpowers/process-reviews/review-after-2026-08-30-fix-wave-regression-amendment-design.md`

**Interfaces:**
- Consumes: Task 1's committed changes (the shipped item 7), to cite its commit SHA in the disposition note.
- Produces: the closed-out review file. Nothing later depends on this task.

- [ ] **Step 1: Get Task 1's commit SHA**

Run: `git log -1 --format=%H -- plugin/skills/brainstorming/SKILL.md`
(Use the printed SHA in Step 2 below, in place of `<task-1-sha>`.)

- [ ] **Step 2: Check off the Recommendation**

Change:
```markdown
- [ ] Add a Self-Review item (or extend an existing one) in `brainstorming/SKILL.md`'s Spec Self-Review, cross-referencing `docs/patterns/re-verify-quotes-against-source-before-citing.md`: before finalizing a spec, grep the cited source for any sentence presented in quotation marks, and re-read the full source fresh if it describes an external or previously-read document whose state might have changed since the last read. Addresses M1 and G1.
```
To:
```markdown
- [x] Add a Self-Review item (or extend an existing one) in `brainstorming/SKILL.md`'s Spec Self-Review, cross-referencing `docs/patterns/re-verify-quotes-against-source-before-citing.md`: before finalizing a spec, grep the cited source for any sentence presented in quotation marks, and re-read the full source fresh if it describes an external or previously-read document whose state might have changed since the last read. Addresses M1 and G1. (Shipped as Spec Self-Review item 7, commit `<task-1-sha>`.)
```

- [ ] **Step 3: Verify the checkbox landed correctly**

Run: `grep -c "\[x\]" docs/superpowers/process-reviews/review-after-2026-08-30-fix-wave-regression-amendment-design.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/process-reviews/review-after-2026-08-30-fix-wave-regression-amendment-design.md
git commit -m "docs(process-reviews): check off Recommendation for quote-verification-self-review-item"
```

---

## Self-Review

**1. Spec coverage:** Task 1 covers the spec's Decision (item 7's text). Task 2 covers the Recommendation disposition. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command. `<task-1-sha>` is a documented placeholder filled from Task 2 Step 1's own output within the same task, not a plan failure.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** Item 7's wording mirrors item 6's exact shape (bold numbered lead-in, one-paragraph explanation, a "See docs/patterns/..." closing sentence naming the specific failure catalog) — checked directly against item 6's real text before finalizing, not assumed similar.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into Task 1's Step 2 and Task 2's disposition note — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md`, `docs/patterns/verify-plan-commands-against-real-content.md`, and `docs/patterns/re-verify-quotes-against-source-before-citing.md` before writing this plan — every numeric claim in this plan (the `1` counts in Task 1 Step 3 and Task 2 Step 3) got verified against real file content, and this plan cites nothing in quotation marks from an external source beyond the review file's own Recommendation text, which got directly grepped and confirmed against the real file before being copied into this plan — applying item 7's own discipline to the very plan shipping it.

**8. Cross-section mechanism consistency:** Task 1 adds item 7 immediately after item 6, which describes a closely related but distinct verification requirement (numeric claims vs. quotes/document-state). Grepped `brainstorming/SKILL.md` for every other mention of "verify," "quotation," and "source" beyond items 6–7 to confirm no other passage describes this same mechanism in a way item 7 would contradict — found none. This plan traces to a design spec; the spec's own Consequences section already states this closes the asymmetry with the numeric-verification sibling pattern, which is exactly what this check confirms holds true.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — this adds a new Self-Review item without changing the Self-Review process's own step sequence. No worked example needs a currency check.

**10. Verified numeric expectations:** Every `Expected:` count in this plan was confirmed by running the actual grep against real file content before being written into this plan — not estimated. See `docs/patterns/verify-plan-commands-against-real-content.md`, applied directly here.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-quote-verification-self-review-item.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
