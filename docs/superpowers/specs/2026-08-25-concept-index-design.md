# Concept Index — Design

**Date:** 2026-08-25
**Status:** Approved

## Context

A comparison against `github.com/kaanozhan/Frame` — an external spec-driven agentic-development tool — surfaced its `intentIndex`: a map from free-form concept keywords ("github," "terminal") to the files that implement them, kept fresh via a pre-commit hook, so an agent jumps straight to the right file instead of searching.

Superfunk carries two partial analogs, neither filling this gap. `project-definition`'s Building Block View maps a codebase's module decomposition — but only at module grain, only when a user explicitly runs the skill, and it goes stale the moment the codebase changes without a re-run. `feature-tracking`'s `roadmap.md` files organize features by module and bundle — a navigable map, but organized around where a feature got filed, not around what concept a reader searches for.

Superfunk already curates context for subagents rather than letting them explore: `.context.md` (per-directory purpose, decisions, watch-outs) and Pseudocode context both get folded into a dispatch by the controller, never left for a subagent to discover on its own. This spec extends that same discipline one level further — a map from concept to file, not just directory to context.

This ships as a general-purpose skill, the same way `project-definition` and `feature-tracking` did — any project adopting this framework gets it, not just superfunk's own repo. The payoff grows with codebase size; superfunk's own repo stays small enough to navigate by directory structure today, so downstream projects that grow larger benefit from this first.

An earlier session Lesson recorded that the controller missed following a three-day-old Finish-step mechanism (per-task outcome capture) while executing its own next plan. This spec's Finish-step wiring states its trigger condition as its own explicit line, not folded into general "other bookkeeping" prose, to avoid the same failure mode.

## Decision

- **New skill: `concept-index`.** Maintains `docs/architecture/concept-index.md` — a single git-tracked markdown table, colocated with `project-definition`'s own output directory rather than a new location.

  ```markdown
  # Concept Index

  | Concept | Type | Location | Description |
  |---|---|---|---|
  | process-review | Skill | `plugin/skills/process-review/` | Synthesizes recent Catches/Misses/Friction/Gaps into a dated review file |
  ```

- **Three concept-unit types**, each keyed to a boundary this project already draws — no new naming scheme, no open vocabulary to keep consistent:
  - **Skill** — one row per `plugin/skills/<name>/`.
  - **Feature** — one row per `specs/<module>/<feature>/` (the `feature-tracking` pipeline), for a downstream project's own domain features.
  - **Directory** — one row per directory meeting `docs/ai-code-guidelines.md`'s existing "significant directory" threshold — the same threshold `.context.md` already uses, so one shared definition of "important enough to index" governs both mechanisms.

  Explicitly out of scope: `docs/superpowers/specs/` and `docs/superpowers/plans/`. That pipeline records this framework's own meta-development history — designing superfunk's skills — not a downstream project's domain concepts. A project adopting this framework indexes what it builds, not how the framework that helped build it evolved.

- **Two entry points, mirroring `project-definition`'s own shape:**
  1. **Full build** — invoked directly on a codebase with no index yet. Scans every `plugin/skills/<name>/`, every `specs/<module>/<feature>/`, and every directory crossing the significance threshold. For a Skill, derives its Description from the skill's own `SKILL.md` frontmatter `description:` field, trimming any "Use when..." framing down to what the skill does. For a Feature, derives it from `spec.md`'s title/summary. For a Directory, derives it from its `.context.md`'s `**Purpose:**` line if one exists; asks the user for a one-liner if it doesn't. Writes the table, commits.
  2. **Incremental maintenance** — wired into `subagent-driven-development`'s Finish step, as its own explicit line alongside the spec Status update, tracker append, and Lesson capture (not folded into general bookkeeping prose): check the plan's own File Structure section for whether it created, renamed, moved, or deleted a `plugin/skills/<name>/`, a `specs/<module>/<feature>/`, or a directory crossing the significance threshold. A create/rename/move adds or updates that row; a delete removes it. No trigger match: skip — most plans touch existing units without adding, moving, or removing one, and skipping avoids an index update on every doc tweak.

- **Consumption wiring** — `subagent-driven-development`'s dispatch step gains a companion check alongside the existing Directory context and Pseudocode context bullets: before dispatching an implementer, check whether the task brief names a concept already in the index. If it does, fold that row's Location into the dispatch context, the same "curated, not raw access" pattern `.context.md` and Pseudocode context already establish — the implementer receives the location, it never searches for it.

## Falsifiable Criteria

1. Running `concept-index`'s full build against a disposable fixture seeded with several real skill directories and one directory carrying a real `.context.md` produces one correctly-described row per skill (sourced from each `SKILL.md`'s frontmatter) and one row for the `.context.md`-bearing directory (sourced from its Purpose line).
2. A disposable `--plugin-dir` trial runs a 1-task plan that creates a new skill directory through `subagent-driven-development`. Finish adds exactly one new row for it, in the same commit pattern already used for the tracker and lessons-learned updates.
3. A second trial runs a 1-task plan that only modifies an existing skill's file, creating no new skill, feature, or significant directory. Finish correctly skips the index update, confirming the trigger condition doesn't fire on every plan.
4. A third trial runs a 1-task plan that deletes an existing skill directory. Finish removes that skill's row from the index.
5. A trial dispatches an implementer whose task brief names an existing indexed skill. The dispatch context includes that skill's indexed Location, sourced from the index.

## Consequences

Every codebase adopting this framework gains one more git-tracked file, updated only when a plan's File Structure section actually adds, moves, or removes an indexed unit — not on every commit.

`subagent-driven-development`'s Finish step gains one more explicit bookkeeping line, and its dispatch-context step gains one more companion check, matching the shape Directory context and Pseudocode context already established.

Superfunk's own repo gains an index too, once run, though its practical value there stays modest until the repo grows past what directory structure alone makes navigable.

## Deferred

- Free-form keyword concepts beyond the three structural-unit types — deferred until a real gap shows a structural unit can't name something worth indexing.
- A rebuild/drift-detection script (comparable to `feature-tracking`'s `rebuild_index.py`) that re-scans the whole codebase and reconciles it against the incrementally-maintained index — deferred; a Python-specific script doesn't port to an arbitrary downstream project's language or stack, so this spec commits to the AI-maintained Finish-step trigger for v1 instead.
- Indexing `docs/superpowers/specs/`/`docs/superpowers/plans/` (this framework's own meta-development history) as its own separate, differently-scoped index — not requested; revisit only if a real need for it surfaces.
