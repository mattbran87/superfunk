# Escalate a Deferred item that survives two consecutive extensions of the same mechanism

When a design spec's Deferred item still applies, unresolved, to a second spec extending the same mechanism, treat that recurrence as the trigger to decide — not as another silent deferral.

## Context

A design spec often defers real test or scope gaps deliberately, with sound reasoning at the time (cost asymmetry, no evidence yet, narrower priority). When a later sub-project extends the same mechanism one clause further, it's easy to copy the same Deferred bullet forward with the same reasoning — the reasoning was sound the first time, so it reads as still sound. But a clean, well-tested sub-project provides no signal that would ever force a revisit: nothing about "the mechanism works" surfaces the gap that was never tested in the first place.

## Pattern

Before finalizing a new spec's Deferred section, check whether any bullet restates a gap already deferred in the spec it extends. If it does:
1. Name the recurrence explicitly — "this gap has now gone untested across N consecutive sub-projects" — rather than restating the original reasoning as if it were new.
2. Decide: resolve it in this sub-project, schedule it for the next one, or record a specific reason it stays deferred a further time. A bare re-copy of the same bullet is not a decision.

## Example

- `cross-section-mechanism-consistency`'s spec deferred negative-case trial coverage, reasoning the cost asymmetry favored testing the positive cases first. `cross-section-sibling-scope`, extending the same two mechanisms one clause further, deferred the identical gap for the identical reasoning, without noting it had already survived one full extension untouched. The final review caught the silent recurrence and named it as a two-sub-project-old streak, not a fresh call.

## Originating lessons

- "A Deferred item that survives two consecutive sub-projects on the same mechanism needs an explicit decision, not a third deferral" (2026-08-27-cross-section-sibling-scope)
