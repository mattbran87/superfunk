# Run 1 — inconclusive, criterion mis-specified

## Verdict

Run 1 yields no evidence about the widening. Its detection criteria named one
specific sentence per fixture. Both widened arms interrogated a claim of the
target class at a different site in the same document, and both control arms
did not. The criteria therefore measured which sentence an agent chose to
examine, not whether the widened item changed behaviour.

`docs/patterns/ab-test-live-trials-for-behavior-change.md` Rule 3 governs this:
a criterion that forecloses success returns a negative regardless of the
mechanism's quality, and counts as a trial-design defect rather than as
evidence. Recorded as inconclusive. Neither a pass nor a failure.

## What the blind judge returned

| Judge label | Arm | Verdict |
|---|---|---|
| A | F1 · widened | YES |
| B | F1 · control | NO |
| C | F2 · control | NO |
| D | F2 · widened | NO |

The judge scored A on "Zero specs carry the heading ... does not establish
which branch fired." That sentence addresses the `Alternatives Considered`
count, not the keyword probe the criterion named. Scored strictly, no arm hit
its pre-registered claim.

## Observed, and explicitly post-hoc

Both widened arms produced a target-class finding. Neither control did.

- F1 widened, attributed in its own output to "(line 18, check 6)": zero
  headings proves the output never appeared, and does not establish which
  branch fired.
- F2 widened: the probe backing "no mechanism retires a rule" covered 19 skills
  and missed the three newest; it re-ran the probe across all 22 and reported
  that the claim holds while its stated basis does not.
- F2 control cleared the target premise using the wrong evidence class: "all
  three subsumption clusters check out against the real item text".

This observation carries no weight as evidence. It arrived after the outputs
existed, and run 2 exists to test it against a criterion registered first.

## Trial artifact — the harness leaked into the fixture

Both arms read their own `--plugin-dir` path as project state. F1 control built
a blocking finding on `C:\sf-bcv-plugins\arm1\skills\` as a third lineage of
the skills, including that its `plugin.json` already reads 6.3.0. F2 widened
disclosed the same thing and named the pattern file that exists only in the
arm-2 copy.

The contamination stays symmetric, so it does not favour either arm. It does
consume attention, and a blocking false finding can crowd out a real one. Run 2
inherits this limitation unchanged.
