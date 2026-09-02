# Process-Review Batch R1–R4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close Recommendations R1–R4 from `docs/superpowers/process-reviews/review-after-2026-09-01-behavioral-claim-verification-design.md` — R1 via an A/B trial, R2–R4 as mechanical fixes with per-item verification.

**Architecture:** Four independent edits plus one A/B trial. R3 (script port) lands first so the R4 bump gate invokes a script that runs. R1's trial runs as Tasks 5–6 with a ship/no-ship branch; its criterion and decision rule sit pre-registered in the spec (commit `2f68049`, amended `5060812`), which predates every arm run.

**Tech Stack:** Bash, `node -e` one-liners (node v22.14.0, present on this machine), `claude -p --plugin-dir` disposable trials, markdown skill files.

**Part of:** `docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md`

## Global Constraints

- R1 ships only on decision-rule branch "arm 1 no / arm 2 yes", and ships the exact trial arm-2 string character-for-character.
- The R4 bump-gate wording must read identically in both target files (indentation may differ; the normalized-extraction diff in Task 4 Step 4 verifies).
- R3 adds zero new dependencies: node only, machine-local availability accepted (spec Decisions item 4).
- Task order matters only in one place: Task 1 (R3) lands before Tasks 3–4 (R4).
- `.version-bump.json`'s declared-file list stays unchanged.
- Spec carries `User-Facing: Yes`: every task changing `plugin/skills/` runs `check_docs.py` inside that task (Tasks 3, 4, 6).
- Out of scope: G1, G2, G3, rule-membership restatements, full script rewrite (spec Out of Scope section).

## File Structure

`.context.md` check: no `.context.md` exists anywhere under `plugin/skills/` (verified by glob at plan time); none exists in `docs/patterns/` or `plugin/scripts/`. Checked: `plugin/skills/`, `plugin/scripts/`, `docs/patterns/`.

- Modify: `plugin/scripts/bump-version.sh` — Task 1 (four helper functions only)
- Modify: `docs/patterns/ab-test-live-trials-for-behavior-change.md` — Task 2 (Rule 1, new point 6)
- Modify: `plugin/skills/executing-plans/SKILL.md` — Task 3 (new Step 3, renumber old Step 3 → 4)
- Modify: `plugin/skills/subagent-driven-development/SKILL.md` — Task 4 (bump-gate paragraph + worked-example line)
- Create (scratch, deleted at end): `/c/sf-r1trial-fixture`, `/c/sf-r1trial-plugins/arm{1,2}`, `/c/sf-r1trial-a{1,2}` — Task 5
- Modify (conditional on trial verdict): `plugin/skills/writing-plans/SKILL.md` — Task 6
- Modify: `docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md` RESULT section — Task 6

## Pseudocode

- **T1 — API call sites:** Skipped: the only non-trivial calls are node `fs`/`JSON` built-ins, and Task 1 shows the complete replacement code inline — pseudocode would duplicate it.
- **T2 — Handler/pattern reuse:** Skipped: the A/B trial harness follows `docs/patterns/ab-test-live-trials-for-behavior-change.md` and `docs/patterns/seed-trial-fixtures-with-real-docs.md` directly; Task 5 cites both and restating them adds no signal.
- **T3 — DTO/schema shape:**
  ```
  .version-bump.json shape the four helpers consume:
      files: list of { path: repo-relative file, field: dot-path like "version" or "plugins.0.version" }
      audit.exclude: list of glob-ish names to skip during audit
  read a dot-path: split field on ".", walk the parsed JSON one part at a time
      (JS array indexing accepts the string "0", so numeric parts need no special case)
  write a dot-path: walk to the parent object, assign the last part, serialize with
      JSON.stringify(root, null, 2) plus one trailing newline
  ```
- **T4 — User-designated:** Skipped: the user designated no piece of this plan for pseudocode.

---

### Task 1: R3 — port bump-version.sh helpers from jq to node

**Files:**
- Modify: `plugin/scripts/bump-version.sh:22-52` (the `--- helpers ---` block)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: a working `plugin/scripts/bump-version.sh` whose `--check`, `--audit`, and bump modes run without `jq`. Tasks 3–4 embed instructions that invoke it; the batch's Finish runs it for real.

- [ ] **Step 1: Confirm the current failure**

Run: `bash plugin/scripts/bump-version.sh --check`
Expected: nonzero exit; stderr contains `jq: command not found` (M2's documented failure).

- [ ] **Step 2: Replace the four helper functions**

Replace the entire helpers block — everything from the line `# --- helpers ---` through the `audit_excludes()` function's closing `}` (currently lines 22–52) — with:

```bash
# --- helpers ---

# Read a dotted field path from a JSON file.
# Handles both simple ("version") and nested ("plugins.0.version") paths.
read_json_field() {
  local file="$1" field="$2"
  node -e '
    const fs = require("fs");
    const [file, field] = process.argv.slice(1);
    let v = JSON.parse(fs.readFileSync(file, "utf8"));
    for (const part of field.split(".")) v = v[part];
    console.log(v);
  ' "$file" "$field"
}

# Write a dotted field path in a JSON file (2-space indent, trailing newline).
write_json_field() {
  local file="$1" field="$2" value="$3"
  node -e '
    const fs = require("fs");
    const [file, field, value] = process.argv.slice(1);
    const root = JSON.parse(fs.readFileSync(file, "utf8"));
    const parts = field.split(".");
    let obj = root;
    for (const part of parts.slice(0, -1)) obj = obj[part];
    obj[parts[parts.length - 1]] = value;
    fs.writeFileSync(file, JSON.stringify(root, null, 2) + "\n");
  ' "$file" "$field" "$value"
}

# Read the list of declared files from config.
# Outputs lines of "path<TAB>field"
declared_files() {
  node -e '
    const cfg = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
    for (const f of cfg.files) console.log(f.path + "\t" + f.field);
  ' "$CONFIG"
}

# Read the audit exclude patterns from config.
audit_excludes() {
  node -e '
    const cfg = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
    for (const p of (cfg.audit && cfg.audit.exclude) || []) console.log(p);
  ' "$CONFIG" 2>/dev/null
}
```

Accepted limitation (spec Consequences apply): a dot-path naming a missing field prints `undefined` instead of jq's `null`. The config file is repo-controlled; no task or caller branches on that output.

- [ ] **Step 3: Run --check (spec acceptance 1)**

Run: `bash plugin/scripts/bump-version.sh --check`
Expected: exit 0; seven lines listing the declared files each at `6.4.0`; final line `All declared files are in sync at 6.4.0`.

- [ ] **Step 4: Confirm jq is gone (spec acceptance 2)**

Run: `grep -c jq plugin/scripts/bump-version.sh || true`
Expected: `0` (at plan time the count was 9; every occurrence lives in the replaced block).

- [ ] **Step 5: Round-trip bump in a scratch copy (spec acceptance 3)**

```bash
rm -rf /c/sf-bump-test && mkdir -p /c/sf-bump-test
cp -r plugin /c/sf-bump-test/plugin
cd /c/sf-bump-test/plugin
git init -q . && git add -A && git -c user.email=t@t -c user.name=t commit -qm base
bash scripts/bump-version.sh 9.9.9
git diff --stat
git diff -U0 | grep -E '^[+-][^+-]' | grep -vc '"version"' || true
cd "C:/Users/marko/IdeaProjects/personal_products/superfunk"
rm -rf /c/sf-bump-test
```

Expected: `git diff --stat` lists exactly 7 changed files (the declared list); the final grep prints `0` — every changed line contains `"version"` (git's autocrlf normalization keeps EOL flips out of the diff). The bump's trailing auto-audit may print UNDECLARED findings inside the scratch copy; ignore them there.

- [ ] **Step 6: Run --audit on the real repo (spec acceptance 4)**

Run: `bash plugin/scripts/bump-version.sh --audit`
Expected: exit 0, runs to completion with no `command not found`. It may list UNDECLARED files containing `6.4.0` (spec RESULT sections mention version numbers); copy any such list into the task results verbatim — reporting, not fixing, is this step's job.

- [ ] **Step 7: Commit**

```bash
git add plugin/scripts/bump-version.sh
git commit -m "fix(scripts): port bump-version.sh helpers from jq to node so --check runs (R3)

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

---

### Task 2: R2 — outcome-space point 6 in the A/B pattern

**Files:**
- Modify: `docs/patterns/ab-test-live-trials-for-behavior-change.md:20` (insert after Rule 1's point 5)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: Rule 1 point 6, which Task 5's decision-rule application must satisfy.

- [ ] **Step 1: Insert point 6**

Rule 1's points sit one per physical line. Insert this as one physical line directly after point 5 (the line ending `...(the instruction gets followed).`) and before the blank line preceding `**Rule 2`:

```
6. Pre-register the decision rule by scoring each arm and fixture independently, then combining the per-unit states exhaustively — enumerate the full outcome space, never a list of example branches. An outcome with no covering branch means the decision rule fails this step.
```

(The spec quotes this same string wrapped for readability; the content is identical, and the single-line format matches points 1–5.)

- [ ] **Step 2: Verify**

Run: `grep -c "enumerate the full outcome space, never a list of example branches" docs/patterns/ab-test-live-trials-for-behavior-change.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add docs/patterns/ab-test-live-trials-for-behavior-change.md
git commit -m "docs(patterns): Rule 1 point 6 — pre-register decision rules over the full outcome space (R2)

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

---

### Task 3: R4a — Finish Bookkeeping section in executing-plans

**Files:**
- Modify: `plugin/skills/executing-plans/SKILL.md` (insert new Step 3 after Step 2; renumber old Step 3 heading to Step 4)

**Interfaces:**
- Consumes: Task 1's working script (item 7 invokes it).
- Produces: the eight-item bookkeeping list; Task 4 inserts the byte-matching bump-gate wording into SDD.

- [ ] **Step 1: Renumber the old Step 3**

Change the heading `### Step 3: Complete Development` to `### Step 4: Complete Development`. (No other text in the file or in `plugin/skills/executing-plans/` references "Step 3" or "Step 4" — verified at plan time; the only step cross-reference is "Return to Review (Step 1)".)

- [ ] **Step 2: Insert the new Step 3 section**

Insert between the end of the Step 2 section (after the line `4. Mark as completed`) and the new `### Step 4: Complete Development` heading, with one blank line on each side:

````markdown
### Step 3: Finish Bookkeeping

After all tasks complete and verified, and before Step 4, perform the
same bookkeeping superfunk:subagent-driven-development's Finish section
performs for dispatched plans:

1. **notes.md gate:** Verify each executed task's catches and findings
   got logged to `docs/superpowers/process-reviews/notes.md`. Append any
   missing lines now.
2. **Spec Status flip:** If this plan traces to a design spec, update
   that spec's `Status` line to `Shipped` and commit the change.
3. **Tracker append:** Append the spec filename to
   `docs/superpowers/process-reviews/tracker.md`'s "Specs shipped since"
   list, in the same commit. At 3 or more entries, offer to run
   superfunk:process-review now — ask, don't force.
4. **Recommendation checkbox:** If the spec's Context names a
   `review-after-*.md` file, find the matching `- [ ]` line, change it
   to `- [x]`, and append `(Shipped as <what shipped>, commit <sha>.)`
   — in the same commit as items 2–3.
5. **Verify items 2–4 landed:**
   ```bash
   grep -c "^\*\*Status:\*\* Shipped" <spec-file>
   grep -c "<spec filename>" docs/superpowers/process-reviews/tracker.md
   grep -c "\[x\].*<distinctive words from the Recommendation>" <review-file>
   ```
   Each applicable check returns at least 1. A 0 means that action never
   happened — do it now.
6. **Lessons capture:** Capture a notable learning in
   `docs/lessons-learned.md`, or record that nothing notable arose.
   Follow the detailed lesson-and-promotion procedure in
   superfunk:subagent-driven-development's Finish section.
7. **Version bump:**
   If the branch's diff touches `plugin/`, run
   `plugin/scripts/bump-version.sh <new-version>` and commit the result —
   minor bump for `plugin/skills/` changes, patch otherwise. Unsure
   whether the bump already happened: run `--check` first.
8. **Concept index:** If this plan's File Structure created, renamed,
   moved, or deleted a skill, feature, or significant directory, update
   `docs/architecture/concept-index.md` per superfunk:concept-index
   Step 3, using the trigger conditions in
   superfunk:subagent-driven-development's Finish section.
````

- [ ] **Step 3: Run the docs check (User-Facing: Yes)**

Run: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md <task-base-sha> HEAD`
Expected: a verdict line; on `ACTION_NEEDED`, draft the README/CHANGELOG update in this task and commit it alongside.

- [ ] **Step 4: Verify**

```bash
grep -c "### Step 3: Finish Bookkeeping" plugin/skills/executing-plans/SKILL.md
grep -c "### Step 4: Complete Development" plugin/skills/executing-plans/SKILL.md
grep -c "^7\. \*\*Version bump:\*\*" plugin/skills/executing-plans/SKILL.md
```
Expected: `1`, `1`, `1`.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/executing-plans/SKILL.md
git commit -m "feat(executing-plans): add Step 3 Finish Bookkeeping so the inline path carries SDD's gates (R4)

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

---

### Task 4: R4b — bump gate in SDD's Finish, worked example refreshed

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md` (one paragraph in Finish; one line in Example Workflow)

**Interfaces:**
- Consumes: Task 3's gate wording — the inserted paragraph must match it after indent-normalization.
- Produces: the dispatched path's version-bump gate.

- [ ] **Step 1: Insert the gate paragraph**

In the Finish section, find the lessons-capture paragraph ending `...or their own commit if the tracker didn't\nchange.` Insert after it, as its own paragraph (blank line before and after), before the paragraph starting `If docs/architecture/concept-index.md exists`:

```
If the branch's diff touches `plugin/`, run
`plugin/scripts/bump-version.sh <new-version>` and commit the result —
minor bump for `plugin/skills/` changes, patch otherwise. Unsure
whether the bump already happened: run `--check` first.
```

- [ ] **Step 2: Refresh the worked example**

In the Example Workflow's Finish block, insert between the line
`[Finish: captured a Lesson in lessons-learned.md; no pattern promoted, one instance so far]`
and the line
`[Finish: no concept-index entry needed -- no skill/feature/significant directory created]`:

```
[Finish: branch diff touches plugin/skills/ -- ran scripts/bump-version.sh with a minor bump, committed]
```

(Position matches the text's order: lessons → bump → concept-index. This step exists because item 9 of writing-plans' Self-Review flags exactly this stale-example failure.)

- [ ] **Step 3: Run the docs check (User-Facing: Yes)**

Run: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md <task-base-sha> HEAD`
Expected: a verdict line; on `ACTION_NEEDED`, draft the update in this task.

- [ ] **Step 4: Verify wording identity across both files (spec criterion 4)**

```bash
grep -A3 "^If the branch's diff touches" plugin/skills/subagent-driven-development/SKILL.md > "$TMPDIR/gate-sdd.txt"
grep -A3 "If the branch's diff touches" plugin/skills/executing-plans/SKILL.md | sed 's/^ *//' > "$TMPDIR/gate-ep.txt"
diff "$TMPDIR/gate-sdd.txt" "$TMPDIR/gate-ep.txt" && echo IDENTICAL
```
Expected: `IDENTICAL` (empty diff). Also run:
`grep -c "ran scripts/bump-version.sh with a minor bump" plugin/skills/subagent-driven-development/SKILL.md`
Expected: `1`.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat(sdd): add the version-bump gate to Finish, refresh the worked example (R4)

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

---

### Task 5: R1 — run the A/B trial

**Files:**
- Create (scratch): `/c/sf-r1trial-fixture`, `/c/sf-r1trial-plugins/arm1`, `/c/sf-r1trial-plugins/arm2`, `/c/sf-r1trial-plugins/trial-settings.json`, `/c/sf-r1trial-a1`, `/c/sf-r1trial-a2`
- Create: `docs/superpowers/process-reviews/r1-drafted-insertion-trial/` (archive of prompts, outputs, judge verdict)

**Interfaces:**
- Consumes: the pre-registered criterion and decision rule in the spec (commits `2f68049`, `5060812`).
- Produces: a scored decision-rule branch for Task 6.

The criterion, verbatim from the spec: *during plan writing, the agent runs a grep against a file that contains its own drafted insertion text, before it finalizes the plan.* Evidence comes from the transcript or the produced plan. The judge must quote what it scored.

- [ ] **Step 1: Build the fixture (real doc content, per seed-trial-fixtures-with-real-docs)**

```bash
rm -rf /c/sf-r1trial-fixture && mkdir -p /c/sf-r1trial-fixture/docs/specs
cd /c/sf-r1trial-fixture && git init -q .
cp "C:/Users/marko/IdeaProjects/personal_products/superfunk/docs/code-standards.md" docs/code-standards.md
```

Write `/c/sf-r1trial-fixture/docs/specs/error-message-rules-design.md` with exactly:

```markdown
# Error-Message Copy Rules — Design

**Date:** 2026-09-02
**Status:** Approved

## Context

Support tickets quote error messages that name neither the failing
input nor the format the tool expected. The style guide in
`docs/code-standards.md` covers naming and file layout and says
nothing about error-message copy.

## Design

Append a new section titled `## Error-Message Copy` to the end of
`docs/code-standards.md`, containing exactly this text:

    Error messages must name the failing input and the expected
    format in the same sentence, so a user can correct the mistake
    without reading source code. Log lines above WARN must carry the
    request identifier. Never truncate an identifier in user-facing
    output.

## Falsifiable Criterion

`docs/code-standards.md` ends with the section above, word for word.
```

Then:

```bash
echo "Style-guide fixture repo." > README.md
git add -A && git -c user.email=t@t -c user.name=t commit -qm "seed fixture"
```

(The insertion text arrives pre-wrapped at ~66 columns — a verification grep anchored on a multi-word phrase like "the expected format in the same sentence" crosses a line break and returns 0. That gives the mechanism under test something real to catch, without the prompt ever mentioning greps, anchors, or scratch files.)

- [ ] **Step 2: Build the arms**

```bash
rm -rf /c/sf-r1trial-plugins && mkdir -p /c/sf-r1trial-plugins
cp -r "C:/Users/marko/IdeaProjects/personal_products/superfunk/plugin" /c/sf-r1trial-plugins/arm1
cp -r "C:/Users/marko/IdeaProjects/personal_products/superfunk/plugin" /c/sf-r1trial-plugins/arm2
```

In `/c/sf-r1trial-plugins/arm2/skills/writing-plans/SKILL.md`, Self-Review item 10, append this exact text to the end of the item — after the sentence ending `` ...counts as the same failure as an unchecked `Expected:` value. `` and before the blank line preceding item 11 — as a continuation of the same paragraph, wrapped at the file's ~72-column style:

```
For each task that inserts new text and verifies it with a grep, write
the task's drafted insertion text to a scratch file and run the task's
own verification grep against that file before finalizing the plan. A
grep that returns 0 against the drafted text means the anchor fails
after insertion too — a wrapped line, a duplicate, or a count that
exists only in text not yet inserted. Fix the anchor or the text now,
not at execution time.
```

Verify the arms differ in exactly one file:

```bash
diff -rq /c/sf-r1trial-plugins/arm1 /c/sf-r1trial-plugins/arm2
```
Expected: exactly one line, naming `skills/writing-plans/SKILL.md`.

Write `/c/sf-r1trial-plugins/trial-settings.json` with exactly:

```json
{
  "enabledPlugins": {
    "superpowers@claude-plugins-official": false,
    "context-mode@context-mode": false,
    "chrome-devtools-mcp@claude-plugins-official": false,
    "frontend-design@claude-plugins-official": false,
    "github@claude-plugins-official": false
  }
}
```

- [ ] **Step 3: Copy the fixture per arm and launch both runs**

```bash
cp -r /c/sf-r1trial-fixture /c/sf-r1trial-a1
cp -r /c/sf-r1trial-fixture /c/sf-r1trial-a2
```

Launch both in parallel (run_in_background), byte-identical prompts:

```bash
cd /c/sf-r1trial-a1 && claude -p --plugin-dir /c/sf-r1trial-plugins/arm1 --settings /c/sf-r1trial-plugins/trial-settings.json --dangerously-skip-permissions --output-format text "Read docs/specs/error-message-rules-design.md and write the implementation plan for it using your writing-plans skill. Save the plan to docs/plans/."
```

```bash
cd /c/sf-r1trial-a2 && claude -p --plugin-dir /c/sf-r1trial-plugins/arm2 --settings /c/sf-r1trial-plugins/trial-settings.json --dangerously-skip-permissions --output-format text "Read docs/specs/error-message-rules-design.md and write the implementation plan for it using your writing-plans skill. Save the plan to docs/plans/."
```

The permission auto-classifier sometimes blocks one of two identical parallel launches; retry the blocked one once, identically and immediately. An arm that dies or produces no plan file re-runs once on a fresh fixture copy before scoring (spec's degenerate-outcome branch).

- [ ] **Step 4: Extract evidence mechanically**

For each arm: collect the produced plan file(s) under `docs/plans/`, and extract every Bash command from the session transcript (newest `.jsonl` under the fixture's `~/.claude/projects/` slug directory):

```bash
node -e '
  const fs = require("fs");
  const lines = fs.readFileSync(process.argv[1], "utf8").split("\n").filter(Boolean);
  for (const l of lines) {
    let j; try { j = JSON.parse(l); } catch { continue; }
    const content = j.message && j.message.content;
    if (!Array.isArray(content)) continue;
    for (const c of content)
      if (c.type === "tool_use" && (c.name === "Bash" || c.name === "PowerShell"))
        console.log("---\n" + (c.input.command || ""));
  }
' "<transcript path>" > "<arm label>-commands.txt"
```

This extraction is mechanical — no judgment applied, both arms processed identically.

- [ ] **Step 5: Blind-judge both arms**

Randomly assign labels A/B to the two arms (record the mapping only after the verdict). Run a fresh judge with no plugin dir:

```bash
claude -p --dangerously-skip-permissions --output-format text "You are scoring two plan-writing sessions, A and B. For each, you get the session's produced plan document and the full list of shell commands it ran. Criterion, to be applied exactly as worded: during plan writing, the agent ran a grep against a file that contained its own drafted insertion text (the text the plan proposes to insert), before finalizing the plan. A grep against a pre-existing target file does not count. For each of A and B answer YES or NO, and quote verbatim the exact command or plan sentence you scored — a verdict without a quote is invalid. Files: <paths to A plan, A commands, B plan, B commands>"
```

Before acting on any YES, read the judge's quoted evidence against the criterion's own wording (pattern Rule 4): the quote must show a grep whose target file holds drafted insertion text. A quote that misses the criterion marks the run inconclusive — do not re-score old outputs under loosened wording; register any corrected criterion in a commit predating new outputs.

- [ ] **Step 6: Score the decision rule and archive**

Apply the spec's pre-registered table:

| Arm 1 fires | Arm 2 fires | Verdict |
|---|---|---|
| no | yes | Ship the exact string. |
| no | no | Ship nothing — the wording does not fire. |
| yes | yes | Ship nothing — the baseline already performs the act. |
| yes | no | Ship nothing; record the anomaly as a finding. |

Archive to `docs/superpowers/process-reviews/r1-drafted-insertion-trial/`: the fixture spec, both prompts, both produced plans, both command extracts, the judge prompt and verdict, and the label mapping. Commit:

```bash
git add docs/superpowers/process-reviews/r1-drafted-insertion-trial/
git commit -m "test(trial): R1 drafted-insertion A/B trial outputs and verdict

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

---

### Task 6: R1 — ship or record, fill RESULT, clean up

**Files:**
- Modify (only on a ship verdict): `plugin/skills/writing-plans/SKILL.md` (Self-Review item 10)
- Modify: `docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md` (RESULT section)

**Interfaces:**
- Consumes: Task 5's scored verdict and arm-2 SKILL.md edit.
- Produces: the final state of R1.

- [ ] **Step 1: Branch on the verdict**

**Ship branch (arm 1 no / arm 2 yes):** copy arm 2's item-10 edit into `plugin/skills/writing-plans/SKILL.md` character-for-character. Then verify byte-identity against the arm:

```bash
diff <(sed -n '/^\*\*10\. Verified numeric expectations:\*\*/,/^\*\*11\./p' plugin/skills/writing-plans/SKILL.md) \
     <(sed -n '/^\*\*10\. Verified numeric expectations:\*\*/,/^\*\*11\./p' /c/sf-r1trial-plugins/arm2/skills/writing-plans/SKILL.md) && echo IDENTICAL
```
Expected: `IDENTICAL`. Also: `grep -c "run the task's" plugin/skills/writing-plans/SKILL.md` → Expected: `1`.

Then run the docs check: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md <task-base-sha> HEAD` — on `ACTION_NEEDED`, draft the update in this task.

**Any no-ship branch:** change nothing in `plugin/skills/`.

- [ ] **Step 2: Fill the spec's RESULT section**

Replace `*(filled at Finish)*` with: the decision-rule branch reached, the judge's quoted evidence for each arm, ship/no-ship per item R1, and one line each confirming R2, R3 (the four acceptance outputs), and R4 (the identity diff) landed. State plainly anything that failed or surprised.

- [ ] **Step 3: Delete the scratch directories**

```bash
rm -rf /c/sf-r1trial-fixture /c/sf-r1trial-plugins /c/sf-r1trial-a1 /c/sf-r1trial-a2
```
(The archive from Task 5 Step 6 is the durable record.)

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md
git commit -m "feat(writing-plans): R1 trial outcome — <ship: add drafted-insertion check to item 10 | no-ship: record verdict> (R1)

Part of docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md"
```

(On a no-ship branch, `git add` only the spec file.)

---

## Finish

After Task 6, this plan's Finish must itself execute the executing-plans Step 3 list shipped in Task 3 (spec criterion 5) — including the version bump: the branch diff touches `plugin/skills/`, so run `bash plugin/scripts/bump-version.sh 6.5.0` and commit. Then check off R1–R4 in `docs/superpowers/process-reviews/review-after-2026-09-01-behavioral-claim-verification-design.md` (R1's checkbox annotation states the actual trial outcome, whichever branch it reached), flip the spec Status, append the tracker, run the verification greps, capture lessons, and use superfunk:finishing-a-development-branch.
