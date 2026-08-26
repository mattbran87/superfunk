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

**Rule 2 — verifying a trigger correctly does NOT fire needs a scenario the agent evaluates itself, not a stated answer.**

1. Write the negative-case dispatch prompt as a scenario only — describe what changed (or didn't), never name which specific trigger paragraph governs the outcome.
2. Never state the expected answer in the prompt ("nothing crossed a boundary," "this shouldn't fire") — ask the agent to determine and report that itself.
3. If the trial as written already tells the agent the answer, treat that as a trial-design defect before trusting a "correctly skipped" result — rewrite it as a scenario-only prompt and re-run before relying on the finding.
4. No second arm or checkout is needed for this rule — the fix is prompt design, not an A/B comparison.

## Example

- **Rule 1:** A new reviewer instruction ("re-read the cited doc before citing it in a finding") got verified by a trial that primed a false belief about a doc's rule and confirmed the reviewer caught it. The trial's own prompt said "follow the reviewer template's instructions about re-reading cited docs" and "quote the exact current text ... read fresh from disk" — both force the correct behavior regardless of the instruction under test. A true A/B run (same fixture, no coaching, once against the plugin before the instruction shipped and once after) found both arms independently caught the planted error — the pre-edit reviewer did this unprompted. The instruction added no detectable behavioral difference in this scenario. The design spec's Falsifiable Criterion got corrected to say so explicitly, rather than let the original coached trial's "pass" stand as unqualified proof.
- **Rule 2:** A trial meant to confirm a Finish-step trigger correctly skips a plan that only modifies an existing file (no add/rename/delete) told the agent directly: "This plan's File Structure section stated: 'Modify: ...' -- no skill, feature, or directory was created, renamed, moved, or deleted." The agent's report that it "correctly made no change" proved only that it can read a scenario it was handed the answer to. The trial showed the instruction is followable, not that the trigger logic itself discriminates a real non-crossing from a crossing.

## Originating lessons

- "A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior" (2026-08-24-review-recommendations-followup)
- "A trial confirming a trigger doesn't fire must not hand the agent its own answer" (2026-08-25-concept-index)
