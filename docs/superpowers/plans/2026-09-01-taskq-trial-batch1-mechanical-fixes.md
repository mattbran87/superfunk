# Taskq Trial Batch 1 — Mechanical Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the 8 cheap/mechanical fixes from `docs/superpowers/specs/2026-09-01-taskq-trial-batch1-mechanical-fixes-design.md` (F9.3, F13, F14, F1, F3a, F7, F2, F2a).

**Architecture:** Each task edits one or two skill files with an exact, pre-verified text replacement, then runs a grep to confirm the new text landed and the old text (where replaced) is gone. F14 also creates one new pattern file. No production code, no test suite — verification is read-through plus grep, per the spec's own Falsifiable Criteria.

**Tech Stack:** Markdown skill files under `plugin/skills/`; one new file under `docs/patterns/`.

## Global Constraints

- Every edit's new text must match its Decision block in the design spec verbatim — do not paraphrase during implementation.
- Before editing, confirm the exact old-text block appears exactly once in the target file (already confirmed during plan-writing below) — an Edit against non-unique old text fails or, worse, matches the wrong occurrence.
- Touch no content beyond what each task names. Do not fix unrelated wording noticed along the way — file it as a separate observation instead.
- No task in this plan produces or consumes a runtime interface — every task is an independent documentation edit.

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user did not request pseudocode for any part of this plan.

---

### Task 1: `brainstorming` scaffold-offer — F9.3 Format-block sentence + F1 skip conditions

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md:70-81`

**Interfaces:**
- Consumes: none.
- Produces: none — no later task depends on this edit.

- [ ] **Step 1: Confirm baseline (new text absent, old text present and unique)**

Run:
```bash
grep -c "Format block verbatim" plugin/skills/brainstorming/SKILL.md
grep -c "already establishes them observably" plugin/skills/brainstorming/SKILL.md
grep -c "ask up to three questions, one at a time" plugin/skills/brainstorming/SKILL.md
```
Expected: `0`, `0`, `1` (confirmed during plan-writing).

- [ ] **Step 2: Edit the scaffold-offer bullet**

In `plugin/skills/brainstorming/SKILL.md`, find this exact block (inside the "Understanding the idea" bullet list):

```markdown
- Check for a `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` at the project
  root, and for `docs/ai-code-guidelines.md`. If either is missing,
  offer once (ask-don't-force, never blocking): "This project has no
  [instructions file for AI agents / coding conventions doc] yet.
  Want me to scaffold a starter version from a few quick questions
  before we continue?" If accepted, ask up to three questions, one at
  a time: the project's language/stack (skip if already evident from
  existing files), any coding conventions already followed informally,
  and anything future sessions should know upfront (build/test
  commands, architecture notes). Draft whichever file(s) were missing
  from the answers, commit them, then continue. If declined, or both
  files already exist, proceed without further mention.
```

Replace it with:

```markdown
- Check for a `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` at the project
  root, and for `docs/ai-code-guidelines.md`. If either is missing,
  offer once (ask-don't-force, never blocking): "This project has no
  [instructions file for AI agents / coding conventions doc] yet.
  Want me to scaffold a starter version from a few quick questions
  before we continue?" If accepted, ask up to three questions, one at
  a time: the project's language/stack (skip if already evident from
  existing files), any coding conventions already followed informally
  (skip if a linter or formatter config already establishes them
  observably), and anything future sessions should know upfront —
  build/test commands, architecture notes (ask this one outright on a
  new or near-empty repo; observation cannot substitute for it there).
  Draft whichever file(s) were missing from the answers, commit them,
  then continue. If drafting `docs/ai-code-guidelines.md`, its
  Per-Directory Context Files section must copy this project's own
  Format block verbatim (the `**Purpose:**` bold line, not a
  `## Purpose` heading or any other paraphrase) — this is the exact
  line `concept-index` parses, so the two halves stay in sync by
  construction rather than by chance. If declined, or both files
  already exist, proceed without further mention.
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "Format block verbatim" plugin/skills/brainstorming/SKILL.md
grep -c "already establishes them observably" plugin/skills/brainstorming/SKILL.md
grep -c "ask this one outright" plugin/skills/brainstorming/SKILL.md
```
Expected: `1`, `1`, `1`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "fix(brainstorming): add skip conditions to scaffold questions, pin .context.md template (F1, F9.3)"
```

---

### Task 2: `writing-plans` Self-Review item 10 — F13 numeric-budget scope

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md:238-247`

**Interfaces:**
- Consumes: none.
- Produces: none.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "also covers any numeric budget" plugin/skills/writing-plans/SKILL.md
grep -c "re-discovering the same trap." plugin/skills/writing-plans/SKILL.md
```
Expected: `0`, `1` (confirmed during plan-writing — item 10 currently ends on this exact sentence).

- [ ] **Step 2: Edit item 10**

In `plugin/skills/writing-plans/SKILL.md`, find this exact block:

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

Replace it with:

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
re-discovering the same trap. This item's scope also covers any
numeric budget the plan's Global Constraints section states — a
line-count ceiling, a performance target, a size limit. Sum each
task's own added or changed line counts against a stated ceiling
before finalizing the plan; a budget nobody checked against the
plan's own arithmetic counts as the same failure as an unchecked
`Expected:` value.
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "also covers any numeric budget" plugin/skills/writing-plans/SKILL.md
```
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "fix(writing-plans): widen Self-Review item 10 to asserted budgets, not just enumerated counts (F13)"
```

---

### Task 3: Task reviewer's token-containment trap + new pattern file — F14

**Files:**
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md:88-95`
- Create: `docs/patterns/assert-on-a-token-the-context-cannot-supply.md`

**Interfaces:**
- Consumes: none.
- Produces: `docs/patterns/assert-on-a-token-the-context-cannot-supply.md`, which Task 3's own edit cross-references. No later task in this plan depends on it.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "already supplies that token" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
ls docs/patterns/assert-on-a-token-the-context-cannot-supply.md
```
Expected: `0`; `ls` reports the file does not exist (confirmed during plan-writing).

- [ ] **Step 2: Edit the Mutation Check section**

In `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`, find this exact block:

```markdown
    Skip this check only for a test with no clear guarded line to revert (a
    pure smoke test, for example) and say so. A related trap: a test
    comparing two strings with `in` (substring containment) instead of
    `==` can look like it asserts equality while accepting anything one
    string contains the other — if a comparison the plan or spec treats
    as an equality guarantee uses `in`, flag it even if its own mutation
    check passes, since containment can stay true across a mutation that
    breaks the equality the test actually meant to pin.
```

Replace it with:

```markdown
    Skip this check only for a test with no clear guarded line to revert (a
    pure smoke test, for example) and say so. A related trap: a test
    comparing two strings with `in` (substring containment) instead of
    `==` can look like it asserts equality while accepting anything one
    string contains the other — if a comparison the plan or spec treats
    as an equality guarantee uses `in`, flag it even if its own mutation
    check passes, since containment can stay true across a mutation that
    breaks the equality the test actually meant to pin. A second related
    trap: an assertion that a document or output contains a specific
    token can pass today only because something else in the same
    content already supplies that token — deleting the exact thing the
    assertion exists to protect then leaves it green. For any assertion
    of this shape, check whether the asserted token already appears
    elsewhere in the same content, independent of the mutation check
    above. See docs/patterns/assert-on-a-token-the-context-cannot-supply.md.
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "already supplies that token" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
```
Expected: `1`.

- [ ] **Step 4: Create the pattern file**

Create `docs/patterns/assert-on-a-token-the-context-cannot-supply.md`:

```markdown
# Assert on a Token the Context Cannot Supply

A containment assertion (`"X" in output`) that stays green after deleting
the thing it guards, because the surrounding content already supplies `X`
some other way.

## Context

A guard checks that a document, output, or diff contains some specific
word or flag, chosen to avoid pinning exact wording. This applies whenever
a plan or reviewer writes a "contains" assertion instead of an equality
assertion.

## Pattern

For every assertion that content contains a chosen token, check whether
that token — or a superstring/synonym of it — already appears elsewhere in
the same content before the guarded change ships. If it does, the
assertion cannot discriminate the guarded change from its absence; either
pick a token that appears nowhere else, or assert on the specific location
(a line number, a section) instead of a bare substring search.

## Example

A README guard asserted `"JSON" in section`, chosen as a "distinctive
noun" to avoid pinning wording. The same section already contained
`"JSON-serializable"` one line above the bullet the guard existed to
protect — deleting that bullet left the assertion green, because the
neighboring word alone satisfied it.

## Originating lessons

- "Non-discriminating containment guards" (taskq-trial-batch1-mechanical-fixes)
```

- [ ] **Step 5: Verify the file exists with all required sections**

Run:
```bash
grep -c "^## " docs/patterns/assert-on-a-token-the-context-cannot-supply.md
```
Expected: `4` (Context, Pattern, Example, Originating lessons).

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/subagent-driven-development/task-reviewer-prompt.md docs/patterns/assert-on-a-token-the-context-cannot-supply.md
git commit -m "fix(subagent-driven-development): name the token-containment guard trap, promote pattern (F14)"
```

---

### Task 4: `finishing-a-development-branch` Step 7 — F3a recognize `.claude/worktrees/`

**Files:**
- Modify: `plugin/skills/finishing-a-development-branch/SKILL.md:191-197`

**Interfaces:**
- Consumes: none.
- Produces: none.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "\.claude/worktrees/" plugin/skills/finishing-a-development-branch/SKILL.md
grep -c "Superpowers$" plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `0`, `0` — the literal old text is `Superpowers` followed by a line break, not end-of-line; use Step 2's exact block match instead of relying on this second check. (This second grep is a sanity check only, not a gate.)

- [ ] **Step 2: Edit Step 7**

In `plugin/skills/finishing-a-development-branch/SKILL.md`, find this exact block:

```markdown
**If `WORKTREE_PATH` is under `.worktrees/` or `worktrees/`:** Superpowers
created this worktree — we own cleanup:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```
```

Replace it with:

```markdown
**If `WORKTREE_PATH` is under `.worktrees/`, `worktrees/`, or
`.claude/worktrees/`:** Superpowers created this worktree — we own
cleanup. If a native worktree-exit tool created it (the same one
`using-git-worktrees` used to enter it), try that tool first — it owns
placement and branching, so it is the matching way back out. Fall back to
the manual commands below only if no native exit tool exists, or it
fails:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "\.claude/worktrees/" plugin/skills/finishing-a-development-branch/SKILL.md
grep -c "native worktree-exit tool created it" plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `1`, `1`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/finishing-a-development-branch/SKILL.md
git commit -m "fix(finishing-a-development-branch): recognize .claude/worktrees/, prefer native exit tool (F3a)"
```

---

### Task 5: `finishing-a-development-branch` Option 2 — F7 forge-confirmation sentence

**Files:**
- Modify: `plugin/skills/finishing-a-development-branch/SKILL.md:135-148`

**Interfaces:**
- Consumes: none — independent of Task 4's edit to the same file (different section, non-overlapping line range).
- Produces: none.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "Confirm the forge CLI actually created a PR" plugin/skills/finishing-a-development-branch/SKILL.md
grep -c "Keep the worktree — your human partner iterates on PR feedback there." plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `0`, `1`.

- [ ] **Step 2: Edit Option 2**

In `plugin/skills/finishing-a-development-branch/SKILL.md`, find this exact block:

```markdown
Then create the pull/merge request against <base-branch> with the forge's
tooling — its CLI if one is available, or the creation URL most forges
print when you push — following the repo's PR template and conventions if
present, and report the URL to your human partner.

Keep the worktree — your human partner iterates on PR feedback there.
```

Replace it with:

```markdown
Then create the pull/merge request against <base-branch> with the forge's
tooling — its CLI if one is available, or the creation URL most forges
print when you push — following the repo's PR template and conventions if
present, and report the URL to your human partner.

Confirm the forge CLI actually created a PR — its exit status and printed
URL — before reporting one back to your human partner; a successful push
alone does not mean a PR exists. If the repository has no forge remote (a
bare or local-only `origin`), say so plainly and stop after the push.

Keep the worktree — your human partner iterates on PR feedback there.
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "Confirm the forge CLI actually created a PR" plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/finishing-a-development-branch/SKILL.md
git commit -m "fix(finishing-a-development-branch): require confirming a PR actually exists before reporting success (F7)"
```

---

### Task 6: `subagent-driven-development` Finish — F2 disambiguate "merged"

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md:558`

**Interfaces:**
- Consumes: none.
- Produces: none.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "its fixes are merged" plugin/skills/subagent-driven-development/SKILL.md
grep -c "fix wave's commits sit" plugin/skills/subagent-driven-development/SKILL.md
```
Expected: `1`, `0` (confirmed during plan-writing).

- [ ] **Step 2: Edit the Finish section's opening sentence**

In `plugin/skills/subagent-driven-development/SKILL.md`, find this exact text:

```markdown
When the final whole-branch review is clean and its fixes are merged,
check whether this plan traces to a design spec (named in the plan's
Goal line or a task's commit trailer, e.g. "Part of
docs/superpowers/specs/..."). If it does, update that spec's `Status`
```

Replace it with:

```markdown
When the final whole-branch review is clean and its fix wave's commits sit
on this branch — not yet merged to the base branch, which
`finishing-a-development-branch` handles afterward — check whether this
plan traces to a design spec (named in the plan's Goal line or a task's
commit trailer, e.g. "Part of docs/superpowers/specs/..."). If it does,
update that spec's `Status`
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "fix wave's commits sit" plugin/skills/subagent-driven-development/SKILL.md
grep -c "its fixes are merged" plugin/skills/subagent-driven-development/SKILL.md
```
Expected: `1`, `0`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "fix(subagent-driven-development): clarify Finish's 'merged' means on-branch, not merged to base (F2)"
```

---

### Task 7: `finishing-a-development-branch` Overview — F2a bookkeeping-responsibility sentence

**Files:**
- Modify: `plugin/skills/finishing-a-development-branch/SKILL.md:8-12`

**Interfaces:**
- Consumes: none — independent of Tasks 4 and 5's edits to the same file (different section, non-overlapping line range).
- Produces: none.

- [ ] **Step 1: Confirm baseline**

Run:
```bash
grep -c "Spec-Status and process-review-tracker bookkeeping is the dispatching" plugin/skills/finishing-a-development-branch/SKILL.md
grep -c "Announce at start: \"I'm using the finishing-a-development-branch skill to complete this work.\"" plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `0`, `1`.

- [ ] **Step 2: Edit the Overview section**

In `plugin/skills/finishing-a-development-branch/SKILL.md`, find this exact block:

```markdown
**Core principle:** Verify tests → Detect environment → Offer review → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."
```

Replace it with:

```markdown
**Core principle:** Verify tests → Detect environment → Offer review → Present options → Execute choice → Clean up.

Spec-Status and process-review-tracker bookkeeping is the dispatching
skill's job (`subagent-driven-development`'s Finish section), and it runs
before this skill gets invoked — none of the 3 options below repeat it.
Arriving here from a path that skips that Finish step (a manual merge, or
`superfunk:executing-plans`, which has no Finish step of its own) means
that bookkeeping has not happened; flag this to your human partner rather
than assuming it already did.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."
```

- [ ] **Step 3: Verify the edit landed**

Run:
```bash
grep -c "Spec-Status and process-review-tracker bookkeeping is the dispatching" plugin/skills/finishing-a-development-branch/SKILL.md
```
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/finishing-a-development-branch/SKILL.md
git commit -m "fix(finishing-a-development-branch): state the bookkeeping-responsibility boundary in Overview (F2a)"
```

---

## Self-Review

**1. Spec coverage:** Task 1 covers F9.3 and F1; Task 2 covers F13; Task 3 covers F14 (both the sentence and the pattern file); Task 4 covers F3a; Task 5 covers F7; Task 6 covers F2; Task 7 covers F2a. All 8 findings from the spec's Decision section have a task. No gaps.

**2. Placeholder scan:** No "TBD"/"TODO"/"add appropriate" language anywhere in this plan. Every step shows the exact old and new text, not a description of the change.

**3. Type consistency:** N/A — no code, no types or function signatures span tasks.

**4. Pseudocode coverage:** All four triggers stated as `Skipped` with a real reason (no API calls, no handler reuse, no DTO shapes, no user-designated pseudocode) in the Pseudocode section above.

**5. Sibling-pattern parity:** Task 4, 5, and 7 each add a sentence next to an existing sibling instruction in `finishing-a-development-branch/SKILL.md`. Checked each against its neighbors: Task 4's addition matches Step 7's existing terse, instruction-only tone; Task 5's matches Option 2's existing prose style; Task 7's matches the Overview's existing one-line declarative style. No mismatch found.

**6. Rule-restatement accuracy:** This plan's task text restates the spec's Decision blocks in six different target files. Each restatement is a verbatim copy of the spec's own Decision block (re-checked side by side against `docs/superpowers/specs/2026-09-01-taskq-trial-batch1-mechanical-fixes-design.md` while writing this plan) — none narrows, broadens, or drops scope from the spec.

**7. Lessons-learned check:** Reviewed `docs/lessons-learned.md` for entries relevant to editing skill-file prose or promoting patterns. The existing entries on quote/count verification (behind `docs/patterns/verify-plan-commands-against-real-content.md` and `docs/patterns/re-verify-quotes-against-source-before-citing.md`) already apply and were followed while writing this plan — every grep count above is a real, just-run result, and every quoted old-text block was re-read from the live file, not carried over from the spec's own quotes.

**8. Cross-section mechanism consistency:** Task 6 edits Finish's own trigger language ("merged"). Grepped `subagent-driven-development/SKILL.md` for every other mention of "merged" relative to Finish/branch integration: the `digraph process` node labels, the Final Review section's fix-wave text, and the Example Workflow use "merged" only in senses unaffected by this edit (branch integration happens in `finishing-a-development-branch`, referenced separately). No contradiction found; no spec update needed since none of those other mentions describe the same mechanism this edit clarifies.

**9. Worked-example currency:** Checked `subagent-driven-development/SKILL.md`'s Example Workflow (the `[Finish: ...]` bracket lines near the end) against Task 6's edit — the worked example doesn't quote the "merged" sentence itself, only summarizes Finish's outcomes, so it needs no update.

**10. Verified numeric expectations:** Every `Expected:` value above (Task 1's three greps, Task 2's two, Task 3's two plus the `## ` count of 4, Task 4's two, Task 5's two, Task 6's two, Task 7's two) reflects a command actually run against the live files during plan-writing, shown in the tool output above this plan — not an estimate.

**11. Template compliance:** This plan's header includes Goal, Architecture, Tech Stack, and Global Constraints, matching `writing-plans`' required header.

**12. User-facing documentation timing:** The spec's `User-Facing:` field reads `No` — this section does not apply.

**13. Hostile-input pass:** Every task in this plan is a static text replacement against a file already confirmed to exist and already confirmed to contain the exact old-text block exactly once. The class of input this doesn't handle — the target file changing between plan-writing and execution (a concurrent edit) — is accepted as a limitation: if an implementer's Step 2 fails to find the exact old-text block, that is a legitimate BLOCKED condition (the file changed underneath the plan), not a defect in this plan; the implementer should stop and report rather than guess at a fuzzy match.

**14. Stale-workaround grep:** No task in this plan removes a limitation, an unsupported case, or a manual step — every task adds a sentence or a new check. This item does not apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-01-taskq-trial-batch1-mechanical-fixes.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
