# Executing-Plans Review Step Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a whole-branch review step to `executing-plans` between task execution and Finish bookkeeping, closing the review-step half of F4 that R4's bookkeeping fix didn't reach.

**Architecture:** One new step ("Step 2.5: Whole-Branch Review") gets inserted into `plugin/skills/executing-plans/SKILL.md`, reusing `requesting-code-review`'s existing `code-reviewer.md` template when subagent dispatch works, falling back to the same rubric applied directly when it doesn't. Step 3's opening sentence gets one clause changed so the new ordering is unambiguous from the file's own text.

**Tech Stack:** Markdown skill file (`plugin/skills/executing-plans/SKILL.md`); no code, no test suite — verification is read-through plus grep, per this project's own convention for skill-content changes.

## Global Constraints

- The inserted Step 2.5 text and the Step 3 opening-line change must match the design spec's Decision block verbatim — do not paraphrase during implementation.
- Touch no content beyond what the spec's Decision section names. Do not edit Step 1, Step 2, or Step 4 beyond what's specified.
- Every grep verification command in this plan was run against a scratch copy of its own drafted insertion during plan-writing (per `writing-plans` Self-Review item 10's drafted-insertion check) — all anchors confirmed to survive insertion before this plan was finalized.

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user did not request pseudocode for any part of this plan.

---

### Task 1: Insert Step 2.5 and update Step 3's opening line

**Files:**
- Modify: `plugin/skills/executing-plans/SKILL.md:25-37`

**Interfaces:**
- Consumes: none.
- Produces: none — no later task in this plan depends on this edit.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "Step 2.5" plugin/skills/executing-plans/SKILL.md
grep -c "After all tasks complete and verified, and before Step 4, perform the" plugin/skills/executing-plans/SKILL.md
```
Expected: `0`, `1` (confirmed during plan-writing).

- [ ] **Step 2: Insert Step 2.5 between Step 2 and Step 3**

In `plugin/skills/executing-plans/SKILL.md`, find this exact block:

```markdown
### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Finish Bookkeeping

After all tasks complete and verified, and before Step 4, perform the
```

Replace it with:

```markdown
### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 2.5: Whole-Branch Review

After all tasks complete and verified, and before Step 3's bookkeeping,
review the whole branch — mirroring `subagent-driven-development`'s
Final Review, adapted for a session that may or may not have subagent
access:

1. **Documentation check:** If this plan traces to a design spec (named
   in the plan's Goal line or a task's commit trailer), run `python
   plugin/skills/documentation/scripts/check_docs.py <spec-file>
   <merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or `ALREADY_UPDATED`:
   continue. `ACTION_NEEDED`: invoke superfunk:documentation's Step 2 to
   draft the README/CHANGELOG update and commit it before continuing. No
   design spec: skip this check.
2. **Attempt to dispatch a reviewer.** Try dispatching a subagent on the
   most capable available model, using superfunk:requesting-code-review's
   [code-reviewer.md](../requesting-code-review/code-reviewer.md), with
   `BASE_SHA` = the commit before Step 1 began and `HEAD_SHA` = the
   current commit.
3. **No subagent dispatch available:** perform the same review yourself,
   directly — read the full diff between those two commits and apply
   `code-reviewer.md`'s own rubric (plan alignment, code quality,
   architecture, testing, production readiness) and Output Format
   (Strengths, Issues by severity, Recommendations, Assessment) as your
   own direct assessment, not a dispatched subagent's report.
4. **Findings:** append one line per finding to
   `docs/superpowers/process-reviews/notes.md`
   (`- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`), then
   fix all of them in one pass — not one fix per finding — and run
   exactly one scoped re-review of the fix diff (dispatched if possible,
   direct otherwise). Adjudicate any residual finding as
   `subagent-driven-development`'s Final Review does: park a contestable
   or non-load-bearing finding with a ruling, or stop and report to your
   human partner if it's load-bearing — with the same one-time exception
   for a regression the fix itself introduces (bounded to fire at most
   once, only for a defect the fix wave caused). There is no second fix
   wave for a finding the first wave simply failed to fix.
5. **Bug-tracking:** for each parked finding whose ruling calls it real
   rather than contestable, invoke superfunk:bug-tracking's Step 2 to
   record it in `docs/bugs/` before continuing — this is `executing-plans`'
   only opportunity to do so; nothing else in this skill preserves a
   deferred finding once the review above is done. No real-and-deferred
   parked findings: skip this step.

Only once this review is clean does Step 3 begin.

### Step 3: Finish Bookkeeping

After Step 2.5's review is clean, and before Step 4, perform the
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "Step 2.5" plugin/skills/executing-plans/SKILL.md
grep -c "After Step 2.5's review is clean" plugin/skills/executing-plans/SKILL.md
grep -c "After all tasks complete and verified, and before Step 4, perform the" plugin/skills/executing-plans/SKILL.md
```
Expected: `2` (the new heading plus Step 3's updated reference), `1`, `0`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/executing-plans/SKILL.md
git commit -m "feat(executing-plans): add Step 2.5 whole-branch review, closing F4's review-step gap"
```

---

### Task 2: Live trials for both review paths

**Files:**
- None modified — this task only verifies Task 1's edit via disposable trials, per the design spec's Falsifiable Criteria 4 and 5.

**Interfaces:**
- Consumes: Task 1's shipped edit to `plugin/skills/executing-plans/SKILL.md`.
- Produces: none.

- [ ] **Step 1: Trial the dispatch-available path (Criterion 4)**

Create a fresh scratch git repo and drive a small, real plan through `executing-plans` with subagent dispatch available (the normal in-session condition):

```bash
mkdir -p /tmp/sf-executing-plans-trial && cd /tmp/sf-executing-plans-trial && git init -q
mkdir -p docs/superpowers/plans
cat > docs/superpowers/plans/2026-09-02-trial-widget.md <<'PLANEOF'
# Trial Widget Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A trivial one-function module, used only to exercise executing-plans' new review step.

**Architecture:** Single file, single function.

**Tech Stack:** Python.

## Global Constraints

- None.

### Task 1: Add widget.py

**Files:**
- Create: `widget.py`

- [ ] **Step 1: Write widget.py**

```python
def widget():
    return "widget"
```

- [ ] **Step 2: Commit**

```bash
git add widget.py
git commit -m "feat: add widget"
```
PLANEOF
git add docs/superpowers/plans/2026-09-02-trial-widget.md
git commit -q -m "docs(plans): add trial widget plan"
claude -p --plugin-dir "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin" --dangerously-skip-permissions --output-format text "Use superfunk:executing-plans to execute docs/superpowers/plans/2026-09-02-trial-widget.md. Subagent dispatch is available in this environment."
```

Read the printed transcript (and, if the last-printed message doesn't show a dispatch, the session's `.jsonl` transcript directly — per this project's own documented `claude -p` last-message-only caveat) for evidence that Step 2.5 fired: a `Skill` or `Agent` dispatch using `code-reviewer.md`'s template, occurring after Task 1 completed and before any Status-flip or tracker-append bookkeeping.

Expected: the transcript shows a reviewer dispatch (or a direct self-performed review, if the harness declined to dispatch) between task completion and Step 3's bookkeeping — confirmed by reading the transcript, not assumed from a clean final message.

- [ ] **Step 2: Trial the no-dispatch path (Criterion 5)**

Reuse the same scratch repo. Re-run with dispatch unavailable simulated via an explicit instruction (the same technique this project's own disposable trials have used for simulating environment constraints):

```bash
cd /tmp/sf-executing-plans-trial
git checkout -q -- . 2>/dev/null; git clean -qfdx 2>/dev/null
claude -p --plugin-dir "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin" --dangerously-skip-permissions --output-format text "Use superfunk:executing-plans to execute docs/superpowers/plans/2026-09-02-trial-widget.md. Subagent dispatch is NOT available in this environment — you must perform Step 2.5's review yourself, directly, without attempting to dispatch a subagent."
```

Read the transcript for evidence Step 2.5 ran as a direct self-review: Strengths/Issues/Assessment-shaped output produced by the session itself, not a subagent dispatch, occurring before Step 3's bookkeeping.

Expected: the transcript shows a direct review (no `Skill`/`Agent` dispatch for the review itself) with the same Output Format shape `code-reviewer.md` specifies, before Step 3's bookkeeping runs.

- [ ] **Step 3: Clean up the scratch repo**

```bash
rm -rf /tmp/sf-executing-plans-trial
```

- [ ] **Step 4: Record trial results**

No commit for this task (it modifies no tracked files) — record both trials' outcomes in this plan's own outcomes file at Finish time, per the Outcome field convention.

---

## Self-Review

**1. Spec coverage:** Task 1 implements the spec's entire Decision section (Step 2.5's insertion, Step 3's opening-line change). Task 2 covers Falsifiable Criteria 4 and 5. Criteria 1–3 are satisfied directly by Task 1's own Step 3 verification (read-through equivalent via exact-block matching, plus the grep counts). No gap.

**2. Placeholder scan:** No "TBD"/"TODO"/"add appropriate" language. Every step shows exact before/after text or a complete, runnable command.

**3. Type consistency:** N/A — no code, no types or signatures span tasks.

**4. Pseudocode coverage:** All four triggers stated as `Skipped` with a real reason in the Pseudocode section above.

**5. Sibling-pattern parity:** Step 2.5 sits between two existing steps (Step 2, Step 3) in the same file. Checked its tone and structure against both neighbors: like Step 3, it uses a numbered sub-list for its internal items; like Step 1's "When to Stop and Ask for Help" cross-references, it names the skill it mirrors (`subagent-driven-development`'s Final Review) rather than restating that skill's full text. Consistent with the file's existing shape.

**6. Rule-restatement accuracy:** Step 2.5's fix-loop language ("one fix pass... exactly one scoped re-review... the same one-time exception for a regression the fix wave caused") restates `subagent-driven-development`'s Final Review fix-wave rule. Re-read that rule's actual current text (`plugin/skills/subagent-driven-development/SKILL.md` lines 534–554) side by side with this plan's restatement during plan-writing: both describe the same one-fix-pass-plus-one-re-review structure with the same bounded one-time regression exception. No narrowing or broadening found.

**7. Lessons-learned check:** Reviewed `docs/lessons-learned.md` for entries relevant to skill-file prose edits and verification-anchor drafting. The line-wrap verification-anchor lesson (taskq-trial-batch1-mechanical-fixes) applies directly — addressed by writing every drafted insertion to a scratch file and re-running its own grep before finalizing this plan (see the transcript above this plan; all six anchors confirmed before this document was written).

**8. Cross-section mechanism consistency:** Task 1 edits Step 3's own opening sentence, which describes when Step 3 fires relative to other steps — a lifecycle-ordering mechanism. Grepped `plugin/skills/executing-plans/SKILL.md` (the only file in this skill's directory besides `SKILL.md` itself is none — `executing-plans/` has no sibling top-level files) and the design spec for every other mention of "Step 3," "Step 4," and "Finish Bookkeeping": Step 4's own text ("After all tasks complete and verified" — its own independent phrasing, describing Step 4 relative to Step 3, not Step 2) does not describe the Step 2-to-Step-3 transition this edit changes, so it needs no update. No contradiction found. Per this item's own instruction, this plan traces to a design spec (`docs/superpowers/specs/2026-09-02-executing-plans-review-step-design.md`) — its Consequences section already covers why no other file needed a change (the fix is scoped entirely to `executing-plans/SKILL.md`), so no further spec edit is needed here.

**9. Worked-example currency:** `executing-plans/SKILL.md` has no worked-example section (unlike `subagent-driven-development`'s "Example Workflow"). N/A.

**10. Verified numeric expectations:** Every `Expected:` count above was verified by writing the exact drafted insertion to a scratch file and running the exact grep against it before finalizing this plan (shown in the tool output immediately preceding this plan's creation) — not estimated, and not carried over from the design spec's own prose.

**11. Template compliance:** This plan's header includes Goal, Architecture, Tech Stack, and Global Constraints, matching `writing-plans`' required header.

**12. User-facing documentation timing:** The spec's `User-Facing:` field reads `No` — this section does not apply.

**13. Hostile-input pass:** Task 1's edit is a static text replacement against a file already confirmed to contain the exact old-text block. The unhandled input class — the file changing underneath this plan between plan-writing and execution — is an accepted limitation: if Task 1's Step 2 can't find the exact block, that's a legitimate BLOCKED condition, not a defect in this plan. Task 2's trial commands assume `claude` resolves on PATH and the fork's plugin directory exists at the path given; if either assumption fails, the trial reports the failure directly rather than silently passing.

**14. Stale-workaround grep:** This plan doesn't remove a limitation, an unsupported case, or a manual step — it adds a new step. This item does not apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-02-executing-plans-review-step.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
