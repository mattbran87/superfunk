# Dangling Doc References and Convention Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close D2/D3 (dangling references to `pattern-template.md`, `ai-code-guidelines.md`, `code-standards.md`) by inlining the pattern structure and guarding the three unguarded doc-read sites, and close D8 (no session ever offers to create a `CLAUDE.md`) by having brainstorming offer to scaffold starter conventions docs.

**Architecture:** Four independent, additive edits to four existing skill files. No code, no tests in the software sense — every task verifies via direct read-back or `grep`, plus three disposable `--plugin-dir` trials for the end-to-end behavioral claims.

**Tech Stack:** Markdown, `grep`, disposable trials.

## Global Constraints

- Every edit must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criteria 1–3).
- `docs/patterns/pattern-template.md` must no longer exist in this repo after Task 1 (per spec Falsifiable Criterion 1).
- `docs/code-standards.md` stays out of the bootstrap offer's scope — only `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` and `docs/ai-code-guidelines.md` get scaffolded (per spec Decision).
- No file outside `plugin/skills/subagent-driven-development/SKILL.md`, `plugin/skills/subagent-driven-development/implementer-prompt.md`, `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`, `plugin/skills/brainstorming/SKILL.md`, and `docs/patterns/pattern-template.md` (deleted) gets touched.

---

## File Structure

Directories touched: `plugin/skills/subagent-driven-development/`, `plugin/skills/brainstorming/`, `docs/patterns/`. Checked the first two for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`). `docs/patterns/` has no `.context.md` either (checked directly).

This plan creates no new files — every edit modifies an existing file, and one file (`docs/patterns/pattern-template.md`) gets deleted — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/subagent-driven-development/SKILL.md` — inline the pattern-template structure into the Finish-step Lessons-learned paragraph
- `plugin/skills/subagent-driven-development/implementer-prompt.md` — guard the conventions-reading instruction
- `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — guard the Project Conventions checklist
- `plugin/skills/brainstorming/SKILL.md` — guard the spec-review bullet, and add the new convention-bootstrap bullet

**File to delete:**
- `docs/patterns/pattern-template.md` — superseded by the inlined instruction; nothing references this path anymore once Task 1 lands

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds or modifies Markdown prose.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Inline the pattern-template structure, delete the old template file

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`
- Delete: `docs/patterns/pattern-template.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the self-contained pattern-promotion instruction every future Finish step (in this repo and every downstream project) follows. Task 4's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm the current pattern-promotion sentence's exact text**

Run: `grep -n "docs/patterns/pattern-template.md" plugin/skills/subagent-driven-development/SKILL.md`
Expected: one match, at line 601 (confirmed via direct read this session).

- [ ] **Step 2: Inline the section structure**

Change:
```markdown
question yes, or when the same failure mode recurs a second time —
whichever comes first. On promotion, write `docs/patterns/<slug>.md`
from `docs/patterns/pattern-template.md`, and add `*Pattern promoted
— see docs/patterns/<slug>.md*` after the entry. Otherwise add `*No
```
To:
```markdown
question yes, or when the same failure mode recurs a second time —
whichever comes first. On promotion, write `docs/patterns/<slug>.md`
with this structure: a `# <Pattern Name>` title and one-line
description, then `## Context` (what situation makes this pattern
apply), `## Pattern` (the rule itself, as an imperative instruction),
`## Example` (one or more worked examples), and `## Originating
lessons` (one bullet per lesson: `- "<title>" (<spec-slug>)`). Add
`*Pattern promoted — see docs/patterns/<slug>.md*` after the entry.
Otherwise add `*No
```

- [ ] **Step 3: Delete the now-unreferenced template file**

Run: `rm docs/patterns/pattern-template.md`

- [ ] **Step 4: Verify the change landed and nothing else references the deleted file**

Run: `grep -c "docs/patterns/pattern-template.md" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `0`

Run: `grep -rc "pattern-template.md" plugin/ --include="*.md" | grep -v ":0"`
Expected: no output (exit 1) — every file under `plugin/` has zero references. Scoped to `plugin/` only, not the whole repo: historical specs, plans, and `notes.md` entries legitimately still mention `pattern-template.md` as a record of what happened, the same "don't rewrite history" precedent this project already applies elsewhere — a repo-wide check would incorrectly expect those to disappear too.

Run: `ls docs/patterns/pattern-template.md`
Expected: `No such file or directory` (the file no longer exists)

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git rm docs/patterns/pattern-template.md
git commit -m "fix(skills): inline pattern-template structure into subagent-driven-development's Finish step"
```

---

### Task 2: Guard the three unguarded doc-read sites

**Files:**
- Modify: `plugin/skills/subagent-driven-development/implementer-prompt.md`
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 1 (three independent files).
- Produces: the three guarded instructions every future implementer subagent, task reviewer, and brainstorming spec-review pass follows. Task 4's verification depends on this task's exact wording.

- [ ] **Step 1: Guard implementer-prompt.md's conventions-reading instruction**

Change:
```markdown
    Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md`
    before you begin — together they hold this project's code
    conventions (naming, control flow, dead code, side effects,
    comments, tests), which apply as you write, and file/commit
    conventions (file naming, git message format), which apply when
    you commit.
```
To:
```markdown
    Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md`
    before you begin, if they exist — together they hold this
    project's code conventions (naming, control flow, dead code, side
    effects, comments, tests), which apply as you write, and
    file/commit conventions (file naming, git message format), which
    apply when you commit. Either file missing: skip reading it and
    follow the category list above as general best practice instead.
```

- [ ] **Step 2: Guard task-reviewer-prompt.md's Project Conventions checklist**

Change:
```markdown
    **Project conventions:**
    - Read `docs/ai-code-guidelines.md` and check whether the diff
      follows it — in particular: naming, explicit-over-implicit, flat
      control flow, dead code, side-effect isolation, why-comments,
      hazard signal words, signal clarity, behavioral test naming.
    - Read `docs/code-standards.md` and check whether the diff and its
      commit messages follow it — in particular: file naming, commit
      message format, and the severity-trailer rule for risky changes.
    - A violation is a Code Quality finding like any other, cited by
      file:line.
```
To:
```markdown
    **Project conventions:**
    - Read `docs/ai-code-guidelines.md`, if it exists, and check
      whether the diff follows it — in particular: naming,
      explicit-over-implicit, flat control flow, dead code,
      side-effect isolation, why-comments, hazard signal words, signal
      clarity, behavioral test naming. File missing: skip this check —
      the categories above still apply as general best practice, but
      cite specific evidence only from a document you actually read.
    - Read `docs/code-standards.md`, if it exists, and check whether
      the diff and its commit messages follow it — in particular: file
      naming, commit message format, and the severity-trailer rule for
      risky changes. File missing: skip this check, for the same
      reason.
    - A violation is a Code Quality finding like any other, cited by
      file:line.
```

- [ ] **Step 3: Guard brainstorming's spec-review bullet**

Change:
```markdown
- Check the written spec against `docs/code-standards.md`'s Spec File Conventions section before committing — self-contained (readable without external context beyond `CLAUDE.md`), testable acceptance criteria (observable and binary for Falsifiable Criteria, or quoted evidence from disposable scratch trials for a Testing section). That section's Status-line and template rules target feature-tracking's `spec.md`, not this design-spec system — the next bullet's `Status` vocabulary governs here instead.
```
To:
```markdown
- Check the written spec against `docs/code-standards.md`'s Spec File Conventions section before committing, if that file exists — self-contained (readable without external context beyond `CLAUDE.md`), testable acceptance criteria (observable and binary for Falsifiable Criteria, or quoted evidence from disposable scratch trials for a Testing section). That section's Status-line and template rules target feature-tracking's `spec.md`, not this design-spec system — the next bullet's `Status` vocabulary governs here instead. No `docs/code-standards.md` yet: apply the two named criteria directly, without the file.
```

- [ ] **Step 4: Verify all three guards landed**

Run: `grep -c "if they exist" plugin/skills/subagent-driven-development/implementer-prompt.md`
Expected: `1`

Run: `grep -c "if it exists" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: `2`

Run: `grep -c "No \`docs/code-standards.md\` yet" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/implementer-prompt.md plugin/skills/subagent-driven-development/task-reviewer-prompt.md plugin/skills/brainstorming/SKILL.md
git commit -m "fix(skills): guard ai-code-guidelines.md/code-standards.md reads with skip-if-absent phrasing"
```

---

### Task 3: Add the convention-bootstrap bullet to brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from Tasks 1–2 (an independent addition to the same file Task 2 also touches, but a distinct bullet — no conflict, since Task 2's edit is at line 112 and this insertion point sits at line 69–70).
- Produces: the new bootstrap-offer bullet every future brainstorming session checks. Task 4's live trials depend on this task's exact wording.

- [ ] **Step 1: Confirm the insertion point's exact current text**

Run: `grep -n "Read \`docs/lessons-learned.md\` in full" plugin/skills/brainstorming/SKILL.md`
Expected: one match, at line 69 (confirmed via direct read this session).

- [ ] **Step 2: Insert the new bullet**

Change:
```markdown
- Read `docs/lessons-learned.md` in full, and run `Glob docs/patterns/*.md`, reading any pattern file relevant to this idea's domain — both before any clarifying question. Note which patterns you read, or that none applied, when you present findings, so the check stays visible instead of silently not happening. No `docs/lessons-learned.md` yet: skip this check.
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Don't spend questions refining details of a project that needs to be decomposed first.
```
To:
```markdown
- Read `docs/lessons-learned.md` in full, and run `Glob docs/patterns/*.md`, reading any pattern file relevant to this idea's domain — both before any clarifying question. Note which patterns you read, or that none applied, when you present findings, so the check stays visible instead of silently not happening. No `docs/lessons-learned.md` yet: skip this check.
- Check for a `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` at the project
  root, and for `docs/ai-code-guidelines.md`. If either is missing,
  offer once (ask-don't-force, never blocking): "This project has no
  [instructions file for AI agents / coding conventions doc] yet.
  Want me to scaffold a starter version from a few quick questions
  before we continue?" If accepted, ask up to three questions, one at
  a time: the project's language/stack (skip if already evident from
  existing files), any coding conventions already followed informally,
  and anything future sessions should know upfront (build/test
  commands, architecture notes). Draft whichever file(s) were missing
  from the answers, commit them, then continue. If declined, or both
  files already exist, proceed without further mention.
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Don't spend questions refining details of a project that needs to be decomposed first.
```

- [ ] **Step 3: Verify the addition landed**

Run: `grep -c "scaffold a starter version from a few quick questions" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): brainstorming offers to scaffold CLAUDE.md/ai-code-guidelines.md on a fresh project"
```

---

### Task 4: Full verification sweep and live trials

**Files:**
- No files modified — this task only verifies Tasks 1–3.

**Interfaces:**
- Consumes: the finished state of every file Tasks 1–3 touched.
- Produces: pass/fail evidence for every Falsifiable Criterion in the design spec. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — pattern-template inlining**

Run: `grep -A8 "On promotion, write" plugin/skills/subagent-driven-development/SKILL.md`
Expected: text matching the Decision block's inlined structure exactly.

Run: `ls docs/patterns/pattern-template.md 2>&1`
Expected: `No such file or directory` (or the platform-equivalent message)

- [ ] **Step 2: Verify Falsifiable Criterion 2 — the three guards**

Run: `grep -A2 "Also read" plugin/skills/subagent-driven-development/implementer-prompt.md`
Expected: text matching the Decision block's guarded version exactly.

Run: `grep -A8 "Project conventions:" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: text matching the Decision block's guarded version exactly.

Run: `grep -n "No \`docs/code-standards.md\` yet" plugin/skills/brainstorming/SKILL.md`
Expected: one match, in the spec-review bullet.

- [ ] **Step 3: Verify Falsifiable Criterion 3 — the bootstrap bullet**

Run: `grep -B1 -A11 "Check for a \`CLAUDE.md\`" plugin/skills/brainstorming/SKILL.md`
Expected: text matching the Decision block's new bullet exactly, with the lessons-learned/patterns bullet immediately before it and the scope-assessment bullet immediately after.

- [ ] **Step 4: Verify Falsifiable Criterion 4 — scaffold-accepted live trial**

Set up a disposable fixture: a fresh `git init` repo with no `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` and no `docs/ai-code-guidelines.md`.

Run:
```bash
claude -p --plugin-dir <path-to-superfunk>/plugin --dangerously-skip-permissions --session-id <uuid> "I want to build a small command-line tool. Let's figure out what it should do." --add-dir <fixture-path>
```
(Run from the fixture directory.) When the session offers to scaffold conventions docs, answer the three questions with real, specific answers (a real language/stack, a real informal convention, a real note for future sessions) via `--resume <uuid>`.

Expected: both `CLAUDE.md` (or `AGENTS.md`) and `docs/ai-code-guidelines.md` get created with real content matching the templates in the design spec's Decision block — not placeholder text — and get committed, before the session continues to the actual brainstorming topic.

- [ ] **Step 5: Verify Falsifiable Criterion 5 — scaffold-declined live trial**

Repeat Step 4's fixture setup fresh. This time, decline the scaffold offer when it appears.

Expected: no `CLAUDE.md`/`AGENTS.md`/`docs/ai-code-guidelines.md` gets created, and the session proceeds directly to clarifying questions about the actual brainstorming topic with no further mention of the offer.

- [ ] **Step 6: Verify Falsifiable Criterion 6 — SDD-without-guidelines live trial**

Using either fixture from Step 4 or 5 (post-brainstorming, with an approved spec and plan in place, and confirmed no `docs/ai-code-guidelines.md`/`docs/code-standards.md` exist in the fixture), dispatch a single task through the implementer-prompt and task-reviewer-prompt templates.

Expected: the implementer proceeds without error and without attempting to read either missing file as a blocking step. The task reviewer's report contains no finding attributed to either file, and its Project Conventions section explicitly notes both files as absent rather than silently omitting the check.

- [ ] **Step 7: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers Decision ¶1 (pattern-template inlining). Task 2 covers Decision ¶2–4 (the three guards). Task 3 covers Decision ¶5 (the bootstrap bullet). Task 4 covers all six Falsifiable Criteria. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** Task 2's three guards each mirror the exact "skip if absent" phrasing this file already uses elsewhere (`brainstorming`'s own "No `docs/lessons-learned.md` yet: skip this check" for lessons-learned, concept-index's "If the index file doesn't exist yet... skip") — checked against those existing instances before finalizing the wording, not invented fresh. Task 3's new bullet matches its siblings' shape (a why-implicit action, an explicit skip condition, a visibility note) from the same "Explore project context" list.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into each task's Step 2/3 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` and `docs/patterns/verify-plan-commands-against-real-content.md` before writing this plan — every numeric claim in this plan (the `0`, `1`, `2`, `1` counts) got verified by running the actual grep against real file content before being written down. Also applied the specific lesson from this very spec's own writing: re-read the source trial report in full immediately before finalizing this plan, confirming no further corrections landed in it since the spec got approved.

**8. Cross-section mechanism consistency:** Task 1 edits the pattern-promotion mechanism described in `subagent-driven-development/SKILL.md`'s Finish section. Grepped the full file, every other top-level file in `plugin/skills/subagent-driven-development/`, and the design spec for any other description of this mechanism beyond the one paragraph being changed — found none. Task 2 and Task 3 edit three independent doc-read/bootstrap mechanisms with no shared cross-reference elsewhere in their respective files (confirmed via the same grep sweep) — no other passage needed a change. This plan traces to a design spec; the spec's own Consequences section already states why `docs/code-standards.md` stays out of the bootstrap offer's scope, which is exactly what this check confirms holds true.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — Task 1 changes what a step's instruction says, not the sequence of Finish's steps; Tasks 2–3 add independent checks to `brainstorming`'s "Explore project context" list, which has no worked-example section demonstrating it end-to-end (unlike `subagent-driven-development`'s Example Workflow). No worked example needs a currency check.

**10. Verified numeric expectations:** Every `Expected:` count in this plan was confirmed by running the actual grep against real file content before being written into this plan — not estimated. See `docs/patterns/verify-plan-commands-against-real-content.md`, applied directly here.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-pattern-template-and-convention-bootstrap.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
