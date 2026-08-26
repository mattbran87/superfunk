# Process Review Recommendations (Batch 2) — Design

**Date:** 2026-08-26
**Status:** Approved

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-25-concept-index-design.md` left three open Recommendations. This spec closes the first two:

1. Add a mechanical gate confirming `docs/superpowers/process-reviews/notes.md` actually received an entry before a task's fix loop completes — `notes.md` had zero real-time entries for two of the three specs that review covered, despite each having multiple fix rounds.
2. Extend `docs/patterns/ab-test-live-trials-for-behavior-change.md` with a second rule covering a distinct, narrower failure: a trial meant to confirm a trigger condition does not fire on a non-matching case, whose own prompt names the trigger and states the answer, so the trial cannot fail regardless of whether the trigger logic works. This recurred twice this session (`review-recommendations-followup`'s Falsifiable Criterion 2, `concept-index`'s Falsifiable Criterion 3).

The third Recommendation — a harder, less-mechanical Self-Review check for cross-section mechanism consistency — stays out of scope, per its own review entry noting it needs more design thought than a mechanical gate or a doc addition.

## Decision

- **`subagent-driven-development/SKILL.md`'s fix-loop logging template changes.** The current template (`### 4. The fix loop`) reads `- <YYYY-MM-DD> | Catch | Task <N> | <one-line finding>`. Every real entry logged this session instead used `Task <N> (<plan-slug>)` — the parenthetical spec-slug the template's literal text omits, and the exact thing `process-review`'s own synthesis (which groups Catches "by spec") depends on to work. The template updates to match established practice: `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`.

- **`### 5. Complete the task` gains a new explicit check**, alongside the existing outcomes-file bookkeeping: if this task's fix loop ran at least one round, confirm `docs/superpowers/process-reviews/notes.md` contains at least one `Task <N> (<plan-slug>)` entry before marking the task complete. A task whose review passed clean on the first pass never entered the loop — nothing to check. If the check finds no entry, append the missing one(s) now, from the findings the review already reported, before proceeding — the same "stop and do it, don't defer" shape `docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md` already establishes for the sibling outcomes-bookkeeping gap. "At least one entry," not an exact per-finding count: multiple findings sometimes get reasonably combined into one line, and a strict count-match would produce false failures on a legitimately-combined entry.

- **`docs/patterns/ab-test-live-trials-for-behavior-change.md` gains a second rule**, clearly distinguished from the first by its trigger condition. The existing rule covers "does this instruction change behavior" (needs a true two-arm comparison, checked out at two commits). The new rule covers "does this trigger condition correctly NOT fire" — a cheaper case needing no second arm, no checkout, just a different prompt-writing discipline: the trial's own prompt must not name the exact trigger paragraph or state the answer ("nothing crossed a boundary," "this shouldn't fire") — the agent must determine that itself from the scenario it's given, or the trial cannot fail regardless of whether the trigger logic actually discriminates. Each rule's own worked example cites its own real recurrence: Rule 1's covers `review-recommendations-followup`'s Falsifiable Criterion 2 (coached "follow the instructions about re-reading"); Rule 2's covers `concept-index`'s Falsifiable Criterion 3 (told the agent directly "nothing crossed a boundary").

  No new skill wiring: `writing-plans`' existing Self-Review item 7 ("Check `docs/lessons-learned.md` for any entry relevant to this plan's domain") already surfaces this Pattern to a future plan involving live-trial design, the same way it already would for any other Pattern.

## Falsifiable Criteria

1. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the logging template includes the `(<plan-slug>)` parenthetical, and "Complete the task" names the notes.md check as its own explicit line.
2. A disposable `--plugin-dir` trial runs a task through a fix loop (a planted finding forces one round) with the notes.md entry deliberately missing at "Complete the task" time. The controller catches the gap and appends the missing entry before proceeding.
3. A second trial runs a task whose fix loop already logged its entry correctly, confirming the gate doesn't duplicate an existing entry or misfire on the already-compliant case.
4. A direct read-through of the shipped `ab-test-live-trials-for-behavior-change.md` confirms the second rule states a trigger condition distinct from the first, and each rule's own worked example accurately cites its own real recurrence (Rule 1: `review-recommendations-followup`'s Falsifiable Criterion 2; Rule 2: `concept-index`'s Falsifiable Criterion 3) — not necessarily both recurrences duplicated into each example.

## Consequences

Every task whose fix loop runs at least one round now also gets one more mechanical check before completion — a real grep command and an explicit commit step, matching the concreteness the outcomes-bookkeeping gate already carries.

The Pattern file grows by one rule, one worked example, and (after the final review found the notes.md gate's first draft still read as a reminder) one more numbered item stating when a gate needs a git-checkable precondition to become self-enforcing. The final review also surfaced the sub-project's own real-time proof of the problem it exists to solve — Task 3's own notes.md entry landed after the controller marked Task 3 complete — captured as a new Lesson in `docs/lessons-learned.md`.

## Deferred

- The cross-section mechanism-consistency Self-Review check (the review's third Recommendation) — gets its own separate brainstorm, since it needs real design work to make "identify every other section describing the same mechanism" concrete rather than aspirational.
- Retroactively fixing the two already-shipped specs' missing notes.md history (`per-task-outcome-capture`, `review-recommendations-followup`) — the process review already reconstructed those entries once from git log; not re-litigated here.
