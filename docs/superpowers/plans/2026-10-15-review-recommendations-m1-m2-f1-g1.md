# Review Recommendations M1, M2, F1, G1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the four open Recommendations of `review-after-2026-10-15-watchlist-and-findings-batch-design.md` — five-field write-site templates (M1), copy-listing in fix dispatches (M2), reading `process-review` from disk (F1), and plural Recommendation check-off (G1).

**Architecture:** Three tasks, each one a set of exact-text edits to skill files plus one release-note bullet. Task 1 opens a `## v6.8.0 (unreleased)` entry, Tasks 2 and 3 add bullets under it, and Finish dates it in the bump commit.

**Tech Stack:** Markdown skill files, git, bash, Python 3 (`check_docs.py`).

**Spec:** `docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md`

## Global Constraints

- Spec carries `User-Facing: Yes`. Every task runs `check_docs.py` over its own range and adds its own bullet under `## v6.8.0 (unreleased)` in `plugin/RELEASE-NOTES.md`, in the same task.
- No trials (spec Decision 2).
- The two final-review templates (`subagent-driven-development/SKILL.md`, `executing-plans/SKILL.md`) match byte for byte.
- F1 and G1 land in both SDD Finish and `executing-plans` Step 3, worded the same way (spec Decision 4).
- Entries already in `docs/superpowers/process-reviews/notes.md` stay as written. Only the header above `<!-- entries below this line -->` changes.
- In `plugin/RELEASE-NOTES.md`, everything from `## v6.7.0 (2026-10-15)` down stays byte-identical.
- Every target file uses LF line endings. Keep them. Write em dashes (—) as the literal character.
- Every commit carries the trailer `Part of docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md`.
- When a step changes text that describes a mechanism, grep the spec for its quote of that text, and confirm that the quote and the shipped text say the same thing (`docs/patterns/self-apply-cross-section-check-to-hand-fixes.md`).
- Finish bumps to 6.8.0 (minor) and replaces `## v6.8.0 (unreleased)` with `## v6.8.0 (<bump date>)` in the bump commit.

---

## File Structure

`.context.md` check: none exists in any directory this plan touches. Checked: `plugin/skills/subagent-driven-development/`, `plugin/skills/executing-plans/`, `plugin/skills/process-review/`, `docs/superpowers/process-reviews/`, `plugin/`.

| File | Task | Change |
|---|---|---|
| `plugin/skills/subagent-driven-development/SKILL.md` | 1, 2, 3 | Task 1: two templates; Task 2: the M2 sentence twice; Task 3: F1 clause and G1 wording in Finish |
| `plugin/skills/executing-plans/SKILL.md` | 1, 3 | Task 1: the final-review template; Task 3: F1 clause and G1 wording in Step 3 |
| `plugin/skills/process-review/SKILL.md` | 1 | Step 2's four-field sentence |
| `docs/superpowers/process-reviews/notes.md` | 1 | Header paragraph about four-field entries |
| `docs/superpowers/process-reviews/watchlist.md` | 2 | Seventh entry |
| `plugin/RELEASE-NOTES.md` | 1, 2, 3 | Task 1 opens v6.8.0; each task adds one bullet |

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an API; every task edits Markdown.
- **T2 — Handler/pattern reuse:** Skipped: the new template lines copy the five-field shape the `notes.md` header already defines, and the plan gives each line verbatim.
- **T3 — DTO/schema shape:** Skipped: the five-field entry shape already exists in the `notes.md` type table; this plan changes no field.
- **T4 — User-designated:** Skipped: the human partner designated no piece of this plan for pseudocode.

---

### Task 1: Five-field write-site templates (M1)

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md:365`, `:537`
- Modify: `plugin/skills/executing-plans/SKILL.md:61`
- Modify: `plugin/skills/process-review/SKILL.md:43-45` (step 2)
- Modify: `docs/superpowers/process-reviews/notes.md:30-32` (header)
- Modify: `plugin/RELEASE-NOTES.md` (open the v6.8.0 entry)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the heading `## v6.8.0 (unreleased)` and its first bullet, which Tasks 2 and 3 append after.

- [ ] **Step 1: Change the fix-loop template**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
`- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`.
```

with:

```
`- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <check that caught it> | <one-line finding>`.
```

- [ ] **Step 2: Change both final-review templates**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
(`- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`), then
```

with:

```
(`- <YYYY-MM-DD> | Catch | Final review (<plan-slug>) | <check that caught it> | <one-line finding>`), then
```

In `plugin/skills/executing-plans/SKILL.md`, replace (3-space indent):

```
   (`- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`), then
```

with:

```
   (`- <YYYY-MM-DD> | Catch | Final review (<plan-slug>) | <check that caught it> | <one-line finding>`), then
```

- [ ] **Step 3: Correct the four-field claim in `process-review` step 2**

In `plugin/skills/process-review/SKILL.md`, replace:

```
   check, finding). Read a four-field entry as carrying no
   attribution: it predates the attribution field, and nothing
   reconstructs which check found it.
```

with:

```
   check, finding). Read a four-field entry as carrying no
   attribution: it predates the attribution field, or it came from a
   write-site template that still showed four fields (through
   2026-10-15), and nothing reconstructs which check found it.
```

- [ ] **Step 4: Correct the four-field claim in the `notes.md` header**

In `docs/superpowers/process-reviews/notes.md`, replace:

```
Entries below dated before 2026-09-01 carry four fields, without the
check field. They stay as written
```

with:

```
Entries below dated before 2026-09-01 carry four fields, without the
check field, and so do six later entries copied from write-site
templates that still showed four fields (fixed 2026-10-15). They stay
as written
```

The rest of that paragraph (` — reconstructing attribution from` / `memory would fabricate it.`) stays unchanged.

- [ ] **Step 5: Open the v6.8.0 entry**

In `plugin/RELEASE-NOTES.md`, directly above the line `## v6.7.0 (2026-10-15)`, insert:

```
## v6.8.0 (unreleased)

- **`notes.md` write-site templates show all five fields.** The fix-loop and final-review templates in `subagent-driven-development` and `executing-plans` now carry the check field, and a final-review entry names its plan. `process-review` no longer reads every four-field entry as older than 2026-09-01.

```

The Fork note above stays unchanged.

- [ ] **Step 6: Check the edits (spec criteria 1–3)**

```bash
cd /c/Users/marko/IdeaProjects/personal_products/superfunk
S=plugin/skills/subagent-driven-development/SKILL.md; E=plugin/skills/executing-plans/SKILL.md
grep -c "| Catch | Final review | <one-line finding>" $S $E
grep -c "<check that caught it> | <one-line finding>" $S $E
diff <(grep -o "(\`- <YYYY-MM-DD> | Catch | Final review (<plan-slug>).*finding>\`)" $S) <(grep -o "(\`- <YYYY-MM-DD> | Catch | Final review (<plan-slug>).*finding>\`)" $E) && echo IDENTICAL
grep -c "write-site template" plugin/skills/process-review/SKILL.md
grep -c "write-site" docs/superpowers/process-reviews/notes.md
git diff -U0 -- docs/superpowers/process-reviews/notes.md | grep -c '^[-+]- 20'
grep -n "^## v" plugin/RELEASE-NOTES.md | head -2
```

Expected: `0` and `0`; `2` and `1`; `IDENTICAL`; `1`; `1`; `0`; then `## v6.8.0 (unreleased)` followed by `## v6.7.0 (2026-10-15)`.

- [ ] **Step 7: Check the spec's quotes (Global Constraints)**

Run: `grep -n "write-site template\|Final review (<plan-slug>)" docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md`

Read each hit. Each spec quote of the Step 1–4 texts must say what the shipped text says. Report any difference; do not edit the spec.

- [ ] **Step 8: Commit and run the docs check**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md plugin/skills/process-review/SKILL.md docs/superpowers/process-reviews/notes.md plugin/RELEASE-NOTES.md
git commit -m "fix(skills): show all five fields in the notes.md write-site templates

Part of docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.

---

### Task 2: Name every copy in a fix dispatch (M2)

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md` (fix loop "Every round, either way" paragraph; Final Review fix-dispatch paragraph)
- Modify: `docs/superpowers/process-reviews/watchlist.md` (append one entry)
- Modify: `plugin/RELEASE-NOTES.md` (one bullet)

**Interfaces:**
- Consumes: Task 1's `## v6.8.0 (unreleased)` bullet.
- Produces: nothing a later task reads.

- [ ] **Step 1: Add the M2 sentence to the fix loop**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
output; dispatch the re-review once all three are present. Name the
covering test files in the fix message — a one-line fix does not need the
whole suite.
```

with:

```
output; dispatch the re-review once all three are present. Name the
covering test files in the fix message — a one-line fix does not need the
whole suite. When a finding changes text that describes a mechanism, name
every copy of that text in the fix dispatch — sibling files and the design
spec's own quotes — found with a search for each key term, not for one
phrase.
```

- [ ] **Step 2: Add the M2 sentence to the Final Review**

In the same file, replace:

```
dispatch ONE fix subagent with the complete findings list — not one
fixer per finding.
```

with:

```
dispatch ONE fix subagent with the complete findings list — not one
fixer per finding. When a finding changes text that describes a mechanism,
name every copy of that text in the fix dispatch — sibling files and the
design spec's own quotes — found with a search for each key term, not for
one phrase.
```

- [ ] **Step 3: Add the watchlist entry**

In `docs/superpowers/process-reviews/watchlist.md`, directly after the last line of the `g3-attribution-coverage` entry (the line that begins `  - Action when tripped: raise a Recommendation that targets each write site`), append:

```
- **fix-dispatch-copy-listing** (added 2026-10-15, review-recommendations-m1-m2-f1-g1)
  - Watching: the M2 sentence in `subagent-driven-development`'s fix loop and Final Review.
  - Trigger: a scoped re-review finds a stale copy of text that a fix dispatch changed.
  - Action when tripped: trial-gate the M2 sentence per `docs/patterns/ab-test-live-trials-for-behavior-change.md`, or rewrite it.
```

- [ ] **Step 4: Add this task's bullet**

In `plugin/RELEASE-NOTES.md`, directly after Task 1's bullet (the line that begins `- **\`notes.md\` write-site templates show all five fields.**`), insert:

```
- **Fix dispatches name every copy of the text they change.** When a finding changes text that describes a mechanism, the controller lists each copy — sibling files and the design spec's own quotes — in the fix dispatch. A new watchlist entry tracks whether this works.
```

- [ ] **Step 5: Check the edits (spec criteria 4–5)**

```bash
cd /c/Users/marko/IdeaProjects/personal_products/superfunk
python -c "import re;print(re.sub(r'\s+',' ',open('plugin/skills/subagent-driven-development/SKILL.md',encoding='utf-8').read()).count('name every copy of that text in the fix dispatch'))"
grep -c "^- \*\*[a-z0-9-]*\*\* (added 20" docs/superpowers/process-reviews/watchlist.md
grep -A3 "fix-dispatch-copy-listing" docs/superpowers/process-reviews/watchlist.md | grep -c -E "^  - (Watching|Trigger|Action when tripped):"
sed -n '/^## v6.8.0/,/^## v6.7.0/p' plugin/RELEASE-NOTES.md | grep -c "^- "
```

Expected: `2`; `7`; `3`; `2`.

- [ ] **Step 6: Check the spec's quote (Global Constraints)**

Run: `grep -n "name every copy of that text" docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md`

The spec's M2 blockquote must carry the same words as the two shipped copies. Report any difference; do not edit the spec.

- [ ] **Step 7: Commit and run the docs check**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md docs/superpowers/process-reviews/watchlist.md plugin/RELEASE-NOTES.md
git commit -m "feat(subagent-driven-development): name every copy of changed mechanism text in fix dispatches, and watch it

Part of docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.

---

### Task 3: Read `process-review` from disk, and check off every closed Recommendation (F1, G1)

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md` (Finish: the process-review offer, the Recommendation check-off, the third-check lead-in)
- Modify: `plugin/skills/executing-plans/SKILL.md` (Step 3 items 3, 4, and 5)
- Modify: `plugin/RELEASE-NOTES.md` (one bullet)

**Interfaces:**
- Consumes: Task 2's bullet under `## v6.8.0 (unreleased)`.
- Produces: the plural check-off wording that this batch's own Finish uses (spec criterion 8).

- [ ] **Step 1: Add the F1 clause to SDD Finish**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue.
```

with:

```
in this process. Run it if your human partner agrees; otherwise leave
the tracker as-is and continue. If this branch changed
`plugin/skills/process-review/`, follow that file as read from disk,
because the Skill tool serves the text loaded at session start.
```

- [ ] **Step 2: Make the SDD check-off plural**

In the same file, replace:

```
holds the Recommendation this spec closes. Open it, find the matching
`- [ ]` Recommendation by content, and check it off: change it to
```

with:

```
holds the Recommendations this spec closes. Open it, find each matching
`- [ ]` Recommendation by content, and check off every one this spec
closes: change it to
```

Then replace:

```
Run the third check only when a review file was named above. Each
```

with:

```
Run the third check only when a review file was named above, once
per Recommendation this spec closes. Each
```

- [ ] **Step 3: Add the F1 clause to `executing-plans` Step 3 item 3**

In `plugin/skills/executing-plans/SKILL.md`, replace (3-space indent):

```
   list, in the same commit. At 3 or more entries, offer to run
   superfunk:process-review now — ask, don't force.
```

with:

```
   list, in the same commit. At 3 or more entries, offer to run
   superfunk:process-review now — ask, don't force. If this branch
   changed `plugin/skills/process-review/`, follow that file as read
   from disk, because the Skill tool serves the text loaded at session
   start.
```

- [ ] **Step 4: Make the `executing-plans` check-off plural**

In the same file, replace:

```
   `review-after-*.md` file, find the matching `- [ ]` line, change it
   to `- [x]`, and append
```

with:

```
   `review-after-*.md` file, find each matching `- [ ]` line this spec
   closes, change it to `- [x]`, and append
```

Then replace:

```
   Each applicable check returns at least 1. A 0 means that action never
   happened — do it now.
```

with:

```
   Run the third check once per Recommendation this spec closes. Each
   applicable check returns at least 1. A 0 means that action never
   happened — do it now.
```

- [ ] **Step 5: Add this task's bullet**

In `plugin/RELEASE-NOTES.md`, directly after Task 2's bullet (the line that begins `- **Fix dispatches name every copy of the text they change.**`), insert:

```
- **Finish checks off every Recommendation a spec closes.** Both Finish paths now find each matching Recommendation and verify each one. Before a branch that changed `process-review` runs a review, Finish reads that skill from disk, because the Skill tool serves the copy loaded at session start.
```

- [ ] **Step 6: Check the edits (spec criteria 6–7)**

```bash
cd /c/Users/marko/IdeaProjects/personal_products/superfunk
for f in plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md; do
  python -c "import re,sys;t=re.sub(r'\s+',' ',open(sys.argv[1],encoding='utf-8').read());print(t.count('follow that file as read from disk'), t.count('find the matching \`- [ ]\`'), t.count('find each matching \`- [ ]\`'), t.count('once per Recommendation this spec closes'))" $f
done
sed -n '/^## v6.8.0/,/^## v6.7.0/p' plugin/RELEASE-NOTES.md | grep -c "^- "
diff <(git show HEAD:plugin/RELEASE-NOTES.md | sed -n '/^## v6.7.0/,$p') <(sed -n '/^## v6.7.0/,$p' plugin/RELEASE-NOTES.md) && echo BELOW-IDENTICAL
```

Expected: `1 0 1 1` for each of the two files; `3`; `BELOW-IDENTICAL`.

- [ ] **Step 7: Cross-section check (Self-Review item 8)**

Run: `grep -n -i "Recommendation" plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md`

Read each hit. A hit that still treats the check-off as one Recommendation per spec contradicts the new wording. Fix such a hit in this step. The SDD worked-example line `[Finish: no Recommendation to check off -- ...]` states the zero case, so it stays.

- [ ] **Step 8: Check the spec's quotes (Global Constraints)**

Run: `grep -n "read from disk\|find each matching" docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md`

Each spec quote must carry the same words as the shipped text. Report any difference; do not edit the spec.

- [ ] **Step 9: Commit and run the docs check**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md plugin/RELEASE-NOTES.md
git commit -m "fix(skills): read process-review from disk when the branch changed it, and check off every closed Recommendation

Part of docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-review-recommendations-m1-m2-f1-g1-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.
