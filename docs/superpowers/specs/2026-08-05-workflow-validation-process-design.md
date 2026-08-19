# Workflow Validation Process — Design

**Date:** 2026-08-05
**Status:** Shipped

## Context

This project (`superfunk`) rebuilds an AI-assisted, spec-driven engineering framework from the ground up. It builds on lessons learned from an earlier framework (`claude-spec-framework`, also called Casita) instead of continuing that codebase.

The team attempted an in-place v2 rewrite of Casita. That rewrite did not succeed. The framework accrued technical debt over time. The old process shipped each workflow before the team validated it. The team then patched problems found on real projects afterward.

This new framework rests on **Iterative AI-Assisted Engineering** as its foundation. This spec does not define formal principles for that foundation. Evidence gathered from real workflow trials will ground those principles later. The team will not assert them in advance.

This spec covers the first sub-project: a repeatable process to design, test, and validate a candidate workflow's efficacy. The process runs before the framework adopts a workflow, or before that workflow runs on a project that matters. Specific real workflows (for example, a spec-and-planning workflow or a quickfix workflow) fall outside this spec's scope. Each will use this process in its own separate spec.

## Purpose

Give every candidate workflow a structured path from idea to an evidence-backed, shippable process. This replaces the old pattern: ship a workflow first, then discover its problems on real work.

## Core Loop

Six stages apply to each candidate workflow:

### 0. Brainstorm

Explore the design space before you commit to any shape. Review prior art: how Casita approached this, if it did; other frameworks, such as spec-kit and superpowers; and first-principles alternatives. Land on 2-3 rough approaches with a recommendation.

Check each candidate approach against a running anti-pattern checklist. The checklist starts with these questions:

- Does this add a phase gate that doesn't earn its ceremony?
- Does this require a dedicated SME or agent, when a checklist or a single prompt could serve the same purpose?

This checklist grows over time. The team appends new entries as it discovers them during real development. The checklist applies to every future workflow brainstorm, not just this one.

Produces: `brainstorm.md` — considered approaches, rejected approaches with reasons, and anti-pattern check results.

### 1. Diagram

Sketch the chosen approach as a flow or state diagram (mermaid). Capture:

- entry points
- steps
- decision points
- gates
- exit or failure states

This diagram anchors the whole process. Later, trial issues trace back to a specific node or edge in it.

Produces: `diagram.md`.

### 2. Success Criteria

State what "this workflow works" means in falsifiable, checkable terms, before any trial runs. For example: "produces a correct spec.md with at most 1 manual correction, across at least 3 of 4 trials, including one synthetic and one real-project environment." If the team cannot state criteria up front, the diagram needs more work before trial.

Produces: `criteria.md`.

### 3. Test Plan

List the trial scenarios to run. Each scenario specifies:

- **Environment** — a synthetic test project, or a sandboxed copy of a real project
- **Driver** — hands-on (a person drives the session), or an autonomous agent run (unattended; the team reviews the transcript afterward)
- **Variation** — how this trial differs from others: project size or language, ambiguous requirements, mid-workflow interruption, and so on

The team chooses environment and driver per scenario, not once for the whole workflow.

Produces: `test-plan.md`.

### 4. Trials + Trial Log

Run the scenarios from the test plan. Append each trial to the trial log with:

- Environment and driver used
- Outcome: whether the trial met the stated success criteria
- Friction: every point where a human intervened, corrected output, or where the diagram did not match what actually happened

The diagram stays editable through this stage. As trials reveal gaps, the team updates the diagram in place. It does not freeze right after stage 1.

Produces: `trial-log.md` (append-only).

### 5. Verdict

One of:

- **Ship** — the workflow meets its stated criteria; the team promotes its diagram and criteria into a canonical, versioned spec.
- **Revise** — the team identifies a clear fix; return to Diagram (stage 1) or Test Plan (stage 3), whichever stage sits closer to the problem.
- **Kill** — the approach does not work. Document why, and return to Brainstorm (stage 0): the underlying approach, not just its execution, needs to change.

## Testing Environments

Two kinds exist. The team chooses one per scenario at the Test Plan stage:

- **Synthetic test projects** — small, purpose-built repos for fast, cheap iteration on mechanical correctness.
- **Sandboxed copies of real projects** — git worktrees, branches, or clones of real-world projects, used when realism or complexity matters (for example, a workflow that interacts with a messy existing codebase).

Neither serves as the default. The Test Plan stage decides per scenario, based on what the trial needs to prove.

## Trial Drivers

The team also chooses these per scenario at the Test Plan stage:

- **Hands-on** — a person drives the session interactively, for workflows that involve real judgment calls or gates.
- **Autonomous agent run** — an agent runs the workflow unattended against the environment. The team reviews the transcript afterward.

## Promotion Rule

A workflow does not ship because it "feels done." Only evidence recorded in `trial-log.md`, checked against the criteria in `criteria.md`, justifies a Ship verdict. If friction turns up later during real use of a shipped workflow, that triggers a new Revise cycle, not a silent, undocumented patch.

## Artifacts Summary

Each candidate workflow gets a dedicated directory containing:

| File | Produced in stage | Nature |
|---|---|---|
| `brainstorm.md` | 0 | Written once; the team may revisit it on Kill |
| `diagram.md` | 1 | Stays editable during trials; freezes at Ship |
| `criteria.md` | 2 | Written once per loop iteration |
| `test-plan.md` | 3 | Written once per loop iteration |
| `trial-log.md` | 4 | Append-only |

On Ship, the team promotes the diagram and criteria into the workflow's canonical spec. The exact format of that canonical spec depends on the delivery substrate decision noted below. This document does not define that format.

## Deferred Decisions

This spec deliberately leaves these decisions open:

- **Delivery substrate** — whether real workflows ship as Claude Code Skills, slash commands plus agents, an MCP server, or a hybrid. The team will decide this after at least one real workflow runs through this process. That run produces evidence to inform the choice. The team may even run the substrate choice itself through this same loop.
- **Formal Iterative AI-Assisted Engineering principles doc** — deferred until evidence from real workflow trials can ground the principles. The team will not assert them up front.

## Out of Scope

- Any specific real workflow (spec-and-planning workflow, quickfix workflow, and so on): each will use this process in its own spec.
- CLI or distribution tooling.
- SME or agent design.
