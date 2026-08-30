# Doc-Timing Fix and Mutation Check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the two highest-leverage findings from the external bookmark-cli trial — move the documentation check from Finish to a pre-final-review backstop while writing-plans bakes docs into the shipping task itself, and add a mutation check to the task-reviewer prompt.

**Architecture:** Three independent, additive edits to three existing skill files. Two files (`writing-plans/SKILL.md`, `task-reviewer-prompt.md`) gain new sections with no structural reshuffling. One file (`subagent-driven-development/SKILL.md`) has a mechanism relocated: a paragraph moves out of `## Finish` into a new opening paragraph of `## Final Review`, with matching updates to its process diagram and prose Example Workflow. No code, no tests in the software sense — every task verifies via direct read-back or `grep`.

**Tech Stack:** Markdown, Graphviz `dot` syntax (text only, not rendered), `grep`, a disposable `--plugin-dir` trial for the mutation check.

## Global Constraints

- Every new section and Self-Review item's wording must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criteria 1, 4).
- The existing Finish-section documentation-check paragraph must not remain anywhere in `subagent-driven-development/SKILL.md` after this plan — it moves, it doesn't duplicate (per spec Falsifiable Criterion 2).
- The process diagram's new node and the prose Example Workflow's relocated bracket line must both reflect the check running before the final reviewer dispatch, not after (per spec Falsifiable Criterion 3).
- No file outside `plugin/skills/writing-plans/SKILL.md`, `plugin/skills/subagent-driven-development/SKILL.md`, and `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` gets modified.

---

## File Structure

Directories touched: `plugin/skills/writing-plans/`, `plugin/skills/subagent-driven-development/`. Checked both for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`), so no directory context to read.

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/writing-plans/SKILL.md` — add `User-Facing Documentation Timing` section and Self-Review item 12
- `plugin/skills/subagent-driven-development/SKILL.md` — move the documentation check from `## Finish` to `## Final Review`; update the process diagram; update the prose Example Workflow
- `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — add `## Mutation Check` section and its Output Format subsection

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds or relocates Markdown/Graphviz text.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add User-Facing Documentation Timing to writing-plans

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the new plan-writing requirement every future `User-Facing: Yes` spec's plan checks against, and the Self-Review item verifying it. Task 4's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm the current Task Right-Sizing / Bite-Sized Task Granularity boundary**

Run: `grep -n "^## Task Right-Sizing\|^## Bite-Sized Task Granularity" plugin/skills/writing-plans/SKILL.md`
Expected: two matches, confirming where the new section gets inserted between them.

- [ ] **Step 2: Insert the new section**

Change:
```markdown
## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## Bite-Sized Task Granularity
```
To:
```markdown
## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## User-Facing Documentation Timing

If the spec carries `User-Facing: Yes`, the task whose deliverable adds
or changes that user-facing surface must include its own step running
`python plugin/skills/documentation/scripts/check_docs.py <spec-file>
<task-base-sha> <task-head-sha>` and, if it reports `ACTION_NEEDED`,
drafting the README/CHANGELOG update — in that same task, committed
alongside the surface it documents. Never defer this to a separate later
task or to Finish: a reviewer who reaches the final whole-branch review
before the docs exist reviews a branch that contradicts its own README
by construction.

## Bite-Sized Task Granularity
```

- [ ] **Step 3: Append Self-Review item 12**

Change:
```markdown
**11. Template compliance:** Does this plan's own document header
match every element the Plan Document Header section above requires
(Goal, Architecture, Tech Stack, Global Constraints)? A required
section silently missing from this plan's own header counts as the
same class of gap as a missing task for a spec requirement.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```
To:
```markdown
**11. Template compliance:** Does this plan's own document header
match every element the Plan Document Header section above requires
(Goal, Architecture, Tech Stack, Global Constraints)? A required
section silently missing from this plan's own header counts as the
same class of gap as a missing task for a spec requirement.

**12. User-facing documentation timing:** If the spec carries
`User-Facing: Yes`, does the task shipping the user-facing surface
include its own documentation step, per the section above? A plan that
defers this to a separate task or relies on Finish to catch it repeats
the same class of gap this item exists to close.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 4: Verify both additions landed**

Run: `grep -c "User-Facing Documentation Timing" plugin/skills/writing-plans/SKILL.md`
Expected: `1` — the `##` heading line only. Item 12's own heading text uses lowercase "facing" ("User-facing documentation timing"), a distinct case-sensitive string that doesn't match this pattern; checked by inspecting the exact text about to be inserted, not assumed.

Run: `grep -c "User-facing documentation timing" plugin/skills/writing-plans/SKILL.md`
Expected: `1` (item 12's own heading text, lowercase "facing" — distinct string from the `##` section title above)

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): add User-Facing Documentation Timing section and Self-Review item 12 to writing-plans"
```

---

### Task 2: Move the documentation check from Finish to a pre-final-review backstop

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 1 (an independent skill file, though conceptually the two now work together).
- Produces: the corrected `## Final Review` section, `digraph process` block, and prose Example Workflow. Task 4's verification depends on this task's exact wording and positioning.

- [ ] **Step 1: Confirm the current Finish-section paragraph's exact text before removing it**

Run: `grep -n "If this plan traces to a design spec (per the Status-flip check" plugin/skills/subagent-driven-development/SKILL.md`
Expected: one match, at line 614 (confirmed via direct read this session — re-verify the line number hasn't shifted before editing, since earlier tasks in this plan don't touch this file, so it shouldn't have moved).

- [ ] **Step 2: Remove the Finish-section documentation-check paragraph**

Change:
```markdown
If this plan traces to a design spec (per the Status-flip check
above), run `python plugin/skills/documentation/scripts/check_docs.py
<spec-file> <merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or
`ALREADY_UPDATED`: skip the rest of this step. `ACTION_NEEDED`:
invoke superfunk:documentation's Step 2 to draft the README/CHANGELOG
update from the printed spec content. No design spec: skip this step
entirely — nothing to read a `User-Facing` field from.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```
To:
```markdown
Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

- [ ] **Step 3: Add the pre-final-review documentation check as the opening of Final Review**

Change:
```markdown
## Final Review

The final whole-branch review gets a package too: run
```
To:
```markdown
## Final Review

Before dispatching the final reviewer, check whether this plan traces to
a design spec (named in the plan's Goal line or a task's commit trailer,
e.g. "Part of docs/superpowers/specs/..."). If it does, run `python
plugin/skills/documentation/scripts/check_docs.py <spec-file>
<merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or `ALREADY_UPDATED`:
continue to dispatch below — the feature task already handled this, per
writing-plans' User-Facing Documentation Timing requirement.
`ACTION_NEEDED`: invoke superfunk:documentation's Step 2 to draft the
README/CHANGELOG update from the printed spec content, commit it, and
only then dispatch the final reviewer. No design spec: skip this check
entirely. Running this before the final reviewer sees the branch means a
gap the plan's own task missed still gets caught before the most
expensive review runs, not after.

The final whole-branch review gets a package too: run
```

- [ ] **Step 4: Update the process diagram — node declarations**

Change:
```dot
    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" [shape=box];
```
To:
```dot
    "Pre-final-review doc check: check_docs.py, draft if ACTION_NEEDED" [shape=box];
    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" [shape=box];
```

- [ ] **Step 5: Update the process diagram — edges**

Change:
```dot
    "More tasks remain?" -> "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" [label="no"];
    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" -> "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals";
```
To:
```dot
    "More tasks remain?" -> "Pre-final-review doc check: check_docs.py, draft if ACTION_NEEDED" [label="no"];
    "Pre-final-review doc check: check_docs.py, draft if ACTION_NEEDED" -> "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)";
    "Dispatch final code reviewer (../requesting-code-review/code-reviewer.md)" -> "Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals";
```

- [ ] **Step 6: Update the prose Example Workflow — move the documentation bracket line**

Change:
```markdown
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
[Finish: this plan's spec has no User-Facing field set to Yes -- documentation step skipped]

[Delete this plan's workspace — the record now lives in git]

Done! Using superfunk:finishing-a-development-branch.
```
To:
```markdown
[After all tasks]
[Pre-final-review doc check: this plan's spec has no User-Facing field set to Yes -- check skipped]
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

Done! Using superfunk:finishing-a-development-branch.
```

- [ ] **Step 7: Verify the relocation landed correctly**

Run: `grep -c "If this plan traces to a design spec (per the Status-flip check" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0` (the old Finish-section paragraph no longer exists — the new Final Review paragraph uses different opening wording, "Before dispatching the final reviewer, check whether...")

Run: `grep -c "Pre-final-review doc check: check_docs.py, draft if ACTION_NEEDED" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `3` (the digraph's one node declaration plus its two edges — verified by testing this exact substitution against a full copy of the real file before finalizing this plan)

Run: `grep -c "Finish:" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `12` (13 before this task's edit, minus 1 for the renamed bracket line that no longer starts with "Finish:" — verified via direct grep against the real file before finalizing this plan)

- [ ] **Step 8: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "fix(skills): move documentation check from Finish to a pre-final-review backstop in subagent-driven-development"
```

---

### Task 3: Add the Mutation Check to task-reviewer-prompt

**Files:**
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`

**Interfaces:**
- Consumes: nothing from Tasks 1–2 (an independent file).
- Produces: the new reviewer requirement every future task review checks against. Task 4's live-trial verification depends on this task's exact wording.

- [ ] **Step 1: Confirm the current Tests / Part 1 boundary**

Run: `grep -n "## Tests$\|## Part 1: Spec Compliance" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: two matches, confirming where the new section gets inserted between them. (Unanchored at the start: this file's headings sit inside an indented code-fence template, 4 spaces in, so a `^##`-anchored pattern returns nothing — confirmed by running the anchored version first and getting zero matches before switching to this unanchored form.)

- [ ] **Step 2: Insert the Mutation Check section**

Change:
```markdown
    Warnings or other noise in the implementer's reported test output are
    findings — test output should be pristine.

    ## Part 1: Spec Compliance
```
To:
```markdown
    Warnings or other noise in the implementer's reported test output are
    findings — test output should be pristine.

    ## Mutation Check

    For each new test in this diff that asserts a load-bearing property — an
    edge case, an invariant, a boundary condition, or any assertion the plan
    or spec treats as a correctness guarantee, not a trivial "returns X"
    check — revert the specific implementation line(s) the test claims to
    guard, run that one test, confirm it fails (goes red), then restore the
    code to its exact prior state. A test that stays green after reverting
    its guarded line cannot actually catch the regression it claims to
    guard against — report it as an Important finding, not a footnote.
    Skip this check only for a test with no clear guarded line to revert (a
    pure smoke test, for example) and say so.

    ## Part 1: Spec Compliance
```

- [ ] **Step 3: Add the Mutation Check Output Format subsection**

Change:
```markdown
    ### Strengths
    [What's well done? Be specific.]

    ### Issues
```
To:
```markdown
    ### Strengths
    [What's well done? Be specific.]

    ### Mutation Check

    For each load-bearing test mutated: file:line, the line reverted, and
    whether the test went red (✅) or stayed green (❌ — filed as an
    Important finding above).

    ### Issues
```

- [ ] **Step 4: Verify both additions landed**

Run: `grep -c "Mutation Check" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: `2` — both headings sit inside an indented code-fence template (4 spaces), so an anchored `^##`/`^###` pattern doesn't match; verified by running the anchored version first (got 0, unexpectedly) and the unanchored version against the real file before finalizing this check.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat(skills): add Mutation Check to task-reviewer-prompt"
```

---

### Task 4: Full verification sweep and live trial

**Files:**
- No files modified — this task only verifies Tasks 1–3.

**Interfaces:**
- Consumes: the finished state of every file Tasks 1–3 touched.
- Produces: pass/fail evidence for every Falsifiable Criterion in the design spec. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — writing-plans**

Run: `grep -A9 "^## User-Facing Documentation Timing" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's section exactly.

Run: `grep -A4 "12. \*\*User-facing documentation timing" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's item 12 exactly.

- [ ] **Step 2: Verify Falsifiable Criterion 2 — Final Review / Finish**

Run: `grep -A11 "^## Final Review" plugin/skills/subagent-driven-development/SKILL.md`
Expected: text matching the Decision block's new opening paragraph exactly.

Run: `grep -c "If this plan traces to a design spec (per the Status-flip check" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0`

- [ ] **Step 3: Verify Falsifiable Criterion 3 — diagram and prose ordering**

Run: `grep -n "Pre-final-review doc check\|dispatch final code-reviewer" plugin/skills/subagent-driven-development/SKILL.md`
Expected: every `Pre-final-review doc check` line number appears before its corresponding `Dispatch final code reviewer` / `dispatch final code-reviewer` line number, both in the digraph block and in the prose Example Workflow.

- [ ] **Step 4: Verify Falsifiable Criterion 4 — task-reviewer-prompt**

Run: `grep -A11 "## Mutation Check" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: text matching the Decision block's section exactly (both the `##` and `###` headings, since the pattern isn't anchored and the file indents both 4 spaces inside its template code fence).

- [ ] **Step 5: Verify Falsifiable Criterion 5 — live trial**

Set up a disposable fixture in a scratch directory: a task branch containing one Python function with an intentional off-by-one boundary bug and a test that happens to pass despite it (e.g., a function meant to reject `n < 0` that actually checks `n < 1`, paired with a test that only exercises `n = 0` and `n = 5`, never `n = -1`... construct the fixture so the existing test genuinely passes against the bug, matching the trial's own `test_read_is_capped` shape).

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Use the superfunk:subagent-driven-development skill's task-reviewer-prompt.md template to review this fixture task's diff for spec compliance and code quality, including the Mutation Check section." --add-dir <fixture-path>
```

Expected: the reviewer's output includes a `### Mutation Check` section reporting the boundary test mutated, and flags it as an Important finding for staying green after the guarded line got reverted — confirming the check fires and works end-to-end, not just that the prompt text exists.

- [ ] **Step 6: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers Decision ¶1–2 (writing-plans section and item 12). Task 2 covers Decision ¶3–5 (Final Review paragraph, digraph, prose Example Workflow, Finish removal). Task 3 covers Decision ¶6–7 (Mutation Check section and Output Format subsection). Task 4 covers all five Falsifiable Criteria. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A in the code sense — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** Task 1's new `## User-Facing Documentation Timing` section matches its siblings' heading level and prose-paragraph shape (no bullet list, matching `## Task Right-Sizing` immediately above it, not `## Pseudocode`'s bulleted style). Item 12 matches items 1–11's exact bold-numbered-lead-in format. Task 3's `## Mutation Check` section matches `## Tests`' plain-prose shape, and its Output Format subsection matches `### Strengths`' single-paragraph-instruction shape, not the bulleted `### Issues` severity-tier shape.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into each task's Step 2/3 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` before writing this plan, in particular the newly-added entry on self-referential numeric-verification misses (2026-08-28-process-review-recommendations-batch-3) — applied directly: every numeric claim in this plan's Task 2 and Task 4 (the `3` and `12` counts) got verified by testing the exact substitution against a real or scratch copy of the target file before being written down, not estimated.

**8. Cross-section mechanism consistency:** Task 2 edits `subagent-driven-development/SKILL.md`'s documentation-check mechanism, which the file describes in three places: the `## Finish` prose (removed), the `digraph process` block (updated), and the prose Example Workflow (updated). Grepped the full file for every other mention of "check_docs.py", "documentation", and "ACTION_NEEDED" beyond these three spots, plus the design spec, to confirm no fourth description exists that this task would leave stale. Found none — `writing-plans/SKILL.md`'s new Task 1 section describes a different point in the mechanism (the task-level check, not the pre-final-review backstop) and doesn't contradict Task 2's change. This plan traces to a design spec; the spec's own Consequences section already explains why the Finish-time check remains as a backstop rather than being removed entirely, which is exactly what this check confirms holds true.

**9. Worked-example currency:** Task 2 reorders a step in Finish's documented bookkeeping sequence (the documentation check moves out of Finish entirely, into Final Review). The prose Example Workflow demonstrates this exact sequence and gets updated in the same task (Step 6) to match — closing the loop item 9 exists to close.

**10. Verified numeric expectations:** Every `Expected:` count in Task 2 and Task 4 (the `0`, `3`, and `12` values) was confirmed by running the actual grep or a scratch-file substitution test against real file content before being written into this plan — not estimated. See the notes embedded in Task 2 Step 7's expected-value explanations.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-doc-timing-and-mutation-check.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
