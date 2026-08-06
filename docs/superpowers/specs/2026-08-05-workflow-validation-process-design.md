# Workflow Validation Process — Design

**Date:** 2026-08-05
**Status:** Approved for planning

## Context

This project (`superfunk`) is a ground-up rebuild of an AI-assisted, spec-driven engineering framework, building on lessons learned from an earlier framework (`claude-spec-framework` / Casita) rather than continuing that codebase. An in-place v2 rewrite of Casita was attempted and did not go well — the framework had accrued technical debt, and workflows had historically been designed, shipped, and only validated afterward by running them on real projects and patching whatever broke.

The foundation for this new framework is **Iterative AI-Assisted Engineering**. Formal principles for that foundation are deliberately not written yet — they'll be grounded in evidence from running real workflows through the process defined here, rather than asserted up front.

This spec covers the first sub-project: a repeatable process for designing, testing, and validating the efficacy of a candidate workflow *before* it is trusted into the framework or run against a project that matters. Specific real workflows (e.g., a spec/planning workflow, a quickfix workflow) are out of scope for this spec — they will each be designed using the process defined here, as separate specs.

## Purpose

Give every candidate workflow a structured path from idea to evidence-backed, shippable process — replacing the old pattern of shipping a workflow and discovering its problems on real work.

## Core Loop

Six stages, applied to each candidate workflow:

### 0. Brainstorm

Explore the design space before committing to any shape. Review prior art — how Casita approached this (if it did), other frameworks (spec-kit, superpowers), and first-principles alternatives. Land on 2-3 rough approaches with a recommendation.

Explicitly check the candidate approach(es) against a running anti-pattern checklist, seeded with:

- Does this add a phase gate that isn't earning its ceremony?
- Does this require a dedicated SME/agent that could just be a checklist or a single prompt?

This checklist is living — new entries get appended as they're discovered during real development, and it applies to every future workflow brainstorm, not just this one.

Produces: `brainstorm.md` — approaches considered, what was rejected and why, anti-pattern check results.

### 1. Diagram

Sketch the chosen approach as a flow/state diagram (mermaid): entry points, steps, decision points, gates, exit/failure states. This is the anchor artifact — trial issues found later get traced back to a specific node or edge in this diagram.

Produces: `diagram.md`.

### 2. Success Criteria

State what "this workflow works" means in falsifiable, checkable terms, before any trial runs. For example: "produces a correct spec.md with ≤1 manual correction, in ≥3 of 4 trials, across at least one synthetic and one real-project environment." If criteria can't be stated up front, the diagram is not ready for trial.

Produces: `criteria.md`.

### 3. Test Plan

A short list of trial scenarios. Each scenario specifies:

- **Environment** — synthetic test project or sandboxed copy of a real project
- **Driver** — hands-on (a person drives the session) or autonomous agent run (unattended, reviewed via transcript afterward)
- **Variation** — what's different about this trial (project size/language, ambiguous requirements, mid-workflow interruption, etc.)

Environment and driver are chosen per scenario, not fixed globally for the workflow.

Produces: `test-plan.md`.

### 4. Trials + Trial Log

Run the scenarios from the test plan. Each trial is appended to the trial log with:

- Environment and driver used
- Outcome — did it meet the stated success criteria
- Friction — every point where a human had to intervene, correct output, or where the diagram didn't match what actually happened

The diagram is a living artifact during this stage — it gets updated in place as trials reveal gaps, not frozen after stage 1.

Produces: `trial-log.md` (append-only).

### 5. Verdict

One of:

- **Ship** — criteria met; the diagram and criteria are promoted into the workflow's canonical, versioned spec.
- **Revise** — a clear fix is identified; loop back to Diagram (stage 1) or Test Plan (stage 3), whichever is closer to the problem found.
- **Kill** — the approach itself doesn't work; document why and loop back to Brainstorm (stage 0), since the underlying approach — not just its execution — needs to change.

## Testing Environments

Two kinds, chosen per-scenario at the Test Plan stage:

- **Synthetic test projects** — small, purpose-built repos for fast, cheap iteration on mechanical correctness.
- **Sandboxed copies of real projects** — git worktrees, branches, or clones of actual real-world projects, used when realism or complexity matters (e.g., a workflow that needs to interact with a messy existing codebase).

Neither is the default; the Test Plan stage decides per scenario based on what the trial needs to prove.

## Trial Drivers

Also chosen per-scenario at the Test Plan stage:

- **Hands-on** — a person drives the session interactively; used where the workflow involves real judgment calls or gates.
- **Autonomous agent run** — an agent runs the workflow unattended against the environment; the transcript is reviewed afterward.

## Promotion Rule

A workflow does not ship on "feels done." Only evidence recorded in `trial-log.md` against the criteria in `criteria.md` justifies a Ship verdict. If friction is discovered later during real use of a shipped workflow, that triggers a new Revise cycle — not a silent, undocumented patch.

## Artifacts Summary

Per candidate workflow, in a dedicated directory:

| File | Produced in stage | Nature |
|---|---|---|
| `brainstorm.md` | 0 | Written once, may be revisited on Kill |
| `diagram.md` | 1 | Living during trials; frozen at Ship |
| `criteria.md` | 2 | Written once per loop iteration |
| `test-plan.md` | 3 | Written once per loop iteration |
| `trial-log.md` | 4 | Append-only |

On Ship, the diagram and criteria are promoted into the workflow's canonical spec. The exact format of that canonical spec depends on the delivery substrate decision noted below, and is not defined by this document.

## Deferred Decisions

Not resolved by this spec, deliberately:

- **Delivery substrate** — whether real workflows are delivered as Claude Code Skills, slash commands + agents, an MCP server, or a hybrid. This will be decided once at least one real workflow has been run through this process and there's evidence to inform the choice — possibly by running the substrate choice itself through this same loop.
- **Formal Iterative AI-Assisted Engineering principles doc** — deferred until principles can be grounded in evidence from real workflow trials rather than asserted up front.

## Out of Scope

- Any specific real workflow (spec/planning workflow, quickfix workflow, etc.) — each will be designed using this process, as its own spec.
- CLI or distribution tooling.
- SME/agent design.
