# Writing-Plans Self-Review Checks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two new items to `writing-plans`'s Self-Review section — sibling-pattern parity and cross-file rule restatement — per `docs/superpowers/specs/2026-08-20-writing-plans-self-review-checks-design.md`.

**Architecture:** One Find/Replace edit to `plugin/skills/writing-plans/SKILL.md`'s existing Self-Review section, adding items 5 and 6 after the existing item 4.

**Tech Stack:** Markdown skill file, no code, no test framework. Verification is grep, matching the design spec's own Falsifiable Criteria (no disposable trial applies — this adds judgment-based checklist text, not executable behavior).

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds Self-Review items 5 and 6.

---

## Task 1: Add the two Self-Review items

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert items 5 and 6 after the existing item 4**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking, since the file has been edited multiple times this session.

Find:
```
**4. Pseudocode coverage:** Does the Pseudocode section state all four triggers (T1–T4), each either populated with real pseudocode or marked `Skipped: <reason>`? A trigger left out entirely is a plan failure, the same as a missing task for a spec requirement. For each populated trigger, confirm the pseudocode stays natural-language only — no real code, no type annotations, no library calls. For each `Skipped` trigger, confirm the reason names a real absence, not a restatement of the trigger's name.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

Replace with:
```
**4. Pseudocode coverage:** Does the Pseudocode section state all four triggers (T1–T4), each either populated with real pseudocode or marked `Skipped: <reason>`? A trigger left out entirely is a plan failure, the same as a missing task for a spec requirement. For each populated trigger, confirm the pseudocode stays natural-language only — no real code, no type annotations, no library calls. For each `Skipped` trigger, confirm the reason names a real absence, not a restatement of the trigger's name.

**5. Sibling-pattern parity:** When a plan adds a new instruction next to an existing sibling instruction in the same target file, does it mirror that sibling's established shape (a why-explanation, a visibility clause)? If not, add what's missing.

**6. Cross-file rule restatement:** Does this plan restate the same source rule in more than one target file? If so, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^\*\*5. Sibling-pattern parity" plugin/skills/writing-plans/SKILL.md
grep -n "^\*\*6. Cross-file rule restatement" plugin/skills/writing-plans/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat: add sibling-pattern-parity and cross-file-restatement Self-Review checks

Acts on both open Recommendations from the first real process
review. Item 5 catches a recurring Miss (a new instruction failing
to mirror an established sibling's shape). Item 6 operationalizes
docs/patterns/cross-check-shared-rule-restatements.md as an actual
plan-writing check.

Part of docs/superpowers/specs/2026-08-20-writing-plans-self-review-checks-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).
