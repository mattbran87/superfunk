# Outcomes — 2026-10-15-review-recommendations-m1-m2-f1-g1.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->

## Task 1: Five-field write-site templates (M1)
Shipped all five edits (fix-loop template, both final-review templates, process-review's four-field attribution note, notes.md header note, and the new v6.8.0 RELEASE-NOTES entry), committed only the five brief-named paths, and the docs check passed. Step 7's spec-quote comparison found no differences between the spec's quoted Step 1-4 text and the shipped text — no spec edits made. Nothing diverged from the brief on my own initiative.

## Task 2: Name every copy in a fix dispatch (M2)
Shipped the M2 sentence verbatim in both SKILL.md fix-dispatch paragraphs (fix loop and Final Review), appended the `fix-dispatch-copy-listing` watchlist entry, and added the RELEASE-NOTES bullet directly after Task 1's bullet. Nothing diverged from the brief — all exact-text blocks, verification commands, and the commit/docs-check sequence matched their Expected values on the first pass.

## Task 3: Read `process-review` from disk, and check off every closed Recommendation (F1, G1)
Shipped all five edits exactly as the brief specified — F1 disk-read clauses in both SDD Finish and `executing-plans` Step 3 item 3, plural check-off wording in both skills' Finish/Step 3 sections, and the Task 3 RELEASE-NOTES bullet. Nothing diverged from the brief on my own initiative. Step 7's cross-section grep and Step 8's spec-quote grep both came back clean.

## Finish
Final whole-branch review: ready with fixes, two Important and two Minor, all fixed in one wave (`9f007f9`) whose brief listed every copy up front; its scoped re-review found no stale copy. All four Recommendations checked off, one commit each, and the four per-Recommendation greps each returned 1 (spec criterion 8). Lessons: nothing new — the fix brief's one wrong expected count (2 hits, because the controller's own Catch entry carried the asserted phrase) is an instance of `docs/patterns/assert-on-a-token-the-context-cannot-supply.md`.
