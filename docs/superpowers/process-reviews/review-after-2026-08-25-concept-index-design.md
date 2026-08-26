# Process Review — after 2026-08-25-concept-index-design.md

**Date:** 2026-08-26

## Specs Reviewed

- 2026-08-21-per-task-outcome-capture-design.md
- 2026-08-24-review-recommendations-followup-design.md
- 2026-08-25-concept-index-design.md

## Catches

**A note on evidence for this review:** `docs/superpowers/process-reviews/notes.md` holds real-time Catch entries only for `concept-index`. Neither `per-task-outcome-capture` nor `review-recommendations-followup` has a single entry, despite both going through multiple fix rounds. Per this skill's own Step 4, the Catches below for those two specs are reconstructed from `git log` fix-commit messages, not from the running log — the running log itself missed them. This gap is significant enough to appear again under Misses and Gaps below.

**2026-08-21-per-task-outcome-capture-design.md** (reconstructed from git log, `9e14752..ba52f8f`)
- Commit `2397921`: the implementer's Outcome field wasn't scoped away from reviewer-found findings, risking double-counted signal between the ledger and the new outcomes file.
- Commit `3293b6d`: the plan-basename derivation ambiguously said "stripping -design" without specifying the trailing occurrence, and had no fallback for a plan whose filename doesn't share the spec's exact stem.
- Commit `7ac602d`: the Example Workflow and flowchart in `subagent-driven-development/SKILL.md` were never updated to show the new Outcome field or outcomes-file bookkeeping, contradicting the step they illustrate.
- Commit `5a9364d`: the prior fix's own worked-example update introduced a fresh contradiction — its fix-round Outcome example described a reviewer-found-and-fixed finding as its divergence, exactly the category the new scoping rule excludes.

**2026-08-24-review-recommendations-followup-design.md** (reconstructed from git log, `da7a897..df5853b`)
- Commit `7a07d10`: the new re-read instruction covered only re-reading a cited doc, not re-checking the diff itself — one of the two motivating recurrences was actually a diff misreading, which a doc re-read alone would never catch.
- Commit `95268c5`: a genuine two-arm A/B trial (same fixture, no coaching, pre-edit vs. post-edit plugin) found no detectable behavioral difference — the original single-arm trial's "pass" reflected the model's own tendency to verify, not the new instruction. Falsifiable Criterion 2 got corrected to say so honestly instead of overclaiming.
- Commit `0a1adde`: the design spec's Decision block still quoted the pre-broadening instruction after `7a07d10` broadened it, and one E-Prime contraction survived a commit that claimed to have already fixed E-Prime violations in that exact line.

**2026-08-25-concept-index-design.md** (from `docs/superpowers/process-reviews/notes.md`, entries dated 2026-08-25)
- Task 1: Step 3's unattended, automatically-triggered path had no hand-edit check before overwriting or removing an existing row, unlike `project-definition`'s Step 6.
- Task 1: the Feature bullet in Concept Units specified its Description column but never its Concept column, unlike the Skill and Directory bullets.
- Task 1 (round 2): a fix's cross-reference text incorrectly attributed an "interactive run" to Step 2, which can never face an existing row to overwrite.
- Task 1 (round 3): the next fix invented a "human invokes Step 3 directly" scenario, contradicted by Step 3's own "never run this step standalone" sentence.
- Task 2: the commit message cited the wrong Lesson slug; the new Finish-step paragraph had no why-clause, unlike its siblings.
- Task 3: the new dispatch bullet's negative case dropped the visibility clause both sibling bullets carry (deferred to final review as Minor).
- Final review: the deferred Task 3 finding was upgraded to Important once checked against the spec's own stated silent-skip rationale.
- Final review: "confirming first" described a confirmation mechanism the shipped design never implements.
- Final review: the hand-edit detection compared a row's Description against a fresh, non-deterministic re-derivation, and couldn't detect row reordering at all.
- Final review: Falsifiable Criterion 2 contradicted the shipped skill's always-separate-commit rule; Criterion 3's skip trial coached the agent by naming the exact trigger paragraph.
- Final review, round 2: the fix to the hand-edit check overshot into an unconditional human-decision gate on every rename/delete, contradicting Falsifiable Criterion 4 and Task 5's own passed live trial.
- Final review, round 3: the corrected check was still unsatisfiable for a deleted unit (no source left to compare), and Step 1 routed a direct human invocation into a step that declares that impossible — both fixed directly by the controller.
- Final review: the controller missed its own outcomes-bookkeeping mechanism a second time in this same sub-project, despite an explicit start-of-session reminder.
- Final review: the controller's own `git commit --amend` attached the wrong message to a diff — self-caught immediately.

## Misses

- **A fix to one part of a document isn't cross-checked against every other part describing the same mechanism, so a fix round routinely introduces a new inconsistency the next round must catch.** This is the dominant pattern of this review period, not an isolated incident. `per-task-outcome-capture`'s worked-example fix (`5a9364d`) contradicted the same commit's own scoping rule. `concept-index`'s Task 1 needed three consecutive fix rounds (`fb2ef87`, `465a38c`, `31a9aa1`) chasing a single interactive/unattended distinction across Step 1, Step 2, Step 3, and the Hand-editing section — each fix correct in isolation, each leaving a different part of the file out of sync. The final review then repeated the exact same shape twice more: a fix to the hand-edit check (Important #3) overshot into an unconditional gate contradicting Falsifiable Criterion 4 and an already-passed trial, and the corrected version still left Step 1 and the delete path unreconciled with the rest of the file. Five-plus rounds on one file (`concept-index/SKILL.md`) for what is fundamentally one recurring failure mode.
- **A live trial's own coaching language makes the trial pass regardless of whether the mechanism it tests actually works.** `review-recommendations-followup`'s Falsifiable Criterion 2 trial told the agent to "follow the reviewer template's instructions about re-reading" — coaching the exact behavior under test — and a true A/B run later showed the instruction added no detectable value. `concept-index`'s Falsifiable Criterion 3 trial named the exact trigger paragraph and told the agent directly that nothing crossed a boundary, so it showed the instruction is followable, not that the trigger condition itself discriminates. Both recurrences got caught this same review period, by two different mechanisms (a follow-up A/B trial; a final-review read-through) — this is now a proven, recurring trial-design failure, not a one-off.
- **`docs/superpowers/process-reviews/notes.md` didn't get a single real-time entry for two of the three specs this review covers.** The mechanism exists, is documented, and got used correctly for `concept-index` — but `per-task-outcome-capture` and `review-recommendations-followup` show zero entries despite each having multiple fix rounds with real findings. This recurs the same failure shape as the outcomes-bookkeeping Miss below: a controller-owned logging step with no loud downstream failure if skipped.
- **The controller's own outcomes-bookkeeping mechanism (`docs/superpowers/plans/<slug>-outcomes.md`) got missed a second time**, in `concept-index`, despite an explicit start-of-session reminder naming the exact prior failure from `review-recommendations-followup`. Already promoted to a Pattern (`docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md`) as part of this same sub-project's Finish step — noted here because it is squarely this review's business, not to duplicate the promotion.

## Friction

- **`concept-index`'s `plugin/skills/concept-index/SKILL.md`** is the standout friction point of this entire review period: Task 1 alone took three fix rounds before task-level approval, and the final whole-branch review then required two more fix waves plus one direct controller fix to reconcile Step 1, Step 3's item 2, the Hand-editing section, and the design spec's Falsifiable Criteria with each other. No other single file this session has needed this many rounds.
- **`review-recommendations-followup`** needed three fix rounds across its two-task plan (task-reviewer-prompt.md's scope, then the design spec's Falsifiable Criterion 2 honesty correction, then an E-Prime cleanup) — consistent with this window's general pattern that edits to already-shipped, heavily cross-referenced files take more rounds than net-new files.
- **`per-task-outcome-capture`** needed two fix waves after its own final review, both concentrated on the same "Example Workflow contradicts the new instruction" failure shape named above.

## Gaps

- **No check confirms `notes.md` actually received an entry before a task's fix loop closes.** The instruction to log exists (`subagent-driven-development/SKILL.md`'s fix-loop section: "Before the first fix dispatch, append one line per open finding..."), but nothing verifies it happened — the same structural gap the outcomes-bookkeeping Pattern just named for a different mechanism. Two of three specs in this review show the gap in practice.
- **No trial-writing guidance warns against naming the exact mechanism under test inside a "confirm it doesn't fire" trial prompt.** `docs/patterns/ab-test-live-trials-for-behavior-change.md` already covers the "does the instruction change behavior" case (needs a true A/B run) but doesn't yet name the narrower, cheaper failure mode found twice this period: a skip/negative-case trial that hands the agent the answer by naming the trigger condition it's supposed to discriminate on its own.

## Recommendations

- [x] Add a check to `plugin/skills/subagent-driven-development/SKILL.md`'s fix-loop section: before marking a task complete, confirm `docs/superpowers/process-reviews/notes.md` contains at least one entry for each finding that entered the fix loop this task — a mechanical, checkable gate (grep the file for today's date and the task label), not a restated reminder, matching the reasoning `docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md` already sets out for the sibling outcomes-bookkeeping gap. (Shipped as the grep + explicit-commit gate in `subagent-driven-development/SKILL.md`'s Complete-the-task step, commits `04bcec8`/a follow-up correction after the final review caught the first version was still reminder-shaped, not mechanically checkable.)
- [x] Extend `docs/patterns/ab-test-live-trials-for-behavior-change.md` with a second, narrower rule: a trial meant to confirm a trigger condition correctly does NOT fire on a non-matching case must not name the exact trigger paragraph or state the answer ("nothing crossed a boundary") in its own prompt — the agent must determine that itself from the scenario, or the trial cannot fail regardless of whether the trigger logic is correct. (Shipped as Rule 2 of `ab-test-live-trials-for-behavior-change.md`, commit `3334179`.)
- [ ] Add a Self-Review item to `plugin/skills/writing-plans/SKILL.md` (or fold into the existing Sibling-pattern parity item 5): when a plan's task edits one part of a document that describes a mechanism spanning multiple sections (e.g., a routing step, a trigger condition, a cross-referenced policy), require the plan to name every other section describing the same mechanism and confirm the edit doesn't leave them contradicting each other — this is the single most repeated failure shape in this review period and has no check behind it yet.
