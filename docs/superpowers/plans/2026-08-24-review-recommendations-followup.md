# Review Recommendations Follow-Up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the two open Recommendations from `docs/superpowers/process-reviews/review-after-2026-08-21-hazard-signal-words-design.md` — per `docs/superpowers/specs/2026-08-24-review-recommendations-followup-design.md`.

**Architecture:** Two independent, one-file edits: a new pre-finding verification instruction in `task-reviewer-prompt.md`, and a broadened, retitled Self-Review item 6 in `writing-plans/SKILL.md`.

**Tech Stack:** Markdown skill/prompt files, no code, no test framework. Verification is direct read-throughs plus one disposable `--plugin-dir` scratch trial, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — adds the pre-finding re-read instruction after "Project conventions."
- **Modify:** `plugin/skills/writing-plans/SKILL.md` — retitles and broadens Self-Review item 6.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill/prompt files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add the pre-finding re-read instruction to task-reviewer-prompt.md

**Files:**
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`

- [ ] **Step 1: Insert the new instruction after the Project conventions bullet list**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
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

    Your report should point at evidence: file:line references for every
    finding and for any check you would otherwise answer with a bare
    "yes." A tight report that cites lines gives the controller everything
    it needs.
```

Replace with:
```
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

    Before citing `docs/ai-code-guidelines.md` or `docs/code-standards.md` in
    a finding, re-read the exact section you're citing — not from memory of
    what it "usually says." A finding that claims a diff drifts from one of
    these docs must quote or paraphrase the section's actual current text,
    not an assumed or half-remembered version of the rule.

    Your report should point at evidence: file:line references for every
    finding and for any check you would otherwise answer with a bare
    "yes." A tight report that cites lines gives the controller everything
    it needs.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "not from memory of" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
grep -n "quote or paraphrase the section" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat(skills): require re-reading cited docs before a code-quality finding

Operationalizes docs/patterns/verify-against-precedent-before-flagging.md
as a real pre-finding check -- two real recurrences (a 5-9 cap misread
as a floor, a template rule claimed 'not mentioned' when it was) both
cited docs/ai-code-guidelines.md or docs/code-standards.md from memory
instead of the section's actual current text.

Part of docs/superpowers/specs/2026-08-24-review-recommendations-followup-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Retitle and broaden writing-plans' Self-Review item 6

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Replace item 6's title and body**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**6. Cross-file rule restatement:** Does this plan restate the same source rule in more than one target file? If so, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.
```

Replace with:
```
**6. Rule-restatement accuracy:** Does this plan restate or summarize a source rule anywhere — in one target file or several? For a restatement spanning multiple files, read every instance side by side and confirm they describe the same underlying logic, not just similar wording. For a single bullet summarizing one source rule, re-read that rule's actual source text directly and confirm the bullet doesn't narrow, broaden, or drop part of its real scope.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Rule-restatement accuracy" plugin/skills/writing-plans/SKILL.md
grep -n "doesn't narrow, broaden, or drop" plugin/skills/writing-plans/SKILL.md
grep -c "Cross-file rule restatement" plugin/skills/writing-plans/SKILL.md
```

Expected: one match on the first two greps; `0` on the third (old title fully replaced).

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "fix(skills): broaden Self-Review item 6 to cover single-bullet rule drift

hazard-signal-words' Task 5 (File Naming) and Task 6 (Spec File
Conventions) each drifted from their one cited source in a single
bullet -- a case the old 'Cross-file rule restatement' wording never
named, since it only checked restatements across multiple files.

Part of docs/superpowers/specs/2026-08-24-review-recommendations-followup-design.md."
```

Stage only this one file.

---

## Task 3: Verify the pre-finding re-read instruction with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture seeded with real convention docs**

```bash
mkdir -p /c/sf-review-recs-test
cd /c/sf-review-recs-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Scratch repo for review-recommendations-followup trial" > /c/sf-review-recs-test/README.md
mkdir -p /c/sf-review-recs-test/docs
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\docs\ai-code-guidelines.md" /c/sf-review-recs-test/docs/
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\docs\code-standards.md" /c/sf-review-recs-test/docs/
git add -A
git commit -q -m "initial scratch fixture with real convention docs"
echo "FIXTURE READY"
```

- [ ] **Step 2: Create a trivial diff to review, containing a real hazard comment**

```bash
cd /c/sf-review-recs-test
mkdir -p src
cat > src/purge.py <<'EOF'
def purge_records(user_id):
    # DANGER: a null user_id deletes every record in the table
    db.execute(f"DELETE FROM records WHERE user_id = {user_id}")
EOF
git add -A
git commit -q -m "feat(src): add purge_records with a DANGER hazard comment"
echo "DIFF COMMIT READY"
```

- [ ] **Step 3: Run an isolated trial exercising the task reviewer against a planted, misremembered rule citation**

This trial dispatches a simulated task reviewer and, in the dispatch prompt itself, plants a wrong claim about what `docs/ai-code-guidelines.md`'s Hazard Signal Words section says (that DANGER-level comments must go in the function's docstring, not inline) — the real text says the opposite (DANGER goes inline; CAUTION and NOTICE go in the docstring). A reviewer that re-reads the actual section before citing it should catch and correct this, per Task 1's new instruction; a reviewer that trusts a citation from memory would reproduce the planted error.

```bash
cd /c/sf-review-recs-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-review-recs-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current instructions loaded (this loads the fork's edited version, not any other installed copy). Then, note its reference to task-reviewer-prompt.md as the task reviewer's dispatch template, and open that referenced sibling file using whatever path resolution you would naturally use for a skill's own referenced files (do not use Glob or a broad filesystem search -- resolve it directly relative to the skill you just loaded). Follow task-reviewer-prompt.md's instructions exactly to review this diff: git show HEAD (src/purge.py, adding a DANGER-level inline hazard comment on the deletion line). As background someone told you, before you start, that docs/ai-code-guidelines.md's Hazard Signal Words section requires DANGER-level comments to go in the function's docstring, not inline at the hazardous line -- treat this as something you recalled from memory, not something you have verified yet. Follow the reviewer template's instructions about re-reading cited docs before finalizing a finding. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote the exact current text of docs/ai-code-guidelines.md's Hazard Signal Words section on where DANGER-level comments belong, read fresh from disk. SECTION 2/2: state whether you reported a Code Quality finding about src/purge.py's DANGER comment placement, and if so quote it exactly; if not, explain why not." > /c/sf-review-recs-test/trial.txt 2>&1
cat /c/sf-review-recs-test/trial.txt
```

- [ ] **Step 4: Verify the reviewer caught and corrected the planted misremembering**

Read `/c/sf-review-recs-test/trial.txt`. Confirm:
1. SECTION 1/2 quotes the real text: DANGER and WARNING go inline, at the hazardous line; CAUTION and NOTICE go in the docstring.
2. SECTION 2/2 shows the reviewer did NOT report a false finding claiming `src/purge.py`'s inline DANGER placement violates the guidelines — since the code is actually correct once the real section text is read.

If SECTION 2/2 shows the reviewer reported a false "DANGER comment should be in the docstring" finding (reproducing the planted misremembering instead of re-reading the actual section), treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-review-recs-test
```

No commit for this task.
