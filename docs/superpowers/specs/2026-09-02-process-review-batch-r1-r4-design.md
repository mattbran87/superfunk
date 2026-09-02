# Process-Review Batch R1–R4 — Design

**Date:** 2026-09-02
**Status:** Approved
**User-Facing:** Yes

## Context

`docs/superpowers/process-reviews/review-after-2026-09-01-behavioral-claim-verification-design.md`
opened four Recommendations. This batch closes all four in one sub-project
through the full pipeline: spec → plan → execution → Finish. Each
Recommendation traces to a Miss with logged recurrences:

- **R1 ← M3.** Line-wrap verification anchors failed five logged times across
  three sub-projects. The candidate fix worked when a task applied it by hand
  (batch1 outcomes, Task 3). Nothing makes plans apply it.
- **R2 ← M1.** A decision-rule list omitted a covering branch twice in one
  day (`83fd4dd`, `2aa0d8d`). Both specs enumerated example branches instead
  of the outcome space.
- **R3 ← M2.** Version drift recurred in two consecutive review windows. The
  declared guard, `plugin/scripts/bump-version.sh --check`, dies at its first
  `jq` call because `jq` does not exist on this machine (M2 cites the
  notes.md entry).
- **R4 ← M4.** Three of four reviewed specs shipped with zero real-time
  bookkeeping. `executing-plans` owns inline execution and carries no Finish
  section.

### A rule-membership catch on R4's own wording

R4 directs `executing-plans` to mirror "SDD's list (notes.md gate, tracker
append, version bump when `plugin/skills/` changed, lessons capture, spec
Status flip)". Enumeration of that list against SDD's actual Finish section
finds no version-bump step. A grep for "bump" across `plugin/skills/`
returns no instruction — only a metaphor in SDD line 388. The member
"version bump" in R4's mirror-list has zero producers.

This absence explains M2's recurrence: no skill triggers a bump, so every
bump this month happened because a human asked. A mirror of SDD as written
would ship R4's wording while preserving the defect it describes.

**Decision:** this batch adds the bump gate to both SDD's Finish and the new
`executing-plans` section. This expands scope by one file beyond R4's letter,
inside R4's stated intent ("the same gates as the dispatched path").
User-approved during brainstorming.

## Decisions

1. **One batch spec covers all four items.** Follows the taskq-batch1
   precedent: heterogeneous mechanical fixes, one pipeline pass, one Finish.
2. **R1 ships only after an A/B trial, and the trial runs as a plan task.**
   The three prior mechanisms ran spec → trial → ship inline, which bypassed
   every Finish gate (M4). Running the trial inside the plan keeps this batch
   on the fully-gated path. A no-ship verdict on R1 blocks nothing in R2–R4.
3. **The version-bump gate lands in both skills, worded identically.**
   `writing-plans` Self-Review item 6 checks the multi-file restatement at
   plan time.
4. **R3 keeps the bash script and ports only the four `jq` helper
   functions to `node -e`.** Node v22.14.0 runs on this machine (verified by
   `node --version` during brainstorming), and the repo already carries node
   tooling (`package.json`). The script serves repo maintenance on this
   machine, not end users, so machine-local availability suffices. A full
   rewrite would produce a ~220-line diff for logic that works; only the
   `jq` calls die.

## Design

### R1 — drafted-insertion check (trial-gated)

**Target:** `plugin/skills/writing-plans/SKILL.md`, Self-Review item 10
(append to the end of the item).

**Exact string** (on a ship verdict, ship character-for-character):

> For each task that inserts new text and verifies it with a grep, write the
> task's drafted insertion text to a scratch file and run the task's own
> verification grep against that file before finalizing the plan. A grep
> that returns 0 against the drafted text means the anchor fails after
> insertion too — a wrapped line, a duplicate, or a count that exists only
> in text not yet inserted. Fix the anchor or the text now, not at execution
> time.

**Trial design:**

- **Fixture:** one small plan-writing job whose correct insertion text wraps
  across lines, so a plausible multi-word anchor greps 0. Seed it with real
  doc content per `docs/patterns/seed-trial-fixtures-with-real-docs.md`,
  including its harness-symmetry rule.
- **Arms:** arm 1 = current `writing-plans`; arm 2 = identical plus the
  exact string above. `diff -rq` between arm plugin copies must report
  exactly one differing file.
- **Pre-registered class-level criterion:** during plan writing, the agent
  runs a grep against a file that contains its own drafted insertion text,
  before it finalizes the plan. Evidence comes from the transcript or the
  produced plan. The judge must quote the command or plan text it scored,
  per Rule 4 of `docs/patterns/ab-test-live-trials-for-behavior-change.md`.
- **Decision rule** (exhaustive: two arms × two per-arm states):

  | Arm 1 fires | Arm 2 fires | Verdict |
  |---|---|---|
  | no | yes | Ship the exact string. |
  | no | no | Ship nothing — the wording does not fire. |
  | yes | yes | Ship nothing — the baseline already performs the act. |
  | yes | no | Ship nothing; record the anomaly as a finding. |

  Degenerate outcomes get their own branch: an arm run that dies or returns
  unusable output re-runs once before scoring; a judge quote that misses the
  criterion marks the run inconclusive per Rule 4 — register any corrected
  criterion in a commit that predates new outputs.

- Record the verdict in this spec's RESULT section either way.

### R2 — outcome-space sentence in the A/B pattern

**Target:** `docs/patterns/ab-test-live-trials-for-behavior-change.md`,
Rule 1, new point 6.

**Exact string:**

> 6. Pre-register the decision rule by scoring each arm and fixture
> independently, then combining the per-unit states exhaustively — enumerate
> the full outcome space, never a list of example branches. An outcome with
> no covering branch means the decision rule fails this step.

**Self-application:** the R1 decision rule above takes this exact form. No
trial applies — this file guides spec-time work in this repo, not shipped
skill behavior; its evidence (M1, twice recurred) already exists.

### R3 — de-jq bump-version.sh

**Target:** `plugin/scripts/bump-version.sh`.

Port `read_json_field`, `write_json_field`, `declared_files`, and
`audit_excludes` to `node -e` one-liners. Leave all other logic — drift
detection, audit grep, excludes, argument parsing — untouched. The write
path serializes with `JSON.stringify(value, null, 2)` plus a trailing
newline, which matches the manifests' current 2-space format.

**Acceptance (all four must pass on this machine):**

1. `bash plugin/scripts/bump-version.sh --check` exits 0 and reports all
   seven declared files in sync at the current version.
2. A grep for `jq` over the script returns 0 matches.
3. Round-trip: in a scratch copy of the repo, a bump to a test version
   produces a git diff that touches only version-field lines.
4. `--audit` runs to completion.

### R4 — Finish bookkeeping for executing-plans, plus the bump gate in SDD

**Targets:** `plugin/skills/executing-plans/SKILL.md` and
`plugin/skills/subagent-driven-development/SKILL.md`.

In `executing-plans`: insert a new "Step 3: Finish Bookkeeping" and renumber
the current Step 3 to Step 4. The section holds a compact, self-contained
list:

1. notes.md gate — verify each task's catches got logged; append any missing
   lines now.
2. Spec Status flip to `Shipped` when the plan traces to a design spec.
3. Tracker append, and the offer to run `process-review` at 3 or more
   entries.
4. Recommendation checkbox in the named `review-after-*.md` file.
5. The three verification greps (Status, tracker, checkbox).
6. Lessons-learned capture — point to SDD's Finish section for the detailed
   lesson-and-promotion procedure instead of restating it.
7. The version-bump gate (string below).
8. Concept-index update when the plan's File Structure section crossed a
   directory boundary — point to SDD's Finish for the trigger conditions
   and to `superfunk:concept-index` Step 3 for the procedure.

Item 8 comes from self-applying the rule-membership check to this spec's
own mirror-list: SDD's actual Finish holds a concept-index step that R4's
review wording also omitted — the same missing-member shape, caught at
spec time this once.

The full enumeration of SDD's Finish, for the record, holds nine members:
Status flip, tracker append, Recommendation checkbox, verification greps,
lessons capture, concept-index, bug-tracking sweep of parked ledger
findings, workspace deletion, and the finishing-a-development-branch
invocation. The last three stay out of the new section deliberately:
the bug-tracking sweep and workspace deletion read SDD's ledger and
workspace, which inline execution does not create, and `executing-plans`
Step 4 already invokes `finishing-a-development-branch`. A member
excluded with a stated reason differs from a member missed — the first
two drafts of this list missed members.

In SDD's Finish: insert the version-bump gate as its own step. The plan
picks the exact anchor position.

**Bump-gate exact string, identical in both files:**

> If the branch's diff touches `plugin/`, run
> `plugin/scripts/bump-version.sh <new-version>` and commit the result —
> minor bump for `plugin/skills/` changes, patch otherwise. Unsure whether
> the bump already happened: run `--check` first.

**Ordering constraint:** R3 lands before R4 in the plan, so the gate invokes
a script that runs.

**Live verification:** this batch's own Finish must execute the new gate
(6.4.0 → 6.5.0, since the batch changes `plugin/skills/`). A Finish pass
that skips it fails the step's first real test.

## Falsifiable Criteria

1. **R1:** the A/B trial reaches exactly one branch of the pre-registered
   decision rule, and the shipped text (if any) matches the trial's arm-2
   string character-for-character.
2. **R2:** point 6 exists in Rule 1 with the exact string above, and this
   spec's own R1 decision rule demonstrates the required form.
3. **R3:** acceptance checks 1–4 all pass, with command output recorded in
   the plan's task results.
4. **R4:** both target files contain the bump-gate string, byte-identical
   (verify with a grep for a distinctive substring in each file);
   `executing-plans` contains the eight-item section; SDD's Finish contains
   the inserted step.
5. **Batch-level:** the batch's own Finish executes the executing-plans
   bookkeeping list it just shipped, including the version bump to 6.5.0,
   and checks off all four `- [ ]` Recommendations in the review file.

## Out of Scope

- **G1** (title-overlap claims), **G2** (plan-less path owner — needs its
  own design conversation), **G3** (attribution coverage).
- Restatement of the rule-membership check in `writing-plans` or
  `task-reviewer` — standing decision: wait for a second spec-time data
  point.
- A full rewrite of `bump-version.sh` in node or python.
- Any change to `.version-bump.json`'s declared-file list.

## Consequences

- Two skill files now carry the same bump-gate sentence. `writing-plans`
  item 6 checks the restatement at plan time; after that, drift between the
  copies has no automatic guard. Accepted — cheaper than a shared include
  mechanism.
- `executing-plans` item 6 points at SDD's Finish for the lesson procedure.
  A future SDD restructure can break the pointer. Accepted — cheaper than
  dual maintenance of a ~30-line procedure.
- The bump gate's two-branch level rule (minor for `plugin/skills/`, patch
  otherwise) covers mixed diffs: any diff touching `plugin/skills/` takes
  the minor branch.
- Per item 8 of the brainstorming self-review: `finishing-a-development-branch`
  also describes completion mechanics, and this design leaves it unchanged —
  the new Step 3 runs before that skill's invocation and hands it a branch
  whose bookkeeping already landed; no contradiction results.

## RESULT

*(filled at Finish)*
