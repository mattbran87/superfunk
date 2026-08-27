# Process Review — after 2026-08-27-cross-section-sibling-scope-design.md

**Date:** 2026-08-27

## Specs Reviewed

- 2026-08-26-process-review-recommendations-batch-2-design.md
- 2026-08-26-cross-section-mechanism-consistency-design.md
- 2026-08-27-cross-section-sibling-scope-design.md

## Catches

**2026-08-26-process-review-recommendations-batch-2-design.md**
- Task 3: a new Pattern's Originating-lessons citation had no matching entry in `lessons-learned.md`, breaking this project's citation convention — the rule's real origin was a process-review Recommendation, never captured as a Lesson at the time.
- Task 3 (reconstructed from git log, commit `a278a7a`): the shipped Rule 2 worked example presented the phrase "correctly made no change" in quotation marks as if it were the agent's actual trial report; it was actually a paraphrase of the design spec's requirement text, with no record of the agent's real report phrasing surviving.
- Task 4: Task 1's own just-shipped `<plan-slug>` placeholder was never defined precisely; a live trial reasonably used the full dated filename instead of the short slug every real historical entry uses, surfacing the ambiguity before it could recur.
- Final review: the shipped notes.md gate was reminder-shaped (no grep command, no explicit commit step) despite the originating Recommendation explicitly asking for "not a restated reminder" — confirmed by this sub-project's own commit timestamps, which showed a fix-round entry landing 8 minutes after the task was marked complete.
- Final review: both closed Recommendation checkboxes in the prior process review remained unchecked despite being shipped, against an established convention.
- Final review: Falsifiable Criterion 4 claimed a new Pattern rule's worked example "cites both real recurrences," but the shipped design deliberately splits one recurrence per rule's own example — and after the criterion got corrected, the design spec's own Decision bullet still asserted the false original claim, contradicting the criterion in the same document.
- Final review (reconstructed from git log, commit `e8786b6`): a Lesson's promotion note referenced an internal fix-wave label ("Fix 5") with no referent anywhere in the repo.
- Final review: Task 4's own live-trial prompts violated both rules of the A/B-testing Pattern this sub-project shipped one task earlier (named the exact mechanism under test, handed the agent the finding, used the literal disqualifying phrase "read fresh from disk") — a plan defect authored before the Pattern existed, not an execution error.

**2026-08-26-cross-section-mechanism-consistency-design.md**
- Final review: `re-review-prompt.md`'s own Scope section stayed unqualified after the carve-out shipped, contradicting the exception added lower in the same file — the exact failure shape this sub-project exists to catch, found in its own shipped edit.
- Final review: `subagent-driven-development/SKILL.md`'s "flags new breakage in the fix diff only" went stale once the carve-out shipped in a sibling file — item 8's own grep scope (same file plus design spec only) would not have caught this instance.
- Final review: item 8 narrowed Recommendation 3's literal wording ("name every other section") to a grep-and-confirm step producing no written artifact, and the design spec never documented the narrowing at Decision time.
- Final review: both live trials exercised only a positive, single-file, two-branch case — the design-spec clause, the negative (correctly-does-not-fire) case, and a mechanism spanning more than two sections all went untested.
- Final review: Recommendation 3's checkbox, the design spec's Status line, and tracker.md's shipped-specs list all remained unactioned after implementation completed, pending the Finish step.
- Re-review of the final-review fix wave: the first fix wave reconciled one unqualified diff-only statement per file but left a second one standing in each of the same two files — the same recurring shape, caught by the scoped re-review rather than a fresh pass.

**2026-08-27-cross-section-sibling-scope-design.md**
- Task 1: a code-quality review flagged the widened item 8 sentence's length (46 words) and its "if ... names one" construction as new STE violations; both already existed verbatim in already-shipped, already-approved precedent — overridden per `verify-against-precedent-before-flagging` rather than fixed, since fixing only this instance would also have broken parity with the carve-out's identical, unedited clause.
- Final review: the widened clause never states whether "every other file in the same directory" recurses into subdirectories — four skill directories have one, including the directory this whole fix originated from; no live contradiction exists today, but the ambiguity went unrecorded.
- Final review: the design spec never recorded why two abstract carve-out summaries and a Scope pointer needed no edit this time, unlike the prior sub-project where the equivalent abstraction did need one.
- Final review: the prior spec's item-8 visibility gap (no written artifact confirming the check ran) never carried forward into this spec's Deferred section.
- Final review: the negative (correctly-does-not-fire) case has now gone untested across two consecutive sub-projects in this line, with no escalation noting the streak.

## Misses

- **Recommendation/Status/tracker bookkeeping gets deferred until a final review catches the omission, rather than closed the moment implementation finishes.** `process-review-recommendations-batch-2` shipped with both of the prior review's Recommendation checkboxes still unchecked; `cross-section-mechanism-consistency` shipped with its own Recommendation 3 checkbox, the design spec's Status line, and the tracker's shipped-specs list all unactioned — in both cases the final review, not the controller's own Finish pass, is what caught it.
- **A design spec's scope decision (a narrowing, or a "why this file needed no edit" call) goes unrecorded at Decision time, surfacing only when a final review asks for the reasoning.** `cross-section-mechanism-consistency` narrowed Recommendation 3's "name every other section" wording to a grep-and-confirm step with no written artifact, undocumented; `cross-section-sibling-scope` initially left unrecorded why two abstract summaries and a Scope pointer needed no edit despite the equivalent abstraction needing one in the predecessor sub-project. Both required a final review to force the documentation into existence.
- **A negative-case (correctly-does-not-fire) trial gap gets deferred with the same reasoning across successive extensions of the same mechanism, with nothing forcing a revisit.** `cross-section-mechanism-consistency` deferred it first; `cross-section-sibling-scope` deferred the identical gap again, unaware the deferral itself was now a repeat. Already surfaced independently by `cross-section-sibling-scope`'s own final review and promoted to a Lesson and Pattern (`docs/patterns/escalate-deferred-items-on-second-recurrence.md`) — named here too since this review's own evidence trail reaches the same conclusion independently.

## Friction

- **`cross-section-mechanism-consistency`'s carve-out/Scope fix** needed two full fix-wave rounds after the final review (`99ed48c`, then a scoped re-review found a second instance requiring `3d75180`) to close what is fundamentally one recurring contradiction shape — a smaller-scale repeat of the exact "chasing one distinction across sections" friction the prior review period named for `concept-index`. Already addressed going forward by the newly-promoted `docs/patterns/self-apply-cross-section-check-to-hand-fixes.md`, which states the expectation that a hand-fix to mechanism-describing content typically needs a second reconciliation round — no new Recommendation needed here; revisit only if a third round is needed on a future instance.

## Gaps

- **No check states whether "every other file in the same `plugin/skills/<name>/` directory" recurses into subdirectories.** Four skill directories currently have one (including `subagent-driven-development/scripts/`), and no file in any of them currently carries mechanism prose that would matter — but the ambiguity is unresolved in both shipped clauses, discovered by `cross-section-sibling-scope`'s final review with no earlier check having named it.

## Recommendations

- [x] Add a git-checkable gate to `plugin/skills/subagent-driven-development/SKILL.md`'s Finish step confirming a spec's Recommendation checkbox (when the plan closes one), Status line, and tracker entry are all updated in the same Finish pass — not left for a final review to catch. Recurred in `process-review-recommendations-batch-2` and `cross-section-mechanism-consistency`. (Shipped as the Recommendation-checkbox paragraph and three-part verification gate in `subagent-driven-development/SKILL.md`'s Finish section, commit `f07207d`.)
- [x] Resolve the negative-case (correctly-does-not-fire) trial gap for `plugin/skills/writing-plans/SKILL.md`'s item 8 and `plugin/skills/subagent-driven-development/re-review-prompt.md`'s carve-out with an actual disposable `--plugin-dir` trial. Deferred across two consecutive sub-projects (`cross-section-mechanism-consistency`, `cross-section-sibling-scope`) with the same reasoning both times; per `docs/patterns/escalate-deferred-items-on-second-recurrence.md`, this recurrence itself is the trigger to resolve it now rather than defer a third time. (Shipped as two Rule-2-compliant negative-case trials confirming both mechanisms correctly discriminate the "trigger words" style-guidance near-miss from a real mechanism claim, commits in `2026-08-27-cross-section-negative-case-trials.md`'s outcomes.)
- [x] Add a recursion-boundary clarification (e.g. "non-recursive") to the sibling-directory clause in both `plugin/skills/writing-plans/SKILL.md` (item 8) and `plugin/skills/subagent-driven-development/re-review-prompt.md` (the carve-out) — currently unstated in both, noted only in `2026-08-27-cross-section-sibling-scope-design.md`'s Deferred section. (Shipped as a "(top-level files only, not subdirectories)" parenthetical in both clauses, commits `e7a4c82`/`3f4f99d`.)
- [ ] Add a Self-Review item (or extend an existing one) in `plugin/skills/writing-plans/SKILL.md` requiring a design spec's Deferred or Consequences section to state WHY an adjacent file needed no edit whenever a plan's own dog-fooding of a cross-section check reports "nothing else needs updating" — this reasoning has twice now been added only reactively, after a final review asked for it.
