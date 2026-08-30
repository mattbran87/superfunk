# Cross-Reference Verification Pattern — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

`review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md` names two Recommendations, closing Miss M1 and Gap G1:

1. Self-Review items 6 (`brainstorming/SKILL.md`), 10, and 12 (`writing-plans/SKILL.md`) instruct authors to verify a numeric or pattern-matching claim, but none point to `docs/patterns/verify-plan-commands-against-real-content.md`, which already catalogues five distinct failure shapes an author would otherwise have to rediscover from scratch (line-vs-occurrence counting, anchored patterns against indented/fenced content, case sensitivity, a phrase's other appearances in the same file, a substring legitimately retained elsewhere).
2. The same review asked whether `2026-08-30-doc-timing-and-mutation-check-design.md`'s deferred "scripted verification helper" idea deserved reconsideration, given seven manual-verification misses across the three specs that review covered.

Reconsidering the second point directly: every one of those seven misses got caught, before shipping, by the same "run the actual command" step items 6/10/12 already mandate. The mechanism worked every time it ran — the high recurrence reflects the manual step catching real mistakes, not the manual step failing to catch them. A scripted helper would speed up running a plain `grep`, which isn't the bottleneck; the cases that actually took real effort (simulating a multi-line substitution before it lands) needed custom, situation-specific code each time regardless of any generic tool, since each substitution's shape differs. The deferral stands.

## Decision

**`writing-plans/SKILL.md`'s Self-Review items 10 and 12 each gain one added sentence** pointing to the pattern file:

- Item 10 (Verified numeric expectations) gains, appended to its existing text: `See docs/patterns/verify-plan-commands-against-real-content.md for the specific failure shapes a plausible-looking prediction has actually hit before checking it against a known list beats re-discovering the same trap.`
- Item 12 (User-facing documentation timing) needs no addition — it doesn't itself state a numeric or pattern-matching claim; it checks a task-structuring rule. Only item 10 carries this addition in `writing-plans`.

**`brainstorming/SKILL.md`'s Spec Self-Review item 6 gains the same added sentence**, appended to its existing text.

**`review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md`'s second Recommendation gets checked off with a deferral note**, not a shipped note: `(Deferred: reconsidered directly in 2026-08-30-cross-reference-verification-pattern-design.md — every miss this review found already got caught by the existing "run the command" step; a scripted helper would speed up the easy case without addressing the case that actually took effort. Revisit only if a future miss escapes the existing manual step undetected.)`

## Falsifiable Criteria

1. A direct read-through of `writing-plans/SKILL.md`'s item 10 confirms the added sentence exists, worded identically to the Decision block above.
2. A direct read-through of `brainstorming/SKILL.md`'s item 6 confirms the added sentence exists, worded identically to the Decision block above.
3. A direct read-through of `review-after-2026-08-30-rebrand-string-and-worktree-ignore-design.md` confirms its second Recommendation reads `[x]` with the deferral note above, and its first Recommendation reads `[x]` with a shipped note once this spec's plan executes.

## Consequences

A future author hitting item 6, 10, or 12 gets pointed directly at five already-documented failure shapes instead of independently re-learning that verification hides real traps each time — a small reduction in the friction this batch's own three specs each paid at least once.

Declining to build a scripted helper means this same class of miss likely recurs again in some future sub-project — accepted, since every instance so far got caught before shipping, and the cost of building and maintaining a generic tool for a problem the existing manual step already solves outweighs the marginal speed gain.

## Deferred

- The scripted verification helper itself — explicitly not building it, per this spec's own Decision and Consequences. Revisit only if a future numeric or pattern-matching miss ships undetected, past the existing Self-Review step.
