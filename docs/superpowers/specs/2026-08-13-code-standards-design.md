# Code Standards — Design

**Date:** 2026-08-13
**Status:** Shipped

## Context

This spec covers sub-project 3 of 4 in the DO-178C-inspired documentation effort — see `docs/superpowers/specs/2026-08-13-ai-code-guidelines-design.md` for the full context and the four-sub-project breakdown. `docs/code-standards.md` adapts Casita's own `docs/code-standards.md`: file naming, markdown conventions, git conventions, and several other standing engineering rules.

Casita's version mixes genuinely portable conventions with content tied entirely to Casita's own architecture — command files, SME agent modules, an npm-published distribution pipeline. None of that architecture exists in superfunk. This spec covers what carries over, what drops, and what needed real adaptation.

## Decision

- **Dropped entirely — no equivalent in superfunk:** Command File Structure, Command Patterns, SME Persona Structure, and Package Distribution. These describe Casita's `.claude/commands/`, multi-module SME agents, and `casita init` npm pipeline — none of which superfunk has or plans to build the same way.
- **Dropped per explicit decision:** Changelog Conventions (no releases or versioning exist yet — adding the convention now would speculate against an unproven need). Architecture Decision Records (`docs/superpowers/specs/` already documents context, decision, and rationale for every major choice; a separate project-level ADR system would duplicate that role). Lessons vs. Patterns (a knowledge-capture mechanism that belongs to the still-undesigned continuous-improvement sub-project, not a standalone code-standards convention).
- **Ported, adapted:**
  - File Naming — kebab-case docs port unchanged; Casita's zero-padded spec numbering (`001-feature-name`) becomes superfunk's `YYYY-MM-DD-<slug>` convention, matching the date-slug ID scheme decision already made for feature-tracking.
  - Markdown Conventions (headings, formatting, links) — ports essentially unchanged, language- and architecture-agnostic.
  - Git Conventions — ports unchanged in substance; this session's own commit history already follows the exact convention (`type(scope): description`) without ever having it written down until now.
  - Spec File Conventions — Casita's `Planning → Implementation → Testing → Complete` status progression becomes superfunk's actual closed vocabulary (`Planned`/`In Progress`/`Done`/`Deferred`/`Dropped`), and the acceptance-criteria rule names both of this project's real validation tracks (Falsifiable Criteria for full Workflow-Validated specs, Testing sections with scratch-trial evidence for lighter-path additions) instead of assuming one fixed format.
  - CLAUDE.md Maintenance — ports unchanged in substance. `CLAUDE.md` sits at 20 lines today, well under Casita's 150-line target, so this section documents forward-looking discipline rather than an active pruning need.
  - Cross-File Field Dependencies — ported with a real, current example instead of a hypothetical one: `spec.md`'s fields get parsed by `.superfunk/rebuild_index.py`'s `FIELD_RE` via exact regex match today, so the bare-word-format rule this section states already has a concrete stake in the codebase.
  - Edit Tool Guidelines — ports unchanged; general engineering practice, not tied to Casita's architecture.
- **Follow-on work queued, not part of this spec:** reviewing `docs/superpowers/specs/`'s own document quality against Casita's ADR required fields (`Status` lifecycle, `Rationale`, `Alternatives Considered`, `Consequences`) surfaced real gaps during this sub-project's discussion — concretely, nothing currently marks that `2026-08-10-feature-tracking-design.md`'s "not yet built" line about the multi-file split went stale once `2026-08-12-roadmap-multifile-split-automation-design.md` shipped. This gets its own brainstorm-design-plan cycle next, since it's about the shape `brainstorming`'s "Write design doc" step produces, not a code-standards convention.

## Falsifiable Criteria

No trials ran for this sub-project — like `ai-code-guidelines.md` and `principles.md`, it produces a reference document, not executable behavior, so the Workflow Validation Process's Trials stage doesn't apply.

## Deferred

- The design-spec template quality review (Status lifecycle, Rationale, Alternatives Considered, Consequences) — queued as the next sub-project.
- The continuous-improvement mechanism — sub-project 4, not started; expected to address Lessons vs. Patterns as part of its own design.
- Whether `docs/code-standards.md` needs wiring into the skill chain (the same question already answered for `ai-code-guidelines.md` and `principles.md`) — not assessed yet in this spec.
