# Outcomes — 2026-09-02-process-review-batch-r1-r4

## Task 1: R3 — port bump-version.sh helpers from jq to node
- Commit: 5c6b4d2. Spec ✅, quality Approved (one Minor deferred: missing-intermediate-segment error shape differs from jq; cosmetic).
- All four acceptance checks passed with actual outputs recorded: --check exit 0 at 6.4.0 across 7 files; zero jq matches; round-trip diff touched only "version" lines in exactly 7 files; --audit ran to completion with no undeclared findings.
- Outcome: Shipped as planned; no divergence.

## Task 2: R2 — outcome-space point 6 in the A/B pattern
- Commit: 92e6028. Spec ✅, quality Approved. Inserted line character-identical to the registered string, correct position, single physical line.
- Plan defect caught: the plan misquoted point 5's closing parenthetical (logged in notes.md).
- Outcome: Shipped as planned; no divergence.

## Task 3: R4a — Finish Bookkeeping section in executing-plans
- Commit: fa2637c. Spec ✅ (inserted section byte-matches the brief; renumbering clean; items 1-8 verified present), quality Approved.
- DONE_WITH_CONCERNS resolved: check_docs.py printed ACTION_NEEDED; reviewer ruled the no-edit disposition valid (README one-line summaries contradict nothing, no CHANGELOG exists, tool failure modes tracked as BUG-0001/0002).
- Outcome: Shipped as planned; no divergence.

## Task 4: R4b — bump gate in SDD Finish
- Commit: 5e55af4. Spec ✅ (both insertions exact; 6 insertions, 0 deletions), quality Approved.
- Reviewer independently re-ran the normalized identity extraction: IDENTICAL, byte-for-byte including the U+2014 em-dash.
- Minor parked with ruling: worked-example's terse "scripts/bump-version.sh" matches sibling example shorthand; accepted.
- Outcome: Shipped as planned; no divergence.

## Task 5: R1 A/B trial
- Commit: a2bb970 (archive). Controller-run (divergence from dispatch, deliberate: trial harness mechanics + Rule 4 quote-checking duty).
- Both arms ran clean on first launch (no classifier blocks). Blind judge: A(=arm2 treatment) YES — quoted a scratch-file grep of drafted insertion text run before finalization; B(=arm1 control) NO — only greps ran against the pre-existing target, excluded by the criterion. Quotes verified against criterion wording before unsealing the mapping.
- Decision-rule branch: arm1 no / arm2 yes — SHIP the exact string.
- Outcome: Shipped as planned; the mechanism fired unprompted in treatment and not in control on its first genuinely blind test.
