# Review Recommendations Follow-Up — Design

**Date:** 2026-08-24
**Status:** Shipped

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-21-hazard-signal-words-design.md` left two open Recommendations, unaddressed since 2026-08-21:

1. Operationalize `docs/patterns/verify-against-precedent-before-flagging.md` as a real pre-finding check in `task-reviewer-prompt.md`, not only a recorded Lesson. Two real recurrences motivated the Pattern: a code-quality finding read a "5-9 item cap" as a floor (checklist-construction), and a separate finding claimed a template rule "wasn't mentioned" when the shipped bullet named it explicitly (hazard-signal-words). Both cited `docs/ai-code-guidelines.md` or `docs/code-standards.md` from memory instead of re-reading the section.
2. Extend `writing-plans/SKILL.md`'s Self-Review item 6 ("Cross-file rule restatement") to also cover a single bullet summarizing one source rule, not only restatements across multiple files. Hazard-signal-words' Task 5 (File Naming) and Task 6 (Spec File Conventions) each drifted from their one cited source in a single bullet — the narrower case item 6's current wording doesn't name.

This project's practice treats an open Recommendation as work to pick up directly, the same way `lessons-and-patterns`' own two Recommendations got actioned earlier this session.

## Decision

- **`task-reviewer-prompt.md` gains one new instruction**, placed immediately after the existing "Project conventions" bullet list (before "Your report should point at evidence..."):

  ```
  Before citing `docs/ai-code-guidelines.md` or `docs/code-standards.md` in
  a finding, re-read the exact section you're citing — not from memory of
  what it "usually says." A finding that claims a diff drifts from one of
  these docs must quote or paraphrase the section's actual current text,
  not an assumed or half-remembered version of the rule. Then re-check the
  diff hunk the finding is about: confirm what the diff actually contains,
  not what you recall it containing from earlier in the review. Two prior
  reviews filed false findings this way — one misremembered a doc's rule,
  the other claimed a diff omitted something the diff actually included.
  ```

  Scoped to these two docs specifically — every real recurrence cited one of them, not the task brief or Global Constraints. Scoped to the code-quality half of the review, not spec compliance (Part 1) — no logged recurrence shows a spec-compliance finding misreading a cited rule; spec compliance already carries its own "Do Not Trust the Report" discipline for the implementer's claims. Broadened during this sub-project's own final review to also cover re-checking the diff hunk, not only the cited doc — the second motivating recurrence (a finding claiming a template rule "wasn't mentioned" when the shipped bullet named it explicitly) misread the diff itself, not the doc, so the doc-only version would not have prevented it.

- **`writing-plans/SKILL.md`'s Self-Review item 6 broadens in place**, keeping its number (the Recommendation names it specifically) but changing its title and content:

  ```
  **6. Rule-restatement accuracy:** Does this plan restate or summarize a
  source rule anywhere — in one target file or several? For a restatement
  spanning multiple files, read every instance side by side and confirm
  they describe the same underlying logic, not just similar wording. For
  a single bullet summarizing one source rule, re-read that rule's actual
  source text directly and confirm the bullet doesn't narrow, broaden, or
  drop part of its real scope.
  ```

  The title changes from "Cross-file rule restatement" to "Rule-restatement accuracy," since the old title no longer describes what the item checks once the single-bullet case joins it.

## Falsifiable Criteria

1. A direct read-through of the shipped `task-reviewer-prompt.md` confirms the new instruction appears once, in the specified location, naming both docs and describing the re-read requirement.
2. A disposable `--plugin-dir` trial (fixture seeded with real copies of `docs/ai-code-guidelines.md` and `docs/code-standards.md`, per `seed-trial-fixtures-with-real-docs`) dispatches a task-quality reviewer against a diff and a deliberately misremembered rule citation planted in the dispatch context. The reviewer's report shows it re-reading the actual section before citing it, not reproducing the planted misremembering verbatim. **Caveat, added after a true two-arm A/B run** (same fixture and a coaching-free prompt, dispatched once against the pre-edit plugin and once against the post-edit plugin): both arms independently verified the planted claim against the actual doc and declined the false finding — the pre-edit reviewer did this unprompted, before this instruction existed. This scenario does not show the new instruction causing a behavioral difference; it shows this criterion verifies the process (the reviewer's report cites current text, matching the new instruction's letter), not a proven causal change in outcome. Treat this criterion as confirming the reviewer follows the instruction's letter, not as confirming it prevents a finding the model would otherwise have filed.
3. A direct read-through of the shipped `writing-plans/SKILL.md` confirms item 6's title and text cover both the cross-file case and the single-bullet case, and the item number stays 6.

## Consequences

Every task-quality review now re-reads the cited doc section AND re-checks the diff hunk before finalizing a convention-based finding — a small, bounded verification step already implicit in the reviewer's general "Do Not Trust the Report" discipline, made explicit for both recurring failure modes (a misremembered rule, a misread diff).

Every plan's Self-Review pass now explicitly checks single-bullet rule summaries, not only multi-file restatements — closing the exact gap that produced two fix rounds in hazard-signal-words (Tasks 5 and 6).

Both process-review Recommendations close, and the tracker's next review can start from a clean Recommendations backlog.

## Deferred

- Extending the same pre-finding check to spec-compliance findings (Part 1) or to re-review-prompt.md — no logged recurrence justifies it yet; revisit if one shows up.
- Extending the check to citations of the task brief or Global Constraints, not just the two convention docs — same reasoning.
- `verify-against-precedent-before-flagging.md`'s second step (search the broader codebase for the same pattern already shipped elsewhere) — deliberately not operationalized here. It directly conflicts with `task-reviewer-prompt.md`'s existing "Do not crawl the broader codebase" scoping, which keeps a task-scoped reviewer bounded to its diff. Re-reading the cited section (step 1) costs little and stays bounded; a codebase-wide precedent search costs much more, for a review that runs once per task. Revisit only if a recurrence shows step 1 alone does not suffice.
