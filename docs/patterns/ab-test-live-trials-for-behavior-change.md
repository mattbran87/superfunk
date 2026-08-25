# A/B-test a live trial that claims to prove a new instruction changes behavior

When a live trial exists to show a new instruction causes a behavioral change (not just that the instruction reads correctly), run it as a true two-arm comparison against the pre-edit baseline — never as a single coached run.

## Context

A `--plugin-dir` trial can dispatch an agent, plant a false belief or a tempting shortcut, and confirm the agent avoids it. That confirms the agent follows the instruction's letter under the trial's own coaching. It does not confirm the instruction caused the correct outcome, if the agent's dispatch prompt already told it what to do, or if the underlying model already tends to behave correctly without the instruction. A single-arm trial with no baseline comparison cannot distinguish "the instruction worked" from "nothing here needed the instruction at all."

## Pattern

When a trial exists to verify a new instruction changes reviewer or implementer behavior:
1. Write one minimal dispatch prompt that plants the test scenario without coaching the correct response — no "follow the instructions about X," no "confirm by reading fresh from disk," nothing that names the behavior under test.
2. Check out the plugin at two points: immediately before the instruction's commit, and at its current state (including any later fixes).
3. Run the identical coaching-free prompt against both checkouts, using the same fixture.
4. Compare the two results directly. Only a difference between the two arms counts as evidence the instruction changed anything. Identical results in both arms mean the instruction added no detectable value in that scenario — report this honestly, even if an earlier, coached trial already reported a "pass."
5. If the design spec or plan already cites the single-arm trial as its Falsifiable Criterion, correct that criterion once the A/B result comes in — state plainly what the criterion actually shows (the instruction gets followed) versus what it does not show (the instruction changed the outcome).

## Example

- A new reviewer instruction ("re-read the cited doc before citing it in a finding") got verified by a trial that primed a false belief about a doc's rule and confirmed the reviewer caught it. The trial's own prompt said "follow the reviewer template's instructions about re-reading cited docs" and "quote the exact current text ... read fresh from disk" — both force the correct behavior regardless of the instruction under test. A true A/B run (same fixture, no coaching, once against the plugin before the instruction shipped and once after) found both arms independently caught the planted error — the pre-edit reviewer did this unprompted. The instruction added no detectable behavioral difference in this scenario. The design spec's Falsifiable Criterion got corrected to say so explicitly, rather than let the original coached trial's "pass" stand as unqualified proof.

## Originating lessons

- "A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior" (2026-08-24-review-recommendations-followup)
