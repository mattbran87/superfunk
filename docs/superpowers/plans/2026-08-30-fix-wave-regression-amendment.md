# Fix-Wave Regression Amendment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Amend `subagent-driven-development/SKILL.md`'s Final Review section so a regression the fix wave itself introduces gets exactly one additional scoped fix-and-re-review cycle, distinct from the existing rule for findings the wave simply failed to fix.

**Architecture:** One paragraph replacement in one existing skill file, followed by two disposable `--plugin-dir` trials confirming the amended rule's two branches behave correctly. No code, no tests in the software sense — verification is direct read-back and live trial behavior.

**Tech Stack:** Markdown, disposable trials.

## Global Constraints

- The amended paragraph must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criterion 1).
- The process diagram's `"Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals"` node stays unchanged — the spec's own Decision explicitly states this node stays too coarse-grained to need updating.
- No file outside `plugin/skills/subagent-driven-development/SKILL.md` gets modified.

---

## File Structure

Directory touched: `plugin/skills/subagent-driven-development/`. Checked for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`).

This plan creates no new files — the only edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/subagent-driven-development/SKILL.md` — amend the Final Review section's fix-wave adjudication paragraph

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; the edit adds Markdown prose describing a controller decision rule.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Amend the fix-wave adjudication paragraph

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the amended rule every future Final Review adjudication follows. Task 2's live trials depend on this task's exact wording.

- [ ] **Step 1: Confirm the current paragraph's exact text**

Run: `grep -n "Then run exactly one scoped re-review" plugin/skills/subagent-driven-development/SKILL.md`
Expected: one match, at line 541 (confirmed via direct read this session).

- [ ] **Step 2: Replace the paragraph**

Change:
```markdown
Then run exactly one scoped re-review of the fix wave
(`scripts/review-package PLAN_FILE FIX_BASE HEAD` over the fix range,
[re-review-prompt.md](re-review-prompt.md)).
Adjudicate any residual findings as in the task loop's breaker: park with
rulings, or stop on load-bearing ones. There is no second fix wave —
residual load-bearing findings surface to your human partner when
finishing-a-development-branch presents the options.
```
To:
```markdown
Then run exactly one scoped re-review of the fix wave
(`scripts/review-package PLAN_FILE FIX_BASE HEAD` over the fix range,
[re-review-prompt.md](re-review-prompt.md)).
Adjudicate any residual findings as in the task loop's breaker: park with
rulings, or stop on load-bearing ones — with one exception. A finding
that's a regression the fix wave itself introduced (absent before the
wave, not one it failed to address) gets exactly one additional scoped
fix dispatch, scoped to that regression alone, followed by one more
scoped re-review over that narrower range. This stays bounded by
construction: it fires at most once, only for a defect the wave itself
caused. Everything else follows the existing rule unchanged — there is
no second fix wave for a finding the first wave simply failed to fix;
residual load-bearing findings surface to your human partner when
finishing-a-development-branch presents the options.
```

- [ ] **Step 3: Verify the amendment landed**

Run: `grep -c "with one exception" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `1`

Run: `grep -c "There is no second fix wave" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0` (the old unqualified sentence no longer exists as its own standalone statement — the amended text folds the same conclusion into the longer "Everything else follows..." sentence, worded differently)

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "fix(skills): amend Final Review's fix-wave rule to allow one scoped follow-up for a wave-introduced regression"
```

---

### Task 2: Live trials for both branches of the amended rule

**Files:**
- No files modified — this task only verifies Task 1.

**Interfaces:**
- Consumes: the finished state of the file Task 1 touched.
- Produces: pass/fail evidence for the design spec's Falsifiable Criteria 2 and 3. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — the amended text**

Run: `grep -A11 "Then run exactly one scoped re-review" plugin/skills/subagent-driven-development/SKILL.md`
Expected: text matching the Decision block's amended paragraph exactly.

- [ ] **Step 2: Build the regression-introduced fixture**

Set up a disposable fixture: a fresh `git init` repo with a small module and a passing test suite representing "before the fix wave." Simulate a fix wave whose own change introduces a new, distinct bug — for example, a fix that correctly addresses an original finding but changes a function signature in a way that breaks a second, previously-passing test elsewhere in the same file (a real regression, not a finding the wave was dispatched to address).

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Follow the superfunk:subagent-driven-development skill's Final Review section directly. A fix wave just ran (diff attached below) addressing finding X. Its own scoped re-review found a NEW failure in test_something_else — a regression this fix introduced, not one of the findings the wave was dispatched to fix. Per the skill's current rule, what do you do? Quote the exact rule you're following and state your decision." --add-dir <fixture-path>
```

Expected: the response cites the amended paragraph's exception and correctly decides to dispatch exactly one additional scoped fix for the regression alone, followed by one more scoped re-review — not treating this as a second full fix wave, and not silently parking a regression it just introduced.

- [ ] **Step 3: Build the failed-to-fix fixture**

Set up a second disposable trial (same shape, no code changes needed beyond the framing): a fix wave's re-review finds a residual finding that the wave simply failed to address — the same finding from before the fix wave, still present, not a new regression.

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Follow the superfunk:subagent-driven-development skill's Final Review section directly. A fix wave just ran addressing finding X. Its own scoped re-review found that finding Y (one of the original findings the wave was dispatched to fix) is STILL present -- the wave didn't address it. Per the skill's current rule, what do you do? Quote the exact rule you're following and state your decision."
```

Expected: the response correctly applies the unchanged existing rule — park finding Y with a ruling, or stop if load-bearing — and does not dispatch a second fix wave for it.

- [ ] **Step 4: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers the spec's Decision (the amended paragraph). Task 2 covers Falsifiable Criteria 2 and 3 (the two live-trial branches); Criterion 1 gets covered by Task 2 Step 1's direct read-back. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** N/A — this task adds an exception to a single existing rule rather than a new sibling instruction alongside an existing one; no comparable adjacent instruction to mirror.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into Task 1's Step 2 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` and `docs/patterns/verify-plan-commands-against-real-content.md` and `docs/patterns/re-verify-quotes-against-source-before-citing.md` before writing this plan — this plan's own numeric claims (the `1`, `0` counts) got verified against real file content, and this plan quotes nothing from an external source document, so the quote-verification pattern doesn't apply here beyond what already happened during the spec's own self-review.

**8. Cross-section mechanism consistency:** Task 1 edits the fix-wave adjudication rule described in `subagent-driven-development/SKILL.md`'s Final Review section. Grepped the full file for every other mention of "second fix wave," "fix wave," and "scoped re-review" beyond the paragraph being changed, plus the design spec, to confirm no other passage describes this same mechanism. Found the process diagram's `"Final findings?"` node (already addressed explicitly in the spec's own Decision — stays unchanged, too coarse-grained) and the prose Example Workflow's fix-round bracket lines, which describe per-task fix rounds under the task loop's breaker, a different mechanism (per-task, not the whole-branch Final Review fix wave this spec amends) — confirmed by reading both and finding no overlap in the specific rule being changed. This plan traces to a design spec; this sentence documents that check per item 8's own instruction.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — Task 1 adds an exception to an existing step's rule without changing the Final Review sequence's own step count or order. The prose Example Workflow doesn't currently depict a fix-wave regression scenario at all (only a per-task fix round), so no existing worked example needs updating for this addition.

**10. Verified numeric expectations:** Every `Expected:` count in this plan (the `1` and `0` in Task 1 Step 3) was confirmed by reasoning directly from the exact inserted text rather than assumed — the inserted text contains "with one exception" exactly once, and the old standalone sentence "There is no second fix wave —" (as its own sentence start) no longer exists verbatim after the replacement.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-fix-wave-regression-amendment.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
