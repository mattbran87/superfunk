# Lessons Learned

Accumulated knowledge from completed plans. Captured at
`subagent-driven-development`'s Finish step for notable learnings —
specific enough to act on in a future session. Entries live under an
H2 category heading; the first Lesson on a new topic creates its own
heading.

## Workflow

### Cross-check a shared rule's restatements across every file a plan writes it into (2026-08-20-lessons-and-patterns-design)

When translating one design-spec rule into multiple target files within
the same plan (e.g. the same promotion rule written once for
`docs/code-standards.md` and again for `subagent-driven-development/SKILL.md`),
each restatement independently matched its own target file's needs but
diverged from the other's wording — the design spec itself states the
rule once, but paraphrasing it twice, in two separate plan tasks,
without comparing the two paraphrases to each other, let two different
framings of the same rule ship. Both needed a fix round to reconcile.
**Rule:** when a plan restates the same rule in more than one target
file, cross-check every restatement against every other restatement,
not just each one individually against the source spec.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/cross-check-shared-rule-restatements.md*
