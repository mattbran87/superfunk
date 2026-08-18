# Project Principles — Design

**Date:** 2026-08-13
**Status:** Shipped

## Context

This spec covers sub-project 2 of 4 in the DO-178C-inspired documentation effort (structural inspiration, not certification compliance) — see `docs/superpowers/specs/2026-08-13-ai-code-guidelines-design.md` for the full context and the four-sub-project breakdown. `docs/principles.md` adapts Casita's own `docs/principles.md`: five named principles, each a claim backed by mechanisms and testable commitments.

Casita's version leans heavily on mechanisms this project doesn't have — phase gates, dedicated SME agents, a spec-numbering scheme. This spec covers which of the five principles carry over, and how each one's mechanisms map onto what superfunk actually has today rather than what Casita had.

## Decision

- **All five principles carry over**, each re-grounded in superfunk's real mechanisms:
  - **Continuous Improvement** — cites `workflows/anti-patterns.md` (already grew from a real incident), the build-review-fix-re-review loop this session ran on every task, and design docs that already got revised as new evidence arrived. Not a placeholder pointing at the still-undesigned continuous-improvement sub-project — the principle's own rule ("a principle without mechanisms stays aspirational") means it needs real, present-tense evidence, and superfunk already has some. That future sub-project extends this list; it doesn't create it from nothing.
  - **Focused Scope** — Casita's task/spec/group nesting becomes task/feature/module. `task-breakdown-sme` and roadmap groupings become `brainstorming`'s scope-decomposition check and feature-tracking's Bundle structure. The grab-bag exception keeps its core rule (a cluster needs real reflection to justify staying together) but honestly notes superfunk has no reflection mechanism yet — a grab-bag bundle splits by default until one exists.
  - **Mechanisms, Not Goodwill** — ports cleanly. Casita's SME audits and phase gates become superfunk's subagent review loop and `rebuild_index.py`'s derived `blocked`/`blocked_reason` columns, chosen as an example specifically because nothing about it gets typed by hand.
  - **Artifacts Over Memory** — ports cleanly, and already carries superfunk's strongest evidence among the five: `spec.md`/`decisions.md`/`notes.md`/`tasks.md`, `docs/superpowers/specs/`, `docs/superpowers/plans/`, and `subagent-driven-development`'s ledger all stay real and in active use.
  - **User Authority at Decision Points** (renamed from Casita's "at Phase Boundaries," since superfunk has no phases) — reframed entirely around superfunk's real gate points: `brainstorming`'s hard gate, the spec-review gate, `finishing-a-development-branch`'s menu, and the human-in-the-loop review checkpoint. Same underlying claim as Casita's version (Claude proposes, the user decides), lighter mechanisms.
- **Composability by default** (a Casita "candidate," never promoted there either) gets dropped — no written mention. superfunk doesn't yet have enough skill/template surface area to say whether compose-vs-duplicate pressure is a real, earned concern here.
- **Dogfooding as first-class** stays an informal practice, not written up as a principle. Real evidence already exists (the feature-tracking system tracking its own future automation work), but one instance doesn't earn a standing, citable principle yet — revisit once it repeats.

## Falsifiable Criteria

No trials ran for this sub-project — like `ai-code-guidelines.md`, it produces a reference document, not executable behavior, so the Workflow Validation Process's Trials stage doesn't apply.

## Deferred

- `docs/code-standards.md` — sub-project 3, not started.
- The continuous-improvement mechanism — sub-project 4, not started. Expected to extend the Continuous Improvement and Focused Scope principles' Mechanisms lists once it exists, not to require rewriting either principle from scratch.
- Promoting Dogfooding to a written principle, if the practice repeats enough to earn it.
