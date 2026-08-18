# Human-in-the-Loop Review Checkpoint — Design

**Date:** 2026-08-11
**Status:** Shipped

## Context

A comparison against a planned Casita 2.0 phase table (`discovery`, `planning`, `design`, `construction`, `review`, `validation`, `delivery`, `deployment`, `observation`) surfaced one real gap in the Superpowers flow this project uses: `review` currently means two AI subagents (spec-compliance, then code-quality) inside `subagent-driven-development`, plus a final AI reviewer over the whole implementation. A human only reviews the work if the user happens to pick "push and create a PR" in `finishing-a-development-branch` — and even then, review happens outside the flow, on GitHub, not as a step the skill itself asks about.

This spec adds an explicit checkpoint: `finishing-a-development-branch` asks the user, once per feature, whether they want to review the completed work themselves before deciding what happens next.

## Decision

- **New step in `plugin/skills/finishing-a-development-branch/SKILL.md`**, inserted between the existing "Determine Base Branch" step and "Present Options" step. The three steps after it ("Present Options," "Execute Choice," "Cleanup Workspace") shift down by one, and their internal `(Step N)` cross-references get updated to match.
- **Scope:** once per feature, at completion — not once per task. `finishing-a-development-branch` already runs once at the end of every path (subagent-driven, inline, or manual), so this one change covers all of them uniformly.
- **The question:** "Would you like to review the changes yourself before deciding what to do next?"
- **On "no":** skip straight to the existing 4-option menu (merge locally / push and create a PR / keep as-is / discard), unchanged from today.
- **On "yes":** show `git diff --stat <base-branch>...HEAD` for a compact file list. Also point to the feature's Requirements — `spec.md`'s Requirements section when one exists for this work, otherwise the plan doc. This puts what changed next to what the work needed to do. Offer the full diff on request. Wait for explicit confirmation the changes look right before presenting the 4-option menu.
- **Additive, not a replacement:** the AI spec-compliance/code-quality review loop inside `subagent-driven-development` stays exactly as it works today. This adds one independent human checkpoint at the very end, on top of it.

## Deferred

- Remembering the user's answer across multiple `finishing-a-development-branch` runs in one session — it asks every time.
- Per-task review checkpoints — this decision covers whole-feature review only.
- Routing review through a pushed PR by default — the local `git diff --stat` path keeps this step working fully offline.

## Testing

This spec modifies existing plugin skill content, which `plugin/CLAUDE.md` treats as behavior-shaping and holds to a verification bar before it lands. The change adds a required step to an already-structured sequence. It doesn't ask an agent to resist a rule under pressure. So it needs only a baseline trial confirming the step fires correctly on both paths — not the full adversarial pressure-test battery `writing-skills` reserves for discipline skills like TDD.

Verify with a disposable `--plugin-dir` scratch session, the same isolation pattern `superpowers-fork` validated for testing fork changes without touching the live plugin:

1. A synthetic branch with a small, real diff. Run `finishing-a-development-branch` and answer "no" — confirm the 4-option menu appears immediately, matching today's behavior exactly.
2. Same setup, answer "yes" — confirm the file-stat summary and Requirements pointer appear, the full diff shows on request, and the 4-option menu waits for explicit confirmation before appearing.
