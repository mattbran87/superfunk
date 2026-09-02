---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents (Claude Code, Codex CLI, Codex App, Copilot CLI, and Gemini CLI all qualify; see the per-platform tool refs in `../using-superpowers/references/`). If subagents are available, use superfunk:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Ensure an isolated workspace: use superfunk:using-git-worktrees to create one or verify the existing one
2. Read plan file
3. Review critically - identify any questions or concerns about the plan
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Finish Bookkeeping

After all tasks complete and verified, and before Step 4, perform the
same bookkeeping superfunk:subagent-driven-development's Finish section
performs for dispatched plans:

1. **notes.md gate:** Verify each executed task's catches and findings
   got logged to `docs/superpowers/process-reviews/notes.md`. Append any
   missing lines now.
2. **Spec Status flip:** If this plan traces to a design spec, update
   that spec's `Status` line to `Shipped` and commit the change.
3. **Tracker append:** Append the spec filename to
   `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped since"
   list, in the same commit. At 3 or more entries, offer to run
   superfunk:process-review now — ask, don't force.
4. **Recommendation checkbox:** If the spec's Context names a
   `review-after-*.md` file, find the matching `- [ ]` line, change it
   to `- [x]`, and append `(Shipped as <what shipped>, commit <sha>.)`
   — in the same commit as items 2–3.
5. **Verify items 2–4 landed:**
   ```bash
   grep -c "^\*\*Status:\*\* Shipped" <spec-file>
   grep -c "<spec filename>" docs/superpowers/process-reviews/tracker.md
   grep -c "\[x\].*<distinctive words from the Recommendation>" <review-file>
   ```
   Each applicable check returns at least 1. A 0 means that action never
   happened — do it now.
6. **Lessons capture:** Capture a notable learning in
   `docs/lessons-learned.md`, or record that nothing notable arose.
   Follow the detailed lesson-and-promotion procedure in
   superfunk:subagent-driven-development's Finish section.
7. **Version bump:**
   If the branch's diff touches `plugin/`, run
   `plugin/scripts/bump-version.sh <new-version>` and commit the result —
   minor bump for `plugin/skills/` changes, patch otherwise. Unsure
   whether the bump already happened: run `--check` first.
8. **Concept index:** If this plan's File Structure created, renamed,
   moved, or deleted a skill, feature, or significant directory, update
   `docs/architecture/concept-index.md` per superfunk:concept-index
   Step 3, using the trigger conditions in
   superfunk:subagent-driven-development's Finish section.

### Step 4: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superfunk:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent
