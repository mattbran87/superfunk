# Process Review Recommendations, Batch 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close all four Recommendations from `review-after-2026-08-28-superfunk-rebrand-design.md` — two new writing-plans Self-Review items, one new brainstorming Spec Self-Review item, and a refreshed subagent-driven-development process diagram.

**Architecture:** Three independent, additive edits to three existing skill files, each adding a checklist item or diagram node with exact text already fixed by the design spec, followed by one verification task confirming all four Falsifiable Criteria. No code, no tests in the software sense — every task verifies via direct read-back or `grep`.

**Tech Stack:** Markdown, Graphviz `dot` syntax (text only, not rendered), `grep`.

## Global Constraints

- Every new checklist item's wording must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criteria 1–2).
- The process diagram's new node sequence must match the design spec's Decision block exactly, and the old combined `"Final review clean: delete this plan's workspace"` node must not remain anywhere in the file afterward (per spec Falsifiable Criterion 3).
- `grep -c "Finish:" plugin/skills/subagent-driven-development/SKILL.md` must return exactly 13 after this plan's changes (per spec Falsifiable Criterion 4).
- No file outside `plugin/skills/writing-plans/SKILL.md`, `plugin/skills/brainstorming/SKILL.md`, and `plugin/skills/subagent-driven-development/SKILL.md` gets modified — this closes four specific Recommendations, not a broader pass.

---

## File Structure

Directories touched: `plugin/skills/writing-plans/`, `plugin/skills/brainstorming/`, `plugin/skills/subagent-driven-development/`. Checked all three for a `.context.md` file — none exist anywhere under `plugin/` (already confirmed this session via `find plugin -iname ".context.md"`), so no directory context to read.

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/writing-plans/SKILL.md` — append Self-Review items 10 and 11
- `plugin/skills/brainstorming/SKILL.md` — append Spec Self-Review item 6
- `plugin/skills/subagent-driven-development/SKILL.md` — replace one process-diagram node with a five-node Finish sequence

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds Markdown checklist text or Graphviz diagram text.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add Self-Review items 10 and 11 to writing-plans

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the two new Self-Review items every future plan (including this project's own future plans) checks against. Task 4's verification depends on this task's exact wording.

- [ ] **Step 1: Read the current Self-Review section to confirm item 9's exact closing text**

Run: `grep -n "9. \*\*Worked-example currency" plugin/skills/writing-plans/SKILL.md`
Expected: one match, confirming item 9 exists and where it ends (the line immediately before "If you find issues, fix them inline...").

- [ ] **Step 2: Append items 10 and 11**

Change:
```markdown
**9. Worked-example currency:** Does any task add, remove, or reorder a
step in a documented multi-step process (e.g., Finish's bookkeeping
sequence, the fix loop)? If so, check whether a worked example
elsewhere in the same file demonstrates that process. If it does,
update it to reflect the change.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```
To:
```markdown
**9. Worked-example currency:** Does any task add, remove, or reorder a
step in a documented multi-step process (e.g., Finish's bookkeeping
sequence, the fix loop)? If so, check whether a worked example
elsewhere in the same file demonstrates that process. If it does,
update it to reflect the change.

**10. Verified numeric expectations:** For each step whose `Expected:`
value states a specific count (a test count, a grep match count, a
line count), confirm you ran the actual command during plan-writing
and copied its real output — not an estimate, and not carried over
from an earlier draft after other steps changed. An estimated count
nobody actually ran counts as a plan failure, the same as a
placeholder.

**11. Template compliance:** Does this plan's own document header
match every element the Plan Document Header section above requires
(Goal, Architecture, Tech Stack, Global Constraints)? A required
section silently missing from this plan's own header counts as the
same class of gap as a missing task for a spec requirement.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 3: Verify the exact text landed**

Run: `grep -c "10. \*\*Verified numeric expectations\|11. \*\*Template compliance" plugin/skills/writing-plans/SKILL.md`
Expected: `2`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): add Self-Review items 10-11 to writing-plans (verified numeric expectations, template compliance)"
```

---

### Task 2: Add Spec Self-Review item 6 to brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 1 (an independent skill file).
- Produces: the new Spec Self-Review item every future spec (including this project's own future specs) checks against. Task 4's verification depends on this task's exact wording.

- [ ] **Step 1: Read the current Spec Self-Review section to confirm item 5's exact text**

Run: `grep -n "5. \*\*Enforcement check" plugin/skills/brainstorming/SKILL.md`
Expected: one match.

- [ ] **Step 2: Append item 6**

Change:
```markdown
5. **Enforcement check:** Does each design decision in the written spec name what checks or enforces it, or explicitly flag the gap (per Mechanisms, Not Goodwill)? A mechanism named only during the presentation conversation and not carried into the file doesn't count.

Fix any issues inline. No need to re-review — just fix and move on.
```
To:
```markdown
5. **Enforcement check:** Does each design decision in the written spec name what checks or enforces it, or explicitly flag the gap (per Mechanisms, Not Goodwill)? A mechanism named only during the presentation conversation and not carried into the file doesn't count.
6. **Numeric-claim verification:** Does any Context or Decision
section state a specific count (occurrences, files, lines) about the
existing codebase? If so, confirm you ran the actual command and
copied its real output — not an estimate — before finalizing the
spec.

Fix any issues inline. No need to re-review — just fix and move on.
```

- [ ] **Step 3: Verify the exact text landed**

Run: `grep -c "6. \*\*Numeric-claim verification" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): add Spec Self-Review item 6 to brainstorming (numeric-claim verification)"
```

---

### Task 3: Refresh subagent-driven-development's process diagram

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

**Interfaces:**
- Consumes: nothing from Tasks 1–2 (an independent skill file).
- Produces: the corrected `digraph process` block. Task 4's verification depends on this task's exact node text and on the old combined node no longer existing anywhere in the file.

- [ ] **Step 1: Confirm the exact current node and edge text before editing**

Run: `grep -n "Final review clean: delete this plan's workspace" plugin/skills/subagent-driven-development/SKILL.md`
Expected: two matches — one node declaration line, one edge-source line, one edge-target line (three total lines, since the node name appears in the declaration plus both sides of its two edges).

- [ ] **Step 2: Replace the node declarations**

Change:
```dot
    "Final review clean: delete this plan's workspace" [shape=box];
    "Use superfunk:finishing-a-development-branch" [shape=box style=filled fillcolor=lightgreen];
```
To:
```dot
    "Final review clean" [shape=box];
    "Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate" [shape=box];
    "Finish: Lessons-learned, concept-index, bug-tracking, documentation check" [shape=box];
    "Delete this plan's workspace" [shape=box];
    "Use superfunk:finishing-a-development-branch" [shape=box style=filled fillcolor=lightgreen];
```

- [ ] **Step 3: Replace the edges**

Change:
```dot
    "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals" -> "Final review clean: delete this plan's workspace";
    "Final review clean: delete this plan's workspace" -> "Use superfunk:finishing-a-development-branch";
```
To:
```dot
    "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals" -> "Final review clean";
    "Final review clean" -> "Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate";
    "Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate" -> "Finish: Lessons-learned, concept-index, bug-tracking, documentation check";
    "Finish: Lessons-learned, concept-index, bug-tracking, documentation check" -> "Delete this plan's workspace";
    "Delete this plan's workspace" -> "Use superfunk:finishing-a-development-branch";
```

- [ ] **Step 4: Verify the old node is gone and the new sequence exists**

Run: `grep -c "Final review clean: delete this plan's workspace" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0`

Run: `grep -c "Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate\|Finish: Lessons-learned, concept-index, bug-tracking, documentation check" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `5` — verified by testing the exact new diagram text in isolation before writing this plan: each new node name appears on multiple lines (its own declaration, plus each edge line naming it as a source or target), and the one edge line connecting the two new nodes to each other matches both alternatives but still counts as a single line under `grep -c`.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "fix(skills): refresh subagent-driven-development's process diagram to depict Finish's bookkeeping sequence"
```

---

### Task 4: Full verification sweep

**Files:**
- No files modified — this task only verifies Tasks 1–3.

**Interfaces:**
- Consumes: the finished state of every file Tasks 1–3 touched.
- Produces: pass/fail evidence for every Falsifiable Criterion in the design spec. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — writing-plans**

Run: `grep -A5 "10. \*\*Verified numeric expectations" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's item 10 exactly.

Run: `grep -A5 "11. \*\*Template compliance" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's item 11 exactly.

- [ ] **Step 2: Verify Falsifiable Criterion 2 — brainstorming**

Run: `grep -A5 "6. \*\*Numeric-claim verification" plugin/skills/brainstorming/SKILL.md`
Expected: text matching the Decision block's item 6 exactly.

- [ ] **Step 3: Verify Falsifiable Criterion 3 — process diagram**

Run: `grep -c "Final review clean: delete this plan's workspace" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0`

Run: `grep -n "digraph process" -A 65 plugin/skills/subagent-driven-development/SKILL.md | grep "Finish:"`
Expected: 5 matches — the same 5 lines Task 3 Step 4 verifies, all inside the `digraph process` block specifically (not the prose Example Workflow further down the file, which this window doesn't reach). The block spans lines 48–113 (65 lines) after this task's edit — confirmed via `grep -n "digraph process\|^}"` — so `-A 60` undercounts by cutting off before the block's closing brace; `-A 65` is the verified-sufficient window.

- [ ] **Step 4: Verify Falsifiable Criterion 4 — total Finish: count**

Run: `grep -c "Finish:" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `13` (8 existing prose Example Workflow bracket lines, verified via direct grep before this plan's numeric claims got finalized, plus 5 new diagram lines — see Task 3 Step 4's note on why 5, not 2)

- [ ] **Step 5: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers Decision ¶1 (writing-plans items 10–11). Task 2 covers Decision ¶2 (brainstorming item 6). Task 3 covers Decision ¶3 (process diagram). Task 4 covers all four Falsifiable Criteria. No spec section lacks a task.

**Numeric-expectation catch (applying item 10 before it ships):** Task 3 Step 4 and Task 4 Step 4's first draft predicted the new diagram text would add 2 matching lines to a `grep -c "Finish:"` count, by assuming each new node name contributes one match. Testing the exact replacement text in isolation (both the fragment alone and a full simulated post-edit copy of the real file's digraph block) showed each node name actually appears on multiple lines — its own declaration plus every edge naming it as a source or target — contributing 5 matching lines, not 2. Both the design spec's own Falsifiable Criterion 4 and this plan's Task 3/Task 4 predictions got corrected (10 → 13 total) before execution, and the spec's correction got committed separately. Caught by running the real substitution against real file content, not by trusting the first mental count — the exact failure mode this sub-project's own item 10 exists to close.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A in the code sense — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** Task 1's new items 10 and 11 match items 1–9's exact formatting (bold numbered lead-in, one-paragraph explanation). Task 2's new item 6 matches items 1–5's exact formatting (plain numbered lead-in, matching brainstorming's own slightly different existing style — no bold number, unlike writing-plans). Checked both against their immediate sibling items before finalizing, not just against the design spec.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into each task's Step 2 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` and `docs/patterns/self-review-checks-own-required-template.md` before writing this plan — this plan's own header includes every required section (Goal, Architecture, Tech Stack, Global Constraints), checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before Task 1 even started, closing the exact gap this sub-project's own Task 1 fixes for future plans.

**8. Cross-section mechanism consistency:** Task 3 edits `subagent-driven-development/SKILL.md`'s process diagram, which describes the same Finish sequence the file's prose Example Workflow (lines 705–716) already depicts correctly. Grepped the full file for every other reference to "Final review clean," the old combined node name, and the Finish bookkeeping step names, plus the design spec, for any other passage describing this same mechanism. Found none beyond the diagram (now fixed) and the already-correct prose Example Workflow — no other passage needed a change. This plan traces to a design spec; a sentence confirming this check appears in the spec's Consequences section is unnecessary here since the spec's Consequences section already states the diagram now matches the prose Example Workflow, which is exactly what this check confirms.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — Task 3 corrects an illustration of an existing process to match what already happens, not a change to the process itself. No worked example needs a currency check as a result of this plan's own changes.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-28-process-review-recommendations-batch-3.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
