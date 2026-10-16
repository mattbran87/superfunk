# Dispatch Claim Check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship ArcGISProMCP findings A4 and A10 as the spec decides: the implementer checks the controller's Context claims against the tree, and the controller keeps its own text under Context.

**Architecture:** One task. It adds one paragraph to `implementer-prompt.md`, one sentence to SDD Step 1, one watchlist entry, and one release-note bullet under a new `## v6.9.0 (unreleased)` heading. Finish dates that heading and updates the findings file's response section.

**Tech Stack:** Markdown skill files, git, bash, Python 3 (`check_docs.py`).

**Spec:** `docs/superpowers/specs/2026-10-15-dispatch-claim-check-design.md`

## Global Constraints

- Spec carries `User-Facing: Yes`. The task runs `check_docs.py` over its own range and opens the `## v6.9.0 (unreleased)` entry in `plugin/RELEASE-NOTES.md`, in the same task.
- No trial (spec Decision 3).
- In `plugin/RELEASE-NOTES.md`, everything from `## v6.8.0 (2026-10-15)` down stays byte-identical.
- Every target file uses LF line endings. Keep them. Write em dashes (—) as the literal character.
- The commit carries the trailer `Part of docs/superpowers/specs/2026-10-15-dispatch-claim-check-design.md`.
- The spec's quotes of both new sentences must match the shipped text word for word, apart from line wraps (spec criterion 4).
- Finish bumps to 6.9.0 (minor), dates the v6.9.0 heading in the bump commit, and changes the findings file's "In progress" line for A4 and A10 (spec criterion 5).

---

## File Structure

`.context.md` check: none exists in any directory this plan touches. Checked: `plugin/skills/subagent-driven-development/`, `docs/superpowers/process-reviews/`, `plugin/`.

| File | Change |
|---|---|
| `plugin/skills/subagent-driven-development/implementer-prompt.md` | One paragraph under the `## Context` placeholder |
| `plugin/skills/subagent-driven-development/SKILL.md` | One sentence in Step 1's "Task brief" bullet |
| `docs/superpowers/process-reviews/watchlist.md` | Eighth entry |
| `plugin/RELEASE-NOTES.md` | Opens `## v6.9.0 (unreleased)` with one bullet |

## Pseudocode

- **T1 — API call sites:** Skipped: the task calls no API; it edits Markdown.
- **T2 — Handler/pattern reuse:** Skipped: the watchlist entry copies the file's documented four-line format, and the plan gives it verbatim.
- **T3 — DTO/schema shape:** Skipped: no data shape changes.
- **T4 — User-designated:** Skipped: the human partner designated no piece of this plan for pseudocode.

---

### Task 1: Dispatch claim check

**Files:**
- Modify: `plugin/skills/subagent-driven-development/implementer-prompt.md:28`
- Modify: `plugin/skills/subagent-driven-development/SKILL.md:222-224` (Step 1, "Task brief" bullet)
- Modify: `docs/superpowers/process-reviews/watchlist.md` (append)
- Modify: `plugin/RELEASE-NOTES.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the `## v6.9.0 (unreleased)` heading, which Finish dates.

- [ ] **Step 1: Add the implementer-side paragraph**

In `plugin/skills/subagent-driven-development/implementer-prompt.md`, replace (4-space indent):

```
    [Scene-setting: where this fits, dependencies, architectural context]
```

with:

```
    [Scene-setting: where this fits, dependencies, architectural context]

    The controller wrote this section, not the plan. It may carry a claim
    from memory of earlier tasks: a type or file that exists, a count, a
    line number, a commit. Check each such claim against the tree before
    you rely on it. If one does not match, say so in your report rather
    than build around it.
```

- [ ] **Step 2: Add the controller-side placement sentence**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace (2-space indent):

```
  (5) the report-file path and report contract. Exact values (numbers,
  magic strings, signatures, test cases) appear only in the brief. Never
  make a subagent read the whole plan file.
```

with:

```
  (5) the report-file path and report contract. Put parts (1), (3), and
  (4) under the template's Context heading. The implementer checks that
  section's claims against the tree, so a claim you place anywhere else
  skips that check. Exact values (numbers, magic strings, signatures,
  test cases) appear only in the brief. Never make a subagent read the
  whole plan file.
```

- [ ] **Step 3: Add the watchlist entry**

In `docs/superpowers/process-reviews/watchlist.md`, directly after the last line of the `fix-dispatch-copy-listing` entry (the line that begins `  - Action when tripped: trial-gate the M2 sentence`), append:

```
- **dispatch-claim-check** (added 2026-10-15, dispatch-claim-check)
  - Watching: the implementer-prompt sentence that tells an implementer to check the controller's Context claims against the tree.
  - Trigger: a review or an outcomes entry finds a false controller claim in a dispatch that the implementer built on without reporting it.
  - Action when tripped: trial-gate the sentence per `docs/patterns/ab-test-live-trials-for-behavior-change.md`, or rewrite it.
```

- [ ] **Step 4: Open the v6.9.0 entry**

In `plugin/RELEASE-NOTES.md`, directly above the line `## v6.8.0 (2026-10-15)`, insert:

```
## v6.9.0 (unreleased)

- **Implementers check the controller's Context claims against the tree.** The implementer template marks its Context section as controller-written. An implementer checks each existence claim, count, line number, or commit there before it relies on the claim, and it reports any mismatch. A new watchlist entry tracks whether this works.

```

- [ ] **Step 5: Check the edits (spec criteria 1–4)**

```bash
cd /c/Users/marko/IdeaProjects/personal_products/superfunk
python - <<'EOF'
import re
def flat(p): return re.sub(r'\s+', ' ', open(p, encoding='utf-8').read())
ip = open('plugin/skills/subagent-driven-development/implementer-prompt.md', encoding='utf-8').read()
seg = ip[ip.index('## Context'):ip.index('## Before You Begin')]
print(re.sub(r'\s+', ' ', seg).count('The controller wrote this section, not the plan.'),
      flat('plugin/skills/subagent-driven-development/implementer-prompt.md').count('The controller wrote this section, not the plan.'))
print(flat('plugin/skills/subagent-driven-development/SKILL.md').count("Put parts (1), (3), and (4) under the template's Context heading."))
spec = flat('docs/superpowers/specs/2026-10-15-dispatch-claim-check-design.md')
print(spec.count("If one does not match, say so in your report rather than build around it."),
      spec.count("so a claim you place anywhere else skips that check."))
EOF
grep -c "^- \*\*[a-z0-9-]*\*\* (added 20" docs/superpowers/process-reviews/watchlist.md
grep -A3 "^- \*\*dispatch-claim-check\*\*" docs/superpowers/process-reviews/watchlist.md | grep -c -E "^  - (Watching|Trigger|Action when tripped):"
grep -n "^## v" plugin/RELEASE-NOTES.md | head -2
diff <(git show HEAD:plugin/RELEASE-NOTES.md | sed -n '/^## v6.8.0/,$p') <(sed -n '/^## v6.8.0/,$p' plugin/RELEASE-NOTES.md) && echo BELOW-IDENTICAL
```

Expected:
- `1 1`: the paragraph appears once, and that one sits inside the Context section.
- `1`: the placement sentence appears once.
- `1 1`: the spec quotes both sentences.
- `8`, then `3`.
- `## v6.9.0 (unreleased)`, then `## v6.8.0 (2026-10-15)`.
- `BELOW-IDENTICAL`.

- [ ] **Step 6: Cross-section check (Self-Review item 8)**

Run: `grep -n -i "context" plugin/skills/subagent-driven-development/SKILL.md plugin/skills/subagent-driven-development/implementer-prompt.md | grep -v -i "context-mode\|\.context\.md"`

Read each hit. SDD's Step 1 bullets for Directory context, Pseudocode context, and Concept-index context each tell the controller to fold its findings "into the dispatch's Context section". They therefore already put controller text under Context, which the new sentence requires. A hit that tells the controller to place its own claims outside Context contradicts the new sentence. Report each hit and your judgment, and fix a contradiction in this step.

- [ ] **Step 7: Commit and run the docs check**

```bash
git add plugin/skills/subagent-driven-development/implementer-prompt.md plugin/skills/subagent-driven-development/SKILL.md docs/superpowers/process-reviews/watchlist.md plugin/RELEASE-NOTES.md
git commit -m "feat(subagent-driven-development): have implementers check the controller's Context claims against the tree

Part of docs/superpowers/specs/2026-10-15-dispatch-claim-check-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-dispatch-claim-check-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.
