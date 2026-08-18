# Design Spec Template Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Formalize the design-spec `Status` lifecycle with real triggers, add a required Consequences section and a conditional Alternatives Considered section, and retroactively fix the four already-stale specs — per `docs/superpowers/specs/2026-08-13-design-spec-template-quality-design.md`.

**Architecture:** Two skill-file edits (`brainstorming/SKILL.md`'s Documentation step gets the Status/Consequences/Alternatives-Considered/Superseded-by guidance; `subagent-driven-development/SKILL.md`'s Finish step gets the Shipped trigger), plus a plain markdown edit to four existing spec files.

**Tech Stack:** Markdown skill files and markdown spec files, no code, no test framework. Verification is grep checks plus two disposable `--plugin-dir` scratch trials, each narrowly scoped to the relevant step (not a full end-to-end pipeline run, to keep trial cost proportionate to a documentation-only change).

---

## File Structure

- **Modify:** `plugin/skills/brainstorming/SKILL.md` — extends the existing "Documentation" bullet list under "After the Design."
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — extends the existing "Finish" section.
- **Modify:** `docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md`, `docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md`, `docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md`, `docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md` — each gets its `Status` line corrected.

---

## Task 1: Wire the Status/Consequences/Alternatives-Considered/Superseded-by guidance into brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Extend the Documentation bullet list**

Find:
```
**Documentation:**

- Write the validated design (spec) to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (User preferences for spec location override this default)
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git
```

Replace with:
```
**Documentation:**

- Write the validated design (spec) to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (User preferences for spec location override this default)
- Give it a `Status` line: `Proposed`, `Approved` (approved, not yet implemented), or `Superseded by <filename>`. Never a free-text description — `subagent-driven-development`'s Finish step is what advances `Approved` to `Shipped` once the work actually ships.
- Include a `Consequences` section after Decision (and after Falsifiable Criteria or Testing, if either applies): what becomes easier or harder because of this decision, what assumptions must hold.
- If `multi-lens-research` or `branching-research` ran for this decision, capture the comparison (the candidates, the recommendation, the steelmanned alternative) as an `Alternatives Considered` section. Skip the section entirely if no formal research skill ran — an empty one is the placeholder problem the self-review below already bans.
- If this design changes or replaces a decision an earlier spec made, update that earlier spec's `Status` to `Superseded by <this-filename>` as part of writing this one.
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Consequences\|Alternatives Considered\|Superseded by" plugin/skills/brainstorming/SKILL.md
```

Expected: three matches, one per new concept, all inside the new bullets.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat: add Status lifecycle, Consequences, and Alternatives Considered guidance to brainstorming

Documentation now specifies a formal Status vocabulary
(Proposed/Approved/Superseded by <filename> -- Shipped comes from
subagent-driven-development's Finish step), a required Consequences
section, a conditional Alternatives Considered section (only when a
research skill ran), and a check for updating an earlier spec's
Status when a new one supersedes its decision.

Part of docs/superpowers/specs/2026-08-13-design-spec-template-quality-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Wire the Shipped trigger into subagent-driven-development's Finish step

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Extend the Finish section**

Find:
```
## Finish

When the final whole-branch review is clean and its fixes are merged,
delete this plan's workspace (`rm -rf <workspace>`) — the git history is
the record now. Sibling directories belong to other plans; leave them
alone.

Use superpowers:finishing-a-development-branch.
```

Replace with:
```
## Finish

When the final whole-branch review is clean and its fixes are merged,
update the originating design spec's `Status` line from `Approved` to
`Shipped` — this is the only point in the plan where "implemented and
merged" becomes true, so it is the right moment to record it. Then
delete this plan's workspace (`rm -rf <workspace>`) — the git history is
the record now. Sibling directories belong to other plans; leave them
alone.

Use superpowers:finishing-a-development-branch.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Status.*line from .Approved. to" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match, inside the updated Finish section.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: update the design spec's Status to Shipped when a plan finishes

The Finish step is the only point in this skill where 'implemented
and merged' actually becomes true -- it now updates the originating
design spec's Status line from Approved to Shipped there, instead of
leaving that update to happen (or not happen) informally.

Part of docs/superpowers/specs/2026-08-13-design-spec-template-quality-design.md."
```

Stage only this one file.

---

## Task 3: Retroactively fix the four stale spec Status lines

**Files:**
- Modify: `docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md`
- Modify: `docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md`
- Modify: `docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md`
- Modify: `docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md`

- [ ] **Step 1: Confirm current state**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^\*\*Status:\*\*" docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md
```

Expected: all four show `**Status:** Approved, not yet implemented`.

- [ ] **Step 2: Fix each file**

In each of the four files, find:
```
**Status:** Approved, not yet implemented
```

Replace with:
```
**Status:** Shipped
```

- [ ] **Step 3: Verify all four are fixed**

```bash
grep -n "^\*\*Status:\*\*" docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md
```

Expected: all four now show `**Status:** Shipped`.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md docs/superpowers/specs/2026-08-13-ai-code-guidelines-wiring-design.md docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md
git commit -m "fix: correct four design specs' Status to Shipped

All four got fully implemented, tested, and shipped after their
initial commit, but each still read 'Approved, not yet implemented' --
confirmed via git log, each file had exactly one commit ever, its own
creation. Retroactive fix per
docs/superpowers/specs/2026-08-13-design-spec-template-quality-design.md;
the forward-looking trigger (subagent-driven-development's Finish
step) prevents this from recurring."
```

Stage only these four files.

---

## Task 4: Verify brainstorming's Documentation guidance with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with an earlier spec this new one will supersede**

```bash
mkdir -p /c/sf-spec-template-test/docs/superpowers/specs
cd /c/sf-spec-template-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-spec-template-test/docs/superpowers/specs/2026-01-01-widget-cache-design.md <<'EOF'
# Widget Cache — Design

**Date:** 2026-01-01
**Status:** Approved, not yet implemented

## Context

Widgets get recomputed on every request. This spec adds an in-memory cache.

## Decision

- Cache widgets in a process-local dict, keyed by widget ID, no eviction policy yet.
EOF
git add -A
git commit -q -m "initial scratch fixture"
```

- [ ] **Step 2: Run an isolated trial that presents a design explicitly replacing the earlier spec's decision**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-spec-template-test. Use the brainstorming skill for this idea: replace the no-eviction-policy widget cache (see docs/superpowers/specs/2026-01-01-widget-cache-design.md) with an LRU eviction policy, capped at 1000 entries, because the process-local dict grows unbounded in production. Skip asking clarifying questions -- treat this as already fully specified. Go directly through presenting the design and then writing it to docs/superpowers/specs/2026-08-13-widget-cache-lru-design.md, following the skill's Documentation instructions exactly, including any updates to other spec files. After writing both files, report back in exactly 3 numbered sections with literal headers: SECTION 1/3: quote the exact Status line you wrote in the new file. SECTION 2/3: quote the exact Status line now in docs/superpowers/specs/2026-01-01-widget-cache-design.md (the old file) -- read the file fresh, do not rely on memory. SECTION 3/3: quote the new file's Consequences section in full, or state it is missing if you didn't include one." > /c/sf-spec-template-test/trial.txt 2>&1
cat /c/sf-spec-template-test/trial.txt
```

- [ ] **Step 3: Verify all three guidance items fired**

Read `/c/sf-spec-template-test/trial.txt`, and independently read the two files it should have touched:

```bash
cat /c/sf-spec-template-test/docs/superpowers/specs/2026-08-13-widget-cache-lru-design.md 2>/dev/null
cat /c/sf-spec-template-test/docs/superpowers/specs/2026-01-01-widget-cache-design.md
```

Confirm:
1. The new file's `Status` line reads `Approved` (or `Proposed`) — not a free-text string, not `Shipped` (nothing got implemented in this trial).
2. The old file's `Status` line now reads `Superseded by 2026-08-13-widget-cache-lru-design.md` (or the actual filename the trial chose, if it named the file slightly differently — check what it actually wrote).
3. The new file contains a `Consequences` section with real content (not a placeholder), naming something that gets easier or harder, or an assumption that must hold.

If any of the three is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the files actually contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-spec-template-test
```

No commit for this task.

---

## Task 5: Verify subagent-driven-development's Finish trigger with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with an Approved spec**

```bash
mkdir -p /c/sf-finish-trigger-test/docs/superpowers/specs
cd /c/sf-finish-trigger-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-finish-trigger-test/docs/superpowers/specs/2026-01-01-noop-feature-design.md <<'EOF'
# No-op Feature — Design

**Date:** 2026-01-01
**Status:** Approved, not yet implemented

## Context

A trivial feature for testing the Finish step's Status trigger.

## Decision

- Add a function that returns a constant.
EOF
git add -A
git commit -q -m "initial scratch fixture"
```

- [ ] **Step 2: Run an isolated trial that skips straight to the Finish step**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-finish-trigger-test. Assume you are partway through following the subagent-driven-development skill for a plan that implements docs/superpowers/specs/2026-01-01-noop-feature-design.md: all tasks are already complete, and the final whole-branch review just came back clean. Follow the skill's Finish section now, exactly as written -- do not re-read or re-execute any earlier part of the skill, just Finish. After following it, report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state which specific instruction in the Finish section you followed regarding the design spec's Status, quoted from the skill file. SECTION 2/2: read docs/superpowers/specs/2026-01-01-noop-feature-design.md fresh from disk and quote its current Status line verbatim." > /c/sf-finish-trigger-test/trial.txt 2>&1
cat /c/sf-finish-trigger-test/trial.txt
```

- [ ] **Step 3: Verify the Status line actually changed on disk**

Read `/c/sf-finish-trigger-test/trial.txt`, and independently:

```bash
cat /c/sf-finish-trigger-test/docs/superpowers/specs/2026-01-01-noop-feature-design.md
```

Confirm:
1. SECTION 1/2 names the Finish-step instruction about updating Status (not a fabricated or paraphrased rule).
2. SECTION 2/2's quoted Status line, and the independently-read file's actual Status line, both read `Shipped`.
3. Nothing else in the file changed beyond the Status line (spot-check the Context/Decision sections still read as they did in Step 1).

If the Status line wasn't actually changed on disk (only claimed to be), treat this as DONE_WITH_CONCERNS.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-finish-trigger-test
```

No commit for this task — it verifies Tasks 1 and 2 together and touches no repository files.
