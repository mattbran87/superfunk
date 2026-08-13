# AI Code Guidelines Wiring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire explicit `docs/ai-code-guidelines.md` and `.context.md` reading into five `plugin/` fork skill files, per `docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md`, so these documents apply at the moments they're relevant instead of only existing as unread reference material.

**Architecture:** Five targeted text insertions into existing markdown skill/template files — no code, no new files. `implementer-prompt.md` and `task-reviewer-prompt.md` get a baked-in `ai-code-guidelines.md` reference (applies to every task, no per-task curation needed). `subagent-driven-development/SKILL.md`, `brainstorming/SKILL.md`, and `writing-plans/SKILL.md` get a `.context.md` reading instruction at the point each skill actually touches a directory.

**Tech Stack:** Markdown skill files, no code, no test framework. Verification is a mix of structural grep checks (confirming text landed correctly) and disposable `--plugin-dir` scratch trials (confirming an agent following the file actually does what it now says).

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/implementer-prompt.md` — adds one paragraph to the existing "Task Description" section.
- **Modify:** `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — adds one subsection to the existing "Part 2: Code Quality" section.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds one bullet to the "① Dispatch the implementer" section.
- **Modify:** `plugin/skills/brainstorming/SKILL.md` — extends the existing checklist item 1 and the "Understanding the idea" bullet, both already about exploring project context.
- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds one bullet to the "File Structure" section.

---

## Task 1: Wire `docs/ai-code-guidelines.md` into the implementer and reviewer templates

**Files:**
- Modify: `plugin/skills/subagent-driven-development/implementer-prompt.md`
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`

- [ ] **Step 1: Add the read instruction to `implementer-prompt.md`**

Find:
```
    ## Task Description

    Read your task brief first: [BRIEF_FILE]
    It contains the full task text from the plan.

    ## Context
```

Replace with:
```
    ## Task Description

    Read your task brief first: [BRIEF_FILE]
    It contains the full task text from the plan.

    Also read `docs/ai-code-guidelines.md` before writing any code — it
    holds this project's code conventions (naming, control flow, dead
    code, side effects, comments, tests) and applies to everything you
    write in this task.

    ## Context
```

- [ ] **Step 2: Add the check instruction to `task-reviewer-prompt.md`**

Find:
```
    **Structure:**
    - Does each file have one clear responsibility with a well-defined interface?
    - Are units decomposed so they can be understood and tested independently?
    - Is the implementation following the file structure from the plan?
    - Did this change create new files that are already large, or
      significantly grow existing files? (Don't flag pre-existing file
      sizes — focus on what this change contributed.)

    Your report should point at evidence: file:line references for every
```

Replace with:
```
    **Structure:**
    - Does each file have one clear responsibility with a well-defined interface?
    - Are units decomposed so they can be understood and tested independently?
    - Is the implementation following the file structure from the plan?
    - Did this change create new files that are already large, or
      significantly grow existing files? (Don't flag pre-existing file
      sizes — focus on what this change contributed.)

    **Project conventions:** Read `docs/ai-code-guidelines.md` and check
    the diff against it — naming, explicit-over-implicit, flat control
    flow, dead code, side-effect isolation, why-comments, signal
    clarity, behavioral test naming. A violation is a Code Quality
    finding like any other, cited by file:line.

    Your report should point at evidence: file:line references for every
```

- [ ] **Step 3: Verify both edits landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "ai-code-guidelines.md" plugin/skills/subagent-driven-development/implementer-prompt.md plugin/skills/subagent-driven-development/task-reviewer-prompt.md
```

Expected: one match in each file, each inside the new paragraph/subsection shown above (not inside an unrelated line).

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/implementer-prompt.md plugin/skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat: wire docs/ai-code-guidelines.md into implementer and reviewer templates

The implementer template now tells every dispatched subagent to read
docs/ai-code-guidelines.md before writing code. The task-reviewer
template now checks the diff against it explicitly, as a Code Quality
finding category with the template's existing file:line evidence
convention.

Part of docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md."
```

---

## Task 2: Wire `.context.md` into the subagent-driven-development dispatch flow

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Add the directory-context bullet**

Find:
```
- **Task brief:** before dispatching an implementer, run this skill's
  `scripts/task-brief PLAN_FILE N` — it extracts the task's full text to a
  uniquely named file and prints the path. Compose the dispatch so the
  brief stays the single source of
  requirements. Your dispatch should contain: (1) one line on where this
  task fits in the project; (2) the brief path, introduced as "read this
  first — it is your requirements, with the exact values to use verbatim";
  (3) interfaces and decisions from earlier tasks that the brief cannot
  know; (4) your resolution of any ambiguity you noticed in the brief;
  (5) the report-file path and report contract. Exact values (numbers,
  magic strings, signatures, test cases) appear only in the brief. Never
  make a subagent read the whole plan file.
- **Report file:** name the implementer's report file after the brief
```

Replace with:
```
- **Task brief:** before dispatching an implementer, run this skill's
  `scripts/task-brief PLAN_FILE N` — it extracts the task's full text to a
  uniquely named file and prints the path. Compose the dispatch so the
  brief stays the single source of
  requirements. Your dispatch should contain: (1) one line on where this
  task fits in the project; (2) the brief path, introduced as "read this
  first — it is your requirements, with the exact values to use verbatim";
  (3) interfaces and decisions from earlier tasks that the brief cannot
  know; (4) your resolution of any ambiguity you noticed in the brief;
  (5) the report-file path and report contract. Exact values (numbers,
  magic strings, signatures, test cases) appear only in the brief. Never
  make a subagent read the whole plan file.
- **Directory context:** before dispatching, read the `.context.md` for
  every directory this task touches (per `docs/ai-code-guidelines.md`'s
  Per-Directory Context Files section). Fold a short summary of each
  into the dispatch's Context section — the implementer never reads
  `.context.md` itself, it gets curated context, not raw file access to
  figure out on its own. Skip silently for a directory that has none.
- **Report file:** name the implementer's report file after the brief
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Directory context" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match, on the new bullet's opening line.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: wire .context.md reading into the implementer dispatch step

Adds a Directory context bullet to Dispatch the implementer: read
each touched directory's .context.md before dispatching, and fold a
summary into the dispatch's Context section. Coordinator-curated,
since which directories apply varies per task -- unlike
ai-code-guidelines.md, which applies to every task the same way.

Part of docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md."
```

---

## Task 3: Wire `.context.md` into brainstorming and writing-plans

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Update the brainstorming checklist item**

Find:
```
1. **Explore project context** — check files, docs, recent commits
```

Replace with:
```
1. **Explore project context** — check files, docs, recent commits, and `.context.md` for any directory the idea touches
```

- [ ] **Step 2: Update the brainstorming "Understanding the idea" bullet**

Find:
```
**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
```

Replace with:
```
**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits). Read the `.context.md` for any directory you examine, if one exists — it holds the directory's purpose, key decisions, and watch-outs (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section).
```

- [ ] **Step 3: Update writing-plans' File Structure section**

Find:
```
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.
```

Replace with:
```
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.
- Read the `.context.md` for each directory before mapping its role in the plan, if one exists — it holds the directory's purpose, key decisions, and watch-outs (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section).

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.
```

- [ ] **Step 4: Verify all three edits landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "\.context\.md" plugin/skills/brainstorming/SKILL.md plugin/skills/writing-plans/SKILL.md
```

Expected: two matches in `brainstorming/SKILL.md` (checklist item 1, and the "Understanding the idea" bullet), one match in `writing-plans/SKILL.md` (the new File Structure bullet).

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md plugin/skills/writing-plans/SKILL.md
git commit -m "feat: wire .context.md reading into brainstorming and writing-plans

Both skills already had a context-exploration step (brainstorming's
project-context check, writing-plans' File Structure mapping) -- both
now explicitly read .context.md for any directory they touch there,
per docs/ai-code-guidelines.md's Per-Directory Context Files section.

Part of docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md."
```

---

## Task 4: Verify `.context.md` reading with a live trial (brainstorming)

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a real `.context.md`**

```bash
mkdir -p /c/sf-context-md-test/src/payments
cd /c/sf-context-md-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-context-md-test/src/payments/.context.md <<'EOF'
# payments

**Purpose:** Handles payment capture and refund logic.

## Key Design Decisions

- Refunds always go through the original payment method -- no store credit fallback, per a compliance requirement from the payment processor's terms of service.

## What to Be Careful About

- Never log full card numbers, even in debug output -- PCI scope violation.
EOF
mkdir -p /c/sf-context-md-test/docs
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\docs\ai-code-guidelines.md" /c/sf-context-md-test/docs/
git add -A
git commit -q -m "initial scratch fixture"
```

- [ ] **Step 2: Run an isolated trial with forced literal narration**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-context-md-test. Use the brainstorming skill to explore an idea: adding refund-amount validation to src/payments/. As you execute the 'Explore project context' step, format your response as exactly 2 numbered sections with literal headers: SECTION 1/2: List every file you read during context exploration, one per line, with its full path. SECTION 2/2: If you read src/payments/.context.md, quote its 'What to Be Careful About' content verbatim as your first line in this section, then state in one sentence how it will affect your approach to refund-amount validation. If you did NOT read that file, state that explicitly instead of quoting it. Stop after SECTION 2/2 -- do not ask clarifying questions, do not propose a design, this trial only tests the context-exploration step." > /c/sf-context-md-test/trial.txt 2>&1
cat /c/sf-context-md-test/trial.txt
```

- [ ] **Step 3: Verify the trial shows genuine reading, not a fabricated quote**

Read `/c/sf-context-md-test/trial.txt`. Confirm:
1. `src/payments/.context.md` appears in the SECTION 1/2 file list.
2. SECTION 2/2 quotes the actual PCI/card-number sentence from the fixture (not a paraphrase, not a different sentence) — this is the check that catches a model claiming it read the file without actually doing so.
3. The one-sentence application to refund-amount validation makes sense given that quoted content (e.g., mentions not logging sensitive data during validation).

If the quote doesn't match the fixture's actual text, or Section 1/2 doesn't list the file, treat this as DONE_WITH_CONCERNS — the wiring may need stronger wording, not just a passed check.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-context-md-test
```

No commit for this task — it verifies Task 3's `brainstorming` edit (and, by the same pattern, `writing-plans`' identical-shape edit) and touches no repository files.

---

## Task 5: Verify `ai-code-guidelines.md` and `.context.md` together with a live trial (subagent-driven-development dispatch)

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a plan, a `.context.md`, and `ai-code-guidelines.md`**

```bash
mkdir -p /c/sf-sdd-wiring-test/src/utils
cd /c/sf-sdd-wiring-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
mkdir -p /c/sf-sdd-wiring-test/docs
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\docs\ai-code-guidelines.md" /c/sf-sdd-wiring-test/docs/
cat > /c/sf-sdd-wiring-test/src/utils/.context.md <<'EOF'
# utils

**Purpose:** Small, dependency-free helper functions shared across the project.

## Key Design Decisions

- No function here may import from any other project module -- utils must stay a leaf dependency, importable from anywhere without cycles.

## What to Be Careful About

- Do not add a "misc" grab-bag function here. If a helper doesn't fit an existing file's theme, it needs its own file, not a spot in utils.
EOF
mkdir -p /c/sf-sdd-wiring-test/docs/superpowers/plans
cat > /c/sf-sdd-wiring-test/docs/superpowers/plans/2026-01-01-test-plan.md <<'EOF'
# Test Plan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a trivial string-formatting helper to src/utils/.

**Architecture:** One new pure function, no dependencies.

**Tech Stack:** Python.

## Global Constraints

None.

---

## Task 1: Add a title-case helper

**Files:**
- Create: `src/utils/format_helpers.py`

- [ ] **Step 1: Write the function**

```python
def title_case(text: str) -> str:
    return text.title()
```

- [ ] **Step 2: Commit**

```bash
git add src/utils/format_helpers.py
git commit -m "feat: add title_case helper"
```
EOF
git add -A
git commit -q -m "initial scratch fixture"
```

- [ ] **Step 2: Run an isolated trial that composes but does not send the dispatch**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-sdd-wiring-test. Use the subagent-driven-development skill against docs/superpowers/plans/2026-01-01-test-plan.md. Follow the skill's Setup and 'Dispatch the implementer' steps to compose the full Task 1 implementer dispatch prompt exactly as you would pass it to the Agent tool -- but do NOT actually call the Agent tool or dispatch anything. Instead, print the complete composed dispatch prompt text verbatim, wrapped between the literal markers ===DISPATCH START=== and ===DISPATCH END===. Before printing it, state in one sentence whether you read src/utils/.context.md while preparing this dispatch, and if so, quote its 'What to Be Careful About' line verbatim. Stop after printing the dispatch -- do not proceed further into the skill." > /c/sf-sdd-wiring-test/trial.txt 2>&1
cat /c/sf-sdd-wiring-test/trial.txt
```

- [ ] **Step 3: Verify both wired instructions actually reached the composed dispatch**

Read `/c/sf-sdd-wiring-test/trial.txt`. Confirm:
1. The pre-dispatch statement quotes the actual "misc grab-bag" sentence from `src/utils/.context.md` verbatim (not paraphrased, not fabricated) — proves Task 2's wiring fired.
2. The text between `===DISPATCH START===` and `===DISPATCH END===` contains an instruction telling the implementer to read `docs/ai-code-guidelines.md` before writing code — proves Task 1's `implementer-prompt.md` edit reached an actual composed dispatch, not just the template file in isolation.
3. The composed dispatch's Context section reflects something derived from the `.context.md` content (e.g., mentions the no-cross-module-imports rule or the no-grab-bag-functions rule) — proves the coordinator folded a summary in, not just confirmed reading it.

If any of the three is missing or looks fabricated (e.g., a quote that doesn't match the fixture), treat this as DONE_WITH_CONCERNS and report exactly which check failed — do not report success without the evidence quoted above.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-sdd-wiring-test
```

No commit for this task — it verifies Tasks 1 and 2 working together in the real dispatch-composition flow, and touches no repository files.
