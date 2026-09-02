Done — committed as `86f709e`.

## Lesson entry

Appended to `docs/lessons-learned.md:233` under the existing `## Testing` category:

**"A predicted grep count fails on exactly the details that make grepping necessary (2026-08-28-process-review-recommendations-batch-3)"**

The paragraph records all three self-inflicted instances: the `grep -c "Finish:"` total that assumed one matching line per new diagram node name (reused names span several edge lines each), the `-A 60` window on a block that spans 65 lines, and the fact that all three surfaced only by running the substitution and the command against real content — never by re-reading the prediction, since a prediction and a verified result look identical on the page.

It also ties the recurrence to the four earlier instances already in `notes.md`: `documentation`'s "9/9" vs. a real 10, `superfunk-rebrand`'s "135 across 33 files" vs. 116 across 29, its Task 4 "33" vs. a `wc -l` counting lines not occurrences, and its Task 6 predicted `ALREADY_UPDATED` vs. a real `ACTION_NEEDED` plus a crash. Batch-3's `grep -c` miss repeats Task 4's line-versus-occurrence confusion exactly.

**Rule:** treat every count, context window, test total, and tool status a document predicts for a command as an empirical claim about real file content — run the command, read its real output, then write the expected value. Assume a prediction is wrong whenever it rests on a text property you did not measure.

## Promotion decision: promoted

Wrote `docs/patterns/run-the-command-before-writing-its-expected-output.md`. Both promotion triggers fire, not just one: the rule is prospective and applies to every spec, plan, and verification step that states an expected command result, *and* the failure mode has now recurred seven times in a week (four in `notes.md`, three during batch-3's own construction) — far past the second-occurrence threshold.

I kept it a separate Pattern rather than folding into `validate-tools-against-real-project-data.md`. That pattern triggers on "I shipped a tool whose fixtures may not match reality"; this one triggers on "I am about to write an expected value into a document" — different actor, different moment. The Context section cross-links them so neither reads as a duplicate.

## One thing to flag

This repo snapshot does not contain the batch-3 sub-project: no `2026-08-28-process-review-recommendations-batch-3-design.md` in `specs/`, no plan in `plans/`, no commits (git history is a single squashed `9f38832`), and `writing-plans/SKILL.md` still carries 9 Self-Review items, not 12. So the entry's specifics come from your description, corroborated against the real `notes.md` history rather than against the sub-project's own artifacts.

Consequently the rest of Finish's bookkeeping is not done here — the spec Status flip, the `tracker.md` append, and the Recommendation checkbox would normally share a commit with this Lesson. You asked only for the Lessons-learned step, so I left those alone; the Lesson and Pattern went in their own commit as the skill specifies for that case.
