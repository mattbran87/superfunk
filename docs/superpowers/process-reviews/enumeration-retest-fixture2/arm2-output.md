Done — Lessons-learned capture committed as `8cb2fb5`.

## The entry (`docs/lessons-learned.md`, under `## Testing`)

**Title:** *A predicted count or window size written into a verification command measures what you imagined, not what sits on disk (2026-08-28-process-review-recommendations-batch-3)*

The paragraph records that the sub-project shipping three Self-Review items against un-run predicted counts committed that same failure three times in its own spec and plan; it names the `grep -c "Finish:"` total (reused node names span several edge lines each, so the real file returns more) and the `-A 60` window against a 65-line block. The diagnosis it adds beyond the two instances: re-reading a command afterward runs the *same* mental model that produced the prediction, so it confirms rather than tests — which is why all three fell only to running the command against real content.

**Rule:** before writing a predicted number into a document — a `grep -c` total, a `-A N` context window, an expected item count — run the real command against the real current file and record its actual output as the number; a count derived by reasoning about what an edit should produce states a hypothesis about the file, never a measurement of it.

## Promotion decision: promoted, into the existing Pattern

I read all 16 existing `**Rule:**` sentences and compared acts, not titles. Fifteen name different acts (comparing paraphrases, reading a rule's source intent, fixture construction, trial design, git-checkable gates, self-applied cross-section greps). The closest near-miss — "confirm a reviewer's actual input contains what it's told to check" — diagnoses by *reading* a data path, not by executing, so it stayed a non-match.

One match: `2026-08-28-superfunk-rebrand`'s Rule about running a tool against real project paths and prose. Both gather one real execution against the target's own content; both conclude that evidence produced without touching that content — fixture data there, an in-the-head substitution here — predicted the wrong result. Per the skill, a match promotes both entries to one Pattern regardless of either entry's own note, and that Pattern already exists, so I extended `docs/patterns/validate-tools-against-real-project-data.md` rather than opening a second file saying the same thing: retitled to "Validate against real project data — not against fixtures, and not against a predicted result," Context and Pattern text now cover both shapes, batch-3's example and originating-lesson bullet added. Slug unchanged, so the rebrand entry's existing pointer still resolves. Recurrence cleared the threshold independently anyway — three occurrences inside one sub-project.

## Two things to know

- The sub-project's own artifacts aren't in this repo snapshot: no `2026-08-28-process-review-recommendations-batch-3-design.md`, no plan, no `batch-3` string anywhere before my commit, and `git log` held a single commit. I wrote the entry from the account you gave and used the sub-project slug as `<spec-slug>`. The rest of Finish (Status flip, tracker, Recommendation checkbox, the three verification greps) has no spec file to run against here.
- I committed on `master`, the only branch present.

Incidental confirmation of the Lesson itself: `git grep -c "^\*\*Rule:\*\*"` returns 2, not 16 — most Rule sentences sit mid-paragraph. Had I written a predicted count for that grep into this report, it would have been wrong.
