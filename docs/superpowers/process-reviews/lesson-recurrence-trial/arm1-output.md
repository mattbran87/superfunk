Committed as `3492fa7`.

## The Lesson entry

Filed under `## Workflow` in `docs/lessons-learned.md:85`, at the end of that section's chronological run:

**### Three "these checks overlap" claims, all read off titles and first sentences, all wrong (2026-09-01-convention-retirement)**

The paragraph records that the Context named three shipped checks, asserted each overlapped another, and used the three together to argue the Retirements section would find real work on its first run; that two live trials tested all three against shipped text and rejected every one (the checks share subject matter, not coverage); that the mechanism survived the trials unchanged and only its motivating evidence collapsed; and that the sub-project's own output already specified the standard its Context failed — Retirements' fixed reason set requires a Subsumed reason to name the covering check and a Zero-yield reason to state both that no entry attributes a Catch to the check across the last 3 reviews and that the check existed at the window's start.

> **Rule:** before asserting that one check, rule, or gate overlaps another — in a spec's Context, in a Retirement item, or in any argument for removal — read both in full and check the record of what each one has actually caught. A title and an opening sentence state a check's subject; overlap is a claim about coverage and outcomes, and shared subject matter is the weakest possible evidence for it.

## Promotion decision: promoted

Written to `docs/patterns/verify-overlap-claims-before-proposing-removal.md`, with the standard Context / Pattern / Example / Originating lessons structure. Promoted on the prospective-rule test rather than on recurrence: the rule applies to any argument for removal, and this sub-project's own shipped Retirements section makes removal arguments a routine `process-review` output — waiting for a second instance means waiting while the framework generates them on a schedule. The Pattern's three steps are read both in full, consult the catch record, and name the specific evidence in the claim itself; it also records "nothing to retire" as a valid result.

I checked the two nearest existing patterns before writing a new file rather than folding in: `re-verify-quotes-against-source-before-citing.md` covers stale or fabricated *citations* (the source read from memory), and `verify-against-precedent-before-flagging.md` covers a *reviewer* treating a literal rule-match as a defect. Neither covers the distinguishing evidence type here — the record of what a check actually caught.

Two things you should know about what I could verify:

- No `convention-retirement` design spec exists anywhere in this repo; the only trace is the Deferred item in `docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md:303` that spawned it. I used `2026-09-01-convention-retirement` as the slug on that basis. Correct me if the real spec filename differs and I'll update both files.
- The repo's `plugin/skills/process-review/SKILL.md` does not contain the Retirements section either. The shipped text I quoted in the Lesson and the Pattern came from the live plugin copy at `C:/sf-recur-plugins/arm1/skills/process-review/SKILL.md:94-130`, which I read directly. I did not name the three specific checks, since nothing on disk records which three they were.

This was the Lessons-learned step only — the Status flip, tracker append, Recommendation checkbox, concept-index, bug-tracking, and workspace deletion steps of Finish are untouched.
