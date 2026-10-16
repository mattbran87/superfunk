# Review Recommendations M1, M2, F1, G1 — Design

**Date:** 2026-10-15
**Status:** Approved
**User-Facing:** Yes

## Context

`docs/superpowers/process-reviews/review-after-2026-10-15-watchlist-and-findings-batch-design.md` opened four Recommendations. This batch closes all four. Each one traces to logged evidence:

- **M1 ← Miss M1.** The five-field `notes.md` format shipped on 2026-09-01 (`2cdfe94`). The three templates that tell a controller what to append still show four fields:
  - `plugin/skills/subagent-driven-development/SKILL.md:365` (fix loop)
  - `plugin/skills/subagent-driven-development/SKILL.md:537` (Final Review)
  - `plugin/skills/executing-plans/SKILL.md:61` (Step 2.5)

  Six window entries copied that form and carry no check field (`notes.md:142`, `:149-153`). The final-review template also omits the plan slug, so entries `:149-153` name no spec.
- **M2 ← Miss M2.** A change to mechanism text missed a copy of that text 6 times across 2 batches: `notes.md:132-134` (R1–R4) and `:146`, `:148`, `:153` (watchlist-and-findings-batch). In the last two, a fix dispatch the controller wrote changed skill text and left the spec's quote of it stale. A scoped re-review caught each one, a full round late.
- **F1 ← Friction F1.** The review's own run called `Skill(superfunk:process-review)` and got the eight-step text from session start. The shipped file on disk held the nine-step text. A literal run of the served text skips the watchlist and reads every entry as a `Catch`.
- **G1 ← Gap G1.** SDD Finish checks off "the matching `- [ ]` Recommendation", in the singular. watchlist-and-findings-batch closed two Recommendations in one review file, and the controller ticked the second one by hand.

Two sites sit outside the Recommendations' literal text, and this batch covers them:

- `process-review/SKILL.md:44` says a four-field entry "predates the attribution field". The `notes.md` header (lines 30–32) says that entries dated before 2026-09-01 carry four fields. The six entries from M1 contradict both statements.
- `executing-plans/SKILL.md` Step 3 holds its own copy of both the process-review offer (item 3) and the Recommendation check-off (item 4).

## Decisions

1. **One batch, four Recommendations.** Same mold as the R1–R4 batch: mechanical fixes, one pipeline pass, one Finish.
2. **No trials.** M1, F1, and G1 change templates and wording, and each has a grep check. M2 adds an instruction that claims a behavior change, which this project usually trial-gates. Human-partner decision: ship M2 without a trial, and watch it. The 6 logged misses already show that the controller does not list the copies unprompted, which answers the question a control arm would ask (per `docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md`).
3. **M1 fixes the claim that four fields mean "old".** Step 2 and the `notes.md` header both gain the second source of four-field entries. Entries already in the file stay as written.
4. **F1 and G1 land in both copies.** SDD Finish and `executing-plans` Step 3 each get the same change, worded the same way.

## Design

### M1. Five-field write-site templates

1. `plugin/skills/subagent-driven-development/SKILL.md:365`. Change the template to:

   ```
   - <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <check that caught it> | <one-line finding>
   ```

2. `plugin/skills/subagent-driven-development/SKILL.md:537` and `plugin/skills/executing-plans/SKILL.md:61`. Change both templates to:

   ```
   - <YYYY-MM-DD> | Catch | Final review (<plan-slug>) | <check that caught it> | <one-line finding>
   ```

   The two copies stay identical. SDD defines `<plan-slug>` at line 366; `executing-plans` gains its own one-sentence definition beside its template, because an `executing-plans` session may never load SDD.
3. `plugin/skills/process-review/SKILL.md` step 2. Replace "Read a four-field entry as carrying no attribution: it predates the attribution field, and nothing reconstructs which check found it." with "Read a four-field entry as carrying no attribution: it predates the attribution field, or it came from a write-site template that still showed four fields (through 2026-10-15), and nothing reconstructs which check found it."
4. The `notes.md` header, lines 30–32. Replace "Entries below dated before 2026-09-01 carry four fields, without the check field." with "Entries below written before the check field shipped (2026-09-01, `2cdfe94`) carry four fields, without the check field, and so do six later entries copied from write-site templates that still showed four fields (fixed 2026-10-15)." The rest of the paragraph stays.

### M2. Name every copy in a fix dispatch

Add this sentence in two places in `plugin/skills/subagent-driven-development/SKILL.md`:

> When a finding changes text that describes a mechanism, name every copy of that text in the fix dispatch — sibling files and the design spec's own quotes — found with a search for each key term, not for one phrase.

- **Place 1:** the end of the fix loop's "**Every round, either way:**" paragraph.
- **Place 2:** the Final Review paragraph, after "dispatch ONE fix subagent with the complete findings list — not one fixer per finding."

Add a seventh entry to `docs/superpowers/process-reviews/watchlist.md`:

```markdown
- **fix-dispatch-copy-listing** (added 2026-10-15, review-recommendations-m1-m2-f1-g1)
  - Watching: the M2 sentence in `subagent-driven-development`'s fix loop and Final Review.
  - Trigger: a scoped re-review finds a stale copy of text that a fix dispatch changed.
  - Action when tripped: trial-gate the M2 sentence per `docs/patterns/ab-test-live-trials-for-behavior-change.md`, or rewrite it.
```

### F1. Read `process-review` from disk

Add this clause to the process-review offer in both `plugin/skills/subagent-driven-development/SKILL.md` Finish and `plugin/skills/executing-plans/SKILL.md` Step 3 item 3:

> If this branch (the diff from the plan's base commit to HEAD) changed `plugin/skills/process-review/`, follow that file as read from disk, because the Skill tool serves the text loaded at session start.

### G1. Check off every closed Recommendation

1. SDD Finish: "holds the Recommendation this spec closes. Open it, find the matching `- [ ]` Recommendation by content, and check it off" becomes "holds the Recommendations this spec closes. Open it, find each matching `- [ ]` Recommendation by content, and check off every one this spec closes".
2. `executing-plans` Step 3 item 4: "find the matching `- [ ]` line" becomes "find each matching `- [ ]` line this spec closes".
3. Both third verification greps gain a lead-in: run the grep once per closed Recommendation.
4. Both check-off notes name the commit that implemented each Recommendation, so a spec that closes several Recommendations records one commit per Recommendation.

## Falsifiable Criteria

1. `grep -c "| Catch | Final review | <one-line finding>" plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md` returns 0 for each file. `grep -c "<check that caught it> | <one-line finding>"` returns 2 for SDD and 1 for `executing-plans`.
2. The two final-review templates match byte for byte.
3. `process-review/SKILL.md` and the `notes.md` header each name the write-site templates as a second source of four-field entries. `git diff` shows no change to any `notes.md` entry line.
4. The M2 sentence appears exactly twice in SDD, once in each place.
5. `watchlist.md` holds 7 entries, and `fix-dispatch-copy-listing` carries Watching, Trigger, and Action fields.
6. The F1 clause appears once in each of the two files.
7. Neither file contains "find the matching `- [ ]`" any more. Each contains the new plural wording once.
8. This batch's own Finish checks off all four Recommendations in the review file. The four verification greps each return 1.

## Out of Scope

- Rewriting the six existing four-field entries. Reconstructing their check field from memory would fabricate it.
- A trial for M2 (Decision 2). The watchlist entry decides whether one runs later.
- The other Gaps of the review (G2, G3) and its Friction F2. Each one carries a "no action" disposition there.

## Consequences

- Every future `notes.md` entry from a template carries a check field, and every final-review entry names its spec. Attribution coverage then depends on the controller filling the field, not on the template.
- `process-review` step 2 now names two sources of four-field entries. A reader who sees four fields can no longer conclude that the entry predates 2026-09-01.
- The M2 sentence adds work to every fix dispatch that touches mechanism text: one search per key term. The scoped re-review stays as the backstop. Only the watchlist entry measures whether the sentence works.
- The F1 clause helps only a session whose branch changed `process-review` before it runs a review. It does not fix the Skill tool's session-start load, and it covers no other skill.
- G1 makes the check-off rule plural, but the grep still matches each Recommendation by hand-picked words. A Recommendation whose words the controller never picks stays unchecked without a warning.

## Alternatives Considered

| Decision | Candidates | Chosen | Confidence and evidence |
|---|---|---|---|
| M2 trial | A. ship without a trial, and watch; B. trial-gate; C. defer | A | Medium. 6 logged misses across 2 batches (`notes.md:132-134`, `:146`, `:148`, `:153`) show that the controller does not list the copies today. |

## RESULT

*(filled at Finish)*
