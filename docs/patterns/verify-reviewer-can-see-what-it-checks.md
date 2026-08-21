# Verify the reviewer can actually see what it's asked to check

When wiring a new "check X" instruction into a reviewer, confirm the reviewer's actual input contains X, not just that the instruction reads correctly.

## Context

A reviewer (spec-compliance, code-quality, or holistic) reads whatever data-delivery mechanism hands it — a diff, a review package, a report file — not the full repository. A new checking instruction can pass its own spec-compliance and code-quality review purely on wording quality, while the underlying data path silently never carries what the instruction asks about. Nothing about reading the instruction's prose reveals this; only tracing where its input actually comes from does.

## Pattern

When wiring a new check into a reviewer:
1. Identify exactly what mechanism produces the reviewer's input (a script, a diff command, a report format).
2. Trace whether that mechanism's output would actually contain the thing the new instruction asks about.
3. If it wouldn't, fix the mechanism first — the instruction is not the defect; the missing data is.

## Example

- `task-reviewer-prompt.md` gained an instruction to check commit messages for a severity trailer. The reviewer's actual input, `scripts/review-package`, built its commit list with `git log --oneline` — subject lines only. The trailer lives in the commit body. The check was unrunnable, and no amount of polishing the instruction's wording would have caught this; only tracing the data path did.

## Originating lessons

- "When wiring a new reviewer check, verify the reviewer can actually see what it's asked to check" (2026-08-21-hazard-signal-words)
