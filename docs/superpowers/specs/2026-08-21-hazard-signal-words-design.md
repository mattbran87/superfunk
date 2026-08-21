# Hazard Signal Words and Code-Standards Wiring — Design

**Date:** 2026-08-21
**Status:** Approved, not yet implemented

## Context

The user's draft adapts ANSI Z535 signal words (DANGER, WARNING, CAUTION, NOTICE) — the fixed severity vocabulary used on safety signs and in aviation technical manuals. It covers three contexts: chat responses, code comments, and commit messages. This spec ports the last two only, per the user's explicit scope. Chat-response signaling stays out of scope.

superfunk already runs `ai-code-guidelines.md`'s "Why Comments" convention: a `why:` prefix marking a non-obvious constraint. The draft's hazard vocabulary answers a different question — what breaks if a future caller misuses this code, not why the code looks unusual. The two stay separate systems. A line can carry both if it genuinely needs both.

A survey of the fork's skill chain found a real gap: `docs/code-standards.md` gets read nowhere. Only `docs/ai-code-guidelines.md` got wired earlier this session, at two broad points (the implementer, before writing code; the code-quality reviewer, checking a diff) and three narrower points tied to one specific section (Per-Directory Context Files, wired into three separate skill-chain moments). `docs/code-standards.md`'s own Git Conventions section — the existing Conventional Commits rule — has never actually gotten checked by anything. Adding the draft's commit-trailer rule there would inherit the same gap.

This spec closes that gap while landing the new rule. It wires `docs/code-standards.md` the same way `docs/ai-code-guidelines.md` already got wired: two broad points, plus section-specific points matching real trigger moments already in the skill chain.

## Decision

- **New `docs/ai-code-guidelines.md` section: "Hazard Signal Words."** DANGER/WARNING/CAUTION/NOTICE, adapted from the draft's Context 2 table. DANGER and WARNING go inline, at the hazardous line. CAUTION and NOTICE go in the function or class's own documentation comment, since they describe the unit as a whole. Cross-references "Why Comments": a hazard comment answers what breaks if misused; a why comment answers why the code looks unusual. Different questions — a line can carry both.
- **`docs/code-standards.md`'s Git Conventions section gains the commit-trailer rule**, from the draft's Context 3. A footer line — `DANGER:`, `WARNING:`, `CAUTION:`, or `NOTICE:` — present only when it applies, composing with the existing Conventional Commits format the same way `BREAKING CHANGE:` composes with it elsewhere.
- **Broad wiring — `docs/code-standards.md` joins `docs/ai-code-guidelines.md` at its two existing broad read points.**
  - `plugin/skills/subagent-driven-development/implementer-prompt.md` — the existing "read `docs/ai-code-guidelines.md` before writing any code" instruction extends to also name `docs/code-standards.md`.
  - `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — the existing code-quality check against `docs/ai-code-guidelines.md` extends to also check the diff and commit messages against `docs/code-standards.md`.
- **Distributed wiring — two sections, two specific trigger points**, matching how Per-Directory Context Files got wired to three specific moments rather than folded only into the broad read.
  - `plugin/skills/writing-plans/SKILL.md`'s File Structure step gains a check against File Naming, at the point file names get decided.
  - `plugin/skills/brainstorming/SKILL.md`'s "Write design doc" step gains a check against Spec File Conventions, at the point a spec file gets written.
- **No further wiring for the rest of `code-standards.md`.** Lessons vs. Patterns and Checklist Construction already carry their real mechanism directly inside the relevant skill step (the Finish step, the checklists themselves) — a pointer here would duplicate, not add. CLAUDE.md Maintenance, Cross-File Field Dependencies, and Edit Tool Guidelines have no specific recurring trigger point found; the broad read covers them at the right level.

## Falsifiable Criteria

Same disposable `--plugin-dir` baseline-trial approach used for every wiring change this session:

1. Build a scratch fixture with a task whose spec calls for a function with a real, obvious hazard (a delete operation with no null-check) and a commit that changes a default value in a way that affects all callers. Run the implementer dispatch. Confirm the resulting code carries a DANGER-level inline comment. Confirm the resulting commit carries a WARNING-level trailer.
2. Using the same fixture, run the code-quality reviewer against a version with the hazard comment or trailer removed. Confirm it flags the omission, citing `docs/ai-code-guidelines.md` or `docs/code-standards.md` by name.
3. Build a second scratch fixture: a plan whose File Structure step picks a file name that violates File Naming (not kebab-case), and a brainstorm that writes a spec missing a Spec File Conventions requirement. Confirm each distributed wiring point catches its own violation.

## Consequences

Every implementer dispatch and every code-quality review now reads one more file. `docs/code-standards.md`'s existing rules — Git Conventions among them — move from goodwill-only to actually checked, the same shift `ai-code-guidelines.md` went through earlier this session.

A hazard comment and a why comment can both apply to the same line. Nothing merges them into one prefix. A reader checks each independently.

The commit-trailer rule adds one optional line to commit messages. Most commits carry none, the same as `BREAKING CHANGE:` in Conventional Commits today.

Two skill-chain steps (File Structure, Write design doc) each gain one more check. Both apply only at the moment they already run — no new pause, no new step.

## Deferred

- Chat-response signaling (the draft's Context 1) — explicitly out of scope per the user's request.
- Retroactively auditing already-shipped code or commits against these rules — this spec applies forward only.
- Further distributed wiring for `code-standards.md` sections beyond File Naming and Spec File Conventions — revisit if a future review finds a specific gap the two broad points don't cover.
