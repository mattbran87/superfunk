# Mechanisms Not Goodwill Wiring — Design

**Date:** 2026-08-13
**Status:** Approved, not yet implemented

## Context

`docs/principles.md` (shipped in the prior sub-project) prompted an assessment of where each of its five principles actually gets enforced today, versus where it stays unread reference prose — the same question already answered for `docs/ai-code-guidelines.md`. Three principles turned out already mechanized by existing skill behavior (Focused Scope, Artifacts Over Memory, User Authority at Decision Points) — nothing to wire, since the skills that implement them predate this document. Continuous Improvement has a real gap, but it overlaps with the still-undesigned continuous-improvement mechanism (a future sub-project) — patching it now risks a throwaway fix superseded by that design. Mechanisms, Not Goodwill has a real, local gap with no such overlap: nothing currently asks, while a design gets presented, whether each decision's convention has something that checks it. This spec closes that one gap.

## Decision

- **`plugin/skills/brainstorming/SKILL.md`, "Presenting the design"** — adds one bullet, immediately after "Cover: architecture, components, data flow, error handling, testing":

  > For each design decision, name what actually checks or enforces it — a review step, a script, a derived value — not just what states it (per `docs/principles.md`'s Mechanisms, Not Goodwill). A decision with no enforcement mechanism is worth flagging as a gap, not silently presenting as settled.

  This fires at design-presentation time, before a decision gets approved and locked in — matching every other wired instruction in this project's timing pattern (catch the gap before it ships, not after).
- **No other file changes.** This is a single-bullet, single-file addition — unlike the five-file `ai-code-guidelines.md` wiring, `principles.md`'s other four gaps either don't exist (already mechanized) or belong to a not-yet-designed future sub-project.

## Testing

Same baseline-trial approach validated for the `ai-code-guidelines.md` wiring: a disposable `--plugin-dir` scratch session invoking `brainstorming` on a design with at least one enforcement-free decision, confirming the new bullet actually surfaces the gap rather than silently presenting the decision as settled. Not the full adversarial pressure-test battery `writing-skills` reserves for discipline-under-pressure rules — this is a structural addition (a required consideration at an existing step), the same category as the prior wiring work.

## Deferred

- `docs/code-standards.md` — sub-project 3, not started.
- The continuous-improvement mechanism — sub-project 4, not started; expected to close Continuous Improvement's own enforcement gap as part of its design, not as a separate patch.
