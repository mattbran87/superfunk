# Outcomes — 2026-08-30-equality-not-containment-note.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Add the equality-not-containment sentence
Shipped as planned; exact text match confirmed, grep check passed (2 matches, the plan's own corrected prediction). Implemented directly (subagent spawn limit still exhausted). No divergence.

## Task 2: Live trial and final verification
Criterion 1 confirmed exactly via direct read-back. Criterion 2's live trial exceeded expectations: against a fixture with a real planted bug (a trailing-slash `rstrip()` making `for_display` and `for_opening` disagree) and a containment-based test (`opened in listing or listing in opened`) that couldn't catch it, the task reviewer correctly identified the spec violation itself, built an explicit mutation table showing the test stays green under any prefix/substring mutation, and cited "the `in`-instead-of-`==` trap verbatim" by name in its Important findings -- directly invoking the newly-added note's own language. First trial attempt timed out at 90s and again at 150s (environment slowness, not a defect); succeeded on a third attempt with a 280s timeout. Implemented directly. No divergence in shipped content.
