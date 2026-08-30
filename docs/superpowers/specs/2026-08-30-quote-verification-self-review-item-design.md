# Quote Verification Self-Review Item — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

`review-after-2026-08-30-fix-wave-regression-amendment-design.md` names one Recommendation, closing Miss M1 and Gap G1: two specs in the same review batch each cited a source document's content or exact wording from memory rather than a fresh read — one treated a retracted finding as current, the other presented two fabricated "direct quotes." Both already got unified under `docs/patterns/re-verify-quotes-against-source-before-citing.md` at the time each got caught, but the Pattern has no Self-Review cross-reference, unlike its sibling `docs/patterns/verify-plan-commands-against-real-content.md` (numeric-claim verification), which got one from `brainstorming` item 6 and `writing-plans` items 10/12 in the immediately preceding sub-project.

## Decision

**`brainstorming/SKILL.md`'s Spec Self-Review gains item 7**, appended after the existing item 6, matching its sibling's shape and cross-reference style:

```markdown
7. **Quote and source-freshness verification:** Does the spec cite an
external or previously-read document's content, or present anything
in quotation marks? If so, grep the source for the exact quoted
phrase, and re-read the full document fresh if it describes state (a
report, a tracker, a shipped file) that might have changed since you
last read it — not just what you recall it saying. See
docs/patterns/re-verify-quotes-against-source-before-citing.md for
the specific failure shapes a plausible-looking citation has actually
hit before.
```

## Falsifiable Criteria

1. A direct read-through of `brainstorming/SKILL.md`'s Spec Self-Review confirms item 7 exists, worded identically to the Decision block above.

## Consequences

A future spec citing an external document's content or wording gets checked against the same known failure catalog that already closed the equivalent gap for numeric claims — closing the asymmetry between the two sibling patterns' Self-Review coverage.

## Deferred

- The remaining trial findings (D5, D7, D10/M1) — tracked separately for follow-up sub-projects.
