# Process Review — after 2026-08-27-cross-section-recursion-boundary-design.md

**Date:** 2026-08-27

## Specs Reviewed

- 2026-08-27-finish-bookkeeping-gate-design.md
- 2026-08-27-cross-section-negative-case-trials-design.md
- 2026-08-27-cross-section-recursion-boundary-design.md

## Catches

**A note on evidence for this review:** `docs/superpowers/process-reviews/notes.md` holds zero real-time entries for all three specs this review covers, despite genuine findings occurring in two of them. Per this skill's own Step 4, the Catches below get reconstructed from `git log` fix-commit messages, not from the running log. This gap recurs the exact shape a prior review already named and built a mechanical gate for — see Misses and Gaps below for why the gate didn't catch it this time.

**2026-08-27-finish-bookkeeping-gate-design.md**
- Task 1 shipped clean on first pass (self-reviewed directly by the controller after this session's Agent-tool subagent spawn limit was reached) — no fix commits, no Catches from implementation.
- The gate's own first real (second) use, in `cross-section-negative-case-trials`, found a real blind spot: a spec can close a Recommendation while citing only the intermediate specs that deferred it, never the `review-after-*.md` file itself, and the gate would silently report "no review file named" rather than flag a likely-missing citation. Recorded in this spec's own Deferred section (commit `1fa2dea`) rather than fixed as a mechanical check yet.

**2026-08-27-cross-section-negative-case-trials-design.md** (reconstructed from git log, `18f8e4d..7afe61c`)
- Commit `461db45`: Falsifiable Criterion 3, as originally drafted, would have forbidden naming the mechanism under test at all ("item 8," "the carve-out") in either trial's dispatch prompt — a misreading of Rule 2, which only forbids revealing the discriminating fact or the answer, not naming which check to run. Caught before the implementation plan got built around the over-strict wording.
- Commit `ce978c4`: the spec's own Context section never cited `docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-sibling-scope-design.md`, even though this spec closes that review's second Recommendation — citing only the two intermediate specs that had deferred the gap instead. Caught by re-reading the spec once more before running Finish, not by any check that forced the read.

**2026-08-27-cross-section-recursion-boundary-design.md**
- Both tasks shipped clean on first pass, self-reviewed directly, word-for-word match confirmed against the Decision block. No fix commits, no Catches.

## Misses

- **`notes.md` received zero real-time entries across all three specs this review covers, despite genuine findings in two of them.** This recurs the exact shape a prior review already caught and built a mechanical gate for (`subagent-driven-development/SKILL.md`'s Complete-the-task step: "confirm `notes.md` contains at least one entry" when a fix loop runs a round). The gate itself is sound, but its trigger condition — "if this task's fix loop ran at least one round" — assumes the standard dispatched-implementer-then-review cycle. All three specs in this review ran through a different path: the session's Agent-tool subagent spawn limit forced the controller to implement and review every task directly, catching and fixing issues (Criterion 3's scoping, the missing citation) inline rather than through a dispatched implementer's fix loop. The gate never fired because no fix loop, in the structural sense the gate checks for, ever ran — even though real findings occurred that the running log exists to capture.

## Friction

- None meeting the 3-round threshold this review period. All three specs moved through their tasks in a single pass each, direct-implementation mode substituting for the usual subagent dispatch cycle throughout (see Misses and Gaps).

## Gaps

- **No check confirms `notes.md` logging happens when the controller implements and reviews a task directly, without dispatching a subagent.** The existing gate's condition is scoped to "this task's fix loop ran at least one round" — a structure specific to the dispatched-implementer workflow. When subagent dispatch is unavailable (as it was for all three specs in this review) and the controller self-catches a real issue during direct implementation, nothing prompts a `notes.md` entry the way a dispatched fix loop's completion step would.

## Recommendations

- [ ] Widen the `notes.md` logging gate in `plugin/skills/subagent-driven-development/SKILL.md`'s Complete-the-task step (or add a parallel instruction) to also require a `notes.md` entry when the controller implements and reviews a task directly — without subagent dispatch — and catches a real issue during that direct review. The current gate's condition ("if this task's fix loop ran at least one round") never fires in this mode, even when genuine findings occur.
