# Checklist Construction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the general Checklist Construction rule into `docs/code-standards.md`, apply it to `writing-skills`' 27-item checklist as the proof case, and wire failure-log sourcing into `writing-plans`' Self-Review and `test-driven-development`'s Verification Checklist — per `docs/superpowers/specs/2026-08-20-checklist-construction-design.md`.

**Architecture:** One new `docs/code-standards.md` section, one restructuring edit to `writing-skills/SKILL.md`'s checklist, and two single-item additions to `writing-plans/SKILL.md` and `test-driven-development/SKILL.md`.

**Tech Stack:** Markdown skill and doc files, no code, no test framework. Verification is grep only, matching the design spec's own Falsifiable Criteria — this changes checklist structure and prose, not executable behavior a `--plugin-dir` trial can exercise.

---

## File Structure

- **Modify:** `docs/code-standards.md` — adds the "Checklist Construction" section.
- **Modify:** `plugin/skills/writing-skills/SKILL.md` — trims 2 padding items, splits GREEN into two sub-phases, changes the todo-creation instruction to per-phase, adds a top-of-section lessons-learned check.
- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds a lessons-learned check to Self-Review.
- **Modify:** `plugin/skills/test-driven-development/SKILL.md` — adds a lessons-learned check to the Verification Checklist.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill and doc files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add the Checklist Construction section to code-standards.md

**Files:**
- Modify: `docs/code-standards.md`

- [ ] **Step 1: Insert the new section after Lessons vs. Patterns**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
- `[Rule]` A Lesson promotes to a Pattern when it expresses a prospective rule that applies across many future situations, or when the same failure mode recurs a second time — whichever comes first.

---

## CLAUDE.md Maintenance
```

Replace with:
```
- `[Rule]` A Lesson promotes to a Pattern when it expresses a prospective rule that applies across many future situations, or when the same failure mode recurs a second time — whichever comes first.

---

## Checklist Construction

- `[Rule]` Choose READ-DO (a fixed sequence, run in order) or DO-CONFIRM (do the work, then pause and confirm nothing got missed) deliberately, per checklist.
- `[Rule]` A checklist item exists to catch a step people easily skip. An item that restates the obvious earns no place on the list.
- `[Rule]` Cap a single checklist at 5-9 items. Past that, split into grouped sub-checklists by phase or component, each with its own pause point.
- `[Rule]` A DO-CONFIRM checklist checks `docs/lessons-learned.md` for entries relevant to its own domain, once per run, not once per split sub-checklist.

---

## CLAUDE.md Maintenance
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^## Checklist Construction" docs/code-standards.md
grep -n "Cap a single checklist at 5-9 items" docs/code-standards.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/code-standards.md
git commit -m "feat: add the Checklist Construction section to code-standards.md

States four rules adapted from the user's Checklist Manifesto draft:
READ-DO/DO-CONFIRM selection, killer-items-only, a 5-9 item cap with
phase/component splitting, and once-per-run lessons-learned sourcing
for DO-CONFIRM checklists.

Part of docs/superpowers/specs/2026-08-20-checklist-construction-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Restructure writing-skills' Skill Creation Checklist

**Files:**
- Modify: `plugin/skills/writing-skills/SKILL.md`

- [ ] **Step 1: Trim, split, and re-sequence the checklist**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
## Skill Creation Checklist (TDD Adapted)

**IMPORTANT: Create a todo for EACH checklist item below.**

**RED Phase - Write Failing Test:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill - document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase - Write Minimal Skill:**
- [ ] Name uses only letters, numbers, hyphens (no parentheses/special chars)
- [ ] YAML frontmatter with required `name` and `description` fields (max 1024 chars; see [spec](https://agentskills.io/specification))
- [ ] Description starts with "Use when..." and includes specific triggers/symptoms
- [ ] Description written in third person
- [ ] Keywords throughout for search (errors, symptoms, tools)
- [ ] Clear overview with core principle
- [ ] Address specific baseline failures identified in RED
- [ ] Guidance form matches the failure type (see Match the Form to the Failure)
- [ ] For behavior-shaping guidance: wording micro-tested against a no-guidance control (5+ reps, every flagged match read manually) — N/A for pure reference skills
- [ ] Code inline OR link to separate file
- [ ] One excellent example (not multi-language)
- [ ] Run scenarios WITH skill - verify agents now comply

**REFACTOR Phase - Close Loopholes:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table from all test iterations
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Quality Checks:**
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference

**Deployment:**
- [ ] Commit skill to git and push to your fork (if configured)
- [ ] Consider contributing back via PR (if broadly useful)
```

Replace with:
```
## Skill Creation Checklist (TDD Adapted)

Before starting RED, check `docs/lessons-learned.md` for anything
relevant to skill-authoring, and apply anything it flags.

At the start of each phase below, create a todo only for that
phase's items. Complete the phase's work. Confirm against that
phase's list. Then move to the next phase.

**RED Phase - Write Failing Test:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill - document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase — Metadata:**
- [ ] Name uses only letters, numbers, hyphens (no parentheses/special chars)
- [ ] YAML frontmatter with required `name` and `description` fields (max 1024 chars; see [spec](https://agentskills.io/specification))
- [ ] Description starts with "Use when..." and includes specific triggers/symptoms
- [ ] Description written in third person

**GREEN Phase — Content:**
- [ ] Address specific baseline failures identified in RED
- [ ] Guidance form matches the failure type (see Match the Form to the Failure)
- [ ] For behavior-shaping guidance: wording micro-tested against a no-guidance control (5+ reps, every flagged match read manually) — N/A for pure reference skills
- [ ] Code inline OR link to separate file
- [ ] One excellent example (not multi-language)
- [ ] Run scenarios WITH skill - verify agents now comply

**REFACTOR Phase - Close Loopholes:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table from all test iterations
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Quality Checks:**
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference

**Deployment:**
- [ ] Commit skill to git and push to your fork (if configured)
- [ ] Consider contributing back via PR (if broadly useful)
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^\*\*GREEN Phase — Metadata:\*\*" plugin/skills/writing-skills/SKILL.md
grep -n "^\*\*GREEN Phase — Content:\*\*" plugin/skills/writing-skills/SKILL.md
grep -n "Keywords throughout for search" plugin/skills/writing-skills/SKILL.md
grep -n "Clear overview with core principle" plugin/skills/writing-skills/SKILL.md
grep -n "check \`docs/lessons-learned.md\` for anything" plugin/skills/writing-skills/SKILL.md
```

Expected: the first two grep for a match each; the "Keywords throughout" and "Clear overview" greps for zero matches (both removed); the lessons-learned grep for one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-skills/SKILL.md
git commit -m "feat: split GREEN phase, trim padding, add per-phase pause points

GREEN phase's 12 items included 2 that restated general good-writing
advice rather than catching a specific miss -- removed. The
remaining 10 split into GREEN Phase - Metadata (4) and GREEN Phase -
Content (6), both inside the 5-9 cap. Todos now get created per
phase, not all 27 upfront. Adds one lessons-learned check before RED
starts.

Part of docs/superpowers/specs/2026-08-20-checklist-construction-design.md."
```

Stage only this one file.

---

## Task 3: Add the lessons-learned check to writing-plans' Self-Review

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Add item 7**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**6. Cross-file rule restatement:** Does this plan restate the same source rule in more than one target file? If so, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

Replace with:
```
**6. Cross-file rule restatement:** Does this plan restate the same source rule in more than one target file? If so, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.

**7. Lessons-learned check:** Check `docs/lessons-learned.md` for any entry relevant to this plan's domain. Apply anything it flags.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^\*\*7. Lessons-learned check" plugin/skills/writing-plans/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat: add a lessons-learned check to writing-plans' Self-Review

Self-Review is a DO-CONFIRM pass, exactly the shape a failure-log
check fits per the new Checklist Construction rule. No Placeholders
stays untouched -- it's a reference list Self-Review's own scan
consults, not a run-and-confirm pass of its own.

Part of docs/superpowers/specs/2026-08-20-checklist-construction-design.md."
```

Stage only this one file.

---

## Task 4: Add the lessons-learned check to test-driven-development's Verification Checklist

**Files:**
- Modify: `plugin/skills/test-driven-development/SKILL.md`

- [ ] **Step 1: Add the new item**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.
```

Replace with:
```
## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered
- [ ] Checked `docs/lessons-learned.md` for any entry relevant to this work, and applied anything it flags

Can't check all boxes? You skipped TDD. Start over.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Checked \`docs/lessons-learned.md\`" plugin/skills/test-driven-development/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/test-driven-development/SKILL.md
git commit -m "feat: add a lessons-learned check to the Verification Checklist

The Verification Checklist is a DO-CONFIRM pass -- adds the ninth
item (still inside the 5-9 cap) per the new Checklist Construction
rule.

Part of docs/superpowers/specs/2026-08-20-checklist-construction-design.md."
```

Stage only this one file.
