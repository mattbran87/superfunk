# Design Spec Template Quality — Design

**Date:** 2026-08-13
**Status:** Approved, not yet implemented

## Context

Comparing `docs/superpowers/specs/`'s real shape against Casita's ADR required fields — during the `code-standards.md` sub-project's discussion of whether superfunk needs a separate Architecture Decision Record system — surfaced a concrete, already-real gap: `Status` uses ad hoc, inconsistent strings (`Shipped`, `Approved, not yet implemented`, `Approved for planning`), and nothing updates it once a design actually ships. A direct check confirms this happened, not just risked happening: `2026-08-11-human-in-the-loop-review-design.md`, `2026-08-12-roadmap-multifile-split-automation-design.md`, `2026-08-13-ai-code-guidelines-wiring-design.md`, and `2026-08-13-mechanisms-not-goodwill-wiring-design.md` all still read `Approved, not yet implemented`, despite each getting fully implemented, tested, and shipped afterward — confirmed via `git log`, each file has exactly one commit ever, its own creation.

This spec covers the template and process fix, plus the retroactive correction those four files need right now.

## Decision

- **Formal Status lifecycle**, replacing free-text strings: `Proposed` (presented, not yet approved — rare in practice, since `brainstorming`'s hard gate means a spec file usually doesn't exist until approval, but valid for a spec still under revision), `Approved` (approved, not yet implemented), `Shipped` (implemented and merged), or `Superseded by <filename>` (a later spec revised or replaced this one's decision).
- **A real trigger for `Shipped`**: `plugin/skills/subagent-driven-development/SKILL.md`'s "Finish" section gains an instruction — once the final whole-branch review comes back clean and its fixes merge, update the originating design spec's `Status` line from `Approved` to `Shipped`, in the same wrap-up. Without this, `Shipped` stays exactly as unreliable as the free-text version it replaces.
- **A real trigger for `Superseded by`**: `plugin/skills/brainstorming/SKILL.md`'s "Write design doc" step gains a check — before writing a new spec, ask whether it changes or replaces a decision an earlier spec made; if so, update that earlier spec's `Status` to `Superseded by <this-filename>` as part of writing the new one. This is exactly the step that should have run when the roadmap-split-automation spec shipped what `2026-08-10-feature-tracking-design.md` had called "not yet built."
- **New required section: Consequences**, positioned after Decision (and after Falsifiable Criteria or Testing, if either applies), before Deferred. States what becomes easier or harder because of this decision, and what assumptions must hold for it to stay correct. Fills a real gap — `Deferred` only names what's *not* being done; nothing currently names what gets harder because of what *was* decided.
- **Alternatives Considered — conditional, not a fixed template slot.** `brainstorming`'s "Write design doc" step gains a check: if `multi-lens-research` or `branching-research` actually ran for this decision, capture the comparison (the candidates, the recommendation, the steelmanned alternative) as an Alternatives Considered section. If no formal research skill ran, skip the section — forcing an empty one for every simple decision would itself become the placeholder problem the spec self-review already bans.
- **Retroactive fix**: update the four already-shipped specs' `Status` lines (`2026-08-11-human-in-the-loop-review-design.md`, `2026-08-12-roadmap-multifile-split-automation-design.md`, `2026-08-13-ai-code-guidelines-wiring-design.md`, `2026-08-13-mechanisms-not-goodwill-wiring-design.md`) from `Approved, not yet implemented` to `Shipped`. A direct, cheap consequence of this investigation, not separate cleanup work.

## Falsifiable Criteria

No trials for the template/vocabulary decisions themselves — like the prior sub-projects, these produce reference material and prose conventions, not executable behavior. The two skill-file edits (`subagent-driven-development`'s Finish-step trigger, `brainstorming`'s Write-design-doc-step triggers) get the same disposable `--plugin-dir` baseline-trial treatment already used for every prior wiring change in this session.

## Consequences

Every future design spec carries one more required section (Consequences) and, when research ran, a second conditional one (Alternatives Considered) — a small but real increase in what `brainstorming`'s "Write design doc" step produces each time. The `Shipped` trigger only fires through `subagent-driven-development`'s "Finish" step; a design implemented through a different path (direct authoring, the "lighter path" this session used repeatedly for small doc-only additions) won't get its `Status` updated automatically and needs the same manual correction this spec is applying retroactively right now. `docs/ai-code-guidelines.md` and `docs/principles.md` (the two sub-projects shipped via direct authoring, no `subagent-driven-development` pipeline) already show this: both say `Shipped` correctly today, but only because whoever wrote them remembered to set it, not because a mechanism enforced it.

## Deferred

- Closing the gap this spec's own Consequences section names: designs shipped via direct authoring (not `subagent-driven-development`) have no automatic `Shipped` trigger. Revisit if that gap causes a real, observed staleness problem, the same way the `Approved, not yet implemented` gap did.
- The continuous-improvement mechanism — still not started; may eventually want a periodic sweep catching stale `Approved`/`Proposed` statuses the two triggers above miss.
