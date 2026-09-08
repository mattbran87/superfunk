# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

`superfunk` is a ground-up rebuild of an AI-assisted, spec-driven engineering framework, building on lessons learned from an earlier framework (`claude-spec-framework` / Casita) without continuing that codebase. No build/test tooling exists yet — the project is currently in the design and specification stage.

Design specs live in `docs/superpowers/specs/`. See `docs/superpowers/specs/2026-08-05-workflow-validation-process-design.md` for the first sub-project: a repeatable process for designing, diagramming, testing, and validating any candidate workflow's efficacy before it ships into the framework. The working templates and operator guide for that process live in `workflows/` — start there to run a workflow through the process.

When code is added to this project, update this file with:
- Commands for building, linting, testing, and running the project (including how to run a single test)
- High-level architecture notes that require reading multiple files to piece together

## context-mode companion

`context-mode` pairs with superfunk as a recommended companion, never a requirement. Superfunk declares no plugin dependency, because Claude Code resolves none — the manifest carries no dependency key.

- **Probe.** `plugin/hooks/session-start` checks for `~/.claude/plugins/cache/context-mode/` (or the `marketplaces/` copy). When both are missing, it appends one install note after the `</EXTREMELY_IMPORTANT>` block. When either exists, it appends nothing.
- **The probe checks installation, not availability.** A hook subprocess cannot read the agent's tool list. A session can pass the probe and still lack the ctx tools — disabling the plugin leaves the cache directory in place. Never let the probe result drive a skill's branch.
- **Trial isolation.** Trial sessions keep context-mode disabled, per `docs/superpowers/process-reviews/external-trial-bookmark-cli-harness/trial-settings.json`. Set `SUPERFUNK_SKIP_DEP_CHECK=1` in a trial so the injected bootstrap stays byte-identical across machines.
- **No skill calls the ctx tools yet.** Skill-level integration waits on a workflow-validation verdict. Any future ctx step must branch on tool presence and keep a working fallback, because trials run with context-mode off.

## Document writing conventions

All specs and design documents in this project must follow the rules in the `simple-english-docs` skill (`C:\Users\marko\.claude\skills\simple-english-docs`):
- **Simplified Technical English (STE)** rules apply to all documents — sentence length limits, active voice, imperative mood for instructions, one term per concept, vertical lists over dense paragraphs.
- **E-Prime** (no "to be" forms) additionally applies to spec/plan/requirements/design docs — rewrite state-claims ("X is Y") into checkable mechanisms ("X does Y" / "X happens when Y").
- Run the skill's self-check before finalizing any such document.
