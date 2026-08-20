# Process Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Casita's Process Review mechanism into superfunk — a running notes log fed by the existing review loop, a tracker counting shipped specs, a shared `process-review` skill, and two trigger points that surface a due review or an open Recommendation — per `docs/superpowers/specs/2026-08-19-process-review-design.md`.

**Architecture:** Two new seed files (`docs/superpowers/process-reviews/notes.md`, `docs/superpowers/process-reviews/tracker.md`), one new skill (`plugin/skills/process-review/SKILL.md`), and edits to two existing fork skill files (`subagent-driven-development/SKILL.md`'s fix loop, Final Review, and Finish sections; `brainstorming/SKILL.md`'s "Understanding the idea" section).

**Tech Stack:** Markdown skill files and markdown artifacts, no code, no test framework. Verification is grep checks plus two disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Create:** `docs/superpowers/process-reviews/notes.md` — the running, append-only Catch log.
- **Create:** `docs/superpowers/process-reviews/tracker.md` — last-review record and the shipped-since list.
- **Create:** `plugin/skills/process-review/SKILL.md` — the shared review procedure both trigger points invoke.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds the logging step to the fix loop and Final Review, and the tracker/threshold check to the Finish section.
- **Modify:** `plugin/skills/brainstorming/SKILL.md` — adds the tracker gate to "Understanding the idea."

---

## Task 1: Seed the process-reviews artifacts

**Files:**
- Create: `docs/superpowers/process-reviews/notes.md`
- Create: `docs/superpowers/process-reviews/tracker.md`

- [ ] **Step 1: Write the running notes log**

```markdown
# Process Review — Running Notes

Append-only log. Each entry marks one finding a review catches on its
first pass (spec-compliance, code-quality, or the final whole-branch
review), tagged `Catch`. `process-review` reads this log,
cross-references `git log`, and may surface `Miss`, `Friction`, or
`Gap` patterns across entries when it synthesizes a review file.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`

<!-- entries below this line -->
```

Save to `docs/superpowers/process-reviews/notes.md`.

- [ ] **Step 2: Write the tracker**

```markdown
# Process Review Tracker

**Last review:** none yet
**Specs shipped since:** (none)
```

Save to `docs/superpowers/process-reviews/tracker.md`.

- [ ] **Step 3: Verify both files exist with the right content**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "entries below this line" docs/superpowers/process-reviews/notes.md
grep -n "Last review.*none yet" docs/superpowers/process-reviews/tracker.md
```

Expected: one match each.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/process-reviews/notes.md docs/superpowers/process-reviews/tracker.md
git commit -m "feat: seed the process-review running notes log and tracker

Empty starting state for both artifacts -- notes.md accumulates
Catch entries as review loops find issues, tracker.md counts specs
shipped since the last review.

Part of docs/superpowers/specs/2026-08-19-process-review-design.md."
```

Stage only these two files — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Write the process-review skill

**Files:**
- Create: `plugin/skills/process-review/SKILL.md`

- [ ] **Step 1: Write the skill file**

```markdown
---
name: process-review
description: Use when a design-spec Status trigger or brainstorming gate signals a process review is due -- synthesizes recent Catches/Misses/Friction/Gaps into a review file with actionable Recommendations
---

# Process Review

Read `docs/superpowers/process-reviews/notes.md` and recent git
history across the specs shipped since the last review. Synthesize
findings into a dated review file, and reset the tracker.

**Core principle:** real evidence over vibes — every Catch, Miss,
Friction, and Gap in the output traces to a logged note or a specific
commit, not to memory of how the work felt.

## When to Use

Reads `docs/superpowers/process-reviews/tracker.md` and
`docs/superpowers/process-reviews/notes.md`. Invoked by two callers,
never run standalone without one of these triggers:

- `subagent-driven-development`'s Finish step, when the tracker's
  "Specs shipped since" list reaches 3 entries.
- `brainstorming`'s "Understanding the idea" step, when the tracker
  shows a review overdue.

## The Process

1. Read `docs/superpowers/process-reviews/tracker.md`. Note the last
   review's spec filename and date (or "none yet"), and the "Specs
   shipped since" list — these are the specs this review covers.
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet").
3. Cross-reference `git log --oneline` for each shipped spec's
   implementing commits (the spec name usually appears in a commit
   trailer, e.g. "Part of docs/superpowers/specs/..."). For any fix
   commit whose message names a defect with no matching notes.md
   entry, treat it as a Catch the running log missed, and include it.
4. Synthesize the collected Catches into the review's sections:
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers.
   - **Catches** — list each Catch entry, grouped by spec.
   - **Misses** — a Catch that recurs across 2 or more of the
     reviewed specs signals something upstream should catch it
     earlier. Name the pattern and which specs it recurred in.
   - **Friction** — a task or spec whose commit history shows 3 or
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect.
   - **Gaps** — a convention repeatedly caught by the same reviewer,
     with no earlier check backing it up.
   - **Recommendations** — one checkbox item per Miss, Friction
     point, or Gap identified above. Each names a target file and the
     exact change, e.g. `- [ ] Add X check to docs/ai-code-guidelines.md`.
     A Catch alone, with no recurring pattern, needs no
     Recommendation — the review loop already handled it.
5. Write the review to
   `docs/superpowers/process-reviews/review-after-<last-spec-slug>.md`,
   where `<last-spec-slug>` is the filename (minus `.md`) of the most
   recently shipped spec in the "Specs shipped since" list.
6. Update `docs/superpowers/process-reviews/tracker.md`: set "Last
   review" to `<spec-filename> — <YYYY-MM-DD>` (e.g.
   `2026-08-19-process-review-design.md — 2026-08-19`), using this
   review's spec filename and today's date, and clear "Specs shipped
   since" to `(none)`.
7. Commit the review file and the tracker update together.

## No Placeholders

Every Recommendation names a real target file and a real, specific
change — never "improve X" or "consider Y." If a Miss, Friction
point, or Gap has no clear fix, say so explicitly in that section
instead of forcing a vague Recommendation.
```

Save to `plugin/skills/process-review/SKILL.md`.

- [ ] **Step 2: Verify the file exists with correct frontmatter**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^name: process-review" plugin/skills/process-review/SKILL.md
grep -n "review-after-<last-spec-slug>.md" plugin/skills/process-review/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/process-review/SKILL.md
git commit -m "feat: add the process-review skill

A shared procedure invoked by subagent-driven-development's Finish
step and brainstorming's Understanding-the-idea step -- reads the
running notes log and tracker, cross-references git log, and writes
a dated review file with Catches/Misses/Friction/Gaps and checkbox
Recommendations.

Part of docs/superpowers/specs/2026-08-19-process-review-design.md."
```

Stage only this one file.

---

## Task 3: Wire logging and the tracker into subagent-driven-development

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Add the logging step to the fix loop**

Find:
```
Everything else enters the loop. A fix round is one fix dispatch plus one
scoped re-review. Five rounds maximum per task:

**Rounds 1-3 — resume the original implementer.**
```

Replace with:
```
Everything else enters the loop. Before the first fix dispatch,
append one line per open finding to
`docs/superpowers/process-reviews/notes.md`:
`- <YYYY-MM-DD> | Catch | Task <N> | <one-line finding>`. The review
loop is already doing the work; logging it costs one line and feeds
`process-review` later. A fix round is one fix dispatch plus one
scoped re-review. Five rounds maximum per task:

**Rounds 1-3 — resume the original implementer.**
```

- [ ] **Step 2: Add the logging step to the Final Review section**

Find:
```
If the final whole-branch review returns findings, dispatch ONE fix subagent
with the complete findings list — not one fixer per finding.
```

Replace with:
```
If the final whole-branch review returns findings, append one line per
finding to `docs/superpowers/process-reviews/notes.md`
(`- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`), then
dispatch ONE fix subagent with the complete findings list — not one
fixer per finding.
```

- [ ] **Step 3: Add the tracker and threshold check to the Finish section**

Find:
```
## Finish

When the final whole-branch review is clean and its fixes are merged,
check whether this plan traces to a design spec (named in the plan's
Goal line or a task's commit trailer, e.g. "Part of
docs/superpowers/specs/..."). If it does, update that spec's `Status`
line from `Approved` to `Shipped` and commit the change on this branch
— the only point in this process where the work is both reviewed and
merged, so it is the right moment to record it. No spec, or already
`Shipped`: skip this step. Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.

Use superpowers:finishing-a-development-branch.
```

Replace with:
```
## Finish

When the final whole-branch review is clean and its fixes are merged,
check whether this plan traces to a design spec (named in the plan's
Goal line or a task's commit trailer, e.g. "Part of
docs/superpowers/specs/..."). If it does, update that spec's `Status`
line from `Approved` to `Shipped` and commit the change on this branch
— the only point in this process where the work is both reviewed and
merged, so it is the right moment to record it. No spec, or already
`Shipped`: skip this step.

If you updated a spec's Status to `Shipped`, also append its filename
to `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped
since" list, and commit that change in the same commit. If the list
now holds 3 or more filenames, offer to run superpowers:process-review
right now — the same ask-don't-force pattern as any other checkpoint
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.

Then delete this plan's workspace
(`rm -rf <workspace>`) — the git history is the record now. Sibling
directories belong to other plans; leave them alone.

Use superpowers:finishing-a-development-branch.
```

- [ ] **Step 4: Verify all three edits landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "process-reviews/notes.md" plugin/skills/subagent-driven-development/SKILL.md
grep -n "Specs shipped" plugin/skills/subagent-driven-development/SKILL.md
grep -n "superpowers:process-review" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: `process-reviews/notes.md` matches twice (fix loop, Final Review); `Specs shipped` matches once (Finish); `superpowers:process-review` matches once (Finish).

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: wire process-review logging and the shipped-spec tracker into subagent-driven-development

The fix loop and Final Review now log a Catch entry per finding
before dispatching a fix. The Finish section now appends each
newly-Shipped spec to the tracker's shipped-since list, and offers
to run process-review once the list reaches 3.

Part of docs/superpowers/specs/2026-08-19-process-review-design.md."
```

Stage only this one file.

---

## Task 4: Wire the review-due gate into brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Add the tracker gate to "Understanding the idea"**

Find:
```
- Check out the current project state first (files, docs, recent commits). For each directory you examine, attempt to read its `.context.md` — skip if none exists — it holds the directory's purpose, key design decisions, and what to be careful about (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section). Note which directories you checked when you present findings, so the check stays visible instead of silently not happening.
- Before asking detailed questions, assess scope:
```

Replace with:
```
- Check out the current project state first (files, docs, recent commits). For each directory you examine, attempt to read its `.context.md` — skip if none exists — it holds the directory's purpose, key design decisions, and what to be careful about (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section). Note which directories you checked when you present findings, so the check stays visible instead of silently not happening.
- Check `docs/superpowers/process-reviews/tracker.md`, if it exists, for two independent conditions: a review due (3+ specs shipped since the last review, never run), or an open Recommendation in the last review file (an unchecked `- [ ]` item in `docs/superpowers/process-reviews/review-after-*.md`). Surface both, if either applies. Ask your human partner to act on each, or explicitly defer it, before continuing to clarifying questions. A deferred Recommendation gets a `(deferred: <reason>)` note beside the item in the review file. A deferred review-due check gets its note in the tracker instead, since it has no per-item home. No tracker file yet: skip this check.
- Before asking detailed questions, assess scope:
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "process-reviews/tracker.md" plugin/skills/brainstorming/SKILL.md
```

Expected: one match, inside the new bullet.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat: surface an overdue process review or open Recommendation at brainstorming's start

Understanding the idea now checks the process-review tracker before
clarifying questions begin, and asks the user to act on or defer
whatever it finds -- matching Casita's real forcing function (checked
before the next planning starts).

Part of docs/superpowers/specs/2026-08-19-process-review-design.md."
```

Stage only this one file.

---

## Task 5: Verify the Finish-step trigger and process-review with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with 2 specs already tracked and a 3rd about to ship**

```bash
mkdir -p /c/sf-process-review-test/docs/superpowers/specs
mkdir -p /c/sf-process-review-test/docs/superpowers/process-reviews
cd /c/sf-process-review-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-process-review-test/docs/superpowers/specs/2026-01-01-fake-spec-a-design.md <<'EOF'
# Fake Spec A — Design

**Date:** 2026-01-01
**Status:** Shipped

## Context

A trivial fixture spec for testing the process-review trigger.

## Decision

- Add a function that returns a constant.
EOF
cat > /c/sf-process-review-test/docs/superpowers/specs/2026-01-02-fake-spec-b-design.md <<'EOF'
# Fake Spec B — Design

**Date:** 2026-01-02
**Status:** Shipped

## Context

A trivial fixture spec for testing the process-review trigger.

## Decision

- Add a second function that returns a constant.
EOF
cat > /c/sf-process-review-test/docs/superpowers/specs/2026-01-03-fake-spec-c-design.md <<'EOF'
# Fake Spec C — Design

**Date:** 2026-01-03
**Status:** Approved, not yet implemented

## Context

A trivial fixture spec for testing the Finish step's tracker and
threshold behavior.

## Decision

- Add a third function that returns a constant.
EOF
cat > /c/sf-process-review-test/docs/superpowers/process-reviews/tracker.md <<'EOF'
# Process Review Tracker

**Last review:** none yet
**Specs shipped since:** 2026-01-01-fake-spec-a-design.md, 2026-01-02-fake-spec-b-design.md
EOF
cat > /c/sf-process-review-test/docs/superpowers/process-reviews/notes.md <<'EOF'
# Process Review — Running Notes

Append-only log.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`

<!-- entries below this line -->
- 2026-01-01 | Catch | Task 1 | fake-spec-a's first implementer missed the return-type annotation
- 2026-01-02 | Catch | Task 1 | fake-spec-b's first implementer missed the same return-type annotation
EOF
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial that skips straight to the Finish step and agrees to run process-review**

```bash
cd /c/sf-process-review-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-process-review-test. Assume you are partway through following the subagent-driven-development skill for a plan that implements docs/superpowers/specs/2026-01-03-fake-spec-c-design.md: all tasks are already complete, and the final whole-branch review just came back clean. Follow the skill's Finish section now, exactly as written -- do not re-read or re-execute any earlier part of the skill, just Finish. If the Finish section offers to run superpowers:process-review, agree to run it now, and follow that skill's process exactly as written. After completing the Finish section and any process-review run it triggered, report back in exactly 4 numbered sections with literal headers: SECTION 1/4: quote fake-spec-c's current Status line, read fresh from disk. SECTION 2/4: quote tracker.md's current 'Specs shipped since' line, read fresh from disk. SECTION 3/4: list any file matching docs/superpowers/process-reviews/review-after-*.md that now exists, or state none exists -- read the directory fresh, do not rely on memory. SECTION 4/4: quote tracker.md's current 'Last review' line, read fresh from disk." > /c/sf-process-review-test/trial.txt 2>&1
cat /c/sf-process-review-test/trial.txt
```

- [ ] **Step 3: Verify the tracker, spec Status, and review file independently**

Read `/c/sf-process-review-test/trial.txt`, and independently read the files it should have touched:

```bash
cat /c/sf-process-review-test/docs/superpowers/specs/2026-01-03-fake-spec-c-design.md
echo "---"
cat /c/sf-process-review-test/docs/superpowers/process-reviews/tracker.md
echo "---"
ls /c/sf-process-review-test/docs/superpowers/process-reviews/
```

Confirm:
1. `2026-01-03-fake-spec-c-design.md`'s `Status` line reads `Shipped`.
2. `tracker.md`'s "Specs shipped since" line reads `(none)` — process-review ran and reset it.
3. `tracker.md`'s "Last review" line names `2026-01-03-fake-spec-c-design.md` and a date — not `none yet`.
4. A file matching `review-after-2026-01-03-fake-spec-c-design.md` exists, with all six sections (Specs Reviewed, Catches, Misses, Friction, Gaps, Recommendations) and at least the two seeded Catch entries reflected in its Catches section.

If any of these four is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the files actually contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-process-review-test
```

No commit for this task.

---

## Task 6: Verify brainstorming's review-due gate with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with an overdue review and an open Recommendation**

```bash
mkdir -p /c/sf-brainstorm-gate-test/docs/superpowers/process-reviews
cd /c/sf-brainstorm-gate-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-brainstorm-gate-test/docs/superpowers/process-reviews/tracker.md <<'EOF'
# Process Review Tracker

**Last review:** 2026-01-03-fake-spec-c-design.md — 2026-01-05
**Specs shipped since:** 2026-01-10-fake-spec-d-design.md, 2026-01-11-fake-spec-e-design.md, 2026-01-12-fake-spec-f-design.md
EOF
cat > /c/sf-brainstorm-gate-test/docs/superpowers/process-reviews/review-after-2026-01-03-fake-spec-c-design.md <<'EOF'
# Process Review — after 2026-01-03-fake-spec-c-design.md

**Date:** 2026-01-05

## Specs Reviewed

- 2026-01-01-fake-spec-a-design.md
- 2026-01-02-fake-spec-b-design.md
- 2026-01-03-fake-spec-c-design.md

## Catches

- fake-spec-a and fake-spec-b both had their first implementer miss a return-type annotation.

## Misses

- None identified.

## Friction

- None identified.

## Gaps

- Return-type annotations rely entirely on code-quality review catching them; nothing upstream checks for this before the reviewer does.

## Recommendations

- [ ] Add a return-type-annotation reminder to docs/ai-code-guidelines.md's Naming section.
EOF
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial starting a new brainstorm**

```bash
cd /c/sf-brainstorm-gate-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-brainstorm-gate-test. Use the brainstorming skill for this idea: add a one-line helper function that returns the current year as an integer. Go through the skill's checklist item 1, 'Explore project context' / 'Understanding the idea,' exactly as written, including the process-review tracker check. Stop immediately after that check and before asking any clarifying question. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote exactly what you found when you checked docs/superpowers/process-reviews/tracker.md and any review file it pointed to. SECTION 2/2: quote the exact question you asked (or would ask) your human partner about acting on or deferring what you found, before continuing to clarifying questions." > /c/sf-brainstorm-gate-test/trial.txt 2>&1
cat /c/sf-brainstorm-gate-test/trial.txt
```

- [ ] **Step 3: Verify both conditions surfaced**

Read `/c/sf-brainstorm-gate-test/trial.txt`. Confirm:

1. SECTION 1/2 names the review as overdue (3 specs shipped since the last review) — not silently skipped.
2. SECTION 1/2 also names the open Recommendation from `review-after-2026-01-03-fake-spec-c-design.md` (the return-type-annotation item) — not silently skipped.
3. SECTION 2/2 contains an actual act-or-defer question to the human partner, not a fabricated claim that no question was needed.

If any of the three is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the trial actually output.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-brainstorm-gate-test
```

No commit for this task — it verifies Task 4 and touches no repository files.
