# Process Review — after 2026-10-15-watchlist-and-findings-batch-design.md

**Date:** 2026-10-15
**Window:** entries dated after 2026-09-01 (the last review, `2026-09-01-behavioral-claim-verification-design.md`)
**Procedure:** the 9-step `process-review` that this window's last spec shipped. This review gives steps 2, 3, and 5 their first live run. The Skill tool served the pre-change text, so the review followed `plugin/skills/process-review/SKILL.md` as read from disk (see Friction F1).

## Specs Reviewed

- `2026-09-02-process-review-batch-r1-r4-design.md`
  - Outcomes read: `docs/superpowers/plans/2026-09-02-process-review-batch-r1-r4-outcomes.md` (stem rule). The `**Spec:**` rule found no plan, because the field did not exist yet.
- `2026-09-02-executing-plans-review-step-design.md`
  - Outcomes read: `docs/superpowers/plans/2026-09-02-executing-plans-review-step-outcomes.md` (stem rule). The `**Spec:**` rule found no plan.
- `2026-10-15-watchlist-and-findings-batch-design.md`
  - Outcomes read: `docs/superpowers/plans/2026-10-15-watchlist-and-findings-batch-outcomes.md` (stem rule). The `**Spec:**` rule found the same plan, `2026-10-15-watchlist-and-findings-batch.md`, so no second file.

## Catches

The window holds 22 `notes.md` entries: 19 `Catch` and 3 `Watch` (`notes.md:132-153`). Step 4 found no fix commit without a matching entry.

**process-review-batch-r1-r4** (7 entries, all five-field):

- `:132-134` — Three successive enumerations of SDD's Finish list each stopped short (the bump step, then concept-index, then the bug-tracking sweep). The rule-membership check caught all three.
- `:135` — The plan misquoted Rule 1 point 5's ending in an insertion anchor. The implementer flagged it.
- `:136` — The trial archive README pointed at the verdict file for the judge prompt, which the archive lacked.
- `:137` — `executing-plans` Steps 3 and 4 opened with the same phrase. Ruled accepted.
- `:141` — Three "no changelog exists" dispositions contradicted the repo's recorded MAINTAIN position on `plugin/RELEASE-NOTES.md`. The human partner caught it.

**executing-plans-review-step** (2 entries):

- `:142` — Trial 1 invoked `subagent-driven-development` when told to use `executing-plans`. Four fields.
- `:143` — Step 4's opener still repeated the phrase that Step 3 dropped.

**watchlist-and-findings-batch** (10 entries):

- `:144` — The plan dictated a non-imperative commit subject.
- `:145` — The plan's v6.3.0 release-note bullet credited the fork with a header older than the fork.
- `:146` — A fourth spec-trace definition (`re-review-prompt.md:95`) used other words, so the plan's phrase grep missed it.
- `:147` — The new `**Spec:**` rule collided with the date rule's ambiguity skip.
- `:148` — Fix round 1 changed step 3 and left the spec's quote of it stale.
- `:149-153` (final review, four fields each) — duplicate watchlist seeds on step 5's first run; stale deferral notes on two Recommendations; a bump-gate sentence that read two ways; a Consequence claiming a nonexistent watch entry; the fix wave leaving the spec's step-5 quote stale.

## Misses

**M1 — The write-site templates still produce four-field entries, six weeks after the five-field format shipped.** The five-field format, with its check field, shipped on 2026-09-01 (`2cdfe94`). The three templates that tell a controller what to append never changed:

- `plugin/skills/subagent-driven-development/SKILL.md:365` — fix-loop entries: `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`
- `plugin/skills/subagent-driven-development/SKILL.md:537` — final-review entries: `- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`
- `plugin/skills/executing-plans/SKILL.md:61` — the same final-review form

It recurred in 2 of 3 reviewed specs: `notes.md:142` (executing-plans-review-step) and `:149-153` (watchlist-and-findings-batch). The R1–R4 controller added the check field and the plan slug by hand (`:136-137`), so its entries escaped. Two costs follow:

- `process-review` step 2 reads a four-field entry as one that "predates the attribution field". That claim does not hold for these 6 entries.
- The final-review label carries no plan slug. A reader can group entries `:149-153` by spec only from their position in the file.

**M2 — A change to mechanism text misses a copy of that text.** It recurred in 2 of 3 reviewed specs:

- process-review-batch-r1-r4 (`:132-134`): three enumerations of SDD's Finish list, each incomplete.
- watchlist-and-findings-batch: a phrase grep missed a differently worded copy (`:146`). Twice, a fix changed skill text and left the spec's quote of it stale (`:148`, `:153`).

Both promoted patterns already name this failure: `docs/patterns/enumerate-lists-to-their-structural-end.md`, and `docs/patterns/self-apply-cross-section-check-to-hand-fixes.md`, which received this batch's lesson. Both recurrences in this batch came from fix instructions the controller wrote. No skill step asks the author of a fix dispatch to list the copies. The scoped re-review caught each miss, one round late each time.

## Friction

**F1 — The Skill tool served stale skill text in the session that changed the skill.** This review started with `Skill(superfunk:process-review)`. The tool returned the eight-step text from session start, without typed routing or the watchlist step. The shipped file on disk held the nine-step text. A literal run of the returned text skips `watchlist.md` entirely and reads every entry as a `Catch`. The review caught it only because the controller wrote the new steps earlier in the same session. The project memory already records a related limit: newly added skills are not invocable mid-session. This instance concerns a changed skill.

**F2 — Subagent dispatch was unavailable for part of executing-plans-review-step.** Its Task 1 outcome records "subagent spawn limit still exhausted", and the controller implemented directly. `docs/lessons-learned.md` already records this constraint. No new action.

No task in the window reached 3 fix rounds. Task 4 of watchlist-and-findings-batch reached 2, and its final review needed one fix wave plus one regression fix.

## Gaps

**G1 — SDD Finish checks off one Recommendation per spec.** `plugin/skills/subagent-driven-development/SKILL.md` Finish says to "find the matching `- [ ]` Recommendation by content, and check it off", in the singular, with one verification grep. watchlist-and-findings-batch closed two Recommendations in one review file (lines 91 and 92 of `review-after-2026-09-01-convention-retirement-design.md`). The controller ticked both by hand after the final review flagged the singular wording.

**G2 — Plan-dictated text carried defects of four unrelated kinds.** In watchlist-and-findings-batch, task reviews caught three of them in text the plan dictated word for word: a commit-subject convention break (`:144`), a false historical claim (`:145`), and a rule conflict (`:147`). The R1–R4 batch adds a misquote (`:135`). Each kind occurred once, and the four kinds share no single check. No mechanism proposed. Task review caught every one before merge.

**G3 — executing-plans-review-step criterion 5 shipped with a known letter gap.** Its outcomes file records that the no-dispatch review condensed to a one-line verdict rather than the full code-reviewer format. The trial diff gave it nothing to report. The follow-up stays too vague to act on: no record shows whether the condensed form recurs on a real diff.

## Watchlist

**Harvest.** The window holds 3 `Watch` entries (`notes.md:138-140`). The watchlist already holds all 3 as seeds, with the same origin label (`process-review-batch-r1-r4`) and the same triggers, so step 5 skipped all 3. This was the duplicate that the final review predicted, and the skip rule prevented it on its first run.

**Evaluation.** Checked 6 of 6 entries. None tripped:

| Entry | Evidence this window | Result |
|---|---|---|
| `item-10-accretion` | No commit in the window changed `writing-plans` item 10. Its third duty, the drafted-insertion grep, shipped in `ef31db9`, the entry's own baseline. | Not tripped |
| `executing-plans-finish-pointers` | SDD Finish gained sentence-level edits (`d12c77f`, `4871b53`, `a7979b7`). No heading moved, split, or lost its lesson-promotion or concept-index text. | Not tripped |
| `plugin-wide-bump-trigger` | The window holds 3 bumps (6.5.0, 6.6.0, 6.7.0). All 3 are minor bumps for `plugin/skills/` changes, with 0 doc-only patch bumps. | Not tripped |
| `g1-title-based-overlap` | No spec in the window asserts that two checks overlap. A grep for "overlap" in the 3 specs finds only references to G1 itself. | Not tripped |
| `g2-plan-less-shipping` | All 3 specs shipped through a plan. | Not tripped |
| `g3-attribution-coverage` | 6 of 19 Catches carry no check field. That is not a majority (see Retirements), but M1 names the cause. | Not tripped |

No entry left the file. `watchlist.md` needed no change.

## Recommendations

- [ ] **(M1)** Update the three `notes.md` write-site templates to the five-field form. In `plugin/skills/subagent-driven-development/SKILL.md:365`, use `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <check that caught it> | <one-line finding>`. At `:537` and in `plugin/skills/executing-plans/SKILL.md:61`, use `- <YYYY-MM-DD> | Catch | Final review (<plan-slug>) | <check that caught it> | <one-line finding>`, and keep the two final-review copies identical. **Replaces nothing; net new load** — a format correction that brings the templates in line with the format shipped on 2026-09-01. It adds no check.
- [ ] **(M2)** Add one sentence to `plugin/skills/subagent-driven-development/SKILL.md`, in both the fix loop's "Every round, either way" paragraph and the Final Review's fix-dispatch paragraph: "When a finding changes text that describes a mechanism, name every copy of that text in the fix dispatch — sibling files and the design spec's own quotes — found by searching each key term, not one phrase." **Net new load** — 3 recurrences in one batch (`:146`, `:148`, `:153`) plus 3 in R1–R4 (`:132-134`). The scoped re-review caught each one, a full round late.
- [ ] **(F1)** Add one clause to the process-review offer in `plugin/skills/subagent-driven-development/SKILL.md` Finish ("offer to run superfunk:process-review right now"): "if this branch changed `plugin/skills/process-review/`, follow that file as read from disk, because the Skill tool serves the text loaded at session start." **Net new load** — one clause. It fires only when a branch changes the reviewer it then runs.
- [ ] **(G1)** In `plugin/skills/subagent-driven-development/SKILL.md` Finish, change "find the matching `- [ ]` Recommendation by content, and check it off" to "find each matching `- [ ]` Recommendation by content, and check off every one this spec closes". Change the third verification grep's lead-in so that it runs once per closed Recommendation. Make the same change in `plugin/skills/executing-plans/SKILL.md` Step 3 item 4, which also reads "find the matching `- [ ]` line". **Replaces the singular wording; no new check.**

## Retirements

**Attribution coverage in this window:** 19 Catch entries. 13 name a check, 0 read `none — found ad hoc`, and 6 carry no check field (M1 explains why). The check field existed for this whole window, but the two earlier reviews it would need to span had worse coverage. Zero-yield needs 3 reviews of usable data, so it stays unusable this time.

None.
