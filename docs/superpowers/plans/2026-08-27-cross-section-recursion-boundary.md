# Cross-Section Recursion Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `(top-level files only, not subdirectories)` clarification to the sibling-directory clause in both item 8 and the carve-out, per `docs/superpowers/specs/2026-08-27-cross-section-recursion-boundary-design.md`.

**Architecture:** One identical parenthetical inserted into both already-shipped clauses — a wording clarification, not a behavior change.

**Tech Stack:** Markdown skill/prompt files, no code, no test framework. Verification is two direct read-throughs; no live trial, since behavior doesn't change.

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — clarifies item 8's sibling-directory clause.
- **Modify:** `plugin/skills/subagent-driven-development/re-review-prompt.md` — clarifies the carve-out's sibling-directory clause identically.

No other file in either skill's directory restates either clause — confirmed by grep in the prior `cross-section-sibling-scope` plan and still true, since neither file changed since.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill/prompt files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Clarify item 8's sibling-directory clause as non-recursive

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert the parenthetical**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
the same target file, every other file in the same
`plugin/skills/<name>/` directory if the target file lives in one,
and the design spec, if it also describes this mechanism — for every
other mention of the key terms involved, and read each hit. Confirm
the edit doesn't leave any of them contradicting the new content.
```

Replace with:
```
the same target file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the target file lives in one, and the design spec,
if it also describes this mechanism — for every other mention of the
key terms involved, and read each hit. Confirm the edit doesn't leave
any of them contradicting the new content.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "top-level files only, not" plugin/skills/writing-plans/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "docs(skills): clarify item 8's sibling-directory clause as non-recursive

Four skill directories currently have a subdirectory, none holding
mechanism prose today; a naive recursive grep also risks false
positives on unrelated code (e.g. a variable literally named
LIFECYCLE_CHECK_MS). Wording-only clarification, no behavior change.

Part of docs/superpowers/specs/2026-08-27-cross-section-recursion-boundary-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Clarify the carve-out's sibling-directory clause identically

**Files:**
- Modify: `plugin/skills/subagent-driven-development/re-review-prompt.md`

- [ ] **Step 1: Insert the parenthetical**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking. This section sits inside the prompt template's outer fence (a `` ``` `` code block) — your Find/Replace targets only the prose lines shown below, not the fence markers themselves.

Find:
```
    diff: grep the rest of the touched file, every other file in the
    same `plugin/skills/<name>/` directory if the touched file lives in
    one, and the design spec, if the plan's Goal line or a task's
    commit trailer names one — for every other mention of the same key
    terms, and read each hit. A contradiction there is New Breakage,
    not an Out-of-Scope Observation, since the fix itself caused it
```

Replace with:
```
    diff: grep the rest of the touched file, every other file in the
    same `plugin/skills/<name>/` directory (top-level files only, not
    subdirectories) if the touched file lives in one, and the design
    spec, if the plan's Goal line or a task's commit trailer names one
    — for every other mention of the same key terms, and read each
    hit. A contradiction there is New Breakage, not an Out-of-Scope
    Observation, since the fix itself caused it
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "top-level files only, not" plugin/skills/subagent-driven-development/re-review-prompt.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/re-review-prompt.md
git commit -m "docs(skills): clarify the carve-out's sibling-directory clause as non-recursive

Preserves the deliberate parity with item 8 (same clause, identically
worded).

Part of docs/superpowers/specs/2026-08-27-cross-section-recursion-boundary-design.md."
```

Stage only this one file.
