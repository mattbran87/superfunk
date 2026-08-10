# Brainstorm — Project Definition Skill

**Date:** 2026-08-10
**Stage:** 0 — Brainstorm

## Prior Art Reviewed

The `feature-tracking` workflow left an open question: when planning a feature and no module fits, what decides which module a feature belongs to, or whether a new one gets created? Nothing in that design answers this — it assumed a codebase's decomposition into modules already exists as common knowledge, which doesn't hold for a new area of work or an unfamiliar codebase.

arc42 (arc42.org) answers this at the source: its Building Block View section (#5) documents a system's decomposition into components with clear boundaries and responsibilities — exactly the missing reference. arc42's full template runs 12 sections: Introduction and Goals, Constraints, Context and Scope, Solution Strategy, Building Block View, Runtime View, Deployment View, Crosscutting Concepts, Architecture Decisions, Quality Requirements, Risks and Technical Debt, Glossary.

Casita's own roadmap (see `docs/superpowers/specs/2026-08-10-feature-tracking-design.md`) used change tiers — Quickfix, Micro, Standard, Full — to scale process weight to the size of the change. Both the `superpowers-fork` and `feature-tracking` workflows deferred that concept explicitly, each time as its own future topic. A tiered project-definition document (full arc42 for projects that warrant it, a lighter version for smaller ones) sits at the intersection of that deferred idea and the module-assignment gap.

## Approaches Considered

### Approach A — Full arc42 only

Generate the complete 12-section template for every project, regardless of size.

### Approach B — Building Block View only

Generate just the one arc42 section that solves the module-assignment problem. Skip the rest.

### Approach C — Tiered: full arc42 or a lightweight version, user's choice

Two tiers. The user picks explicitly which one a project gets — no heuristic guessing. Both tiers exist as a living document, updatable later, not a one-time artifact.

Content per section comes from codebase exploration where the codebase can answer it (for example, Building Block View, Deployment View), confirmed with the user. Sections that need human judgment or intent (for example, Goals, Constraints, Quality Requirements) come from direct interview instead.

Output structure: both tiers live under the same directory, `docs/architecture/`, regardless of tier. The lightweight tier holds one file there, `docs/architecture/project-definition.md`. Full arc42 holds one file per section instead, `docs/architecture/NN-section-name.md`, mirroring arc42's own numbered-section convention. The shared parent directory keeps "where do I look for this" consistent across tiers. It also lets a project upgrade from lightweight to full later by adding files, not moving or renaming anything.

Built as a Claude Code Skill (conversational, judgment-driven), not a deterministic script. This task requires interviewing, exploring, and synthesizing — not the mechanical file operations `add_feature.py` and `rebuild_index.py` handle.

## Anti-Pattern Check

- Phase gate ceremony: full arc42 carries real ceremony, but the tiered, user-chosen structure keeps it opt-in. A small project takes the lightweight path and never pays for the full template's weight.
- Dedicated SME or agent: this candidate uses a full Skill, not a checklist. That weight earns its keep here. A checklist can't conduct an interview or synthesize codebase exploration into prose, and this task genuinely requires both capabilities.
- Shared live/dev instruction files: this skill's real home sits at `plugin/skills/project-definition/SKILL.md` — inside the forked superpowers content the `superpowers-fork` workflow already validated. Building and testing it must follow that workflow's already-validated isolation rule:
  - develop in-repo
  - never load `superfunk`'s own in-repo `plugin/` as the live session's active plugin
  - test via disposable `--plugin-dir` sessions in separate projects

## Recommendation

Approach C. It resolves the module-assignment gap (Approach B's core value) without forcing full arc42's weight onto every project (Approach A's cost). The tiering also directly answers the change-tier question, deferred twice already.

## Rejected Approaches

Approach A: forces full arc42 ceremony onto every project regardless of size, exactly what the anti-pattern checklist's first entry warns against.

Approach B: solves the immediate module-assignment gap but throws away the rest of arc42's value (Constraints, Architecture Decisions, Quality Requirements) for projects that would benefit from it. It also doesn't address the change-tier question at all.

Within Approach C, three sub-decisions had rejected alternatives:

- Heuristic tier inference (analyzing project signals to recommend a tier, Casita's cycle-selection style): rejected in favor of asking the user directly — simpler, no risk of a wrong inference nobody asked for.
- One-time generation only: rejected in favor of a living document, matching how this project already treats `CLAUDE.md`.
- A prompt-driven script instead of a Skill: rejected — the task's judgment requirements (interviewing, exploring, synthesizing) don't fit a deterministic script's shape.
