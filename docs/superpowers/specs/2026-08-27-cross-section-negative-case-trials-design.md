# Cross-Section Negative-Case Trials — Design

**Date:** 2026-08-27
**Status:** Approved

## Context

The design spec for `cross-section-mechanism-consistency` deferred trial coverage for the negative (correctly-does-not-fire) case for both Self-Review item 8 and the re-review carve-out. `cross-section-sibling-scope`, extending the same two mechanisms one clause further, deferred the identical gap again, for the identical reasoning, without noting the recurrence. `docs/patterns/escalate-deferred-items-on-second-recurrence.md` names exactly this shape: a Deferred item surviving two consecutive sub-projects on the same mechanism needs an explicit decision, not a third deferral. This spec resolves it.

`docs/patterns/ab-test-live-trials-for-behavior-change.md`'s Rule 2 governs how a negative-case trial has to work: the dispatch prompt presents a scenario only, never names which trigger paragraph governs the outcome, and never states the expected answer. Two prior trials in this project violated Rule 2 by doing exactly that, so this spec's trial fixtures need scrutiny against Rule 2 before trusting their results.

## Decision

Two disposable `--plugin-dir` trials, one per touchpoint, sharing one fixture design: a mock skill file (`plugin/skills/mock-skill/routing.md`) holding real routing/trigger/lifecycle content in one section (`## Apply Config`: "never run standalone; always triggered by the setup wizard") and an unrelated `## Style Notes` section elsewhere in the same file.

Each trial's edit adds one sentence to Style Notes: `Avoid trigger words like "always" or "never" in user-facing error messages; keep tone neutral.` This edit contains the literal word "trigger" but describes writing-style guidance, not a routing/trigger/lifecycle mechanism — no invocation condition, no "proceed to" language, no cross-reference. A naive keyword-matching check could misfire here; a genuinely discriminating check should not.

- **Trial A — item 8 (Self-Review):** dispatches a dry-run plan-drafting session with exactly one task (the Style Notes edit above) and asks it to run Self-Review item 8, reporting whether the trigger condition applies and why.
- **Trial B — carve-out (re-review):** dispatches a re-review session against a fix diff making the same edit, asking whether the cross-section check applies to this diff and why.

Neither dispatch prompt names item 8, the carve-out's trigger phrases, or states an expected outcome — each asks the agent to determine and explain its own answer, per Rule 2.

## Falsifiable Criteria

1. Trial A's trial output reports item 8's trigger condition does NOT apply to the Style Notes edit, with reasoning that names the specific reason (the word "trigger" appears in prose about message wording, not in routing/trigger/lifecycle phrasing describing a mechanism) — not just "no keyword match."
2. Trial B's trial output reports the carve-out's cross-section check does NOT apply to this fix diff, with equivalent reasoning.
3. Neither dispatch prompt names "item 8," "Cross-section mechanism consistency," "the carve-out," or states the expected answer anywhere in its own text — verified by re-reading each prompt against Rule 2 before trusting either result.

## Consequences

If both trials pass: this closes the process review's second Recommendation. Both `cross-section-mechanism-consistency-design.md`'s and `cross-section-sibling-scope-design.md`'s Deferred sections get a note confirming the negative case now — the Deferred bullets themselves stay as historical record, not rewritten.

If either trial finds a false positive (item 8 or the carve-out incorrectly treats the Style Notes edit as triggering its cross-section check): that finding names a real defect in the shipped trigger-recognition language, needing its own fix cycle — out of this spec's scope, to brainstorm separately once the actual failure mode emerges.

## Deferred

- A mechanism spanning more than two sections, and the "and the design spec" clause of either instruction — still untested; unrelated to the negative-case gap this spec closes.
- Further near-miss variations (e.g., "if" language with no routing/lifecycle meaning) — one strong near-miss case suffices to establish the discrimination claim; revisit only if a real false positive of a different shape surfaces later.
