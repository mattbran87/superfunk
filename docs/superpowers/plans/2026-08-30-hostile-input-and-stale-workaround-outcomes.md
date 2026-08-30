# Outcomes — 2026-08-30-hostile-input-and-stale-workaround.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Add Self-Review items 13 and 14
Shipped as planned; exact text match confirmed, both grep checks passed (1, 1), baselines verified at 0 before the edit. Implemented directly (subagent spawn limit still exhausted). No divergence.

## Task 2: Create the hunt-the-workaround-not-the-feature pattern
Shipped as planned; content matches exactly, grep check passed (1 match). Implemented directly. No divergence.

## Task 3: Full verification sweep and live trials
All four Falsifiable Criteria confirmed. Criteria 1-2 matched the Decision block exactly on direct read-back (one shell-escaping quirk in the Criterion 1 grep pattern, same class as earlier sub-projects' -- fixed by dropping the backslash-escaped asterisks, not a real content issue).

Criterion 3 (hostile-input pass) exceeded expectations: dispatched against a real fixture `search()` function using an unescaped SQL LIKE pattern, the session correctly named the exact input class (LIKE metacharacters `%`/`_`), independently rediscovering the same defect shape the original trial hit, proposed a correct escaping fix, and additionally named two further unexamined input classes (unbounded result set, `SELECT *` column-shape fragility) unprompted -- item 13's own "each input class" wording earning genuinely thorough output.

Criterion 4 (stale-workaround grep) also exceeded expectations: against a fixture with a stale README limitation and a stale docstring, the session correctly grepped for the workaround's own distinctive words rather than the new feature's name (explicitly reasoning about why "retry" itself would be the wrong general search term even though it happened to also appear here), caught both stale references, and applied the pattern's own "the more helpful the old message, the more dangerous" sharpening correctly to flag the README's "delete and re-add" instruction as actively destructive once the new command ships.

Implemented directly (subagent spawn limit still exhausted). No divergence in any shipped content; both live trials confirm the mechanisms work end-to-end, not just as prompt text.
