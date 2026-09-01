Lessons-learned capture done, committed as `c214033` on `master`.

## The Lesson entry

Filed under `## Workflow` in `docs/lessons-learned.md:85`:

**### A claim that shipped checks overlap needs the record of what each one caught (2026-09-01-convention-retirement)**

The paragraph records that the Context asserted three shipped checks overlapped and leaned on that to argue the Retirements section would find work on its first run; that two live trials examined all three against the shipped text and rejected every one; and that the claims came from titles and first sentences — the level at which checks written for different defects read as near-duplicates, since a title compresses away the specific thing its check catches. It names `notes.md`'s Catch lines as the evidence that would have settled it: two checks sharing one Catch record between them genuinely overlap, two with distinct records do not.

> **Rule:** before asserting in a spec that a shipped check, rule, or gate duplicates another — or that it has earned retirement — establish the claim from the record of what each one has actually caught, not from its title and opening sentence. A check with no Catches since shipping is a real and citable finding, and it differs from a check that duplicates another; surface wording cannot tell those two apart.

## The promotion decision: promoted

I compared this Rule sentence against all 17 existing ones. One matched — **"An added instruction can suppress a behavior the model already produced" (2026-09-01-research-skill-adoption)**: *before adding an instruction to make a model do X, check whether it already does X without one.*

Same act, opposite direction. Both gather a shipped process instruction's function from its text (or from no observation at all) rather than from evidence of its behavior, then edit the instruction set on that basis — one adding, one retiring — and both were falsified by a live run. That entry had deferred promotion pending a second *suppression* instance; this is a second instance of the underlying act, and the skill's comparison rule promotes both regardless of either note's own deferral. So I also amended that entry's promotion note to point at the shared Pattern.

New file `docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md`, with a four-step Pattern (name the behavioral claim → read the Catch record for retirement claims → run a control arm for addition claims, via the existing A/B pattern → record "never fired since shipping" as its own finding), both directions as worked Examples, and both lessons listed as originating.

Nearest non-matches I ruled out, for the record: `verify-against-precedent-before-flagging` (a reviewer's literal rule-match, remedied by source intent — not a catch record), `re-verify-quotes-against-source-before-citing` (verbatim wording; a phrase grep cannot test whether two checks overlap), and `ab-test-live-trials-for-behavior-change`'s Rule 3 (misreading a trial that ran — here the trials were what corrected the error).

**One thing to flag:** this repo snapshot has no `convention-retirement` spec, plan, outcomes file, `notes.md` Catch entries, or `.superpowers/sdd` workspace — `git log` holds a single squashed commit. I wrote the entry from your account of the sub-project and used the dated slug `2026-09-01-convention-retirement` for consistency with every sibling entry, but that slug won't resolve to a file until the spec lands. The other Finish steps (Status flip, tracker append, Recommendation checkbox, notes.md gate, concept-index, bug-tracking) have no artifacts here to act on either — I did only the step you asked for.
