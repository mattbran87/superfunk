# A/B-test or scenario-check a live trial that claims to prove a mechanism works

Two distinct trial-design failures share one root cause: a trial whose own prompt hands the agent enough information that it cannot fail, regardless of whether the mechanism under test actually works.

## Context

A `--plugin-dir` trial can dispatch an agent, plant a scenario, and confirm the agent responds correctly. Two different claims get tested this way, and each has its own way of accidentally becoming unfalsifiable:

- **Claim: "this new instruction changes behavior."** A trial that plants a false belief and confirms the agent avoids it only proves the agent follows the instruction's letter under the trial's own coaching — not that the instruction caused the correct outcome, if the dispatch prompt already told the agent what to do, or if the underlying model already behaves correctly without the instruction.
- **Claim: "this trigger condition correctly does NOT fire on a non-matching case."** A trial that tells the agent which trigger paragraph to check, and states the answer ("nothing crossed a boundary") directly in its own prompt, proves only that the agent can read a scenario it was already told the answer to — not that the trigger logic itself would have discriminated a real non-crossing from a crossing on its own.

## Pattern

**Rule 1 — verifying a behavior change needs a true two-arm comparison, not a single coached run.**

1. Write one minimal dispatch prompt that plants the test scenario without coaching the correct response — no "follow the instructions about X," no "confirm by reading fresh from disk," nothing that names the behavior under test.
2. Check out the plugin at two points: immediately before the instruction's commit, and at its current state (including any later fixes).
3. Run the identical coaching-free prompt against both checkouts, using the same fixture.
4. Compare the two results directly. Only a difference between the two arms counts as evidence the instruction changed anything. Identical results in both arms mean the instruction added no detectable value in that scenario — report this honestly, even if an earlier, coached trial already reported a "pass."
5. If the design spec or plan already cites the single-arm trial as its Falsifiable Criterion, correct that criterion once the A/B result comes in — state plainly what the criterion actually shows (the instruction gets followed) versus what it does not show (the instruction changed the outcome).
6. Pre-register the decision rule by scoring each arm and fixture independently, then combining the per-unit states exhaustively — enumerate the full outcome space, never a list of example branches. An outcome with no covering branch means the decision rule fails this step.

**Rule 2 — verifying a trigger correctly does NOT fire needs a scenario the agent evaluates itself, not a stated answer.**

1. Write the negative-case dispatch prompt as a scenario only — describe what changed (or didn't), never name which specific trigger paragraph governs the outcome.
2. Never state the expected answer in the prompt ("nothing crossed a boundary," "this shouldn't fire") — ask the agent to determine and report that itself.
3. If the trial as written already tells the agent the answer, treat that as a trial-design defect before trusting a "correctly skipped" result — rewrite it as a scenario-only prompt and re-run before relying on the finding.
4. No second arm or checkout is needed for this rule — the fix is prompt design, not an A/B comparison.

**Rule 3 — a negative result needs its scenario checked before it counts as evidence.**

Rule 2 covers a prompt that makes failure impossible. This covers the inverse: a prompt that makes success impossible, where the trial returns a negative no matter how good the mechanism is.

1. When a trial reports the behavior under test did not appear, ask first whether the scenario could have produced it at all. A prompt that settles the question the mechanism exists to reopen forecloses the result before the agent starts.
2. Watch specifically for framing that hands over a decision: "treat this as fully specified," "the requirement is X," "we've decided to build Y." Any of these kills a mechanism whose job is to question whether to build.
3. Rewrite the scenario so the behavior under test stays genuinely available, then re-run before recording the finding.
4. A negative result from a scenario that could not have gone positive is a trial-design defect, not evidence about the mechanism. Do not record it as either a pass or a failure — record it as inconclusive and re-run.

**Rule 4 — a positive result needs its scored evidence checked before it ships anything.**

Rule 3 covers a negative that the scenario foreclosed. This covers the inverse hazard at the other end of the pipeline: a judge's YES that does not actually satisfy the criterion, which ships a mechanism on manufactured evidence.

1. Require the judge to quote the exact sentence it scored, not just a verdict — a bare YES/NO output leaves nothing to audit.
2. Before acting on a YES, read the quoted sentence against the criterion's own wording and confirm it addresses the claim the criterion names, not merely something in the same document.
3. A YES whose quoted evidence misses the criterion is a mis-score, not a pass. Record the run as inconclusive and re-run with a corrected criterion or judge prompt — do not re-score the same outputs under a loosened criterion, which selects the criterion to fit results already seen.

## Example

- **Rule 1:** A new reviewer instruction ("re-read the cited doc before citing it in a finding") got verified by a trial that primed a false belief about a doc's rule and confirmed the reviewer caught it. The trial's own prompt said "follow the reviewer template's instructions about re-reading cited docs" and "quote the exact current text ... read fresh from disk" — both force the correct behavior regardless of the instruction under test. A true A/B run (same fixture, no coaching, once against the plugin before the instruction shipped and once after) found both arms independently caught the planted error — the pre-edit reviewer did this unprompted. The instruction added no detectable behavioral difference in this scenario. The design spec's Falsifiable Criterion got corrected to say so explicitly, rather than let the original coached trial's "pass" stand as unqualified proof.
- **Rule 2:** A trial meant to confirm a Finish-step trigger correctly skips a plan that only modifies an existing file (no add/rename/delete) told the agent directly: "This plan's File Structure section stated: 'Modify: ...' -- no skill, feature, or directory was created, renamed, moved, or deleted." The agent reported completing the check with no index change, which proved only that it can read a scenario it was handed the answer to, not that its trigger logic discriminates on its own.

- **Rule 3:** A trial testing whether a new step-4 requirement makes brainstorming include a do-nothing candidate reported the behavior absent from both arms. The prompt said "treat this as fully specified," which hands the agent a settled decision to build — no candidate set produced under it could have contained a defer option, so the trial could only return a negative. Re-running with a scenario where deferring stayed defensible (180ms p50 latency at 4 requests per second, no complaint or breached SLO) produced the real finding, and it pointed the opposite way: the pre-change arm made "measure before caching" its first approach *and* its recommendation, while the post-change arm carrying the instruction offered three implementations and relegated restraint to a caveat. The first trial's negative said nothing about the mechanism; the second one falsified it outright.

- **Rule 4:** A four-output blind judging returned `A: YES`, which under the pre-registered decision rule meant ship. The sentence the judge quoted addressed a different claim than the criterion named — the `Alternatives Considered` heading count, where the criterion named a keyword-probe inference. Only reading the quote against the criterion's wording caught it; the verdict line alone read as a clean pass. Scored strictly, no arm had met its criterion. The run was recorded as inconclusive, a class-level criterion was registered in a commit that predated any new output, and the trial re-ran fresh — the re-run then produced a genuine detection on the same fixture.

## Originating lessons

- "A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior" (2026-08-24-review-recommendations-followup)
- "A trial confirming a trigger doesn't fire must not hand the agent its own answer" (2026-08-25-concept-index)
- "A negative trial result needs its scenario checked before it counts as evidence" (2026-09-01-research-skill-adoption)
- "A blind judge's YES needs its quoted evidence checked against the criterion before it counts" (2026-09-01-behavioral-claim-verification)
