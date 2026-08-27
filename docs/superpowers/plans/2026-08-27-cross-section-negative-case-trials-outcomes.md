# Outcomes — 2026-08-27-cross-section-negative-case-trials.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Negative-case trial for item 8 (Self-Review)
Shipped as planned; item 8 correctly did not trigger, with rich semantic reasoning distinguishing "trigger" mentioned (as vocabulary to avoid) from "trigger" used (as a mechanism claim), plus scope-mismatch and direction-mismatch analysis explaining why the edit doesn't contradict Apply Config's real routing content despite lexical overlap on all three tokens (trigger/always/never). The trial also proactively identified and explained the exact near-miss scenario that WOULD have fired item 8 ("never use always/never in this skill's docs"), strengthening confidence this is genuine discrimination, not a lucky non-match. Dispatch prompt re-checked against Rule 2 after the fact: named item 8 to invoke it, but phrased the reporting instruction as a symmetric if/if-not branch, never asserting which branch applied. Independently confirmed no dry-run edit landed in the fixture file. No divergence, no follow-ups.
