# Process Review Recommendations (Batch 2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the first two open Recommendations from `docs/superpowers/process-reviews/review-after-2026-08-25-concept-index-design.md` — per `docs/superpowers/specs/2026-08-26-process-review-recommendations-batch-2-design.md`.

**Architecture:** Two independent, small edits: a logging-template fix plus a new mechanical completion gate in `subagent-driven-development/SKILL.md`, and a second rule with a worked example in `docs/patterns/ab-test-live-trials-for-behavior-change.md`.

**Tech Stack:** Markdown skill/pattern files, no code, no test framework. Verification is direct read-throughs plus disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — fixes the fix-loop logging template and adds the notes.md completion gate.
- **Modify:** `docs/patterns/ab-test-live-trials-for-behavior-change.md` — adds a second rule and worked example.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill/pattern files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Fix the fix-loop logging template

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Update the logging template to include the plan-slug parenthetical**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
Everything else enters the loop. Before the first fix dispatch,
append one line per open finding to
`docs/superpowers/process-reviews/notes.md`:
`- <YYYY-MM-DD> | Catch | Task <N> | <one-line finding>`. The review
loop is already doing the work; logging it costs one line and feeds
`process-review` later. A fix round is one fix dispatch plus one
scoped re-review. Five rounds maximum per task:
```

Replace with:
```
Everything else enters the loop. Before the first fix dispatch,
append one line per open finding to
`docs/superpowers/process-reviews/notes.md`:
`- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`.
The parenthetical plan-slug is what lets `process-review` group Catches
by spec later — a bare `Task <N>` is ambiguous across sub-projects that
each have their own Task 1. The review loop is already doing the work;
logging it costs one line and feeds `process-review` later. A fix
round is one fix dispatch plus one scoped re-review. Five rounds
maximum per task:
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Task <N> (<plan-slug>)" plugin/skills/subagent-driven-development/SKILL.md
grep -n "lets \`process-review\` group Catches" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "fix(skills): add the plan-slug to the fix-loop logging template

Every real notes.md entry logged this session already used
Task <N> (<plan-slug>), which process-review's own by-spec grouping
depends on -- the template's literal text never matched practice.

Part of docs/superpowers/specs/2026-08-26-process-review-recommendations-batch-2-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Add the notes.md completion gate

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the gate after the ledger completion bullets**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
### 5. Complete the task

When the review comes back clean — or every open finding is parked with a
ruling at the cap — append the completion line to the ledger in the same
message as your other bookkeeping:

- `Task <N>: complete (commits <base7>..<head7>, review clean)`
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)` after a
  tripped breaker

Also record this task's Outcome field — from the implementer's most
```

Replace with:
```
### 5. Complete the task

When the review comes back clean — or every open finding is parked with a
ruling at the cap — append the completion line to the ledger in the same
message as your other bookkeeping:

- `Task <N>: complete (commits <base7>..<head7>, review clean)`
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)` after a
  tripped breaker

If this task's fix loop ran at least one round, confirm
`docs/superpowers/process-reviews/notes.md` contains at least one
`Task <N> (<plan-slug>)` entry before continuing — a task whose review
passed clean on the first pass never entered the loop, so this check
doesn't apply to it. If no entry exists, append one now for each
finding the review reported, using the findings you already have from
the review, before marking the task complete. Don't defer this the
way outcomes-file bookkeeping was once deferred — the same
mechanical-gate reasoning `docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md`
already sets out applies here too.

Also record this task's Outcome field — from the implementer's most
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "If this task's fix loop ran at least one round" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Don't defer this the" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): gate task completion on notes.md logging

Complete the task now confirms notes.md actually received an entry
for any task whose fix loop ran, before marking it complete --
notes.md had zero real-time entries for two of three specs in the
last process review despite each having multiple fix rounds. A
mechanical gate, not a restated reminder, matching the same reasoning
already applied to the outcomes-bookkeeping gate.

Part of docs/superpowers/specs/2026-08-26-process-review-recommendations-batch-2-design.md."
```

Stage only this one file.

---

## Task 3: Add the second rule to the A/B-testing Pattern

**Files:**
- Modify: `docs/patterns/ab-test-live-trials-for-behavior-change.md`

- [ ] **Step 1: Rename the title to cover both rules, and restructure into two numbered rules**

**Important:** read the file first with the Read tool to confirm the exact current text — do not assume the Find block below is byte-identical without checking.

Find:
```
# A/B-test a live trial that claims to prove a new instruction changes behavior

When a live trial exists to show a new instruction causes a behavioral change (not just that the instruction reads correctly), run it as a true two-arm comparison against the pre-edit baseline — never as a single coached run.

## Context

A `--plugin-dir` trial can dispatch an agent, plant a false belief or a tempting shortcut, and confirm the agent avoids it. That confirms the agent follows the instruction's letter under the trial's own coaching. It does not confirm the instruction caused the correct outcome, if the agent's dispatch prompt already told it what to do, or if the underlying model already tends to behave correctly without the instruction. A single-arm trial with no baseline comparison cannot distinguish "the instruction worked" from "nothing here needed the instruction at all."

## Pattern

When a trial exists to verify a new instruction changes reviewer or implementer behavior:
1. Write one minimal dispatch prompt that plants the test scenario without coaching the correct response — no "follow the instructions about X," no "confirm by reading fresh from disk," nothing that names the behavior under test.
2. Check out the plugin at two points: immediately before the instruction's commit, and at its current state (including any later fixes).
3. Run the identical coaching-free prompt against both checkouts, using the same fixture.
4. Compare the two results directly. Only a difference between the two arms counts as evidence the instruction changed anything. Identical results in both arms mean the instruction added no detectable value in that scenario — report this honestly, even if an earlier, coached trial already reported a "pass."
5. If the design spec or plan already cites the single-arm trial as its Falsifiable Criterion, correct that criterion once the A/B result comes in — state plainly what the criterion actually shows (the instruction gets followed) versus what it does not show (the instruction changed the outcome).

## Example

- A new reviewer instruction ("re-read the cited doc before citing it in a finding") got verified by a trial that primed a false belief about a doc's rule and confirmed the reviewer caught it. The trial's own prompt said "follow the reviewer template's instructions about re-reading cited docs" and "quote the exact current text ... read fresh from disk" — both force the correct behavior regardless of the instruction under test. A true A/B run (same fixture, no coaching, once against the plugin before the instruction shipped and once after) found both arms independently caught the planted error — the pre-edit reviewer did this unprompted. The instruction added no detectable behavioral difference in this scenario. The design spec's Falsifiable Criterion got corrected to say so explicitly, rather than let the original coached trial's "pass" stand as unqualified proof.

## Originating lessons

- "A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior" (2026-08-24-review-recommendations-followup)
```

Replace with:
````
# A/B-test or scenario-check a live trial that claims to prove a mechanism works

Two distinct trial-design failures share one root cause: a trial whose own prompt hands the agent enough information that it cannot fail, regardless of whether the mechanism under test actually works.

## Context

A `--plugin-dir` trial can dispatch an agent, plant a scenario, and confirm the agent responds correctly. Two different claims get tested this way, and each has its own way of accidentally becoming unfalsifiable:

- **Claim: "this new instruction changes behavior."** A trial that plants a false belief and confirms the agent avoids it only proves the agent follows the instruction's letter under the trial's own coaching — not that the instruction caused the correct outcome, if the dispatch prompt already told the agent what to do, or if the underlying model already behaves correctly without the instruction.
- **Claim: "this trigger condition correctly does NOT fire on a non-matching case."** A trial that tells the agent which trigger paragraph to check, and states the answer ("nothing crossed a boundary") directly in its own prompt, proves only that the agent can read a scenario it was already told the answer to — not that the trigger logic itself would have discriminated a real non-crossing from a crossing on its own.

## Pattern

**Rule 1 — verifying a behavior change needs a true two-arm comparison, not a single coached run.**

1. Write one minimal dispatch prompt that plants the test scenario without coaching the correct response — no "follow the instructions about X," no "confirm by reading fresh from disk," nothing that names the behavior under test.
2. Check out the plugin at two points: immediately before the instruction's commit, and at its current state (including any later fixes).
3. Run the identical coaching-free prompt against both checkouts, using the same fixture.
4. Compare the two results directly. Only a difference between the two arms counts as evidence the instruction changed anything. Identical results in both arms mean the instruction added no detectable value in that scenario — report this honestly, even if an earlier, coached trial already reported a "pass."
5. If the design spec or plan already cites the single-arm trial as its Falsifiable Criterion, correct that criterion once the A/B result comes in — state plainly what the criterion actually shows (the instruction gets followed) versus what it does not show (the instruction changed the outcome).

**Rule 2 — verifying a trigger correctly does NOT fire needs a scenario the agent evaluates itself, not a stated answer.**

1. Write the negative-case dispatch prompt as a scenario only — describe what changed (or didn't), never name which specific trigger paragraph governs the outcome.
2. Never state the expected answer in the prompt ("nothing crossed a boundary," "this shouldn't fire") — ask the agent to determine and report that itself.
3. If the trial as written already tells the agent the answer, treat that as a trial-design defect before trusting a "correctly skipped" result — rewrite it as a scenario-only prompt and re-run before relying on the finding.
4. No second arm or checkout is needed for this rule — the fix is prompt design, not an A/B comparison.

## Example

- **Rule 1:** A new reviewer instruction ("re-read the cited doc before citing it in a finding") got verified by a trial that primed a false belief about a doc's rule and confirmed the reviewer caught it. The trial's own prompt said "follow the reviewer template's instructions about re-reading cited docs" and "quote the exact current text ... read fresh from disk" — both force the correct behavior regardless of the instruction under test. A true A/B run (same fixture, no coaching, once against the plugin before the instruction shipped and once after) found both arms independently caught the planted error — the pre-edit reviewer did this unprompted. The instruction added no detectable behavioral difference in this scenario. The design spec's Falsifiable Criterion got corrected to say so explicitly, rather than let the original coached trial's "pass" stand as unqualified proof.
- **Rule 2:** A trial meant to confirm a Finish-step trigger correctly skips a plan that only modifies an existing file (no add/rename/delete) told the agent directly: "This plan's File Structure section stated: 'Modify: ...' -- no skill, feature, or directory was created, renamed, moved, or deleted." The agent's report that it "correctly made no change" proved only that it can read a scenario it was handed the answer to. The trial showed the instruction is followable, not that the trigger logic itself discriminates a real non-crossing from a crossing.

## Originating lessons

- "A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior" (2026-08-24-review-recommendations-followup)
- "A trial confirming a trigger doesn't fire must not hand the agent its own answer" (2026-08-25-concept-index)
````

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^# A/B-test or scenario-check" docs/patterns/ab-test-live-trials-for-behavior-change.md
grep -n "Rule 2 — verifying a trigger correctly does NOT fire" docs/patterns/ab-test-live-trials-for-behavior-change.md
grep -n "A trial confirming a trigger doesn't fire must not hand the agent its own answer" docs/patterns/ab-test-live-trials-for-behavior-change.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/patterns/ab-test-live-trials-for-behavior-change.md
git commit -m "docs(patterns): add the negative-case trial rule to ab-test-live-trials

A distinct, cheaper failure than the existing behavior-change rule:
a trial confirming a trigger correctly does NOT fire, whose own
prompt names the trigger and states the answer, cannot fail
regardless of whether the trigger logic actually discriminates.
Recurred twice this session (review-recommendations-followup's
Falsifiable Criterion 2, concept-index's Falsifiable Criterion 3).

Part of docs/superpowers/specs/2026-08-26-process-review-recommendations-batch-2-design.md."
```

Stage only this one file.

---

## Task 4: Verify the notes.md completion gate with live trials

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a fixture plan and its own notes.md**

```bash
mkdir -p /c/sf-notes-gate-test/docs/superpowers/plans
mkdir -p /c/sf-notes-gate-test/docs/superpowers/process-reviews
cd /c/sf-notes-gate-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/plans/2026-08-26-gate-fixture-test.md <<'EOF'
# Gate Fixture Test Implementation Plan

**Goal:** A trivial one-task plan used only to exercise the notes.md completion gate in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Create a fixture file

Create a file named fixture.txt containing "fixture".
EOF

cat > docs/superpowers/process-reviews/notes.md <<'EOF'
# Process Review — Running Notes

<!-- entries below this line -->
EOF

git add -A
git commit -q -m "initial scratch fixture: fixture plan, empty notes.md"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run a trial simulating Complete the task with the notes.md entry deliberately missing**

```bash
cd /c/sf-notes-gate-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-notes-gate-test. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. Assume you are the controller for the plan at docs/superpowers/plans/2026-08-26-gate-fixture-test.md. Task 1 (Create a fixture file) went through one fix round -- the reviewer found the file was missing a trailing newline, the implementer fixed it. You never appended anything to docs/superpowers/process-reviews/notes.md during that fix round (this was an oversight in an earlier session, not something you did on purpose). Task 1's review is now clean. Follow the Complete the task step exactly, including its notes.md gate. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether you found notes.md missing this task's entry, and what you did about it. SECTION 2/2: quote the exact full contents of docs/superpowers/process-reviews/notes.md after you finish, read fresh from disk." > /c/sf-notes-gate-test/trial-missing.txt 2>&1
cat /c/sf-notes-gate-test/trial-missing.txt
```

- [ ] **Step 3: Verify the missing-entry trial independently**

```bash
cat /c/sf-notes-gate-test/docs/superpowers/process-reviews/notes.md
```

Confirm SECTION 1/2 reports the gate caught the missing entry and appended one, and the file shown in SECTION 2/2 (and independently read above) now contains a `Task 1 (gate-fixture-test)` line naming the trailing-newline finding — not left empty.

If the trial reports completing the task without noticing or fixing the gap, treat this as DONE_WITH_CONCERNS and report exactly what the trial output and file contain.

- [ ] **Step 4: Reset the fixture and run a trial where the entry is already correctly logged**

```bash
cd /c/sf-notes-gate-test
cat > docs/superpowers/process-reviews/notes.md <<'EOF'
# Process Review — Running Notes

<!-- entries below this line -->
- 2026-08-26 | Catch | Task 1 (gate-fixture-test) | Fixture file was missing its trailing newline
EOF
git add -A
git commit -q -m "reset fixture: notes.md already has the correct entry"

claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-notes-gate-test. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. Assume you are the controller for the plan at docs/superpowers/plans/2026-08-26-gate-fixture-test.md. Task 1 (Create a fixture file) went through one fix round, and docs/superpowers/process-reviews/notes.md already has a correct entry for it. Task 1's review is now clean. Follow the Complete the task step exactly, including its notes.md gate. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether you found notes.md already had this task's entry, and what you did about it. SECTION 2/2: quote the exact full contents of docs/superpowers/process-reviews/notes.md after you finish, read fresh from disk." > /c/sf-notes-gate-test/trial-present.txt 2>&1
cat /c/sf-notes-gate-test/trial-present.txt
```

- [ ] **Step 5: Verify the already-logged trial independently**

```bash
cat /c/sf-notes-gate-test/docs/superpowers/process-reviews/notes.md
```

Confirm SECTION 1/2 reports the entry was already present and nothing needed appending, and the file contains exactly one `Task 1 (gate-fixture-test)` line — not duplicated.

If the trial adds a second, duplicate entry, treat this as DONE_WITH_CONCERNS and report exactly what the file contains.

- [ ] **Step 6: Clean up**

```bash
rm -rf /c/sf-notes-gate-test
```

No commit for this task.
