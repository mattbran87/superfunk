# Outcomes — 2026-09-01-convention-retirement.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Give `notes.md` the attribution field
Shipped as planned. The header now documents the five-field format and names `none — found ad hoc` as the value for a Catch no check produced. All 88 pre-existing entries stayed byte-identical, confirmed by `git diff | grep -c "^[+-]- 20"` returning `0`. Em dashes preserved, verified by grepping the literal string rather than by eye.

## Task 2: Teach `process-review` to read both entry shapes
Shipped, with a plan defect the implementer caught. The plan's verification anchor `carrying no attribution` spans a markdown line wrap in the very text the plan prescribed inserting — `carrying no` ends one line, `attribution:` begins the next — so a single-line `grep` returns `0` however correctly the edit lands. The implementer inserted the prescribed text verbatim, ran the command, got `0`, and reported `DONE_WITH_CONCERNS` rather than reflowing the prose to make the check pass. Anchor corrected to `predates the attribution field`, verified at `1`.

## Task 3: Add the Retirements section
Shipped, with a second plan defect the implementer caught. The plan predicted `grep -c "Zero-yield"` would return `2`; the real count is `3`, because the plan's own insertion names it twice — once in the attribution-coverage sentence and once as the bolded reason item — plus once in No Placeholders. Indentation matched the sibling `- **Recommendations**` bullet exactly, at three spaces, verified post-edit.

## Task 4: Require Recommendations to name what they replace
Shipped as planned, no divergence. Three of its four verification commands existed solely to prove Task 3's adjacent Retirements block survived the edit, since the anchor line sits directly above it. All passed, with surrounding lines quoted as evidence.

## Task 5: Run the trial that can falsify the design
Two runs. The mechanism performed well; the trial design was mine and it leaked twice.

**Criterion 6 — passed, both runs.** The Retirements section fired, opened with attribution coverage, and correctly refused to use Zero-yield. Run 2 gave three independent reasons: 9 of 9 entries unattributable, only one prior review in existence against a 3-review requirement, and that review absent from the working tree entirely.

**Criterion 7 — untested.** Both runs proposed zero Retirements, so no proposal existed to independently check. The runs did the opposite of the feared failure: across the two, they examined six candidates and rejected every one against real shipped text rather than reaching for a removal. That is reassuring but is not evidence about how the section behaves when it does propose one. The criterion stays open.

**Criterion 8 — passed in part, on the second attempt.** Run 1's fixture leaked the three subsumption candidates, because the fixture build copied the design spec whose Context names them. Run 2 removed that spec, and the leak survived by a second route: the fixture's git history still held run 1's committed review file, which the run retrieved via `git show`. Both runs detected their own contamination and disclosed it unprompted, without being asked to check for it.

Run 2 did demonstrate genuine independent discovery on a candidate no document named — `writing-plans` item 12, tested for **Vacuous**. It grepped all 10 fixture specs, found exactly one carrying `User-Facing: Yes`, and rejected the vacuity claim on that evidence. It separately tested items 13 and 14 for Zero-yield and rejected them on the check's-age half of the rule, both having shipped inside the window.

**The most useful finding concerns the spec, not the mechanism.** The trials rejected all three subsumption candidates the spec's Context asserted, with citations since verified: `notes.md` 2026-08-28 states the Self-Review "has no item checking a plan's own header against its own required template," which is precisely why item 11 exists rather than duplicating items 1 and 2; and `notes.md` 2026-08-27 records item 8's grep scope as a known gap that does not reach item 9. The spec's Context has been corrected, and the original claims kept for the record.

**Follow-up:** Criterion 7 needs a review that actually proposes a Retirement. Until one does, the design's central risk — a section confidently proposing removal on invented overlap — stays unexercised.
