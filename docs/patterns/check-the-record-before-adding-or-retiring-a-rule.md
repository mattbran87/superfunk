# Check the record before adding or retiring a rule

A claim about what a rule, check, or model already does needs evidence of behavior, not evidence of text.

## Context

This pattern applies whenever a spec argues for editing the instruction set —
adding a new rule, or retiring an existing one — and grounds that argument in a
claim about current behavior:

- "No skill asks for X, so the model does not produce X."
- "These two checks overlap, so one of them can retire."
- "Nothing enforces Y today."

Each claim describes behavior. Each one tempts an author to settle it by
reading text: grep the skill files, read the check titles, skim the opening
sentences. Text answers a different question. A grep proves an instruction's
absence, never a behavior's absence. A title states a check's subject, never
its coverage.

Both directions have shipped a design on a false premise, and a live run
falsified both.

## Pattern

Before a spec's justification rests on what something currently does:

1. **Name the behavioral claim in one sentence.** Write down what the design
   assumes about current behavior. A claim you cannot state plainly stays
   untested by default.
2. **For a retirement or overlap claim, read the record of what each check
   caught.** `docs/superpowers/process-reviews/notes.md` records Catches per
   mechanism. Two checks sharing one Catch record between them overlap. Two
   with distinct records do not, whatever their titles suggest.
3. **For an addition claim, run a control arm.** One pre-change arm answers
   "does the model already do this" in a single run. See
   `ab-test-live-trials-for-behavior-change.md` for the trial design.
4. **Record a null result as a finding, not as an absence of evidence.** "This
   check has caught nothing since it shipped" states a real, citable fact, and
   it differs from "this check duplicates another." Surface wording cannot
   separate the two.

A claim that survives none of these steps still belongs in the spec — labelled
as an assumption, not as a justification.

## Example

**Adding.** `2026-09-01-research-skill-adoption` proposed two additions to
`brainstorming`'s step 4: a null-option candidate and a flip factor. Its
justification ran a keyword probe across all 24 skill files and found zero
matches, then concluded the model produces neither behavior. The A/B trial
found the flip factor in three of four arms, including both pre-change arms.
In the null-option scenario the unmodified skill gave the better answer. The
spec withdrew one section and amended another.

**Retiring.** `2026-09-01-convention-retirement` asserted three shipped checks
overlapped each other and used that to argue the new Retirements section would
find real work on its first run. The claims came from reading check titles and
first sentences. Two live trials examined all three against the shipped text
and rejected every one. `notes.md` already recorded why item 11 exists rather
than duplicating items 1 and 2 — the evidence sat in the record, unread.

## Originating lessons

- "An added instruction can suppress a behavior the model already produced" (2026-09-01-research-skill-adoption)
- "Candidates asserted to justify a design can fail the design's own first test" (2026-09-01-convention-retirement)
