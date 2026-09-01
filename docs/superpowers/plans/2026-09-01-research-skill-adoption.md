# Research Skill Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt `multi-lens-research`, `branching-research`, and `calibrating-recommendations` into `plugin/skills/`, and give `brainstorming`'s step 4 three checkable requirements, so the option-comparison discipline ships with the plugin instead of depending on files outside the repository.

**Architecture:** Six tasks. Task 1 copies three skill directories in and bumps the plugin version. Task 2 repairs the six cross-references the copy brings with it. Tasks 3-5 edit three skill files to add the two harvested mechanisms and rewire `brainstorming`. Task 6 runs the A/B trial that can falsify the change. No code and no test framework — every task verifies by `grep` against real file content, and Task 6 verifies by two-arm live trial.

**Tech Stack:** Markdown skill files, JSON plugin manifests, `grep`, `git worktree`, and disposable `--plugin-dir` scratch trials.

## Global Constraints

- Every text block this plan writes into a target file must match the design spec's Decision block exactly, character-for-character. The spec at `docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md` governs; this plan never paraphrases it.
- Spec Falsifiable Criterion 2 (`grep` for `adhd-research` across `plugin/skills/` returns zero matches) holds only from Task 2 onward. Task 1 deliberately lands the copy with its references intact, so Task 2's diff shows exactly which lines the repair touches.
- After Task 2, `plugin/skills/branching-research/SKILL.md` diverges from `~/.claude/skills/branching-research/SKILL.md`. The plugin copy wins. Do not sync the user-level copy back over it.
- No file outside `plugin/skills/`, `plugin/.claude-plugin/`, `plugin/README.md`, and this plan's own outcomes file gets modified. Task 1's Step 6 documentation check targets `plugin/README.md`, since this repository holds no root `README.md`.
- Task 6 can falsify the change. If both trial arms produce a do-nothing candidate and a named flip factor, stop and report — do not ship Tasks 3-5.

---

## File Structure

Directories touched: `plugin/skills/` and `plugin/.claude-plugin/`. Searched both for a `.context.md` file — `find plugin docs -iname ".context.md"` returns `0` this session, so no directory-context file applies to any task here.

This plan creates three directories by copying existing files. `docs/code-standards.md`'s File Naming section governs new files; each copied file keeps the `SKILL.md` name the skill loader requires, which that section's convention already covers.

**Files to create:**
- `plugin/skills/multi-lens-research/SKILL.md` — copied from `~/.claude/skills/`
- `plugin/skills/branching-research/SKILL.md` — copied from `~/.claude/skills/`
- `plugin/skills/calibrating-recommendations/SKILL.md` — copied from `~/.claude/skills/`

**Files to modify:**
- `plugin/.claude-plugin/plugin.json` — version `6.2.0` to `6.3.0`
- `plugin/.claude-plugin/marketplace.json` — version `6.2.0` to `6.3.0`
- `plugin/skills/branching-research/SKILL.md` — repair six `adhd-research` references
- `plugin/skills/brainstorming/SKILL.md` — step 4 requirements, prose restatement, Alternatives Considered bullet
- `plugin/skills/calibrating-recommendations/SKILL.md` — flip-the-ranking field, Common Mistakes bullet
- `plugin/skills/multi-lens-research/SKILL.md` — null-option baseline in step 3

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API. Every edit adds or replaces Markdown text, copies a file, or runs `grep`.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape. The two JSON manifests get a single string value changed, which adds no shape.
- **T4 — User-designated:** Skipped: the user has not asked for pseudocode on any part of this work.

---

### Task 1: Copy the three skills into the plugin and bump the version

**Files:**
- Create: `plugin/skills/multi-lens-research/SKILL.md`
- Create: `plugin/skills/branching-research/SKILL.md`
- Create: `plugin/skills/calibrating-recommendations/SKILL.md`
- Modify: `plugin/.claude-plugin/plugin.json`
- Modify: `plugin/.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the three skill files every later task edits or verifies. Tasks 2, 4, and 5 all depend on these paths existing.

- [ ] **Step 1: Record the base SHA for this task's documentation check**

Run: `git rev-parse HEAD`
(Use the printed SHA in Step 6 below, in place of `<task-1-base-sha>`. It reads `aa08b7f...` at plan-writing time.)

- [ ] **Step 2: Confirm the plugin holds 19 skills and no `adhd-research` reference**

Run: `ls -d plugin/skills/*/ | wc -l` and `grep -rl "adhd-research" plugin/skills/ | wc -l`
Expected: `19` and `0` (both confirmed by running them this session).

- [ ] **Step 3: Copy the three skill directories**

```bash
for s in multi-lens-research branching-research calibrating-recommendations; do
  mkdir -p "plugin/skills/$s"
  cp "/c/Users/marko/.claude/skills/$s/SKILL.md" "plugin/skills/$s/SKILL.md"
done
```

- [ ] **Step 4: Verify the copy landed**

Run: `ls -d plugin/skills/*/ | wc -l`
Expected: `22`

Run: `for s in multi-lens-research branching-research calibrating-recommendations; do grep -c "^name: $s" "plugin/skills/$s/SKILL.md"; done`
Expected: `1` three times — each file's frontmatter `name:` matches its directory, as the skill loader requires.

- [ ] **Step 5: Bump the version in all seven declared files**

`plugin/.version-bump.json` declares seven files that carry the plugin version. Bump every one from `6.2.0` to `6.3.0`, changing only the version value:

- `plugin/package.json`
- `plugin/.claude-plugin/plugin.json`
- `plugin/.cursor-plugin/plugin.json`
- `plugin/.codex-plugin/plugin.json`
- `plugin/.kimi-plugin/plugin.json`
- `plugin/.claude-plugin/marketplace.json` (field path `plugins.0.version`)
- `plugin/gemini-extension.json`

Do NOT use `plugin/scripts/bump-version.sh`. It requires `jq`, which this environment does not have — `which jq` returns nothing and the script dies at line 46 with `jq: command not found`, confirmed this session. Hand-edit the seven files.

Run:
```bash
cd plugin && for f in package.json .claude-plugin/plugin.json .cursor-plugin/plugin.json .codex-plugin/plugin.json .kimi-plugin/plugin.json .claude-plugin/marketplace.json gemini-extension.json; do printf "%-38s " "$f"; grep -o '"version": *"[0-9.]*"' "$f" | head -2 | tr '\n' ' '; echo; done
```
Expected: all seven print `"version": "6.3.0"`. (All seven read `6.2.0` before this task, confirmed this session.)

- [ ] **Step 6: Run the user-facing documentation check**

The spec carries `User-Facing: Yes`, and this task ships the user-facing surface — three new skills a user can invoke. Commit Step 3-5's changes first so the check has a head SHA to read:

```bash
git add plugin/skills/multi-lens-research plugin/skills/branching-research plugin/skills/calibrating-recommendations plugin/.claude-plugin/plugin.json plugin/.claude-plugin/marketplace.json
git commit -m "feat(skills): adopt multi-lens-research, branching-research, calibrating-recommendations into the plugin"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md <task-1-base-sha> $(git rev-parse HEAD)
```

Expect `ACTION_NEEDED`. This repository holds no root `README.md`, and `check_docs.py:47` matches bare filenames only (`f in ("README.md", "CHANGELOG.md")`), so it cannot report `ALREADY_UPDATED` for a nested path here. BUG-0001 already tracks that defect, Status Open, and this marks its second occurrence. Treat `ACTION_NEEDED` as expected rather than as a signal the doc update got skipped.

Read the Context/Decision/Consequences content the script prints, then add the three adopted skills to `plugin/README.md`'s Skills Library section — the real user-facing list of invocable skills in this repository — and amend it into this task's commit:

```bash
git add plugin/README.md
git commit --amend --no-edit
```

Record the script's exact output in this task's outcomes entry either way.

---

### Task 2: Fit the adopted copies to the plugin

**Files:**
- Modify: `plugin/skills/branching-research/SKILL.md`
- Modify: `plugin/skills/multi-lens-research/SKILL.md`

**Interfaces:**
- Consumes: Task 1's copied skill files.
- Produces: plugin copies whose every skill reference resolves inside `plugin/skills/`, whose REQUIRED SUB-SKILL markers use the house namespace form, and whose descriptions name detectable triggers. Task 6's Step 2 verifies the reference resolution.

Steps 4 and 5 were added after Task 1's code quality review found them. All three repairs share one root cause: these files were written for a user-level context where `adhd-research` exists, no plugin namespace applies, and the description could position against a sibling. None of that holds inside the plugin.

- [ ] **Step 1: Confirm the six references and their line numbers**

Run: `grep -n "adhd-research" plugin/skills/branching-research/SKILL.md`
Expected: 6 matching lines, at 10, 12, 17, 39, 77, and 90 (confirmed by running this against the source file this session; `grep -o ... | wc -l` also returns `6`, so no line carries two references).

- [ ] **Step 2: Rewrite the three positioning references**

These describe the skill by contrast with a skill the plugin omits. Replace each with a positive statement of what this skill does.

Line 10 — change:
```markdown
Native tree-of-thought: dispatch fresh agents under distinct cognitive frames to generate divergent ideas with evaluation forbidden, dispatch a separate critic agent to score/cluster/trap-tag them, then apply `calibrating-recommendations` to reach a defensible pick. Same shape as `adhd-research`, without the external CLI dependency — full control over the frame prompts, no black-box degenerate runs, direct tuning when something's off.
```
To:
```markdown
Native tree-of-thought: dispatch fresh agents under distinct cognitive frames to generate divergent ideas with evaluation forbidden, dispatch a separate critic agent to score/cluster/trap-tag them, then apply `calibrating-recommendations` to reach a defensible pick. Every frame prompt stays visible and editable in this file — no external tool in the loop, no black-box generation step, and direct tuning when a frame underperforms.
```

Line 12 — change:
```markdown
**vs. `adhd-research`:** same synthesis discipline, different generation engine — this one is fully native `Agent` dispatches instead of a shell-out. **vs. `multi-lens-research`:** that skill's four lenses are fixed engineering tradeoffs; this skill's frames are drawn from a broader library (below) and selected per-problem, better suited to naming/strategy/fuzzy-debugging problems where the right angles aren't obviously the four tradeoff dimensions.
```
To:
```markdown
**vs. `multi-lens-research`:** that skill's four lenses are fixed engineering tradeoffs; this skill's frames are drawn from a broader library (below) and selected per-problem, better suited to naming/strategy/fuzzy-debugging problems where the right angles aren't obviously the four tradeoff dimensions.
```

Line 17 — change:
```markdown
- You want `adhd-research`'s shape without installing/depending on the external tool
```
To:
```markdown
- You want wide divergence with every frame prompt under your own control, and no external tool in the loop
```

- [ ] **Step 3: Rewrite the three provenance references**

These cite where a documented failure mode came from. `plugin/skills/process-review/SKILL.md` states the governing principle — real evidence over vibes — so keep the provenance and drop only the unresolvable name.

Line 39 — change:
```markdown
Boundary frames often produce ideas that get trapped by the critic — that's expected and still valuable: a trapped idea with a named mechanistic reason confirms the safer frames' direction, the same way it did repeatedly in `adhd-research` testing.
```
To:
```markdown
Boundary frames often produce ideas that get trapped by the critic — that's expected and still valuable: a trapped idea with a named mechanistic reason confirms the safer frames' direction, the same way it did repeatedly in prior testing of this technique.
```

Line 77 — change:
```markdown
| All ideas get trapped (degenerate shortlist) | Don't force a pick from rejected material. Re-run with tighter framing or added grounding context before shortlisting — same recovery `adhd-research` testing validated. |
```
To:
```markdown
| All ideas get trapped (degenerate shortlist) | Don't force a pick from rejected material. Re-run with tighter framing or added grounding context before shortlisting — the recovery prior testing of this technique validated. |
```

Line 90 — change:
```markdown
- **Collapsing "don't show me the pre-mortem/steelman" into "don't invoke `calibrating-recommendations`"** — confirmed failure mode from `adhd-research` testing. A request about the output's contents is not an instruction about which steps to run.
```
To:
```markdown
- **Collapsing "don't show me the pre-mortem/steelman" into "don't invoke `calibrating-recommendations`"** — confirmed failure mode from prior testing of this technique. A request about the output's contents is not an instruction about which steps to run.
```

- [ ] **Step 4: Add the `superfunk:` namespace prefix to both REQUIRED SUB-SKILL markers**

`plugin/skills/writing-skills/SKILL.md:283` states the house form: `**REQUIRED SUB-SKILL:** Use superfunk:test-driven-development`. All four pre-existing markers in the plugin follow it. Both adopted copies use a bare backticked name instead, which does not match the Skill tool's resolution name.

In `plugin/skills/multi-lens-research/SKILL.md:55`, change ``**REQUIRED SUB-SKILL:** Use `calibrating-recommendations` `` to `**REQUIRED SUB-SKILL:** Use superfunk:calibrating-recommendations`.

In `plugin/skills/branching-research/SKILL.md:69`, make the same substitution. Also split the marker out of the step's sentence bolding: it currently reads `5. **Form a tentative recommendation from the shortlist. REQUIRED SUB-SKILL:** Use ...`, which swallows the marker. It must stand alone as `**REQUIRED SUB-SKILL:**`, matching every house instance.

Leave every bare backticked skill name in ordinary prose unchanged — that form is house-acceptable and appears throughout `brainstorming`, `bug-tracking`, and `documentation`.

Run: `grep -rn "REQUIRED SUB-SKILL" plugin/skills/ | grep -c "superfunk:"`
Expected: `6` — the four pre-existing markers plus these two.

- [ ] **Step 5: Rewrite `branching-research`'s description to name a detectable trigger**

The description at `plugin/skills/branching-research/SKILL.md:3` distinguishes the skill by *"you want the generation and critique steps done natively (no external tool dependency) with full visibility into the framing prompts."* That fails two `writing-skills` rules: it summarizes the workflow (banned at `writing-skills/SKILL.md:102` and `:180`), and it names a tooling preference no problem context ever exhibits, so the skill cannot trigger on a real request. The concrete triggers — fuzzy debugging, naming, API surface design, strategy — sit only in the body at line 16 and never reach the description.

The clause also positions against `adhd-research`, which this plan deliberately leaves at user level, making it the same dangling-reference class this task exists to fix.

Change:
```markdown
description: Use when a problem needs wide creative divergence before a calibrated recommendation, but you want the generation and critique steps done natively (no external tool dependency) with full visibility into the framing prompts.
```
To:
```markdown
description: Use when a problem needs wide creative divergence before a calibrated recommendation — fuzzy debugging, naming, API surface design, or strategy, where the right angles aren't known in advance and a fixed comparison grid would be too narrow.
```

Run: `grep -c "external tool dependency" plugin/skills/branching-research/SKILL.md`
Expected: `0`

- [ ] **Step 6: Verify every reference resolves**

Run: `grep -rc "adhd-research" plugin/skills/branching-research/SKILL.md`
Expected: `0`

Run: `grep -rl "adhd-research" plugin/skills/ | wc -l`
Expected: `0` — satisfying spec Falsifiable Criterion 2.

- [ ] **Step 7: Commit**

```bash
git add plugin/skills/branching-research/SKILL.md plugin/skills/multi-lens-research/SKILL.md
git commit -m "fix(skills): fit adopted research skills to the plugin — references, namespace, trigger"
```

---

### Task 3: Give brainstorming's step 4 three requirements

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: Task 1's copied skills, which the new step-4 text names as the fan-out alternative. Editing this before Task 1 would create the same dangling reference this plan removes.
- Produces: the revised step 4 that Task 6's trial arm B exercises.

- [ ] **Step 1: Confirm the three anchors and their uniqueness**

Run: `grep -c "with trade-offs and your recommendation" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

Run: `grep -c "Propose 2-3 different approaches with trade-offs" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

Run: `grep -c 'If \`multi-lens-research\` or \`branching-research\` ran' plugin/skills/brainstorming/SKILL.md`
Expected: `1`

All three confirmed by running them this session. Note that the bare phrase `Propose 2-3 approaches` returns `4`, not `1` — it also names a node and two edges in the skill's `dot` diagram. Use the longer anchors above, not the bare phrase.

- [ ] **Step 2: Replace the checklist entry (line 27)**

Change:
```markdown
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
```
To:
```markdown
4. **Propose 2-3 approaches** — with trade-offs and your recommendation. Every proposal set meets three requirements: include a do-nothing/defer candidate and name what happens if this design ships nothing; state confidence and name the project-specific evidence behind it; name the factor that, if it moved, would flip the ranking. For a decision with several defensible paths, dispatch `multi-lens-research` or `branching-research` instead of proposing inline.
```

- [ ] **Step 3: Replace the prose restatement (lines 91-94)**

Change:
```markdown
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
- YAGNI ruthlessly - remove unnecessary features from every approach and design
```
To:
```markdown
- Propose 2-3 different approaches with trade-offs
- Include a do-nothing/defer candidate in every proposal set — name what happens if this design ships nothing. All other candidates propose action; nothing else in this skill argues for restraint.
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
- State your confidence, and name the project-specific evidence behind it — a file you read, a prior decision's outcome, a measured quantity. Reasoning depth doesn't count.
- Name the factor that, if it moved, would flip the ranking. A recommendation that wins on every factor says so; one that wins on a single close call names that call.
- YAGNI ruthlessly - remove unnecessary features from every approach and design
```

- [ ] **Step 4: Replace the Alternatives Considered bullet (line 139)**

Change:
```markdown
- If `multi-lens-research` or `branching-research` ran for this decision, capture the comparison (the candidates, the recommendation, the steelmanned alternative) as an `Alternatives Considered` section. Skip the section entirely if no formal research skill ran — an empty one is the placeholder problem the self-review below already bans.
```
To:
```markdown
- Capture an `Alternatives Considered` section in every spec that records a choice between approaches. If `multi-lens-research` or `branching-research` ran for this decision, capture the full comparison — the candidates, the recommendation, the steelmanned alternative. If only step 4's inline proposal ran, capture the short form — the candidates including the do-nothing option, the recommendation with its confidence, and the flip factor. Skip the section only when the design records no choice between approaches; an empty section repeats the placeholder problem the self-review below already bans.
```

- [ ] **Step 5: Verify all three edits landed**

Run: `grep -c "would flip the ranking" plugin/skills/brainstorming/SKILL.md`
Expected: `2` — one in the checklist entry, one in the prose list.

Run: `grep -c "do-nothing/defer candidate" plugin/skills/brainstorming/SKILL.md`
Expected: `2` — one in the checklist entry, one in the prose list.

Run: `grep -c "Skip the section entirely" plugin/skills/brainstorming/SKILL.md`
Expected: `0` — the old wording no longer appears. (It returns `1` before this task, confirmed this session.)

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): give brainstorming step 4 a null option, confidence grounding, and a flip factor"
```

---

### Task 4: Add ranking sensitivity to calibrating-recommendations

**Files:**
- Modify: `plugin/skills/calibrating-recommendations/SKILL.md`

**Interfaces:**
- Consumes: Task 1's copied `plugin/skills/calibrating-recommendations/SKILL.md`.
- Produces: the flip-the-ranking field the fan-out path emits. Task 6's Step 2 verifies it.

- [ ] **Step 1: Confirm the anchors**

Run: `grep -c "grounded in the pre-mortem finding" plugin/skills/calibrating-recommendations/SKILL.md`
Expected: `1` — the bare phrase `What would lower it` returns `2`, since the prose above the output block also names it. Use this longer anchor.

Run: `grep -c "Logging a severe pre-mortem finding without reconsidering" plugin/skills/calibrating-recommendations/SKILL.md`
Expected: `1`

Both confirmed by running them this session.

- [ ] **Step 2: Add the field to the Medium/High recommendation output block**

Change:
```markdown
**What would lower it:** <grounded in the pre-mortem finding>
```
To:
```markdown
**What would lower it:** <grounded in the pre-mortem finding>
**What would flip the ranking:** <the single factor that, if it moved, would reorder the candidates — distinct from what would lower confidence in the pick, which asks how the recommendation fails on its own terms>
```

- [ ] **Step 3: Add the Common Mistakes bullet**

This section uses a bulleted list, not a table. Append after the final bullet.

Change:
```markdown
- **Logging a severe pre-mortem finding without reconsidering** — noting a serious flaw isn't the same as acting on it; the recommendation, confidence, or both must actually respond to what it found.
```
To:
```markdown
- **Logging a severe pre-mortem finding without reconsidering** — noting a serious flaw isn't the same as acting on it; the recommendation, confidence, or both must actually respond to what it found.
- **Restating the pre-mortem as the flip factor** — the pre-mortem asks how the pick fails on its own terms; the flip factor asks how narrowly the pick won. A recommendation that wins by a wide margin on every factor says so plainly; one that wins on a single close call names that call.
```

- [ ] **Step 4: Verify both edits landed**

Run: `grep -c "What would flip the ranking" plugin/skills/calibrating-recommendations/SKILL.md`
Expected: `1`

Run: `grep -c "Restating the pre-mortem as the flip factor" plugin/skills/calibrating-recommendations/SKILL.md`
Expected: `1`

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/calibrating-recommendations/SKILL.md
git commit -m "feat(skills): add ranking-sensitivity field to calibrating-recommendations"
```

---

### Task 5: Add the null-option baseline to multi-lens-research

**Files:**
- Modify: `plugin/skills/multi-lens-research/SKILL.md`

**Interfaces:**
- Consumes: Task 1's copied `plugin/skills/multi-lens-research/SKILL.md`.
- Produces: the null-option baseline on the fan-out path, matching what Task 3 added to the inline path.

- [ ] **Step 1: Confirm the anchor**

Run: `grep -c "this stays symmetric" plugin/skills/multi-lens-research/SKILL.md`
Expected: `1` (confirmed by running it this session).

- [ ] **Step 2: Add the baseline sentence to step 3**

The four lenses each must propose an approach, so no lens can carry the null option. It enters at synthesis instead.

Change:
```markdown
3. **Synthesize.** Build the comparison across all four proposals first — complexity, risk, effort, reversibility — this stays symmetric.
```
To:
```markdown
3. **Synthesize.** Build the comparison across all four proposals first — complexity, risk, effort, reversibility — this stays symmetric. Include a do-nothing/defer baseline in that comparison, even though no lens proposes one — what happens if the project ships nothing here. A baseline that beats all four lens proposals means the fan-out found no approach worth taking, and the honest output says so rather than picking the least-bad proposal.
```

- [ ] **Step 3: Verify the edit landed**

Run: `grep -c "do-nothing/defer baseline" plugin/skills/multi-lens-research/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/multi-lens-research/SKILL.md
git commit -m "feat(skills): add null-option baseline to multi-lens-research synthesis"
```

---

### Task 6: Verify every criterion, and run the A/B trial that can falsify the change

**Files:**
- Create: `/c/sf-step4-test/` (disposable scratch fixture, outside the repository)
- Modify: `docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md` — only if the trial falsifies Criterion 9

**Interfaces:**
- Consumes: every prior task's committed changes.
- Produces: the trial evidence this plan's outcomes entry records. Nothing later depends on this task.

- [ ] **Step 1: Verify the structural criteria (spec Criteria 1, 2, 4-8)**

```bash
ls plugin/skills/multi-lens-research/SKILL.md plugin/skills/branching-research/SKILL.md plugin/skills/calibrating-recommendations/SKILL.md
grep -rl "adhd-research" plugin/skills/ | wc -l
grep -c "do-nothing/defer candidate" plugin/skills/brainstorming/SKILL.md
grep -c "Skip the section entirely" plugin/skills/brainstorming/SKILL.md
grep -c "What would flip the ranking" plugin/skills/calibrating-recommendations/SKILL.md
grep -c "do-nothing/defer baseline" plugin/skills/multi-lens-research/SKILL.md
grep -rn "REQUIRED SUB-SKILL" plugin/skills/ | grep -c "superfunk:"
```
Expected, in order: three paths listed; `0`; `2`; `0`; `1`; `1`; `6`.

Then check the version across all seven declared files, driven off `plugin/.version-bump.json`'s own list rather than a remembered set of paths (spec Criterion 8):

```bash
cd plugin && grep -o '"path": *"[^"]*"' .version-bump.json | sed 's/.*: *"//;s/"//' | while read f; do printf "%-38s " "$f"; grep -o '"version": *"[0-9.]*"' "$f" | head -2 | tr '\n' ' '; echo; done; cd - >/dev/null
```
Expected: seven lines, every one reading `"version": "6.3.0"`.

- [ ] **Step 2: Verify every skill reference in the three adopted files resolves (spec Criterion 3)**

Run this by script rather than by reading, per the criterion's own wording:

```bash
for f in plugin/skills/multi-lens-research/SKILL.md plugin/skills/branching-research/SKILL.md plugin/skills/calibrating-recommendations/SKILL.md; do
  grep -o '`[a-z][a-z0-9-]\{4,\}`' "$f" | tr -d '`' | sort -u | while read n; do
    if [ ! -d "plugin/skills/$n" ]; then echo "UNRESOLVED in $f: $n"; fi
  done
done
```
Expected: only `general-purpose` reported, which names an agent type rather than a skill. Any other name reported means a real dangling reference — fix it before continuing.

- [ ] **Step 3: Build the scratch fixture**

```bash
rm -rf /c/sf-step4-test && mkdir -p /c/sf-step4-test/src/api && cd /c/sf-step4-test
git init -q
printf '# Gateway\n\nPublic HTTP API.\n' > README.md
printf 'def handle(request):\n    return route(request)\n' > src/api/gateway.py
git add -A && git commit -qm "initial"
cd - >/dev/null
```

No convention doc needs copying in: `brainstorming`'s context step reads `.context.md` (none exist in this repo either, confirmed) and its tracker gate explicitly skips when no tracker file exists. Per `docs/patterns/seed-trial-fixtures-with-real-docs.md`, confirm this reasoning holds by checking the trial output for any "file not found" report before trusting the result.

- [ ] **Step 4: Create the arm-A checkout (plugin before Task 3)**

Arm A must hold Task 1 and Task 2's copies but not Task 3's step-4 edit, so both arms have the same three skills available and differ only in step 4.

```bash
git log --oneline -6
git worktree add /c/sf-ab-pre <sha-of-task-2-commit>
```
Use the SHA of Task 2's commit ("fix(skills): resolve branching-research references..."), printed by the `git log` above.

- [ ] **Step 5: Run both arms with the identical, coaching-free prompt**

Per `docs/patterns/ab-test-live-trials-for-behavior-change.md`, the prompt must not name the behavior under test — no "do-nothing," "defer," "null option," "flip," "sensitivity," or "ranking."

```bash
PROMPT="You are in a git repository at /c/sf-step4-test. Use the brainstorming skill to explore this idea: adding rate limiting to the public API in src/api/. Skip the clarifying-questions step -- treat this as fully specified: 100 requests per minute per API key, and over-limit requests get HTTP 429. Go as far as presenting your approaches for this decision, then STOP -- do not present a full design, do not write any file, do not ask a question. Present your approaches exactly as the skill instructs."

claude -p --plugin-dir "/c/sf-ab-pre/plugin" --dangerously-skip-permissions --output-format text "$PROMPT" > /c/sf-step4-test/arm-a.txt 2>&1
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "$PROMPT" > /c/sf-step4-test/arm-b.txt 2>&1
```

- [ ] **Step 6: Compare the two arms**

```bash
for a in a b; do
  echo "=== ARM $a ==="
  grep -ci "do nothing\|do-nothing\|defer\|status quo\|ship nothing" /c/sf-step4-test/arm-$a.txt
  grep -ci "flip\|would reorder\|closest call\|hinges on" /c/sf-step4-test/arm-$a.txt
done
```

Read both files in full, not only the counts — a low count with the concept present in different words still counts as present.

Expected: arm B names a do-nothing/defer candidate and a flip factor. Arm A names neither.

**This step can falsify the change.** If arm A also produces both, the revised step 4 added no detectable behavioral difference. Record that plainly, correct spec Criterion 9 to state what the trial actually shows, and stop rather than claiming a pass — per Rule 1, step 5 of `docs/patterns/ab-test-live-trials-for-behavior-change.md`.

- [ ] **Step 7: Clean up the scratch worktree**

```bash
git worktree remove /c/sf-ab-pre
rm -rf /c/sf-step4-test
```

- [ ] **Step 8: Commit any spec correction**

Only if Step 6 falsified Criterion 9:

```bash
git add docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md
git commit -m "docs(specs): correct Criterion 9 to state what the A/B trial actually showed"
```

If Step 6 confirmed the difference, this task commits nothing — its evidence lands in the outcomes file instead.

---

## Self-Review

**1. Spec coverage:** Decision section 1 (adopt three skills, version bump, `adhd-research` stays out) → Task 1. Section 2 (repair six references, two classes) → Task 2. Section 3 (step 4 requirements, prose restatement) → Task 3 Steps 2-3. Section 4 (Alternatives Considered branch) → Task 3 Step 4. Section 5 (flip-the-ranking field, Common Mistakes bullet) → Task 4. Section 6 (null-option baseline) → Task 5. Criteria 1-8 → Task 6 Steps 1-2. Criterion 9 → Task 6 Steps 3-6. No spec requirement lacks a task.

**2. Placeholder scan:** No "TBD", "TODO", or "similar to Task N". Three deliberate runtime substitutions appear — `<task-1-base-sha>` (Task 1 Step 6) and `<sha-of-task-2-commit>` (Task 6 Step 4) — each preceded by the exact command that prints the value. Every text edit shows complete before-and-after content.

**3. Type consistency:** The three skill directory names appear identically in every task. Each phrase the greps verify matches the exact text its own edit writes — `do-nothing/defer candidate`, `do-nothing/defer baseline`, `What would flip the ranking`, and `would flip the ranking`. Checked Task 3 Step 5 against Task 3 Steps 2-3. Checked Task 4 Step 4 against Task 4 Steps 2-3. Checked Task 5 Step 3 against Task 5 Step 2. Note one deliberate distinction: `candidate` on the inline path, `baseline` on the fan-out path. The greps keep the two separate.

**4. Pseudocode coverage:** All four triggers stated. Each carries `Skipped:` with a reason naming a real absence — no API call, no handler pattern, no data shape, no user request — rather than restating the trigger name.

**5. Sibling-pattern parity:** Task 4's new Common Mistakes bullet mirrors its siblings' shape — bold lead-in, em-dash, then the why. Task 3's new prose bullets carry the same imperative-plus-rationale shape as the existing `YAGNI ruthlessly` sibling. Task 4 Step 3 records that this section uses bullets rather than a table. The design spec originally specified a table row; that error got corrected in the spec before this plan reached its first draft.

**6. Rule-restatement accuracy:** The null-option rule appears in three target files — `brainstorming` (twice: checklist and prose) and `multi-lens-research` (once). Read side by side, all three describe the same underlying logic: a do-nothing option enters the comparison because nothing else argues for restraint. The wording differs where the mechanism differs — `brainstorming` says "candidate" because the agent generates the set itself; `multi-lens-research` says "baseline" because no lens can produce it and synthesis must add it. That difference tracks the mechanism rather than drift, per `docs/patterns/cross-check-shared-rule-restatements.md`.

**7. Lessons-learned check:** Read `docs/lessons-learned.md` in full before writing this plan. Four entries apply directly. The three self-referential numeric-verification entries — batch-3, doc-timing-and-mutation-check, and rebrand-string — drove running every `Expected:` command against real content this session. That caught two real traps: `Propose 2-3 approaches` returns `4` rather than `1`, and `What would lower it` returns `2` rather than `1`. Both anchors got replaced with longer unique ones. The "source document can change after you've read it once" entry drove a fresh read of `calibrating-recommendations` rather than a citation from the earlier read this session. That fresh read surfaced the table-versus-bullet error in the spec.

**8. Cross-section mechanism consistency:** Task 3 edits routing language — step 4 now says "dispatch `multi-lens-research` or `branching-research` instead." Grepped `plugin/skills/brainstorming/SKILL.md` for every other mention of those two names and of `Alternatives Considered`. Line 139 carries the only other mention, and Task 3 Step 4 edits it in the same task, so the two cannot diverge. The skill's `dot` diagram carries a `"Propose 2-3 approaches"` node and two edges naming it. Those stay unchanged: they label the step rather than describe its requirements, matching how every other node in that diagram labels its step. `plugin/skills/brainstorming/` holds no other top-level file. The design spec describes the same mechanism and matches.

**9. Worked-example currency:** Task 3 adds requirements to an existing step without adding, removing, or reordering any step in the checklist or the diagram. Task 6's structural checks confirm the step count stays unchanged. No worked example elsewhere in `brainstorming/SKILL.md` demonstrates step 4's output, so none needs updating.

**10. Verified numeric expectations:** Every `Expected:` value in this plan came from running the actual command this session against real file content. Verified this session:

- `19` skill directories under `plugin/skills/`
- `0` files under `plugin/skills/` naming `adhd-research`
- `6` `adhd-research` lines, and `6` occurrences, in `branching-research`
- `1` for each of the five edit anchors
- `1` for each `"6.2.0"` manifest match
- `1` for `Skip the section entirely`
- `1` for `Logging a severe pre-mortem finding`

Two values follow arithmetically from edits this plan specifies rather than from an independent measurement. The `22` in Task 1 Step 4 comes from 19 + 3. The `2` counts in Task 3 Step 5 come from one occurrence per edited block. Task 6 Step 2's resolution script uses a `-d` directory test rather than a substring count. A bare substring count cannot isolate a skill name from a longer name containing it, per `docs/patterns/verify-plan-commands-against-real-content.md`.

**11. Template compliance:** This plan's header carries Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header section.

**12. User-facing documentation timing:** The spec carries `User-Facing: Yes`. Task 1 ships the user-facing surface — three newly available skills — and includes its own `check_docs.py` step in that same task, committed alongside. No later task and no Finish step carries this.

**13. Hostile-input pass:** Task 1 Step 3's loop does not handle a pre-existing `plugin/skills/<name>/SKILL.md`; `cp` would overwrite it silently. Step 2 guards that case by confirming the count reads `19` before the copy, so an unexpected 20 or more stops the task. Task 6 Step 3's `rm -rf /c/sf-step4-test` does not handle the path already holding unrelated work; the path stays scratch-only and carries this trial's own name. Task 6 Step 5's `$PROMPT` contains no shell metacharacters and stays inside double quotes. Task 6 Step 4's `git worktree add` fails when `/c/sf-ab-pre` survives an earlier run. Step 7's `git worktree remove` performs that cleanup. A stale directory needs `git worktree remove --force` before a retry. Recorded rather than handled, since each names a single-operator scratch path.

**14. Stale-workaround grep:** No task removes a limitation from a tool — no error message, docstring, or README text describes a missing capability this plan adds. The closest case, `brainstorming`'s `Skip the section entirely if no formal research skill ran`, gets replaced by Task 3 Step 4, and Task 3 Step 5 verifies it drops to `0` occurrences. Grepped the repository for that phrase's distinctive words outside the skill file itself: it appears nowhere else, so no stale reference survives the change.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-01-research-skill-adoption.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
