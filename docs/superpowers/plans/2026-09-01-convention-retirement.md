# Convention Retirement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `process-review` the ability to propose removing a check or a gate, and give `notes.md` the attribution field that makes per-check yield computable.

**Architecture:** Five tasks over two files. Task 1 changes `notes.md`'s documented format. Tasks 2-4 change `plugin/skills/process-review/SKILL.md` — how it reads entries, a new Retirements output section, and a rule on Recommendations. Task 5 runs the trial that can falsify the design. No code and no test framework; every task verifies by `grep` against real file content, and Task 5 verifies by disposable `--plugin-dir` trial plus an independent checking pass.

**Tech Stack:** Markdown skill files, `grep`, and disposable `--plugin-dir` scratch trials.

## Global Constraints

- Every text block this plan writes matches the design spec's Decision block exactly, character for character. `docs/superpowers/specs/2026-09-01-convention-retirement-design.md` governs.
- **The 88 pre-existing `notes.md` entries stay byte-identical.** Task 1 changes only the header. Spec Criterion 5 fails if `git diff` shows any change to a line beginning `- 2026-0`.
- No file outside `docs/superpowers/process-reviews/notes.md`, `plugin/skills/process-review/SKILL.md`, and this plan's own outcomes file gets modified.
- **Task 5 can falsify this design.** If a proposed Retirement fails independent checking, stop and report rather than shipping.
- Do not supply the trial with the three subsumption candidates named in the spec's Context. Spec Criterion 8 depends on that.

---

## File Structure

Directories touched: `docs/superpowers/process-reviews/` and `plugin/skills/process-review/`. `find plugin docs -iname ".context.md"` returns `0` this session, so no directory-context file applies.

This plan creates no new files. Every edit modifies an existing file, so `docs/code-standards.md`'s File Naming section does not apply.

**Files to modify:**
- `docs/superpowers/process-reviews/notes.md` — header format line and two explanatory paragraphs
- `plugin/skills/process-review/SKILL.md` — Step 2 entry reading, Step 5 Retirements section, Step 5 Recommendations rule, No Placeholders extension

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API. Every edit adds Markdown text or runs `grep`.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern. Task 3 adds a sixth output section beside five existing ones, reusing that file's prose shape rather than a code pattern.
- **T3 — DTO/schema shape:** Skipped: the `notes.md` entry line grows from four fields to five, which Task 1 states literally in the file. Restating it as pseudocode adds nothing the Decision block does not already give.
- **T4 — User-designated:** Skipped: the user has not asked for pseudocode on any part of this work.

---

### Task 1: Give `notes.md` the attribution field

**Files:**
- Modify: `docs/superpowers/process-reviews/notes.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the documented five-field format Task 2 teaches `process-review` to read.

- [ ] **Step 1: Confirm the current format line and the baselines**

Run: `grep -n "^Format:" docs/superpowers/process-reviews/notes.md`
Expected: one match at line 9.

Run: `grep -c "check that caught it\|found ad hoc\|four fields" docs/superpowers/process-reviews/notes.md`
Expected: `0` (confirmed by running it this session).

- [ ] **Step 2: Replace the format line**

Change:
```markdown
Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`
```
To:
```markdown
Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <check that caught it> | <one-line finding>`

The fourth field names the specific check that produced the Catch — for
example `writing-plans item 10`, `brainstorming item 6`, or
`SDD spec-review`. When no check produced it, write exactly
`none — found ad hoc`. That value records a real fact and keeps
attribution honest: a format offering no way to say "nothing caught
this" pressures a writer to invent one.

Entries below dated before 2026-09-01 carry four fields, without the
check field. They stay as written — reconstructing attribution from
memory would fabricate it.
```

- [ ] **Step 3: Verify the header changed and no entry did**

Run: `grep -c "check that caught it" docs/superpowers/process-reviews/notes.md`
Expected: `1`

Run: `grep -c "found ad hoc" docs/superpowers/process-reviews/notes.md`
Expected: `1`

Run: `git diff -- docs/superpowers/process-reviews/notes.md | grep -c "^[+-]- 20"`
Expected: `0` — no line beginning `- 20` (an entry) appears as added or removed. Spec Criterion 5 requires this. A non-zero result means an entry got touched; revert and redo.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/process-reviews/notes.md
git commit -m "feat(process-review): add check-attribution field to notes.md format

Part of docs/superpowers/specs/2026-09-01-convention-retirement-design.md

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Teach `process-review` to read both entry shapes

**Files:**
- Modify: `plugin/skills/process-review/SKILL.md`

**Interfaces:**
- Consumes: Task 1's documented five-field format.
- Produces: the reading rule Task 3's Zero-yield reason depends on.

- [ ] **Step 1: Confirm the anchor**

Run: `grep -c "if the tracker reads \"none yet\"" plugin/skills/process-review/SKILL.md`
Expected: `1`

- [ ] **Step 2: Extend Step 2's reading instruction**

Change:
```markdown
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet").
```
To:
```markdown
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet"). An entry carries either four
   fields (date, Catch, label, finding) or five (date, Catch, label,
   check, finding). Read a four-field entry as carrying no
   attribution: it predates the attribution field, and nothing
   reconstructs which check found it. Read the literal value
   `none — found ad hoc` in a five-field entry the same way — a real
   record that no check produced that Catch, not a missing value.
```

- [ ] **Step 3: Verify**

Run: `grep -c "carrying no attribution" plugin/skills/process-review/SKILL.md`
Expected: `1`

Run: `grep -c "found ad hoc" plugin/skills/process-review/SKILL.md`
Expected: `1` — Task 3 raises this to `2`.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/process-review/SKILL.md
git commit -m "feat(process-review): read four-field and five-field notes.md entries

Part of docs/superpowers/specs/2026-09-01-convention-retirement-design.md

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Add the Retirements section

**Files:**
- Modify: `plugin/skills/process-review/SKILL.md`

**Interfaces:**
- Consumes: Task 2's reading rule, which supplies the attribution the Zero-yield reason needs.
- Produces: the section Task 5's trial exercises.

- [ ] **Step 1: Confirm both anchors**

Run: `grep -c "no Recommendation — the review loop already handled it." plugin/skills/process-review/SKILL.md`
Expected: `1`

Run: `grep -c "instead of forcing a vague Recommendation." plugin/skills/process-review/SKILL.md`
Expected: `1`

- [ ] **Step 2: Add the Retirements section to Step 5's list**

Change:
```markdown
     no Recommendation — the review loop already handled it.
6. Write the review to
```
To:
```markdown
     no Recommendation — the review loop already handled it.
   - **Retirements** — one checkbox item per check or gate this
     review proposes removing. Open the section with the window's
     attribution coverage: how many entries name a check against how
     many read `none — found ad hoc` or carry no check field at all.
     A window where unattributed entries dominate makes Zero-yield
     unusable, and the section says so rather than proposing removals
     the data cannot support. Each item names the check, the proposed
     action, and exactly one reason from this set:
     - **Subsumed** — name the check that already covers it.
     - **Superseded** — name what changed in the mechanism it guards.
     - **Vacuous** — name the precondition that never holds here.
     - **Zero-yield** — no entry attributes a Catch to this check
       across the last 3 reviews, and the check existed at the start
       of that window. State both facts.
     A review that finds nothing to retire writes "None." A reason
     outside this set does not qualify — an open-ended reason lets
     any check get argued away, which turns removal into a tool for
     deleting whatever a reviewer finds inconvenient.
6. Write the review to
```

- [ ] **Step 3: Extend No Placeholders to cover Retirements**

Change:
```markdown
instead of forcing a vague Recommendation.
```
To:
```markdown
instead of forcing a vague Recommendation.

Every Retirement names a real check and a real reason from the fixed
set. A Subsumed reason names the covering check; a Superseded reason
names what changed; a Vacuous reason names the precondition; a
Zero-yield reason states the review count and the check's age. A
reason naming none of these counts as a placeholder, the same as a
vague Recommendation. Proposing a removal on an overlap that does not
hold damages the framework faster than proposing no removal at all.
```

- [ ] **Step 4: Verify**

Run: `grep -c "Subsumed" plugin/skills/process-review/SKILL.md`
Expected: `2` — one in Step 5's reason set, one in No Placeholders.

Run: `grep -c "Zero-yield" plugin/skills/process-review/SKILL.md`
Expected: `2` — same two locations.

Run: `grep -c "found ad hoc" plugin/skills/process-review/SKILL.md`
Expected: `2` — Task 2's Step 2 plus this task's attribution-coverage line.

(These three counts follow from the drafted text above, counted occurrence by occurrence, not from a command run before the edit exists. Step 4 runs them for real.)

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/process-review/SKILL.md
git commit -m "feat(process-review): add advisory Retirements section with four fixed reasons

Part of docs/superpowers/specs/2026-09-01-convention-retirement-design.md

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Require Recommendations to name what they replace

**Files:**
- Modify: `plugin/skills/process-review/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 3 — this edit sits in the Recommendations bullet, above the Retirements section.
- Produces: the addition-time rule that stops accumulation at its source.

- [ ] **Step 1: Confirm the anchor**

Run: `grep -c "A Catch or a one-off outcomes entry" plugin/skills/process-review/SKILL.md`
Expected: `1`

- [ ] **Step 2: Add the rule to the Recommendations bullet**

Change:
```markdown
     docs/ai-code-guidelines.md`. A Catch or a one-off outcomes entry
     alone, with no recurring pattern and no concrete follow-up, needs
     no Recommendation — the review loop already handled it.
```
To:
```markdown
     docs/ai-code-guidelines.md`. A Catch or a one-off outcomes entry
     alone, with no recurring pattern and no concrete follow-up, needs
     no Recommendation — the review loop already handled it. A
     Recommendation that adds a check or a gate names the check it
     replaces, or states `net new load` followed by a one-line
     justification. No Recommendation adds a check silently.
```

- [ ] **Step 3: Verify**

Run: `grep -c "net new load" plugin/skills/process-review/SKILL.md`
Expected: `1`

Run: `grep -c "no Recommendation — the review loop already handled it." plugin/skills/process-review/SKILL.md`
Expected: `1` — the anchor survives, since the addition follows it on the same line.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/process-review/SKILL.md
git commit -m "feat(process-review): require Recommendations to name what they replace

Part of docs/superpowers/specs/2026-09-01-convention-retirement-design.md

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Run the trial that can falsify the design

**Files:**
- Create: `/c/sf-retire-test/` (disposable scratch fixture, outside the repository)

**Interfaces:**
- Consumes: every prior task's committed changes.
- Produces: the trial evidence this plan's outcomes entry records. Nothing later depends on this task.

- [ ] **Step 1: Verify the structural criteria (spec Criteria 1-5)**

```bash
grep -c "check that caught it" docs/superpowers/process-reviews/notes.md
grep -c "found ad hoc" docs/superpowers/process-reviews/notes.md
grep -c "Subsumed" plugin/skills/process-review/SKILL.md
grep -c "Zero-yield" plugin/skills/process-review/SKILL.md
grep -c "carrying no attribution" plugin/skills/process-review/SKILL.md
grep -c "net new load" plugin/skills/process-review/SKILL.md
git log -p --follow -- docs/superpowers/process-reviews/notes.md | grep -c "^-- 20"
```
Expected, in order: `1`, `1`, `2`, `2`, `1`, `1`, `0`. The last confirms that no historical entry ever left the file.

- [ ] **Step 2: Build the fixture with this repository's real files**

Per `docs/patterns/seed-trial-fixtures-with-real-docs.md`, the fixture holds the real docs the skill reads, not a bare scratch repo.

```bash
rm -rf /c/sf-retire-test && mkdir -p /c/sf-retire-test/docs/superpowers/process-reviews /c/sf-retire-test/docs/superpowers/plans /c/sf-retire-test/docs/superpowers/specs
cd /c/sf-retire-test && git init -q
R=/c/Users/marko/IdeaProjects/personal_products/superfunk
cp $R/docs/superpowers/process-reviews/notes.md docs/superpowers/process-reviews/
cp $R/docs/superpowers/process-reviews/tracker.md docs/superpowers/process-reviews/
cp $R/docs/superpowers/plans/*-outcomes.md docs/superpowers/plans/ 2>/dev/null
cp $R/docs/superpowers/specs/2026-08-30-*.md $R/docs/superpowers/specs/2026-09-01-*.md docs/superpowers/specs/
mkdir -p plugin/skills && cp -r $R/plugin/skills/writing-plans $R/plugin/skills/brainstorming plugin/skills/
git add -A && git commit -qm "fixture"
cd - >/dev/null
```

Set the fixture tracker's "Specs shipped since" to three real spec filenames so the review has a window to cover.

- [ ] **Step 3: Run `process-review` against the fixture**

The prompt names no candidate and no reason. Per spec Criterion 8 and `docs/patterns/ab-test-live-trials-for-behavior-change.md` Rule 2, it must not hand the agent its own answer.

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-retire-test. A process review is due. Use the process-review skill and carry it through to writing the review file. Then print the complete review file you wrote, verbatim, between the literal markers ===REVIEW START=== and ===REVIEW END===." > /c/sf-retire-test/trial.txt 2>&1
```

- [ ] **Step 4: Check that a Retirements section appeared (spec Criterion 6)**

```bash
grep -c "Retirements" /c/sf-retire-test/trial.txt
sed -n '/## Retirements/,/^## /p' /c/sf-retire-test/trial.txt
```
Expected: a Retirements section exists, opens with attribution coverage, and either names at least one check with a reason from the fixed set, or states "None."

A run producing "None." does not falsify the design — it means the section fired and found nothing. Record it and note that Criterion 7 then has nothing to check.

- [ ] **Step 5: Independently check every proposed Retirement (spec Criterion 7)**

This step carries the design's real risk. For each Retirement the trial proposed, dispatch a fresh agent given only the proposed Retirement text and read access to the repository — not the trial output, and not this plan:

```
A process review proposed retiring this check:

<paste the single Retirement item verbatim>

Read the relevant skill files in C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin\skills\ and determine whether the stated reason actually holds. For a Subsumed reason, does the named covering check genuinely cover this one's territory? For Superseded, did the named mechanism actually change? For Vacuous, does the precondition genuinely never hold in this project? For Zero-yield, do the stated review count and check age match the real notes.md?

Answer HOLDS or DOES NOT HOLD, then quote the specific file text that decides it. Default to DOES NOT HOLD if the evidence is ambiguous.
```

Expected: every proposed Retirement returns HOLDS.

**A single DOES NOT HOLD falsifies the design.** Stop, do not ship Tasks 3-4, record the invented overlap verbatim in the outcomes file, and report to the user. A Retirements section proposing deletions on overlap that fails checking damages the framework more than shipping no retirement mechanism at all.

- [ ] **Step 6: Clean up**

```bash
rm -rf /c/sf-retire-test
```

- [ ] **Step 7: Record the outcome**

Write the trial's verdict into `docs/superpowers/plans/2026-09-01-convention-retirement-outcomes.md`, including the full Retirements section the trial produced and each independent check's verdict. If Step 5 falsified the design, correct spec Criterion 7 to state what the trial showed, and commit that correction.

---

## Self-Review

**1. Spec coverage:** Decision section 1 (attribution field, `none — found ad hoc`, no backfill) → Task 1. Section 2 (Retirements section, four fixed reasons, 3-review threshold, attribution coverage) → Task 3 Step 2. Section 3 (Recommendations name what they replace) → Task 4. Section 4 (enforcement) → Task 3 Step 3's No Placeholders extension, plus Task 2's reading rule. Criteria 1-5 → Task 5 Step 1. Criterion 6 → Task 5 Step 4. Criterion 7 → Task 5 Step 5. Criterion 8 → Task 5 Step 3's prompt, which names no candidate. No spec requirement lacks a task.

**2. Placeholder scan:** No "TBD", "TODO", or "similar to Task N". Task 5 Step 5 contains a `<paste the single Retirement item verbatim>` slot, which the trial's own output fills at runtime — the surrounding prompt text stays complete. Every edit shows full before-and-after content.

**3. Type consistency:** The four reason names — Subsumed, Superseded, Vacuous, Zero-yield — appear identically in Task 3 Step 2, Task 3 Step 3, and Task 5 Step 5's checking prompt. The literal `none — found ad hoc` appears identically in Task 1 Step 2, Task 2 Step 2, and Task 3 Step 2. Checked each against the others.

**4. Pseudocode coverage:** All four triggers stated, each `Skipped:` with a reason naming a real absence rather than restating the trigger name.

**5. Sibling-pattern parity:** Task 3's Retirements bullet mirrors its five sibling section bullets in Step 5 — bold name, em-dash, then what the section contains and what qualifies for it. Task 3 Step 3's No Placeholders paragraph mirrors the existing paragraph's shape: what the entry must name, then what counts as a violation. Task 4's addition continues the Recommendations bullet's existing sentence rhythm.

**6. Rule-restatement accuracy:** The four reasons appear in two places — Task 3 Step 2 defines them, Task 3 Step 3 states what each must name. Read side by side, the second restates the first's requirements without narrowing or broadening any. The `none — found ad hoc` value appears in three places, each with a different verb on the same value:

- `notes.md`'s format explanation — how to write it
- `process-review` Step 2 — how to read it
- the Retirements attribution line — how to count it

Read side by side, the three describe one value from three angles without contradicting each other.

**7. Lessons-learned check:** Read `docs/lessons-learned.md`. Four entries apply. The numeric-verification entries drove running every baseline in this plan against real content this session — all six `grep -c` baselines returned `0`, confirmed. The quote-verification entry drove reading `process-review`'s Step 2 and Recommendations text directly rather than citing an earlier read. The newest entry says a negative trial result needs its scenario checked. That drove Task 5 Step 4's note that a "None." result does not falsify the design, so a quiet run avoids getting misread as a failure.

**8. Cross-section mechanism consistency:** Tasks 2, 3, and 4 all edit routing and lifecycle language in one file. Grepped `plugin/skills/process-review/SKILL.md` for every mention of `notes.md`, "Recommendations", and "section" and read each hit. The description line at `:3` lists what the skill synthesizes and does not enumerate output sections, so adding a sixth does not contradict it. Step 6 writes the review file and names no section list. `plugin/skills/process-review/` holds no other top-level file. `brainstorming/SKILL.md:68` and `subagent-driven-development` both invoke `process-review` on triggers this plan does not change.

**9. Worked-example currency:** Task 3 adds a section to Step 5's list without reordering Steps 1-8. `process-review/SKILL.md` carries no worked example demonstrating its output, so none needs updating. `subagent-driven-development`'s Example Workflow does not depict process-review's output sections — a known pre-existing gap recorded in `notes.md` on 2026-08-27, not introduced here.

**10. Verified numeric expectations:** Every pre-edit baseline came from running the command this session. Verified:

- `Subsumed`, `Zero-yield`, `net new load`, `found ad hoc`, `Retirement`, and `carrying no attribution` each return `0` in `process-review/SKILL.md`
- `check that caught it`, `found ad hoc`, and `four fields` each return `0` in `notes.md`
- `^Format:` returns one match, at line 9
- the three Task 2-4 edit anchors each return `1`

Task 3 Step 4's post-edit counts (`2`, `2`, `2`) follow from counting occurrences in the drafted text. That step states as much, and runs the commands for real rather than presenting the prediction as a measurement.

**11. Template compliance:** This plan's header carries Goal, Architecture, Tech Stack, and Global Constraints, checked against `writing-plans/SKILL.md`'s Plan Document Header section.

**12. User-facing documentation timing:** The spec carries `User-Facing: No`. This item does not apply.

**13. Hostile-input pass:** Task 5 Step 2's `rm -rf /c/sf-retire-test` does not handle the path holding unrelated work; the path stays scratch-only and carries this trial's name. Its `cp $R/docs/superpowers/specs/2026-08-30-*.md` glob fails silently when no file matches, leaving the fixture thinner than intended. Step 4 surfaces that, since a review with no specs to cover produces an empty window. Task 1 Step 2's edit does not handle a `notes.md` whose format line already changed; Step 1 guards it by confirming exactly one `^Format:` match first. Task 5 Step 3's prompt contains double quotes inside a double-quoted shell string — it uses only the literal markers and no inner quotes, verified by reading it. Recorded rather than handled, since each names a single-operator scratch path.

**14. Stale-workaround grep:** No task removes a limitation from a tool. Task 1 replaces `notes.md`'s old four-field format line, and Task 1 Step 3 verifies the new phrase lands. That old format text names no error message or docstring a user would have hit, so it falls outside this item's trigger. Grepped the repository for the old format line's distinctive words outside `notes.md` itself. `process-review/SKILL.md` describes the entry shape in prose rather than reproducing the format string, and Task 2 updates that prose in the same plan. No stale reference survives.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-01-convention-retirement.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
