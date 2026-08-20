# Lessons and Patterns Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Casita's Lessons and Patterns mechanism — capture at `subagent-driven-development`'s Finish step, consumption at `brainstorming`'s Understanding-the-idea step, plus the deferred "Lessons vs. Patterns" section in `docs/code-standards.md` — per `docs/superpowers/specs/2026-08-20-lessons-and-patterns-design.md`.

**Architecture:** Two new seed artifacts (`docs/lessons-learned.md`, `docs/patterns/pattern-template.md`), one new `docs/code-standards.md` section, and edits to two existing fork skill files (`subagent-driven-development/SKILL.md`'s Finish step, `brainstorming/SKILL.md`'s Understanding-the-idea step).

**Tech Stack:** Markdown skill files and markdown artifacts, no code, no test framework. Verification is grep checks plus two disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Create:** `docs/lessons-learned.md` — the running Lesson log.
- **Create:** `docs/patterns/pattern-template.md` — the Pattern file template.
- **Modify:** `docs/code-standards.md` — adds the "Lessons vs. Patterns" section.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds Lesson capture to the Finish step.
- **Modify:** `plugin/skills/brainstorming/SKILL.md` — adds Lesson/Pattern reading to Understanding the idea.

---

## Task 1: Seed the lessons-learned and pattern-template artifacts

**Files:**
- Create: `docs/lessons-learned.md`
- Create: `docs/patterns/pattern-template.md`

- [ ] **Step 1: Write the running Lesson log**

```markdown
# Lessons Learned

Accumulated knowledge from completed plans. Captured at
`subagent-driven-development`'s Finish step for notable learnings —
specific enough to act on in a future session. Entries live under an
H2 category heading; the first Lesson on a new topic creates its own
heading.
```

Save to `docs/lessons-learned.md`.

- [ ] **Step 2: Write the pattern template**

```markdown
# <Pattern Name>

<One-line description of the reusable rule.>

## Context

<What situation makes this pattern apply.>

## Pattern

<The rule itself, stated as an imperative instruction.>

## Example

<One or more worked examples showing the rule applied.>

## Originating lessons

- "<Lesson title>" (<spec-slug>)
```

Save to `docs/patterns/pattern-template.md`.

- [ ] **Step 3: Verify both files exist with the right content**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Accumulated knowledge from completed plans" docs/lessons-learned.md
grep -n "^## Originating lessons" docs/patterns/pattern-template.md
```

Expected: one match each.

- [ ] **Step 4: Commit**

```bash
git add docs/lessons-learned.md docs/patterns/pattern-template.md
git commit -m "feat: seed the lessons-learned log and pattern template

Empty starting state for both artifacts -- lessons-learned.md
accumulates entries as subagent-driven-development's Finish step
captures them, pattern-template.md defines the structure a promoted
Lesson becomes.

Part of docs/superpowers/specs/2026-08-20-lessons-and-patterns-design.md."
```

Stage only these two files — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Add the Lessons vs. Patterns section to code-standards.md

**Files:**
- Modify: `docs/code-standards.md`

- [ ] **Step 1: Insert the new section after Spec File Conventions**

Find:
```
- `[Preference]` `spec.md`'s `Status:` line stays current: `Planned` → `In Progress` → `Done` (or `Deferred`/`Dropped`)

---

## CLAUDE.md Maintenance
```

Replace with:
```
- `[Preference]` `spec.md`'s `Status:` line stays current: `Planned` → `In Progress` → `Done` (or `Deferred`/`Dropped`)

---

## Lessons vs. Patterns

Two related but distinct artifacts capture what the project learns from real work.

- `[Rule]` A Lesson answers *what happened and what to watch out for* — one retrospective fact, tied to the plan that surfaced it. Lives in `docs/lessons-learned.md`.
- `[Rule]` A Pattern answers *what future work should do* — a prospective, reusable rule that applies across many future situations. Lives in `docs/patterns/` as its own file.
- `[Preference]` Secondary test when the distinction feels unclear: one specific fact tied to one context makes a Lesson; a rule that applies broadly makes a Pattern.
- `[Rule]` A Lesson gets captured at `subagent-driven-development`'s Finish step; "nothing notable" counts as a complete answer.
- `[Rule]` A Lesson promotes to a Pattern when it expresses a prospective rule, or when the same failure mode recurs a second time — whichever comes first.

---

## CLAUDE.md Maintenance
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^## Lessons vs. Patterns" docs/code-standards.md
grep -n "one specific fact tied to one context" docs/code-standards.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/code-standards.md
git commit -m "feat: add the Lessons vs. Patterns section to code-standards.md

Ports Casita's Lesson (retrospective) vs. Pattern (prospective)
distinction, deferred here since the docs/code-standards.md
sub-project. States the capture and promotion rules that
subagent-driven-development's Finish step now implements.

Part of docs/superpowers/specs/2026-08-20-lessons-and-patterns-design.md."
```

Stage only this one file.

---

## Task 3: Wire Lesson capture into subagent-driven-development's Finish step

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Add the capture step**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking, since the file has been edited multiple times this session. If it doesn't match exactly, locate the equivalent paragraph by content/context and adapt precisely, preserving the instruction's intent.

Find:
```
If you updated a spec's Status to `Shipped`, also append its filename
to `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped
since" list, and commit that change in the same commit. If the list
now holds 3 or more filenames, offer to run superpowers:process-review
right now — the same ask-don't-force pattern as any other checkpoint
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.

Then delete this plan's workspace
```

Replace with:
```
If you updated a spec's Status to `Shipped`, also append its filename
to `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped
since" list, and commit that change in the same commit. If the list
now holds 3 or more filenames, offer to run superpowers:process-review
right now — the same ask-don't-force pattern as any other checkpoint
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.

Capture a notable learning in `docs/lessons-learned.md`, or record
that nothing notable arose — either answer completes this step. A
new Lesson entry: `### <title> (<spec-slug>)` as an H3 heading under
the nearest-fitting H2 category (create one if none fits), a prose
paragraph ending in a **Rule:** sentence, then a promotion note. Ask:
"Does this Lesson express a prospective rule that applies across many
future situations?" A second instance of the same failure mode
justifies promoting even when that question reads ambiguous. On
promotion, write `docs/patterns/<slug>.md` from
`docs/patterns/pattern-template.md`, and add `*Pattern promoted — see
docs/patterns/<slug>.md*` after the entry. Otherwise add `*No pattern
promoted — <one-line reason>.*` after the entry. Commit both the
Lesson (and, if written, the Pattern) in the same commit as the
tracker update above, or their own commit if the tracker didn't
change.

Then delete this plan's workspace
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Capture a notable learning" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Pattern promoted — see" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: capture a notable learning at the Finish step

Adds Lesson capture (or an explicit nothing-notable answer) after
the existing Status/tracker steps, plus the promotion question and
tiebreaker that turns a recurring Lesson into a Pattern file.

Part of docs/superpowers/specs/2026-08-20-lessons-and-patterns-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .`.

---

## Task 4: Wire Lesson/Pattern reading into brainstorming's Understanding the idea

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Add the reading bullet**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
- Check `docs/superpowers/process-reviews/tracker.md`, if it exists, for two independent conditions: a review due (3+ specs shipped since the last review, never run), or an open Recommendation in the last review file (an unchecked `- [ ]` item in `docs/superpowers/process-reviews/review-after-*.md`). Surface both, if either applies. Ask your human partner to act on each, or explicitly defer it, before continuing to clarifying questions. A deferred Recommendation gets a `(deferred: <reason>)` note beside the item in the review file. A deferred review-due check gets its note in the tracker instead, since it has no per-item home. No tracker file yet: skip this check.
- Before asking detailed questions, assess scope:
```

Replace with:
```
- Check `docs/superpowers/process-reviews/tracker.md`, if it exists, for two independent conditions: a review due (3+ specs shipped since the last review, never run), or an open Recommendation in the last review file (an unchecked `- [ ]` item in `docs/superpowers/process-reviews/review-after-*.md`). Surface both, if either applies. Ask your human partner to act on each, or explicitly defer it, before continuing to clarifying questions. A deferred Recommendation gets a `(deferred: <reason>)` note beside the item in the review file. A deferred review-due check gets its note in the tracker instead, since it has no per-item home. No tracker file yet: skip this check.
- Read `docs/lessons-learned.md` in full, and run `Glob docs/patterns/*.md`, reading any pattern file relevant to this idea's domain — both before any clarifying question. No `docs/lessons-learned.md` yet: skip this check.
- Before asking detailed questions, assess scope:
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Glob docs/patterns" plugin/skills/brainstorming/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat: read lessons-learned and patterns during Understanding the idea

Before clarifying questions begin, brainstorming now reads
docs/lessons-learned.md in full and globs docs/patterns/ for
anything relevant to the idea's domain -- matching Casita's real
Planning-time recall of accumulated knowledge.

Part of docs/superpowers/specs/2026-08-20-lessons-and-patterns-design.md."
```

Stage only this one file.

---

## Task 5: Verify Finish-step Lesson capture with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a pre-seeded lessons-learned.md holding one prior instance of a failure mode**

```bash
mkdir -p /c/sf-lessons-test/docs/patterns
cd /c/sf-lessons-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-lessons-test/docs/lessons-learned.md <<'EOF'
# Lessons Learned

Accumulated knowledge from completed plans.

## Workflow

### First implementer forgot to run the linter before committing (fake-spec-a)

The first implementer for fake-spec-a committed without running the
project's linter, and a formatting issue slipped through spec
compliance review, caught only by code quality review. **Rule:** every
implementer runs the linter before committing, not just before
marking the task done.

**Tags:** none yet — tags deferred.

*No pattern promoted — first instance of this failure mode.*
EOF
cat > /c/sf-lessons-test/docs/patterns/pattern-template.md <<'EOF'
# <Pattern Name>

<One-line description of the reusable rule.>

## Context

<What situation makes this pattern apply.>

## Pattern

<The rule itself, stated as an imperative instruction.>

## Example

<One or more worked examples showing the rule applied.>

## Originating lessons

- "<Lesson title>" (<spec-slug>)
EOF
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial that skips straight to the Finish step, reporting a second instance of the same failure mode**

```bash
cd /c/sf-lessons-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-lessons-test. Assume you are partway through following the subagent-driven-development skill: all tasks are already complete, the final whole-branch review just came back clean, and there is no design spec to trace this plan to (skip the Status/tracker steps). This plan's own implementer also forgot to run the linter before committing, on Task 2, and it was caught by code quality review -- the same failure mode already recorded in docs/lessons-learned.md for fake-spec-a. Follow the skill's Finish section now, exactly as written, starting from the Lesson-capture step. Report back in exactly 3 numbered sections with literal headers: SECTION 1/3: quote the exact new Lesson entry you wrote to docs/lessons-learned.md, read fresh from disk. SECTION 2/3: state whether you promoted a Pattern, and if so, quote the new file docs/patterns/ now contains, read fresh from disk. SECTION 3/3: quote the promotion note you added after the Lesson entry (Pattern promoted or No pattern promoted)." > /c/sf-lessons-test/trial.txt 2>&1
cat /c/sf-lessons-test/trial.txt
```

- [ ] **Step 3: Verify the Lesson entry, promotion, and tiebreaker independently**

Read `/c/sf-lessons-test/trial.txt`, and independently read the files it should have touched:

```bash
cat /c/sf-lessons-test/docs/lessons-learned.md
echo "---"
ls /c/sf-lessons-test/docs/patterns/
```

Confirm:
1. `docs/lessons-learned.md` now has a second H3 entry, correctly formatted (`### <title> (<spec-slug>)`, prose ending in a **Rule:** sentence).
2. Because this is a second instance of the same failure mode (linter not run before commit), the tiebreaker fires: a new file exists under `docs/patterns/` (not just `pattern-template.md`), following the template's structure.
3. The new Lesson entry carries a `*Pattern promoted — see docs/patterns/<slug>.md*` note, naming the actual file that exists.

If any of the three is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the files actually contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-lessons-test
```

No commit for this task.

---

## Task 6: Verify brainstorming reads lessons-learned and patterns with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a lesson and a real pattern file**

```bash
mkdir -p /c/sf-lessons-read-test/docs/patterns
cd /c/sf-lessons-read-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-lessons-read-test/docs/lessons-learned.md <<'EOF'
# Lessons Learned

Accumulated knowledge from completed plans.

## Workflow

### Always run the linter before committing (fake-spec-a, fake-spec-b)

Two implementers in a row committed without running the linter.

**Rule:** every implementer runs the linter before committing.

*Pattern promoted — see docs/patterns/run-linter-before-commit.md*
EOF
cat > /c/sf-lessons-read-test/docs/patterns/run-linter-before-commit.md <<'EOF'
# Run the linter before committing

Every implementer runs the project's linter before committing, not
just before marking a task done.

## Context

Two implementers in a row committed lint failures that only surfaced
during code quality review.

## Pattern

Before committing, run the project's linter and fix anything it
flags.

## Example

`npm run lint` (or the project's equivalent) before `git commit`,
every time.

## Originating lessons

- "Always run the linter before committing" (fake-spec-a, fake-spec-b)
EOF
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial starting a new brainstorm**

```bash
cd /c/sf-lessons-read-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-lessons-read-test. Use the brainstorming skill for this idea: add a small helper script that runs some project tasks and commits the result. Go through the skill's checklist item 1, 'Explore project context' / 'Understanding the idea,' exactly as written, including reading docs/lessons-learned.md and scanning docs/patterns/. Stop immediately after that reading and before asking any clarifying question. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote what you found when you read docs/lessons-learned.md. SECTION 2/2: state whether docs/patterns/run-linter-before-commit.md seemed relevant to this idea, and if so, quote the guidance you'd carry into the design from it." > /c/sf-lessons-read-test/trial.txt 2>&1
cat /c/sf-lessons-read-test/trial.txt
```

- [ ] **Step 3: Verify both reads happened**

Read `/c/sf-lessons-read-test/trial.txt`. Confirm:

1. SECTION 1/2 quotes real content from `docs/lessons-learned.md` — not a fabricated summary.
2. SECTION 2/2 correctly identifies `run-linter-before-commit.md` as relevant to an idea that involves committing, and carries forward its actual guidance (run the linter before committing).

If either check fails, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the trial actually output.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-lessons-read-test
```

No commit for this task — it verifies Task 4 and touches no repository files.
