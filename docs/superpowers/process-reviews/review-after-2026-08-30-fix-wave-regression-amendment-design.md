# Process Review — after 2026-08-30-fix-wave-regression-amendment-design.md

**Date:** 2026-08-30

## Specs Reviewed

- 2026-08-30-cross-reference-verification-pattern-design.md
- 2026-08-30-pattern-template-and-convention-bootstrap-design.md
- 2026-08-30-fix-wave-regression-amendment-design.md

## Catches

**2026-08-30-cross-reference-verification-pattern-design.md**
- None. Both tasks shipped clean on first pass; no findings.

**2026-08-30-pattern-template-and-convention-bootstrap-design.md**
- Spec self-review: most of the spec's D2/D3 fix got written from an earlier read of the external trial findings report, treating its original finding ("the files don't exist anywhere," "the framework invented a format") as settled — the report carried a same-day correction, embedded in the same file, retracting both claims. Surfaced only because a tangential numeric claim needed checking against the source, and the spec got fully rewritten around the corrected finding before shipping.
- Task 1: the plan's verification predicted a repo-wide grep for `pattern-template.md` would return zero everywhere, but historical specs, plans, and notes.md entries legitimately still mention the filename as a record of what happened — the check was too broad and got scoped to `plugin/` only.
- Task 4 live trial: the scaffold-accepted trial surfaced a real but minor behavioral gap — the session deferred its own scaffold offer once it decided the timing wasn't right, then didn't proactively bring it back without an explicit prompt asking what happened to it. Not filed as a bug given single occurrence and minor severity.

**2026-08-30-fix-wave-regression-amendment-design.md**
- Spec self-review: two "direct quotes" in the Context section, attributed to the trial's own internal process-review file, turned out to be paraphrases reconstructed from memory rather than the file's actual text — caught by grepping the source for the quoted phrases and finding no match, then fixing both against the real text.

## Misses

### M1. Citing a source's content or wording from memory instead of a fresh read — 2 occurrences across 2 specs

The pattern-template-and-convention-bootstrap Catch (a retracted finding treated as current) and the fix-wave-regression-amendment Catch (two quotes reconstructed from memory, one fabricated outright) are the same underlying failure: treating an earlier read of a document as still authoritative, whether for its content or its exact wording. Both already got promoted to a single Pattern (`docs/patterns/re-verify-quotes-against-source-before-citing.md`) at the time each was caught. This Miss entry exists to note the recurrence formally and check whether the promoted Pattern needs the same treatment its sibling (numeric-claim verification) already got.

## Friction

None rising to the 3-fix-round threshold. `pattern-template-and-convention-bootstrap`'s three Catches spanned spec-writing, one task, and one live trial — not concentrated fix rounds on a single task.

## Gaps

### G1. The newly-promoted quote-verification pattern has no Self-Review cross-reference, unlike its numeric-verification sibling

`docs/patterns/verify-plan-commands-against-real-content.md` (the numeric-claim-verification pattern) got a direct cross-reference from `writing-plans` item 10 and `brainstorming` item 6 in the immediately preceding sub-project, closing a Gap that same review named. `docs/patterns/re-verify-quotes-against-source-before-citing.md` — promoted this same review period, addressing the identical class of self-referential miss for quotes and document-state claims rather than numbers — has no equivalent cross-reference from any Self-Review item. Without one, a future spec author re-derives "verify quotes against source" from scratch instead of being pointed at the pattern's own catalogued examples, the same gap G1 (of the prior review) closed for numeric claims.

## Recommendations

- [x] Add a Self-Review item (or extend an existing one) in `brainstorming/SKILL.md`'s Spec Self-Review, cross-referencing `docs/patterns/re-verify-quotes-against-source-before-citing.md`: before finalizing a spec, grep the cited source for any sentence presented in quotation marks, and re-read the full source fresh if it describes an external or previously-read document whose state might have changed since the last read. Addresses M1 and G1. (Shipped as Spec Self-Review item 7, commit `a8589511a10ff0b5041de5a3b45f326c9a18f2a8`.)
