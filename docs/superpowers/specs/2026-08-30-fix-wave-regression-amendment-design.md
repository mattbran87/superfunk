# Fix-Wave Regression Amendment — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

The external bookmark-cli trial's D9 finding, independently confirmed by the trial's own internal process-review (filed as G1), names a gap in `subagent-driven-development/SKILL.md`'s Final Review section: "There is no second fix wave — residual load-bearing findings surface to your human partner when finishing-a-development-branch presents the options."

In cycle 3, the single permitted fix wave introduced a new crash: `for_opening` read `parts.port`, which raises on a malformed port. One typo'd URL stored a poison row that made `bm list` exit 3 displaying nothing — every bookmark invisible. The re-review of that same wave caught it. The rule as written left three options, all bad: merge a known crash that hides the user's entire library, stop the human to approve a one-line guard after they had already given blanket consent, or break the stated rule. The framework broke the rule, dispatched one extra scoped fix, and declared the reasoning explicitly — the best available choice, but still a rule violation the rule's own shape forced.

The trial's own process-review (`review-after-2026-08-29-edit-command-design.md`, G1) reached the same diagnosis independently: "The rule exists to prevent unbounded review-fix cycles. A regression introduced *by* the wave and found *by* its own re-review does not risk that: it is bounded by construction, because the re-review happens once." That same review's Recommendations section already drafted the amendment this spec ships: "Amend the Final Review section of `plugin/skills/subagent-driven-development/SKILL.md` to allow exactly one follow-up dispatch scoped to regressions the fix wave itself introduced, distinguished from findings it failed to fix, which stay parked. Still capped at one, still followed by verification."

## Decision

**`subagent-driven-development/SKILL.md`'s Final Review section's fix-wave paragraph gains one exception**, distinguishing a regression the wave introduces from a finding the wave fails to fix:

```markdown
Then run exactly one scoped re-review of the fix wave
(`scripts/review-package PLAN_FILE FIX_BASE HEAD` over the fix range,
[re-review-prompt.md](re-review-prompt.md)).
Adjudicate any residual findings as in the task loop's breaker: park with
rulings, or stop on load-bearing ones — with one exception. A finding
that's a regression the fix wave itself introduced (absent before the
wave, not one it failed to address) gets exactly one additional scoped
fix dispatch, scoped to that regression alone, followed by one more
scoped re-review over that narrower range. This stays bounded by
construction: it fires at most once, only for a defect the wave itself
caused. Everything else follows the existing rule unchanged — there is
no second fix wave for a finding the first wave simply failed to fix;
residual load-bearing findings surface to your human partner when
finishing-a-development-branch presents the options.
```

The process diagram's `"Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals"` node stays unchanged — it already condenses the whole fix-wave stage into one box at a level too coarse to show this internal distinction, and the overall stage count (one fix dispatch, one re-review, then adjudicate) still holds for the common case this box describes.

## Falsifiable Criteria

1. A direct read-through of `subagent-driven-development/SKILL.md`'s Final Review section confirms the amended paragraph exists, worded identically to the Decision block above.
2. A disposable `--plugin-dir` trial constructs a fixture where a scoped fix wave's own change introduces a new, distinct regression (absent before the fix, not among the findings the fix dispatch targeted). Following the amended rule, the controller correctly dispatches exactly one additional scoped fix for that regression, runs one more scoped re-review, and does not treat this as a second full fix wave for the original findings.
3. A second disposable trial constructs a fixture where the re-review finds a residual finding the fix wave simply failed to address (not a new regression). The controller correctly applies the unchanged existing rule — park with a ruling, or stop if load-bearing — without dispatching a second fix.

## Consequences

A future fix wave that introduces its own regression gets exactly one more bounded chance to fix that specific regression, closing the gap that forced a real rule violation in the trial. The distinction between "the wave failed to fix this" and "the wave caused this" stays load-bearing: conflating them either reintroduces unbounded fix cycles (if any residual finding gets a second wave) or reintroduces the original gap (if a genuine regression stays unaddressed until a human notices).

## Deferred

- The remaining trial findings (D5, D7, D10/M1) — tracked separately for follow-up sub-projects.
