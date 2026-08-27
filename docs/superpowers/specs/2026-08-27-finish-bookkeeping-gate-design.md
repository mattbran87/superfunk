# Finish Bookkeeping Gate — Design

**Date:** 2026-08-27
**Status:** Shipped

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-sibling-scope-design.md` named its first Recommendation: Finish's own bookkeeping — a spec's `Status` line, the tracker's "Specs shipped since" list, and a closed Recommendation's checkbox — recurred as unactioned in two specs (`process-review-recommendations-batch-2`, `cross-section-mechanism-consistency`), caught only by a later final review rather than at Finish time itself.

Reading `plugin/skills/subagent-driven-development/SKILL.md`'s current Finish section during this brainstorm found the root cause runs deeper than a missing gate: the section never instructs the controller to check off a Recommendation checkbox at all. Only the `Status` flip and the tracker append exist as written steps today. The checkbox omission recurred because nothing told the controller to do it, not because a written step got skipped.

A naive gate design — grepping the review file for the shipping spec's own filename — would produce a false negative against this session's own already-correct work: the real `(Shipped as ...)` annotations already in the repo cite implementing commit SHAs and file names, never the spec's filename or slug. The gate instead needs to match on a snippet of the Recommendation's own original wording, something the controller already holds after locating and checking off the matching bullet.

## Decision

`subagent-driven-development/SKILL.md`'s Finish section gains one new paragraph, inserted between the existing tracker-append paragraph and the Lessons-learned capture paragraph:

```
If the spec's Context section names a
`docs/superpowers/process-reviews/review-after-*.md` file, that file
holds the Recommendation this spec closes. Open it, find the matching
`- [ ]` Recommendation by content, and check it off: change it to
`- [x]` and append `(Shipped as <what shipped>, commit <sha>.)` naming
this spec and its key implementing commit. Commit this change in the
same commit as the Status and tracker updates above. No review file
named: skip this step.
```

Immediately after it, a verification block:

```
Before moving on, verify this Finish pass's own bookkeeping landed:

grep -c "^\*\*Status:\*\* Shipped" <spec-file>
grep -c "<spec filename>" docs/superpowers/process-reviews/tracker.md
grep -c "\[x\].*<a few distinctive words from the Recommendation's own original text>" <review-file>

Run the third check only when a review file was named above. Each
check that applies should return at least 1. A 0 means that action
never happened — do it now, before starting the Lessons-learned
capture below, not left for a later final review to notice.
```

The third grep matches on wording drawn from the Recommendation bullet itself, not the spec's filename — the controller already has this text in hand from the matching step above, and it survives into the checked-off line regardless of what the shipped-as annotation cites.

The whole paragraph and gate apply only inside the existing "if it does [trace to a spec]" branch of Finish — a plan with no design spec skips all of it, matching the Status paragraph's existing skip clause.

## Falsifiable Criteria

1. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the new Recommendation-checkbox paragraph and the three-grep verification block exist, in that order, between the tracker-append paragraph and the Lessons-learned paragraph.
2. A disposable `--plugin-dir` trial builds a fixture spec (Status: Approved, Context naming a fixture review-after file), a fixture tracker.md missing the spec's filename, and a fixture review-after file with the matching Recommendation still `- [ ]`. Running Finish against this fixture completes all three actions (Status flip, tracker append, checkbox check-off) and the three verification greps all return at least 1 afterward.
3. A second trial builds the same three fixtures already fully compliant (Status: Shipped, tracker already lists the spec, Recommendation already `- [x]`). Running Finish's verification block against this fixture confirms all three greps already return at least 1, and no duplicate edit or re-commit happens.

## Consequences

Every Finish pass that traces to a design spec gains one more paragraph to read and, when a Recommendation applies, one more file to edit — negligible added cost, since most specs already require reading their own Context section during Finish's existing Status-flip check.

A spec with no design spec, or a spec not tracing to any process-review Recommendation, sees no change: the new paragraph and its gate both skip cleanly via existing precedent (the "no spec, skip" and "no review file named, skip" clauses).

## Deferred

- Automatically identifying WHICH `- [ ]` Recommendation matches a given spec when a review file lists more than one open Recommendation — stays a controller judgment call (read the Recommendation text, compare to the spec's Context), not a mechanical match. No evidence yet shows this judgment call producing a wrong match.
- Extending this same three-part gate shape to any other Finish-adjacent bookkeeping not yet identified — revisit only if a new gap of this shape surfaces.
- **Discovered in first real use (2026-08-27, `cross-section-negative-case-trials`):** the gate depends entirely on a spec's Context section citing the originating `review-after-*.md` file. Nothing checks that a spec genuinely closing a Recommendation actually includes this citation — a spec author can reference the Recommendation's history only through the intermediate specs that deferred it (as this sub-project's own first draft did) and the gate will silently treat it as "no review file named," never flagging the missing citation. Caught and fixed by hand before Finish ran; no mechanical check exists yet to catch this for a future spec. Revisit if it recurs.
