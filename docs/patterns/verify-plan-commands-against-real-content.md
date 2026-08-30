# Verify a plan's commands against real content, not just its numeric prediction

A plan's `Expected:` value is only as trustworthy as the command that produces it — verify both the number and the pattern against real file content before finalizing either.

## Context

Writing a plan step that predicts a specific count (a grep match count, a line count) invites two distinct failure modes, not one. The first is a wrong number: the author reasons about how many times a string should appear and gets the arithmetic wrong (a reused name spanning multiple lines, a window too small to reach the end of a block). The second, easier to miss, is a wrong pattern: a command that returns zero matches every time, not because the content is absent but because the command's own assumptions don't hold against the real file — most commonly, an anchored pattern (`^##`) assumed to match a heading that actually sits inside an indented code-fence template, never at column 0. A zero-match result reads as "nothing found," which is indistinguishable from "the pattern can't possibly match here" without independently confirming the target content actually exists another way.

## Pattern

Before finalizing any plan step with a predicted count or a grep-based verification command, run that exact command (or a faithful substitution test) against the real target file's actual current content — not a mental model of the file's structure. If the result doesn't match the prediction, diagnose why before writing the corrected value: a genuine arithmetic error and a structurally-broken pattern need different fixes, and only checking the number leaves the pattern's own validity unverified.

## Example

- A plan predicted `grep -c "User-Facing Documentation Timing"` would return 2, assuming a new Self-Review item's text would repeat a section's exact capitalized heading phrase. The item's actual text used different capitalization ("User-facing documentation timing"), a distinct case-sensitive string — the real count was 1.
- A plan's verification step used `grep -c "^## Mutation Check"` against a file that wraps its entire reviewer template in an indented code fence. Every heading in that file sits four spaces in, never at column 0, so the anchored pattern returned 0 regardless of whether the new section existed — a structurally guaranteed false negative, not a miscounted true positive.

## Originating lessons

- "A tool's passing fixture-based unit tests don't prove it works against a real project's actual paths and text" (2026-08-28-superfunk-rebrand)
- "Writing a check for unverified numeric claims doesn't exempt the document writing it" (2026-08-28-process-review-recommendations-batch-3)
- "The same self-referential blind spot recurred twice more, in two new shapes" (2026-08-30-doc-timing-and-mutation-check)
