# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

`superfunk` is a ground-up rebuild of an AI-assisted, spec-driven engineering framework, building on lessons learned from an earlier framework (`claude-spec-framework` / Casita) without continuing that codebase. No build/test tooling exists yet — the project is currently in the design and specification stage.

Design specs live in `docs/superpowers/specs/`. See `docs/superpowers/specs/2026-08-05-workflow-validation-process-design.md` for the first sub-project: a repeatable process for designing, diagramming, testing, and validating any candidate workflow's efficacy before it ships into the framework.

When code is added to this project, update this file with:
- Commands for building, linting, testing, and running the project (including how to run a single test)
- High-level architecture notes that require reading multiple files to piece together

## Document writing conventions

All specs and design documents in this project must follow the rules in the `writing-controlled-documents` skill (`C:\Users\marko\.claude\skills\writing-controlled-documents`):
- **Simplified Technical English (STE)** rules apply to all documents — sentence length limits, active voice, imperative mood for instructions, one term per concept, vertical lists over dense paragraphs.
- **E-Prime** (no "to be" forms) additionally applies to spec/plan/requirements/design docs — rewrite state-claims ("X is Y") into checkable mechanisms ("X does Y" / "X happens when Y").
- Run the skill's self-check before finalizing any such document.
