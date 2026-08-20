# Pseudocode During Planning — Design

**Date:** 2026-08-20
**Status:** Approved, not yet implemented

## Context

Casita's spec 099 defined a triggered pseudocode mechanism for its Planning phase. Four conditions — API call sites, handler/pattern reuse, DTO/schema shape, user-designated — produce natural-language pseudocode in `notes.md`, before task breakdown starts. A repo-wide check found zero populated examples across 21 fired triggers. Every one recorded `Skipped: <reason>` instead.

This traces to Casita's own repo producing no application code. Its specs edit templates, prompts, and docs, so the triggers rarely find a real API call site, handler, or schema to describe. The user's own experience of pseudocoding helping came from separate projects that used Casita to build real applications, where these same triggers meet real code.

superfunk today resembles Casita's own repo more than an application project — it ships skills, docs, and scripts, not application features. This spec ports the mechanism anyway, for two reasons. superfunk's own code work will grow past skill-file edits over time. Every project that adopts superfunk downstream builds real application code from day one. It inherits this mechanism through the template.

superfunk's `writing-plans` already requires complete, runnable code in every task step (per its Task Structure: "Complete code in every step"). Pseudocode cannot live inside a task step without duplicating or contradicting that rule. Casita avoids this collision by keeping pseudocode one phase earlier, in Planning's `notes.md`, before task breakdown starts. superfunk has no separate notes.md. `writing-plans` produces the plan document directly. This spec places pseudocode as a distinct step and section inside that same document, positioned before Task Structure. This preserves Casita's phase-ordering without inventing a new file type.

Casita also left a real gap unbuilt: nothing in its Implementation phase ever reads the pseudocode Planning wrote. The mechanism captures a decision. No downstream step checks or reuses it — the exact failure this project's Mechanisms, Not Goodwill principle warns against. This spec closes that gap for superfunk's version.

## Decision

- **New step in `plugin/skills/writing-plans/SKILL.md`**, positioned between the existing "File Structure" and "Task Structure" sections. It evaluates four triggers against the files and responsibilities File Structure just mapped, unchanged from Casita:
  - **T1 — API call sites.** A task calls an external or internal API with more than a trivial signature.
  - **T2 — Handler/pattern reuse.** A task implements a handler, controller, or pattern this codebase already uses elsewhere, where the shape matters.
  - **T3 — DTO/schema shape.** A task defines or consumes a data shape with more than one or two fields.
  - **T4 — User-designated.** The user asks for pseudocode on a specific piece of this plan.
- **Format:** natural-language pseudocode only — standard idioms (`for each`, `if`, `return`), no language-specific syntax, no type system, no library calls. This matches Casita's own format rule, reused directly.
- **Skip allowed, with a reason.** A fired trigger that adds no signal beyond what File Structure already states gets `Skipped: <one-line reason>` instead of forced content. An empty or padded pseudocode block counts as the same placeholder problem `writing-plans`' Self-Review already bans.
- **Output location:** a new `## Pseudocode` section in the plan document itself, between File Structure and Task Structure. No separate file — the plan stays the single artifact for this work, matching Artifacts Over Memory.
- **No mid-write pause.** The user reviews the Pseudocode section along with the rest of the plan at `writing-plans`' existing "Plan complete, please review" handoff. This keeps the skill's current interaction model intact, rather than adding a new interruption pattern for one step alone.
- **Implementation link — closes Casita's gap.** `plugin/skills/subagent-driven-development/SKILL.md`'s "① Dispatch the implementer" step gains a bullet, alongside the existing "Directory context" bullet: when a task's trigger fired with real (non-`Skipped`) pseudocode, fold that subsection into the dispatch's Context. A subagent that never reads the pseudocode gains nothing from Planning having written it.
- **Self-review addition.** `writing-plans`' Self-Review section gains a fourth check. Confirm each of T1–T4 carries either real pseudocode or an explicit `Skipped: <reason>`. No trigger stays silently omitted from the written plan.

## Falsifiable Criteria

Same disposable `--plugin-dir` baseline-trial approach used for every wiring change this session:

1. Build a scratch spec/plan scenario with two tasks. One clearly fires T1 (a real API call with a non-trivial signature). One fires no trigger at all. Run `writing-plans`. Confirm the Pseudocode section populates T1 with real natural-language pseudocode. Confirm it records `Skipped: <reason>` for T2–T4.
2. Run the same scratch plan through `subagent-driven-development`. Confirm the implementer dispatch for T1's task includes the pseudocode subsection in its Context. Confirm the dispatch for the no-trigger task does not.

## Consequences

Every plan that fires at least one trigger now carries an extra section and an extra reviewed decision point. This addition scales to how often triggers actually fire, not a fixed cost per plan.

Plans with no real API calls, handlers, or schemas get four `Skipped` lines and nothing else. This matches most of superfunk's own skill-file work today, and Casita's own repo's real experience.

Function signatures, call patterns, and data shapes become visible and reviewable during Planning, instead of surfacing for the first time as committed code. Restructuring a plan costs less than restructuring code the more expensive Implementation step already committed.

The `writing-plans` self-review grows by one check. A plan missing this check counts as incomplete, the same as a spec requirement with no task covering it.

## Deferred

- A fifth, superfunk-specific trigger for `plugin/skills/*.md` edits — considered and declined for this pass. The four Casita triggers already ported apply generally, and no evidence yet shows skill-file edits need a distinct trigger.
- Retroactively pseudocoding any already-shipped plan — this spec applies forward only, from the next plan `writing-plans` produces.
