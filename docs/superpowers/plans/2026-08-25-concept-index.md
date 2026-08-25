# Concept Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a `concept-index` skill that maps every Skill, feature-tracking Feature, and significant Directory to its location and description, and wire it into `subagent-driven-development`'s Finish step (incremental maintenance) and dispatch step (consumption) — per `docs/superpowers/specs/2026-08-25-concept-index-design.md`.

**Architecture:** One new skill file (`plugin/skills/concept-index/SKILL.md`) defining the index format and both its entry points (full build, incremental maintenance), plus two wiring edits to `plugin/skills/subagent-driven-development/SKILL.md` — a new explicit Finish-step bookkeeping paragraph, and a new dispatch-context bullet alongside the existing Directory context and Pseudocode context bullets.

**Tech Stack:** Markdown skill files, no code, no test framework. Verification is direct read-throughs plus disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Create:** `plugin/skills/concept-index/SKILL.md` — the new skill: concept-unit definitions, full-build process, incremental-maintenance process.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds the Finish-step bookkeeping paragraph and the dispatch-context bullet.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Create the concept-index skill

**Files:**
- Create: `plugin/skills/concept-index/SKILL.md`

- [ ] **Step 1: Write the skill file**

```bash
mkdir -p "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\concept-index"
```

Write this exact content to `plugin/skills/concept-index/SKILL.md`:

````markdown
---
name: concept-index
description: Use when a codebase needs a fast concept-to-file lookup, especially as it grows past what directory structure alone makes navigable. Maintains docs/architecture/concept-index.md, a table mapping every skill, feature-tracking feature, and significant directory to its location and a one-line description.
---

# Concept Index

## Overview

Maintains `docs/architecture/concept-index.md`: a single git-tracked markdown table mapping three kinds of existing structural units — Skills, Features, and significant Directories — to their location and a one-line description. The index lets an agent find "where does X live" without searching, the same way a `.context.md` file gives an agent a directory's purpose without inferring it from file contents.

Two entry points exist: a full build (this skill, invoked directly, for a codebase with no index yet) and incremental maintenance (`subagent-driven-development`'s Finish step, triggered when a plan adds, renames, moves, or removes an indexed unit — see that skill's Finish section, not this one, for the trigger logic).

## Concept Units

A concept unit is one of:

- **Skill** — a directory at `plugin/skills/<name>/` containing a `SKILL.md`. Described by that file's own frontmatter `description:` field.
- **Feature** — a directory at `specs/<module>/<feature>/` (the `feature-tracking` pipeline), excluding `specs/_template/`. Described by its `spec.md`'s `#` heading and Requirements section.
- **Directory** — any directory meeting `docs/ai-code-guidelines.md`'s Per-Directory Context Files section's significant-directory threshold: "any directory with 3 or more non-generated files, or any top-level directory whose purpose is not evident from its name alone," excluding `.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`. Described by its own `.context.md`'s `**Purpose:**` line, if one exists.

Never index `docs/superpowers/specs/` or `docs/superpowers/plans/` — that pipeline records this framework's own meta-development history (designing this project's own skills), not a downstream project's domain concepts.

## Process

### Step 1: Check for an existing index

Look for `docs/architecture/concept-index.md`. If it exists, this run is incremental maintenance — proceed to Step 3, and add/update/remove only the rows the current change calls for; never rebuild the whole table from scratch on top of an existing one. If it doesn't exist, proceed to Step 2.

### Step 2: Full build

Scan the codebase for every concept unit:

1. Every `plugin/skills/<name>/` directory containing a `SKILL.md`.
2. Every `specs/<module>/<feature>/` directory two levels under `specs/`, excluding `specs/_template/`.
3. Every directory meeting the significant-directory threshold from the Concept Units section above.

For each unit, derive its Description:

- **Skill:** read the `SKILL.md` frontmatter `description:` field directly. If it opens with "Use when...", trim that framing and keep the sentence(s) describing what the skill actually does or maintains.
- **Feature:** read the `spec.md`'s `#` heading (the feature name) and its Requirements section's first line, if populated. If Requirements is still the template's HTML-comment placeholder, use the heading alone.
- **Directory:** read the `.context.md`'s `**Purpose:**` line, if the file exists. If a Directory-type unit has no `.context.md`, ask the user for a one-line description rather than guessing one.

Write the table to `docs/architecture/concept-index.md`, with this exact header and column order:

```markdown
# Concept Index

| Concept | Type | Location | Description |
|---|---|---|---|
```

Sort rows alphabetically by Concept. Commit the file.

### Step 3: Incremental maintenance

Triggered by `subagent-driven-development`'s Finish step — never run this step standalone; it needs a specific plan's File Structure section as input, not a fresh codebase scan. Given that plan's File Structure section:

1. A new `plugin/skills/<name>/`, `specs/<module>/<feature>/`, or newly-significant directory: add one row, deriving its Description the same way Step 2 does for that unit type.
2. A renamed or moved unit: update its existing row's Concept name and/or Location — do not add a duplicate row.
3. A deleted unit: remove its row entirely.
4. No File Structure entry crosses any of these three boundaries: make no change to the index.

Commit the index change in its own small commit, separate from the plan's other Finish-step bookkeeping commits.

## Updating an Existing Index by Hand

A user may edit `docs/architecture/concept-index.md` directly (correcting a description, reordering rows). Never overwrite a hand-edited row without confirming with the user first — the same living-document discipline `project-definition` applies to its own generated sections.
````

- [ ] **Step 2: Verify the file was created correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^name: concept-index" plugin/skills/concept-index/SKILL.md
grep -n "^### Step 3: Incremental maintenance" plugin/skills/concept-index/SKILL.md
grep -c "^##" plugin/skills/concept-index/SKILL.md
```

Expected: one match on the first two greps; the third should report `5` (Overview, Concept Units, Process, and two more headings — count the actual H2s in what you wrote and confirm it matches what you see, adjusting your expectation to the real count rather than forcing a specific number).

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/concept-index/SKILL.md
git commit -m "feat(skills): add the concept-index skill

Maps every plugin/skills/<name>/, specs/<module>/<feature>/, and
significant directory to its location and a one-line description in
docs/architecture/concept-index.md -- a full-build entry point for a
codebase with no index yet, and an incremental-maintenance entry
point that subagent-driven-development's Finish step will call into.

Part of docs/superpowers/specs/2026-08-25-concept-index-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Wire concept-index maintenance into Finish

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the concept-index bookkeeping paragraph into Finish**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
Capture a notable learning in `docs/lessons-learned.md`, or record
that nothing notable arose — either answer completes this step. A
new Lesson entry: `### <title> (<spec-slug>)` as an H3 heading under
the nearest-fitting H2 category (create one if none fits), a prose
paragraph ending in a **Rule:** sentence, then a promotion note. Use
the design spec's own slug for `<spec-slug>` when one exists; no
spec: use this plan's own filename slug instead. Ask: "Does this
Lesson express a prospective rule that applies across many future
situations?" A Lesson promotes to a Pattern when it answers that
question yes, or when the same failure mode recurs a second time —
whichever comes first. On promotion, write `docs/patterns/<slug>.md`
from `docs/patterns/pattern-template.md`, and add `*Pattern promoted
— see docs/patterns/<slug>.md*` after the entry. Otherwise add `*No
pattern promoted — <one-line reason>.*` after the entry. Commit both
the Lesson (and, if written, the Pattern) in the same commit as the
tracker update above, or their own commit if the tracker didn't
change.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

Replace with:
```
Capture a notable learning in `docs/lessons-learned.md`, or record
that nothing notable arose — either answer completes this step. A
new Lesson entry: `### <title> (<spec-slug>)` as an H3 heading under
the nearest-fitting H2 category (create one if none fits), a prose
paragraph ending in a **Rule:** sentence, then a promotion note. Use
the design spec's own slug for `<spec-slug>` when one exists; no
spec: use this plan's own filename slug instead. Ask: "Does this
Lesson express a prospective rule that applies across many future
situations?" A Lesson promotes to a Pattern when it answers that
question yes, or when the same failure mode recurs a second time —
whichever comes first. On promotion, write `docs/patterns/<slug>.md`
from `docs/patterns/pattern-template.md`, and add `*Pattern promoted
— see docs/patterns/<slug>.md*` after the entry. Otherwise add `*No
pattern promoted — <one-line reason>.*` after the entry. Commit both
the Lesson (and, if written, the Pattern) in the same commit as the
tracker update above, or their own commit if the tracker didn't
change.

If `docs/architecture/concept-index.md` exists, check this plan's own
File Structure section for whether it created, renamed, moved, or
deleted a `plugin/skills/<name>/`, a `specs/<module>/<feature>/`, or a
directory crossing `docs/ai-code-guidelines.md`'s significant-directory
threshold. If so, use superpowers:concept-index's Step 3 to add,
update, or remove that row, and commit the index change in its own
small commit. If the index file doesn't exist yet, or no File
Structure entry crosses one of those three boundaries, skip this step
— do not run a full rebuild here, and do not treat a missing index as
something this step must create.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "check this plan's own" plugin/skills/subagent-driven-development/SKILL.md
grep -n "do not treat a missing index" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): wire concept-index maintenance into Finish

Finish now checks the plan's own File Structure section for a
created, renamed, moved, or deleted skill/feature/significant
directory, and calls into concept-index's incremental-maintenance
step when one exists -- stated as its own explicit paragraph, not
folded into the surrounding bookkeeping prose, per the Lesson from
per-task-outcome-capture about a mechanism getting missed when it's
not stated as its own visible check.

Part of docs/superpowers/specs/2026-08-25-concept-index-design.md."
```

Stage only this one file.

---

## Task 3: Wire concept-index consumption into the dispatch step

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the concept-index context bullet after Pseudocode context**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
- **Report file:** name the implementer's report file after the brief
  (brief `…/task-N-brief.md` → report `…/task-N-report.md`) and put it in
  the dispatch prompt. The implementer writes the full report there and
  returns only status, commits, a one-line test summary, and concerns.
```

Replace with:
```
- **Concept-index context:** if `docs/architecture/concept-index.md`
  exists, check whether the task brief names a concept already in the
  index (a skill it modifies, a feature it extends). If it does, fold
  that row's Location into the dispatch's Context section, the same
  "curated, not raw access" pattern Directory context and Pseudocode
  context already establish — the implementer receives the location,
  it never searches for it. No index file, or the brief names nothing
  in it: no mention needed.
- **Report file:** name the implementer's report file after the brief
  (brief `…/task-N-brief.md` → report `…/task-N-report.md`) and put it in
  the dispatch prompt. The implementer writes the full report there and
  returns only status, commits, a one-line test summary, and concerns.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Concept-index context" plugin/skills/subagent-driven-development/SKILL.md
grep -n "it never searches for it" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(skills): fold indexed concept locations into dispatch context

Before dispatching an implementer, the controller now checks whether
the task brief names a concept already in docs/architecture/concept-index.md
and folds its Location into the dispatch -- the same curated-context
pattern already established for Directory context and Pseudocode
context.

Part of docs/superpowers/specs/2026-08-25-concept-index-design.md."
```

Stage only this one file.

---

## Task 4: Verify the full-build entry point with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with real skill directories and a real .context.md**

```bash
mkdir -p /c/sf-concept-index-build-test/plugin/skills/example-skill-one
mkdir -p /c/sf-concept-index-build-test/plugin/skills/example-skill-two
mkdir -p /c/sf-concept-index-build-test/important-tooling
cd /c/sf-concept-index-build-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/example-skill-one/SKILL.md <<'EOF'
---
name: example-skill-one
description: Use when a user needs an example skill for testing. Generates a trivial example file demonstrating the pattern.
---

# Example Skill One

Body content not relevant to this trial.
EOF

cat > plugin/skills/example-skill-two/SKILL.md <<'EOF'
---
name: example-skill-two
description: Coordinates two other example skills to produce a combined report.
---

# Example Skill Two

Body content not relevant to this trial.
EOF

cat > important-tooling/one.py <<'EOF'
# placeholder file 1
EOF
cat > important-tooling/two.py <<'EOF'
# placeholder file 2
EOF
cat > important-tooling/three.py <<'EOF'
# placeholder file 3
EOF
cat > important-tooling/.context.md <<'EOF'
# Important Tooling

**Purpose:** Houses the three build-support scripts used by CI.

## Key Design Decisions

- Kept flat, no subpackages, since the scripts don't share code today.

## What to Be Careful About

- Don't add a fourth script without checking whether it belongs in a new directory.
EOF

git add -A
git commit -q -m "initial scratch fixture: two skills, one significant directory with .context.md"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the full build**

```bash
cd /c/sf-concept-index-build-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-concept-index-build-test. Use the Skill tool to invoke concept-index. No docs/architecture/concept-index.md exists yet, so follow the skill's full-build process (Step 2) against this repository. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote the exact full contents of docs/architecture/concept-index.md after you finish, read fresh from disk. SECTION 2/2: state how many rows you produced and list each row's Concept and Type." > /c/sf-concept-index-build-test/trial.txt 2>&1
cat /c/sf-concept-index-build-test/trial.txt
```

- [ ] **Step 3: Verify the index independently**

Read `/c/sf-concept-index-build-test/trial.txt`, and independently read the file it should have written:

```bash
cat /c/sf-concept-index-build-test/docs/architecture/concept-index.md
```

Confirm:
1. Exactly 3 rows: `example-skill-one` (Skill), `example-skill-two` (Skill), `important-tooling` (Directory).
2. `example-skill-one`'s Description reflects its `SKILL.md` frontmatter with the "Use when..." framing trimmed (should describe generating a trivial example file, not just restate "Use when a user needs an example skill").
3. `example-skill-two`'s Description reflects its frontmatter directly (no "Use when..." framing existed to trim).
4. `important-tooling`'s Description matches its `.context.md`'s Purpose line: "Houses the three build-support scripts used by CI."
5. Table header and column order match exactly: `| Concept | Type | Location | Description |`.

If any row is missing, malformed, or its Description is copied verbatim including "Use when..." framing that should have been trimmed, treat this as DONE_WITH_CONCERNS and report exactly what the file contains.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-concept-index-build-test
```

No commit for this task.

---

## Task 5: Verify the Finish-step trigger (add, skip, delete) with live trials

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with an existing index and a fixture plan**

```bash
mkdir -p /c/sf-concept-index-finish-test/docs/architecture
mkdir -p /c/sf-concept-index-finish-test/docs/superpowers/plans
mkdir -p /c/sf-concept-index-finish-test/plugin/skills/existing-skill
cd /c/sf-concept-index-finish-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/existing-skill/SKILL.md <<'EOF'
---
name: existing-skill
description: Handles an existing example task, already indexed before this trial begins.
---

# Existing Skill

Body content not relevant to this trial.
EOF

cat > docs/architecture/concept-index.md <<'EOF'
# Concept Index

| Concept | Type | Location | Description |
|---|---|---|---|
| existing-skill | Skill | `plugin/skills/existing-skill/` | Handles an existing example task, already indexed before this trial begins. |
EOF

git add -A
git commit -q -m "initial scratch fixture: one skill already indexed"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run a trial simulating Finish for a plan that ADDS a new skill**

```bash
mkdir -p /c/sf-concept-index-finish-test/plugin/skills/new-skill
cat > /c/sf-concept-index-finish-test/plugin/skills/new-skill/SKILL.md <<'EOF'
---
name: new-skill
description: Processes a new kind of example request added by this trial's fixture plan.
---

# New Skill

Body content not relevant to this trial.
EOF
cd /c/sf-concept-index-finish-test
git add -A
git commit -q -m "feat(skills): add new-skill (fixture commit simulating a completed plan)"

cd /c/sf-concept-index-finish-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-concept-index-finish-test. Assume you are the controller running subagent-driven-development's Finish step. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. This plan's File Structure section stated: 'Create: plugin/skills/new-skill/SKILL.md'. Follow Finish's concept-index bookkeeping paragraph exactly. Report back in exactly 1 section with literal header SECTION 1/1: quote the exact full contents of docs/architecture/concept-index.md after you finish, read fresh from disk." > /c/sf-concept-index-finish-test/trial-add.txt 2>&1
cat /c/sf-concept-index-finish-test/trial-add.txt
```

- [ ] **Step 3: Verify the ADD trial independently**

```bash
cat /c/sf-concept-index-finish-test/docs/architecture/concept-index.md
echo "---"
cd /c/sf-concept-index-finish-test && git log --oneline
```

Confirm: the index now has 2 rows (`existing-skill` unchanged, `new-skill` added), and a separate commit exists for the index change (not folded into the fixture's own `feat(skills): add new-skill` commit).

- [ ] **Step 4: Run a trial simulating Finish for a plan that ONLY modifies an existing skill (no add/rename/delete)**

```bash
cd /c/sf-concept-index-finish-test
echo "# an additional line" >> plugin/skills/existing-skill/SKILL.md
git add -A
git commit -q -m "fix(skills): tweak existing-skill (fixture commit simulating a completed plan)"

claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-concept-index-finish-test. Assume you are the controller running subagent-driven-development's Finish step. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. This plan's File Structure section stated: 'Modify: plugin/skills/existing-skill/SKILL.md' -- no skill, feature, or directory was created, renamed, moved, or deleted. Follow Finish's concept-index bookkeeping paragraph exactly. Report back in exactly 1 section with literal header SECTION 1/1: state whether you made any change to docs/architecture/concept-index.md, and why or why not." > /c/sf-concept-index-finish-test/trial-skip.txt 2>&1
cat /c/sf-concept-index-finish-test/trial-skip.txt
```

- [ ] **Step 5: Verify the SKIP trial independently**

```bash
cat /c/sf-concept-index-finish-test/docs/architecture/concept-index.md
echo "---"
cd /c/sf-concept-index-finish-test && git log --oneline
```

Confirm: the index file is byte-identical to Step 3's version (still 2 rows, nothing changed), SECTION 1/1 explicitly states no change was made and why, and no new commit touching `docs/architecture/concept-index.md` exists beyond the one from Step 3.

- [ ] **Step 6: Run a trial simulating Finish for a plan that DELETES a skill**

```bash
cd /c/sf-concept-index-finish-test
rm -rf plugin/skills/new-skill
git add -A
git commit -q -m "fix(skills): remove new-skill (fixture commit simulating a completed plan)"

claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-concept-index-finish-test. Assume you are the controller running subagent-driven-development's Finish step. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. This plan's File Structure section stated: 'Delete: plugin/skills/new-skill/'. Follow Finish's concept-index bookkeeping paragraph exactly. Report back in exactly 1 section with literal header SECTION 1/1: quote the exact full contents of docs/architecture/concept-index.md after you finish, read fresh from disk." > /c/sf-concept-index-finish-test/trial-delete.txt 2>&1
cat /c/sf-concept-index-finish-test/trial-delete.txt
```

- [ ] **Step 7: Verify the DELETE trial independently**

```bash
cat /c/sf-concept-index-finish-test/docs/architecture/concept-index.md
echo "---"
cd /c/sf-concept-index-finish-test && git log --oneline
```

Confirm: the index now has 1 row (`existing-skill` only — `new-skill`'s row removed), and a separate commit exists for this removal.

If any of the three trials shows the wrong row count, a folded-in commit instead of a separate one, or a skip trial that made an unwanted change, treat this as DONE_WITH_CONCERNS and report exactly which trial failed and what the file/git log actually contain.

- [ ] **Step 8: Clean up**

```bash
rm -rf /c/sf-concept-index-finish-test
```

No commit for this task.

---

## Task 6: Verify dispatch-context consumption with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with an indexed skill and a fixture plan referencing it**

```bash
mkdir -p /c/sf-concept-index-dispatch-test/docs/architecture
mkdir -p /c/sf-concept-index-dispatch-test/docs/superpowers/plans
mkdir -p /c/sf-concept-index-dispatch-test/plugin/skills/target-skill
cd /c/sf-concept-index-dispatch-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/target-skill/SKILL.md <<'EOF'
---
name: target-skill
description: Handles the target task this dispatch trial references.
---

# Target Skill

Body content not relevant to this trial.
EOF

cat > docs/architecture/concept-index.md <<'EOF'
# Concept Index

| Concept | Type | Location | Description |
|---|---|---|---|
| target-skill | Skill | `plugin/skills/target-skill/` | Handles the target task this dispatch trial references. |
EOF

cat > docs/superpowers/plans/2026-08-25-dispatch-fixture-test.md <<'EOF'
# Dispatch Fixture Test Implementation Plan

**Goal:** A trivial one-task plan used only to exercise concept-index dispatch-context consumption in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Extend target-skill

Modify plugin/skills/target-skill/SKILL.md to add one more sentence to its body.
EOF

git add -A
git commit -q -m "initial scratch fixture: one indexed skill, one fixture plan referencing it"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the dispatch-context check**

```bash
cd /c/sf-concept-index-dispatch-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-concept-index-dispatch-test. Use the Skill tool to invoke subagent-driven-development first to load its current instructions. You are about to dispatch an implementer for Task 1 of docs/superpowers/plans/2026-08-25-dispatch-fixture-test.md, which modifies plugin/skills/target-skill/SKILL.md. Follow the Dispatch the implementer step's Concept-index context bullet exactly. Do not actually dispatch a subagent -- instead, report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether target-skill is named in docs/architecture/concept-index.md, and if so quote its exact Location. SECTION 2/2: quote the exact Context-section text you would fold into the dispatch prompt for this concept, per the bullet's instructions." > /c/sf-concept-index-dispatch-test/trial.txt 2>&1
cat /c/sf-concept-index-dispatch-test/trial.txt
```

- [ ] **Step 3: Verify the consumption trial**

Read `/c/sf-concept-index-dispatch-test/trial.txt`. Confirm SECTION 1/2 correctly finds `target-skill` in the index and quotes its Location as `` `plugin/skills/target-skill/` `` exactly, and SECTION 2/2 shows the agent actually composing dispatch-context text that includes that Location — not a generic restatement, and not an empty/skipped answer.

If SECTION 1/2 reports the concept wasn't found, or SECTION 2/2 shows no location folded into the context, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-concept-index-dispatch-test
```

No commit for this task.
