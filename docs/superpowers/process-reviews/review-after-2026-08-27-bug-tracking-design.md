# Process Review — after 2026-08-27-bug-tracking-design.md

**Date:** 2026-08-27

## Specs Reviewed

- 2026-08-27-cross-section-clean-result-documentation-design.md
- 2026-08-27-notes-md-direct-mode-gate-design.md
- 2026-08-27-bug-tracking-design.md

## Catches

**2026-08-27-cross-section-clean-result-documentation-design.md**
- None. Both tasks shipped clean on first pass; no findings.

**2026-08-27-notes-md-direct-mode-gate-design.md**
- Task 2: the plan's Find block anchored a backfill edit to an entry mislabeled "(cross-section-recursion-boundary)"; the real notes.md entry at that point in the file read "(cross-section-sibling-scope)" — caught immediately when the Edit tool reported no match, fixed by re-reading the file's actual tail, and logged as the first real exercise of this same plan's own newly-widened direct-implementation gate.

**2026-08-27-bug-tracking-design.md**
- Final review: `subagent-driven-development/SKILL.md`'s Example Workflow never depicts any of Finish's bookkeeping steps (Status flip, tracker, Recommendation-checkbox, notes.md gate, Lessons-learned, concept-index, and now bug-tracking) — pre-existing across five prior Finish additions, not introduced by this sub-project. Documented in the design spec's Deferred section and promoted to a Pattern (`docs/patterns/refresh-worked-examples-when-their-process-changes.md`), since this recurs the same shape a sixth time (one prior fix, five more additions since that never revisited it).

## Misses

None meeting the 2-or-more-specs recurrence threshold this review period. The two Catches above are distinct in shape (a plan-drafting anchor error; a stale illustrative example), each a single occurrence within this batch.

## Friction

None. All three specs moved through their tasks in a single pass each; no fix rounds, no adjudication needed.

## Gaps

- **A worked example illustrating a multi-step process has no check forcing it to stay current when that process gains a new step.** `subagent-driven-development/SKILL.md`'s Example Workflow now demonstrates a Finish sequence six steps shorter than the real one, having gone unrevisited across five additions since its one prior fix. Already named as a Pattern (see Catches above); this Gap entry exists to generate its own Recommendation rather than leave the Pattern as documentation-only.

## Recommendations

- [x] Refresh `subagent-driven-development/SKILL.md`'s Example Workflow section to show the real, current Finish sequence: the spec Status flip, tracker update, Recommendation-checkbox check, notes.md gate, Lessons-learned capture, concept-index step, and bug-tracking ledger scan — not just the workspace-deletion step it currently jumps straight to. (Shipped, commit `f9843f3`; also added the fix-loop's own missing notes.md bracket, a third instance of the same shape found while brainstorming.)
- [x] Add a check (a Self-Review item in `writing-plans/SKILL.md`, or an explicit line in `subagent-driven-development/SKILL.md` itself) requiring a plan that adds a step to a documented multi-step process to also check whether a worked example elsewhere in the same file demonstrates that process, and update it if so — per `docs/patterns/refresh-worked-examples-when-their-process-changes.md`'s own stated rule, closing the mechanism gap that let six additions in a row skip this check. (Shipped as Self-Review item 9 in `writing-plans/SKILL.md`, commit `bfb49e2`; live trial confirmed it correctly triggers and identifies the specific example needing an update.)
