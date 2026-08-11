---
name: project-definition
description: Use when a project needs an architecture reference document — especially when it's unclear which module a new feature belongs to, or when starting a new project and its structure isn't defined yet. Generates a tiered project-definition document (full arc42 or a lightweight subset) that becomes the authoritative reference for the project's module decomposition.
---

# Project Definition

## Overview

Generates and maintains a project-definition document based on the arc42 architecture template (arc42.org). This document becomes the authoritative reference for how the project decomposes into modules — the thing to consult when filing a new feature and it's unclear which `specs/<module>/` it belongs to.

Two tiers exist. The user picks explicitly; never infer or guess the tier from project signals.

- **Lightweight** — three sections, one file: `docs/architecture/project-definition.md`.
- **Full** — all twelve arc42 sections, one file per section: `docs/architecture/NN-section-name.md`.

The document is a living artifact. Running this skill again on a project that already has `docs/architecture/` updates it, not replaces it from scratch.

## Process

### Step 1: Check for an existing document

Look for `docs/architecture/`. If it already exists, ask the user whether they want to update specific sections or leave existing sections alone and only fill gaps. If it doesn't exist, proceed to Step 2.

### Step 2: Ask which tier

Ask directly: "Full arc42 (all 12 sections) or the lightweight version (Goals, Constraints, Building Block View)?" Do not recommend one over the other based on project size or any other inferred signal — this is the user's call every time.

### Step 3: Work through the section list for the chosen tier

**Lightweight section list** (write to `docs/architecture/project-definition.md`, in this order):
1. Introduction and Goals
2. Constraints
3. Building Block View

**Full section list** (write each to its own `docs/architecture/NN-section-name.md`):
1. Introduction and Goals
2. Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architecture Decisions
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

For each section, use its designated source strategy below. Never skip straight to writing a section without following its strategy first.

### Step 4: Per-section source strategy

Each section falls into one of three strategies:

**Codebase-first** (explore, then confirm with the user):
- **Building Block View** — explore the actual directory/package structure. Draft a description of each major module and its responsibility. Present the draft to the user and ask them to correct anything wrong before writing the file.
- **Runtime View** — trace the actual call/data flow for the project's 2-3 most important scenarios by reading the code. Draft the flow, confirm with the user.
- **Deployment View** — inspect actual deployment config, infra-as-code, or CI/CD files if present. Draft the deployment topology, confirm with the user.

**Codebase-adjacent** (draw from project artifacts other than source code, then confirm):
- **Architecture Decisions** — read every `specs/<module>/<feature>/decisions.md` file that exists. Draft a project-level summary of the decisions that affect overall architecture (not every per-feature decision — only the ones with project-wide consequence). Ask the user which additional project-level decisions belong here that aren't captured in any feature's `decisions.md`.

**Mixed** (explore for a draft, then interview for what exploration can't answer):
- **Constraints** — note any technical constraints already evident in the codebase (language, framework, deployment target already chosen). Then ask the user directly about business, regulatory, or organizational constraints exploration can't surface.
- **Context and Scope** — note external systems/APIs the code actually integrates with. Then ask the user to confirm scope boundaries — what's explicitly out of scope.
- **Crosscutting Concepts** — note patterns actually used across the codebase (shared middleware, common error handling, logging conventions). Then ask the user about the rationale and any crosscutting intentions not yet implemented.
- **Risks and Technical Debt** — note code-level signals (TODOs, deprecated dependencies, missing tests) as candidate risks. Then ask the user to confirm severity and add non-code risks (staffing, timeline, external dependencies).
- **Glossary** — extract candidate domain terms from code naming (class names, key identifiers, module names). Then ask the user to confirm or correct each definition.

**Interview-only** (exploration can't meaningfully answer these):
- **Introduction and Goals** — ask what this project tries to achieve, for whom, and why it matters.
- **Solution Strategy** — ask about the major architectural bets and the reasoning behind them.
- **Quality Requirements** — ask about performance targets, security requirements, and other quality priorities.

### Step 5: Write the file(s)

Lightweight: append each section to `docs/architecture/project-definition.md` under its own heading, in the order listed in Step 3.

Full: write each section to its own `docs/architecture/NN-section-name.md`, using the two-digit number and a slugified section name (for example, `05-building-block-view.md`).

### Step 6: Updating an existing document

When Step 1 finds an existing document:
- If the user asked to update specific sections, re-run Steps 4-5 for only those sections.
- Before overwriting any section a user has hand-edited since it was last generated, show the proposed new content and ask for confirmation. Never silently replace hand-edited content.
- If the user asked to fill gaps only, skip any section that already has content, and run Steps 4-5 only for missing sections.
