# AI Code Guidelines — Design

**Date:** 2026-08-13
**Status:** Shipped

## Context

This spec covers sub-project 1 of 4 in a larger effort: adapting DO-178C-style planning-document *categories* — not certification compliance itself — into superfunk's spec-creation process, using Casita's own equivalents as real precedent. Casita's `docs/ai-code-guidelines.md`, `docs/code-standards.md`, and `docs/principles.md` map loosely onto SDP (development methodology) and PSAC (top-level plan) territory; a fourth sub-project adapts Casita's process-review cadence into a continuous-improvement mechanism, drawing on SQAP (process audits) and SCMP (problem reporting) as inspiration.

`ai-code-guidelines.md` goes first: of the three documents, it needs the fewest judgment calls, since Casita's version already reads as project- and language-agnostic advice rather than Casita-specific mechanics.

Scope decision from the broader discussion: these documents serve superfunk's own development now, and become templates other projects adopt through superfunk/Superpowers later. The distribution mechanism itself — how a project adopting superfunk actually receives this file — stays out of scope for this sub-project. No such mechanism exists yet, and building one before a second consuming project exists would speculate against an unproven need.

## Decision

- **Location:** `docs/ai-code-guidelines.md`, a `docs/` root sibling to `docs/superpowers/` — not inside it. `docs/superpowers/` stays reserved for the Workflow Validation Process's dated specs and plans, per `CLAUDE.md`; this document works as standing project reference, not a dated design artifact.
- **Content — ported essentially as-is:** File Organization, Naming, Explicit Over Implicit, Flat Control Flow, Zero Dead Code Policy, Side Effect Isolation, Retrieval-Oriented Documentation, Why Comments, Signal Clarity, and Behavioral Test Naming. All read as portable engineering + AI-generation rationale with no Casita-specific artifact names, command structures, or phase-gate language baked in.
- **Content — ported, adapted:** Per-Directory Context Files keeps its concept and `.context.md` format, with two real changes. First, the "Significant Directory" exclusion rule drops Casita's blanket "any dot-prefixed directory" exclusion — `.superfunk/` holds real, hand-authored scripts (`add_feature.py`, `rebuild_index.py`, `split_roadmap.py`) and needs a `.context.md` despite its dot prefix, so the rule now excludes version-control/generated directories by name instead of by a leading dot. Second, the Loading Model section replaces Casita's numbered-phase-prompt trigger (superfunk has none) with superfunk's actual skill chain: `brainstorming`'s context-exploration step, `writing-plans`' File Structure step, and the coordinator reading a directory's `.context.md` before folding it into a subagent's scene-setting context.
- **Content — cross-referenced, not duplicated:** Casita's "Recommendations Carry Confidence and Grounding" and "Steelman the Strongest Alternative" sections become one short pointer to `calibrating-recommendations` (invoked via `multi-lens-research`/`branching-research`), rather than restating that mechanism's behavior as a standing rule. This follows an explicit choice made during brainstorming: superfunk keeps this discipline skill-scoped, invoked when a real decision needs to weigh named alternatives, not applied to every recommendation in ordinary conversation.
- **Content — cut, not ported:** Casita's "Audit Step-Number References" and "New Mechanisms Require an Action Step" sections govern editing numbered process lists and prompt-triggered mechanisms — prompt/skill-file engineering, not code. Caught during user review after the first draft shipped both verbatim: they don't fit a document scoped to code conventions, even though both describe real gaps this session's own review process caught while editing `finishing-a-development-branch/SKILL.md` and `rebuild_index.py`. Cut rather than kept, since the document's scope — code conventions — matters more than any one section's individual relevance. Candidates for `principles.md` or `code-standards.md` if this insight earns a place there later.
- **No lineage note inside the document itself.** An early draft opened with a sentence naming Casita as the source and summarizing what got adapted — cut for the same reason as the two sections above: this spec is where that context belongs, not the reference document a contributor reads for the guidelines themselves.
- **Worked examples grounded in superfunk's own history**, not hypothetical ones: the Per-Directory Context Files section cites the `plugin/` isolation constraint from the human-in-the-loop-review-checkpoint work.

## Falsifiable Criteria

No trials ran for this sub-project — it produces a reference document, not executable behavior, so the Workflow Validation Process's Trials stage doesn't apply. The self-review before the first commit caught one issue (the dot-prefix exclusion rule, an unstated conflict between Casita's rule and `.superfunk/`'s real significance) and fixed it before shipping. User review after that commit caught two more: a scope mismatch (two sections about editing process lists and prompt-triggered mechanisms, not code, in a document scoped to code conventions) and unnecessary self-referential prose (a lineage note duplicating what this spec already covers). Both went out in a follow-up commit — self-review and user review each caught something the other missed.

## Deferred

- `docs/principles.md` and `docs/code-standards.md` — sub-projects 2 and 3, not started. The two sections cut from this document ("Audit Step-Number References," "New Mechanisms Require an Action Step") could earn a place in one of these later, once their scope exists to weigh them against.
- The continuous-improvement mechanism (SQAP/SCMP-inspired process-review cadence) — sub-project 4, not started; depends on the other three documents existing first, since it needs something concrete to audit against.
- The distribution mechanism that lets an adopting project receive this file from superfunk/Superpowers — no consuming project exists yet to design against.
