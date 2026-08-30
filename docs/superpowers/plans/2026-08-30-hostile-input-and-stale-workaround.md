# Hostile-Input Pass and Stale-Workaround Grep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Self-Review items 13 (hostile-input pass) and 14 (stale-workaround grep) to `writing-plans/SKILL.md`, and create `docs/patterns/hunt-the-workaround-not-the-feature.md` in this repo.

**Architecture:** Two additive edits — a Self-Review extension in one existing skill file, and one new Pattern file, adapted from the trial fixture's own version. No code, no tests in the software sense — every task verifies via direct read-back or `grep`, plus two disposable `--plugin-dir` trials for the end-to-end behavioral claims.

**Tech Stack:** Markdown, `grep`, disposable trials.

## Global Constraints

- Items 13 and 14 must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criterion 1).
- `docs/patterns/hunt-the-workaround-not-the-feature.md` must match the design spec's Decision block exactly (per spec Falsifiable Criterion 2).
- No file outside `plugin/skills/writing-plans/SKILL.md` and `docs/patterns/hunt-the-workaround-not-the-feature.md` gets touched.

---

## File Structure

Directory touched: `plugin/skills/writing-plans/`, and a new file created in `docs/patterns/`. Checked `plugin/skills/writing-plans/` for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`). `docs/patterns/` has no `.context.md` either (checked directly).

The new file's name, `hunt-the-workaround-not-the-feature.md`, already follows `docs/code-standards.md`'s File Naming section (kebab-case for markdown files) — it matches the name the trial's own process-review already gave it, kept unchanged for continuity between the two repos.

**Files to modify:**
- `plugin/skills/writing-plans/SKILL.md` — append Self-Review items 13 and 14

**File to create:**
- `docs/patterns/hunt-the-workaround-not-the-feature.md`

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds Markdown text.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add Self-Review items 13 and 14

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the two new Self-Review items every future plan checks against. Task 3's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm item 12's exact current closing text**

Run: `grep -n "User-facing documentation timing" -A6 plugin/skills/writing-plans/SKILL.md`
Expected: text ending in "the same class of gap this item exists to close." followed by the "If you find issues..." closing line — confirmed via direct read this session.

- [ ] **Step 2: Append items 13 and 14**

Change:
```markdown
**12. User-facing documentation timing:** If the spec carries
`User-Facing: Yes`, does the task shipping the user-facing surface
include its own documentation step, per the section above? A plan that
defers this to a separate task or relies on Finish to catch it repeats
the same class of gap this item exists to close.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```
To:
```markdown
**12. User-facing documentation timing:** If the spec carries
`User-Facing: Yes`, does the task shipping the user-facing surface
include its own documentation step, per the section above? A plan that
defers this to a separate task or relies on Finish to catch it repeats
the same class of gap this item exists to close.

**13. Hostile-input pass:** For each code block a task specifies, name
the input class it does not handle — metacharacters in user-supplied
text, a value that already exists, a discarded return value, an
operation that cannot be cancelled, or any other input the block's
own logic doesn't account for. Either handle it in the plan, or
record it as an accepted limitation in the spec's Consequences
section. A code block with an unexamined input class counts as a plan
failure, the same as a missing test.

**14. Stale-workaround grep:** If any task removes a limitation (a
missing command, an unsupported case, a manual step), write down the
exact phrase the tool used to describe that limitation — the error
message, docstring, or README text a user would have hit. Grep the
codebase for that phrase's distinctive words — not the new feature's
name, which limitation-era text never mentions — per
docs/patterns/hunt-the-workaround-not-the-feature.md. List every hit
as a task requirement: each one either needs updating to reflect the
new capability, or needs removing if it no longer applies.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 3: Verify both additions landed**

Run: `grep -c "Hostile-input pass" plugin/skills/writing-plans/SKILL.md`
Expected: `1`

Run: `grep -c "Stale-workaround grep" plugin/skills/writing-plans/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): add Self-Review items 13-14 to writing-plans (hostile-input pass, stale-workaround grep)"
```

---

### Task 2: Create the hunt-the-workaround-not-the-feature pattern

**Files:**
- Create: `docs/patterns/hunt-the-workaround-not-the-feature.md`

**Interfaces:**
- Consumes: nothing from Task 1 (an independent new file, though item 14 references it).
- Produces: the Pattern file item 14 cites. Task 3's verification depends on this task's exact content.

- [ ] **Step 1: Confirm the file doesn't already exist**

Run: `ls docs/patterns/hunt-the-workaround-not-the-feature.md 2>&1`
Expected: `No such file or directory` (confirmed via direct check this session).

- [ ] **Step 2: Write the file**

Create `docs/patterns/hunt-the-workaround-not-the-feature.md` with this exact content:

```markdown
# Hunt The Workaround, Not The Feature

When a change removes a limitation, the stale text sits wherever the
limitation forced a workaround — and none of it names the new feature.

## Context

A release removes a constraint: a missing command arrives, an
unsupported case becomes supported, a manual step gets automated. The
new surface gets documented carefully, because it's what the work was
about.

What doesn't get found is everything written around the absence. A
limitation propagates outward from the code that lacks it: error
messages that route users to a workaround, rationale comments
explaining why something was deferred, "Current limitations" lists,
test comments justifying an awkward workaround, prose describing the
old behavior sitting near prose describing the new. Searching for the
feature's name finds none of these — they predate it and talk about
its absence.

## Pattern

Before shipping, grep for the workaround the limitation forced — the
phrase users were told to do instead — not for the feature's name.
Write down the sentence the tool used to say when someone hit the
limitation. Search for its distinctive words. Every hit either turns
false the moment the feature ships, or needs to point at the new
path instead.

Check the same terms in: error strings, comments near the code that
enforced the limitation, the README's limitation list, and any test
whose comment explains a workaround.

A useful sharpening: the more helpful the old message was, the more
dangerous it becomes. A message that merely said "not supported" goes
inert once support arrives. A message that said "do X instead"
actively directs users at X — and if X causes harm, it keeps causing
harm after the safe path exists.

## Example

A bookmark-manager CLI shipped an `edit` command so a bookmark's title
could get fixed without losing its permanent id and tags. The final
review found `add --title` on an already-saved URL still printing
"already saved — --title ignored; remove and re-add to change it."
Correct when written; after `edit` shipped, it directed users at the
one operation that destroys the id and every tag — precisely the
damage the round existed to prevent. Grepping for `edit` would have
found none of the four stale references (two code comments, a test
comment, a README paragraph). Grepping for `re-add` — the workaround —
found all four.

The same failure happened one round earlier: after a retry command
shipped, a docstring still read "wired to no command yet" and the
README still listed the retry gap as a limitation — that instance
blocked a merge.

## Originating lessons

- "Removing a limitation means hunting the workaround it forced" (2026-08-30-hostile-input-and-stale-workaround)
```

- [ ] **Step 3: Verify the file exists with the right content**

Run: `grep -c "Hunt The Workaround, Not The Feature" docs/patterns/hunt-the-workaround-not-the-feature.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add docs/patterns/hunt-the-workaround-not-the-feature.md
git commit -m "docs: add hunt-the-workaround-not-the-feature pattern"
```

---

### Task 3: Full verification sweep and live trials

**Files:**
- No files modified — this task only verifies Tasks 1–2.

**Interfaces:**
- Consumes: the finished state of both files Tasks 1–2 touched.
- Produces: pass/fail evidence for every Falsifiable Criterion in the design spec. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — items 13 and 14**

Run: `grep -A7 "13. \*\*Hostile-input pass" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's item 13 exactly.

Run: `grep -A8 "14. \*\*Stale-workaround grep" plugin/skills/writing-plans/SKILL.md`
Expected: text matching the Decision block's item 14 exactly. (Item 14's text runs 9 lines including its own lead line, one more than item 13's 8 — counted directly against the drafted text before finalizing this command, not assumed uniform.)

- [ ] **Step 2: Verify Falsifiable Criterion 2 — the pattern file**

Run: `diff <(cat docs/patterns/hunt-the-workaround-not-the-feature.md) <(echo "expected content")` — in practice, read the file back directly and compare against the Decision block's content line by line.
Expected: exact match.

- [ ] **Step 3: Verify Falsifiable Criterion 3 — hostile-input pass live trial**

Set up a disposable fixture: a plan document containing one task whose code block implements a search function with no metacharacter escaping (matching the trial's own `search()` LIKE-wildcard shape).

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Apply writing-plans' Self-Review item 13 (hostile-input pass) to this task's code block: [paste the fixture's search function]. Name the input class it doesn't handle, per the item's own instructions." --add-dir <fixture-path>
```

Expected: the response correctly names the unescaped-metacharacter input class (e.g., `%` and `_` in a SQL `LIKE` pattern, or the fixture's equivalent) and either proposes a fix or states this needs recording as an accepted Consequence.

- [ ] **Step 4: Verify Falsifiable Criterion 4 — stale-workaround grep live trial**

Set up a second disposable fixture: a small codebase where a task removes a limitation (e.g., adds a `retry` command), and a stale reference to the old limitation still exists elsewhere (a README line reading "no retry command yet", a docstring saying the same).

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Apply writing-plans' Self-Review item 14 (stale-workaround grep) to this plan: it adds a 'retry' command. Grep the fixture for the old limitation's workaround phrase, per the item's own instructions, and list what you find." --add-dir <fixture-path>
```

Expected: the response greps for the old limitation's distinctive words (not "retry," the new feature's name) and correctly surfaces the stale README/docstring references as task requirements needing an update.

- [ ] **Step 5: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers Decision ¶1–2 (items 13–14). Task 2 covers Decision ¶3 (the pattern file). Task 3 covers all four Falsifiable Criteria. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** Items 13 and 14 match items 1–12's exact bold-numbered-lead-in format. Checked directly against item 12's real text before finalizing, not assumed similar.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into Task 1's Step 2 and Task 2's Step 2 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md`, `docs/patterns/verify-plan-commands-against-real-content.md`, and `docs/patterns/re-verify-quotes-against-source-before-citing.md` before writing this plan — every numeric claim in this plan (the `1`, `1` counts) got verified against real file baselines, and the pattern file's content in Task 2 got copied verbatim from the design spec (itself already checked against the trial fixture's real file during the spec's own writing) rather than re-derived from memory.

**8. Cross-section mechanism consistency:** Task 1 adds items 13–14 after item 12, in the same Self-Review list as items 1–12. Grepped `writing-plans/SKILL.md` for every other mention of "hostile," "workaround," and "input class" beyond items 13–14 to confirm no other passage describes this mechanism in a way the new items would contradict — found none. This plan traces to a design spec; the spec's own Consequences section states what closes, which is exactly what this check confirms holds true.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — this adds two new Self-Review items without changing the Self-Review process's own step sequence. No worked example needs a currency check.

**10. Verified numeric expectations:** Every `Expected:` count in this plan was confirmed by running the actual grep against real file content, or checking real file non-existence, before being written into this plan — not estimated.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

**13. Hostile-input pass:** N/A — this plan's own tasks contain no code blocks implementing runtime logic; every "code block" in this plan is Markdown/documentation content, not a function processing external input.

**14. Stale-workaround grep:** N/A — this plan doesn't remove any limitation from superfunk itself; it adds two new checks. No prior limitation's workaround text exists to search for.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-hostile-input-and-stale-workaround.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
