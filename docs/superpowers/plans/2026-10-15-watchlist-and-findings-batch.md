# Watchlist and Findings Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the seven parts (A–G) of `docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md`: a durable watchlist, the RELEASE-NOTES backfill and bump duty, the `check_docs.py` path, encoding, and section-parse fixes, a `**Spec:**` plan-header field, and a five-type `notes.md` vocabulary.

**Architecture:** Four tasks, ordered so that each shared file changes once per task and each task's doc check can pass on its own. Task 1 fixes `check_docs.py` first, so later tasks' `plugin/RELEASE-NOTES.md` edits register as doc updates. Each task adds one bullet to an open `## v6.7.0 (unreleased)` entry, and Finish dates that entry in the bump commit.

**Tech Stack:** Python 3.7 or later (`check_docs.py` calls `sys.stdout.reconfigure`; pytest), Markdown skill files, git, bash.

**Spec:** `docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md`

## Global Constraints

- Spec carries `User-Facing: Yes`. Every task runs `check_docs.py` over its own range and adds its own bullet under `## v6.7.0 (unreleased)` in `plugin/RELEASE-NOTES.md`, in the same task.
- No trials (spec Decision 2). No task dispatches a `--plugin-dir` session.
- In `plugin/RELEASE-NOTES.md`, everything from the `## v6.2.0 (2026-07-23)` heading down stays byte-identical.
- Both bump-gate copies (`subagent-driven-development/SKILL.md`, `executing-plans/SKILL.md`) read identically after indent normalization.
- The three spec-trace definitions (SDD Final Review, SDD Finish, `executing-plans` Step 2.5 item 1) name their sources in one order: the `**Spec:**` field, the Goal line, a task's commit trailer.
- Entries already in `docs/superpowers/process-reviews/notes.md` stay as written. Only the header above `<!-- entries below this line -->` changes.
- Every target file uses LF line endings. Keep them.
- Every commit carries the trailer `Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md`.
- Finish bumps to 6.7.0 (minor: the diff touches `plugin/skills/`). The bump commit replaces `## v6.7.0 (unreleased)` with `## v6.7.0 (<bump date>)`. That edit satisfies the new release-notes duty for this batch (spec criterion 11).
- Out of scope: G1/G2/G3 themselves, the SDD Finish step that reads `Gap` entries, findings A1–A4 and A7–A10, and a `**Spec:**` field for the 42 existing plans.

---

## File Structure

`.context.md` check: none exists in any directory this plan touches. Checked: `plugin/skills/documentation/`, `plugin/skills/documentation/scripts/`, `plugin/skills/process-review/`, `plugin/skills/writing-plans/`, `plugin/skills/subagent-driven-development/`, `plugin/skills/executing-plans/`, `plugin/`, `docs/superpowers/process-reviews/`, `docs/bugs/`, `docs/superpowers/specs/`.

| File | Task | Change |
|---|---|---|
| `plugin/skills/documentation/scripts/check_docs.py` | 1 | Heading pattern, `SECTION_NOT_FOUND` marker, UTF-8 stdout, two nested doc paths |
| `plugin/skills/documentation/scripts/test_check_docs.py` | 1 | Six new tests |
| `plugin/skills/documentation/SKILL.md` | 1 | Step 2 item 3 learns the marker |
| `docs/bugs/BUG-0001-check-docs-nested-path-matching.md`, `docs/bugs/BUG-0002-check-docs-windows-encoding-crash.md`, `docs/bugs/tracker.md` | 1 | Status `Fixed`, Resolution filled |
| `docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md` | 1 | Deferred bullet annotated as resolved |
| `plugin/RELEASE-NOTES.md` | 1, 2, 3, 4 | Task 1 opens v6.7.0; Task 2 adds the Fork note and v6.3.0–v6.6.0; each task adds one bullet |
| `plugin/skills/subagent-driven-development/SKILL.md` | 2, 4 | Task 2: bump-gate duty and worked-example line; Task 4: two spec-trace definitions |
| `plugin/skills/executing-plans/SKILL.md` | 2, 4 | Task 2: bump-gate duty; Task 4: one spec-trace definition |
| `docs/superpowers/process-reviews/notes.md` | 3 | Header: five-type table and pipe rule |
| `docs/superpowers/process-reviews/watchlist.md` | 3 | Create, with six seed entries |
| `plugin/skills/process-review/SKILL.md` | 3, 4 | Task 3: step 2 rewrite, new step 5, synthesis clauses, renumber; Task 4: step 3 third rule, Specs Reviewed |
| `plugin/skills/writing-plans/SKILL.md` | 4 | Header template `**Spec:**` line, item 11 element list |

The new file `watchlist.md` follows `docs/code-standards.md` File Naming: kebab-case markdown.

## Pseudocode

- **T1 — API call sites:** Skipped: no task adds a call. `check_docs.py` keeps its one `git diff --name-only` call unchanged.
- **T2 — Handler/pattern reuse (Task 4):** the third outcomes rule mirrors the shape of step 3's two existing lookup rules.
  ```
  for each spec in the review window:
      found = outcomes file by stem rule, else by date rule (unchanged)
      for each plan file that is not an outcomes file:
          if the plan's Spec header line names this spec:
              add that plan's outcomes file to found, if it exists
      read every file in found, once each
      list every file in found under the spec in Specs Reviewed, or "none"
  ```
- **T3 — DTO/schema shape (Task 3):** a `notes.md` entry carries five fields, and field 2 decides the route.
  ```
  for each entry dated after the last review:
      split the entry on each pipe that has no backslash before it
      read type from field 2
      if type is Catch: send to the Catch synthesis (four or five fields, as before)
      if type is Miss: send to Misses, with no recurrence threshold
      if type is Gap: send to Gaps; if field 4 is empty, read it as "no mechanism proposed"
      if type is Friction: send to Friction
      if type is Watch: send to the watchlist step
  ```
- **T4 — User-designated:** Skipped: the human partner designated no piece of this plan for pseudocode.

---

### Task 1: `check_docs.py` section parse, paths, and encoding (spec parts D and E)

**Files:**
- Modify: `plugin/skills/documentation/scripts/check_docs.py:15-20` (`extract_section`), `:36` (start of `main`), `:47` (doc path set), `:56-62` (section printing)
- Test: `plugin/skills/documentation/scripts/test_check_docs.py` (append six tests)
- Modify: `plugin/skills/documentation/SKILL.md:35` (Step 2 item 3)
- Modify: `plugin/RELEASE-NOTES.md:1-3`
- Modify: `docs/bugs/BUG-0001-check-docs-nested-path-matching.md`, `docs/bugs/BUG-0002-check-docs-windows-encoding-crash.md`, `docs/bugs/tracker.md`
- Modify: `docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md:79`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `extract_section(spec_text, heading) -> str` (same signature; returns `""` when no heading matches). The marker string `SECTION_NOT_FOUND: read "<heading>" from the spec directly`. The heading `## v6.7.0 (unreleased)` in `plugin/RELEASE-NOTES.md`, which Tasks 2–4 append bullets under.

- [ ] **Step 1: Append the six failing tests**

Append to the end of `plugin/skills/documentation/scripts/test_check_docs.py`:

```python


def test_extract_section_numbered_heading():
    spec = "## 1. Context\n\nNumbered context.\n\n## 2. Decision\n\nNumbered decision.\n"
    assert extract_section(spec, "Context") == "Numbered context."
    assert extract_section(spec, "Decision") == "Numbered decision."


def test_extract_section_plural_heading():
    spec = "## Decisions\n\nPlural decision.\n\n## Consequences\n\nLast.\n"
    assert extract_section(spec, "Decision") == "Plural decision."


def test_extract_section_rejects_longer_heading():
    spec = "## Decision Log\n\nNot the decision.\n"
    assert extract_section(spec, "Decision") == ""


def test_end_to_end_missing_section_prints_marker(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text(
        "**Date:** 2026-10-15\n**User-Facing:** Yes\n\n"
        "## Context\n\nUsers hit a bug.\n\n"
        "## Decision\n\nFix the bug this way.\n"
    )
    base_sha = _commit_all(repo, "base")
    (repo / "fix.py").write_text("x = 2")
    head_sha = _commit_all(repo, "fix")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 1
    assert result.stdout.startswith("ACTION_NEEDED")
    assert 'SECTION_NOT_FOUND: read "Consequences" from the spec directly' in result.stdout
    assert "Users hit a bug." in result.stdout


def test_end_to_end_already_updated_nested_release_notes(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text("**Date:** 2026-10-15\n**User-Facing:** Yes\n\n## Context\n\nSomething.\n")
    base_sha = _commit_all(repo, "base")
    (repo / "plugin").mkdir()
    (repo / "plugin" / "RELEASE-NOTES.md").write_text("# Notes")
    head_sha = _commit_all(repo, "update release notes")

    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "ALREADY_UPDATED: plugin/RELEASE-NOTES.md" in result.stdout


def test_end_to_end_em_dash_on_cp1252_console(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    spec = repo / "spec.md"
    spec.write_text(
        "**Date:** 2026-10-15\n**User-Facing:** Yes\n\n"
        "## Context\n\nAn em dash — and an arrow → here.\n",
        encoding="utf-8",
    )
    base_sha = _commit_all(repo, "base")
    (repo / "fix.py").write_text("x = 2")
    head_sha = _commit_all(repo, "fix")

    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    result = subprocess.run(
        [sys.executable, CHECK_DOCS_PATH, str(spec), base_sha, head_sha],
        cwd=repo, capture_output=True, env=env
    )
    assert result.returncode == 1
    assert b"Traceback" not in result.stderr
    assert "An em dash — and an arrow → here." in result.stdout.decode("utf-8")
```

`test_extract_section_rejects_longer_heading` guards the widened pattern against over-match. It passes before and after the change.

- [ ] **Step 2: Run the tests and watch five fail**

Run: `cd plugin/skills/documentation/scripts && python -m pytest -q test_check_docs.py`
Expected: `5 failed, 11 passed`. The failures: `test_extract_section_numbered_heading`, `test_extract_section_plural_heading`, `test_end_to_end_missing_section_prints_marker`, `test_end_to_end_already_updated_nested_release_notes`, `test_end_to_end_em_dash_on_cp1252_console`.

- [ ] **Step 3: Implement the four script edits**

In `check_docs.py`, replace the `extract_section` pattern line:

```python
    pattern = r'^## ' + re.escape(heading) + r'\n(.*?)(?=^## |\Z)'
```

with:

```python
    pattern = r'^##\s+(?:\d+\.\s+)?' + re.escape(heading) + r's?[ \t]*\n(.*?)(?=^## |\Z)'
```

In `main()`, replace:

```python
    spec_file, base_sha, head_sha = sys.argv[1], sys.argv[2], sys.argv[3]
```

with:

```python
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    spec_file, base_sha, head_sha = sys.argv[1], sys.argv[2], sys.argv[3]
```

Replace:

```python
    doc_files = [f for f in files if f in ("README.md", "CHANGELOG.md")]
```

with:

```python
    doc_files = [f for f in files if f in ("README.md", "CHANGELOG.md", "plugin/README.md", "plugin/RELEASE-NOTES.md")]
```

Replace:

```python
    print("ACTION_NEEDED")
    print("## Context")
    print(context)
    print("## Decision")
    print(decision)
    print("## Consequences")
    print(consequences)
```

with:

```python
    print("ACTION_NEEDED")
    for heading, body in (("Context", context), ("Decision", decision), ("Consequences", consequences)):
        print("## " + heading)
        print(body or 'SECTION_NOT_FOUND: read "{}" from the spec directly'.format(heading))
```

- [ ] **Step 4: Run the tests and watch all pass**

Run: `cd plugin/skills/documentation/scripts && python -m pytest -q test_check_docs.py`
Expected: `16 passed`.

- [ ] **Step 5: Run the script against real project data (spec criteria 5 and 6)**

Run from the repo root:

```bash
python - <<'EOF'
import glob, os, re, sys
sys.path.insert(0, 'plugin/skills/documentation/scripts')
from check_docs import extract_section, read_user_facing
for root in ['.', os.path.expanduser('~/source/repos/ArcGISProMCP')]:
    specs = glob.glob(root + '/docs/superpowers/specs/*-design.md')
    if not specs:
        print(root, 'absent'); continue
    uf = [s for s in specs if read_user_facing(open(s, encoding='utf-8').read()) == 'Yes']
    empty = sum(1 for s in uf for h in ('Context', 'Decision', 'Consequences')
                if not extract_section(open(s, encoding='utf-8').read(), h))
    print(root, 'user-facing', len(uf), 'empty', empty)
EOF
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-09-02-executing-plans-review-step-design.md HEAD~1 HEAD; echo "exit $?"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md HEAD~1 HEAD > /dev/null; echo "exit $?"
```

Expected:
- `. user-facing 8 empty 0`. The count reads 8 because this batch's own spec joins the 7 measured at spec time.
- `.../ArcGISProMCP user-facing 16 empty 0`, or `absent` on a machine without that repo.
- `NOT_APPLICABLE: User-Facing field is 'No', not 'Yes'` then `exit 0`.
- `exit 1` with no traceback for the em-dash spec.

- [ ] **Step 6: Teach `documentation` Step 2 the marker**

In `plugin/skills/documentation/SKILL.md`, replace:

```
3. If the output starts with `ACTION_NEEDED`: read the Context/Decision/Consequences content the script printed. Draft:
```

with:

```
3. If the output starts with `ACTION_NEEDED`: read the Context/Decision/Consequences content the script printed. A section printed as `SECTION_NOT_FOUND` means the script could not find that heading in the spec — read that section from the spec file directly. Draft:
```

Run: `grep -c "SECTION_NOT_FOUND" plugin/skills/documentation/SKILL.md`
Expected: `1`.

- [ ] **Step 7: Open the v6.7.0 entry with this task's bullet**

In `plugin/RELEASE-NOTES.md`, replace the first three lines:

```
# Superpowers Release Notes

## v6.2.0 (2026-07-23)
```

with:

```
# Superpowers Release Notes

## v6.7.0 (unreleased)

- **`check_docs.py` reads numbered and plural section headings, and marks a section it cannot find.** `## 2. Decision` and `## Decisions` now match. A missing section prints `SECTION_NOT_FOUND: read "<heading>" from the spec directly` in place of an empty body. The script also recognizes `plugin/README.md` and `plugin/RELEASE-NOTES.md`, and no longer crashes on a Windows console.

## v6.2.0 (2026-07-23)
```

- [ ] **Step 8: Commit the fix**

```bash
git add plugin/skills/documentation/scripts/check_docs.py plugin/skills/documentation/scripts/test_check_docs.py plugin/skills/documentation/SKILL.md plugin/RELEASE-NOTES.md
git commit -m "fix(documentation): check_docs.py reads numbered and plural headings, marks a missing section, fixes nested paths and Windows output

Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md"
```

- [ ] **Step 9: Close both bugs and annotate the rebrand spec**

Use the SHA from Step 8 as `<fix-sha>`.

In `docs/bugs/BUG-0001-check-docs-nested-path-matching.md`: change `**Status:** Open` to `**Status:** Fixed`, and replace the `## Resolution` body line with:

```
`check_docs.py`'s doc-path set now lists `plugin/README.md` and `plugin/RELEASE-NOTES.md` beside the two root-level names (commit `<fix-sha>`). A test covers a nested `plugin/RELEASE-NOTES.md`. The set stays an explicit list: a doc file outside it still reads as `ACTION_NEEDED`.
```

In `docs/bugs/BUG-0002-check-docs-windows-encoding-crash.md`: change `**Status:** Open` to `**Status:** Fixed`, and replace the `## Resolution` body line with:

```
`main()` now calls `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` before any output (commit `<fix-sha>`). A test runs the script under `PYTHONIOENCODING=cp1252` with an em dash and an arrow in the spec, and checks for no traceback.
```

In `docs/bugs/tracker.md`: change the `Open` Status cell to `Fixed` in both rows.

In `docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md`, append to the end of the Deferred bullet that begins `- Recognizing \`RELEASE-NOTES.md\``:

```
 (Resolved by `2026-10-15-watchlist-and-findings-batch-design.md`, part D: `check_docs.py` now recognizes `plugin/RELEASE-NOTES.md`.)
```

Run: `grep -c "Fixed" docs/bugs/tracker.md; grep -c "Resolved by \`2026-10-15" docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md`
Expected: `2`, then `1`.

- [ ] **Step 10: Run the docs check over this task's range**

Run: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md <task-base-sha> HEAD`
Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0. The fixed script now recognizes the Step 7 edit.

- [ ] **Step 11: Commit the bookkeeping**

```bash
git add docs/bugs/ docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md
git commit -m "docs(bugs): close BUG-0001 and BUG-0002, resolve the rebrand spec's RELEASE-NOTES deferral

Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md"
```

---

### Task 2: RELEASE-NOTES backfill and the bump-gate duty (spec parts B and C)

**Files:**
- Modify: `plugin/RELEASE-NOTES.md` (Fork note, one bullet, four backfilled versions)
- Modify: `plugin/skills/subagent-driven-development/SKILL.md:631-633` (bump gate), `:752` (worked example)
- Modify: `plugin/skills/executing-plans/SKILL.md:111-114` (bump gate)

**Interfaces:**
- Consumes: Task 1's `## v6.7.0 (unreleased)` heading and its bullet.
- Produces: the gate sentence that Finish follows at this batch's own bump.

- [ ] **Step 1: Add the Fork note**

In `plugin/RELEASE-NOTES.md`, replace:

```
# Superpowers Release Notes

## v6.7.0 (unreleased)
```

with:

```
# Superpowers Release Notes

> **Fork note.** superfunk diverged from obra/superpowers after v6.2.0.
> Entries above the v6.2.0 heading describe superfunk. Upstream later
> released its own v6.3.0 with different content, so the two histories
> share version numbers by coincidence only.

## v6.7.0 (unreleased)
```

- [ ] **Step 2: Add this task's bullet and the four backfilled versions**

Directly after Task 1's bullet (the line that begins `- **\`check_docs.py\` reads numbered`), insert this bullet line:

```
- **Every version bump writes a RELEASE-NOTES entry.** Both Finish paths add the entry in the same commit as the bump. This file gains entries for v6.3.0 through v6.6.0.
```

Then, between that bullet's following blank line and `## v6.2.0 (2026-07-23)`, insert:

```
## v6.6.0 (2026-09-03)

- **`executing-plans` reviews the whole branch before Finish.** A new Step 2.5 runs the documentation check, then dispatches a whole-branch reviewer — or applies the same rubric directly when no subagent dispatch exists. It fixes every finding in one pass with one scoped re-review, and files real-and-deferred parked findings to `docs/bugs/`.

## v6.5.0 (2026-09-02)

- **`writing-plans` Self-Review item 10 checks drafted insertions.** Each task's verification grep now runs against the task's drafted text in a scratch file before the plan ships. An A/B trial gated this change.
- **Trial decision rules enumerate the outcome space.** Rule 1 of `docs/patterns/ab-test-live-trials-for-behavior-change.md` gains point 6: score each arm on its own, then combine the per-arm states exhaustively.
- **`bump-version.sh` no longer needs `jq`.** Its JSON reads moved to node, so `--check` runs on a machine without `jq`.
- **`executing-plans` gains Finish bookkeeping, and both Finish paths gain a version-bump gate.**

## v6.4.0 (2026-09-01)

- **`process-review` gains a Retirements section.** A review can propose the removal of a check for one of four fixed reasons: Subsumed, Superseded, Vacuous, or Zero-yield. `notes.md` entries gain a field that names the check behind each Catch, and every Recommendation names the check it replaces or states `net new load`.
- **Fixes from the taskq trial, batch 1.** `brainstorming` scaffold questions gain skip conditions. `finishing-a-development-branch` confirms that a PR exists before it reports success, and recognizes `.claude/worktrees/`. `writing-plans` item 10 covers asserted budgets. `subagent-driven-development` names the token-containment guard trap.
- **Three trial-gated checks.** `brainstorming` Spec Self-Review item 2 gains the rule-membership check, and item 6 widens to behavioral claims. Lesson promotion in `subagent-driven-development` compares a new Rule sentence against every existing one before it writes the promotion note.

## v6.3.0 (2026-09-01)

- **superfunk forks from obra/superpowers.** The plugin takes the superfunk name and the `superfunk:` skill prefix. Install commands point at `mattbran87/superfunk`.
- **A process feedback loop.** `process-review` synthesizes the `notes.md` running log and per-task outcome files into dated reviews. `docs/lessons-learned.md` captures lessons at Finish and promotes recurring ones to `docs/patterns/`. Finish gains bookkeeping gates.
- **Eight new skills:** `process-review`, `concept-index`, `bug-tracking`, `documentation`, `project-definition`, `multi-lens-research`, `branching-research`, and `calibrating-recommendations`.
- **Stronger planning checks.** `writing-plans` gains a Pseudocode section, and its Self-Review grows to 14 items.

```

The version contents come from the commit ranges between bump commits (`349b21c` for 6.3.0, `bc442a5` for 6.4.0, `4e11aba` for 6.5.0, `6ae85e9` for 6.6.0). The spec's part B lists them.

- [ ] **Step 3: Check the file's shape**

```bash
grep -n "^## v\|^> \*\*Fork" plugin/RELEASE-NOTES.md | head -7
sed -n '/^## v6.7.0/,/^## v6.6.0/p' plugin/RELEASE-NOTES.md | grep -c "^- "
diff <(git show HEAD:plugin/RELEASE-NOTES.md | sed -n '/^## v6.2.0/,$p') <(sed -n '/^## v6.2.0/,$p' plugin/RELEASE-NOTES.md) && echo BELOW-IDENTICAL
git diff --numstat -- plugin/RELEASE-NOTES.md
```

Expected: the Fork note on line 3, then headings `v6.7.0 (unreleased)`, `v6.6.0`, `v6.5.0`, `v6.4.0`, `v6.3.0`, `v6.2.0` in that order; `2` bullets under v6.7.0; `BELOW-IDENTICAL`; a `--numstat` line whose second column reads `0` (no deleted lines).

- [ ] **Step 4: Add the release-notes duty to both bump gates**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
minor bump for `plugin/skills/` changes, patch otherwise. Unsure
whether the bump already happened: run `--check` first.
```

with:

```
minor bump for `plugin/skills/` changes, patch otherwise. Unsure
whether the bump already happened: run `--check` first. Before that
commit, append this version's entry to `plugin/RELEASE-NOTES.md` — a
`## vX.Y.Z (date)` heading and at least one bullet — and include it in
the same commit as the bump.
```

In `plugin/skills/executing-plans/SKILL.md`, replace (3-space indent):

```
   minor bump for `plugin/skills/` changes, patch otherwise. Unsure
   whether the bump already happened: run `--check` first.
```

with:

```
   minor bump for `plugin/skills/` changes, patch otherwise. Unsure
   whether the bump already happened: run `--check` first. Before that
   commit, append this version's entry to `plugin/RELEASE-NOTES.md` — a
   `## vX.Y.Z (date)` heading and at least one bullet — and include it in
   the same commit as the bump.
```

- [ ] **Step 5: Refresh the SDD worked example (Self-Review item 9)**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace:

```
[Finish: branch diff touches plugin/skills/ -- ran scripts/bump-version.sh with a minor bump, committed]
```

with:

```
[Finish: branch diff touches plugin/skills/ -- ran scripts/bump-version.sh with a minor bump, appended the RELEASE-NOTES entry, committed both together]
```

- [ ] **Step 6: Run the identity diff over the extended gate (spec criterion 4)**

```bash
grep -A6 "^If the branch's diff touches" plugin/skills/subagent-driven-development/SKILL.md > "$TMPDIR/gate-sdd.txt"
grep -A6 "If the branch's diff touches" plugin/skills/executing-plans/SKILL.md | sed 's/^ *//' > "$TMPDIR/gate-ep.txt"
diff "$TMPDIR/gate-sdd.txt" "$TMPDIR/gate-ep.txt" && echo IDENTICAL
grep -c "append this version's entry to" plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md
grep -c "appended the RELEASE-NOTES entry" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: `IDENTICAL`; `1` for each of the two files; `1`.

- [ ] **Step 7: Run the docs check over this task's range**

Run: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md <task-base-sha> HEAD`
Expected after the commit in Step 8: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0. Run it after Step 8.

- [ ] **Step 8: Commit**

```bash
git add plugin/RELEASE-NOTES.md plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md
git commit -m "docs(release-notes): backfill v6.3.0-v6.6.0, add the fork note, make every bump write an entry

Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md"
```

---

### Task 3: Entry-type vocabulary and the watchlist (spec parts G and A)

**Files:**
- Modify: `docs/superpowers/process-reviews/notes.md:3-9` (header only)
- Create: `docs/superpowers/process-reviews/watchlist.md`
- Modify: `plugin/skills/process-review/SKILL.md:34-42` (step 2), `:61-65` (end of step 4, new step 5), `:66-83` (synthesis clauses), `:112-121` (renumber)
- Modify: `plugin/RELEASE-NOTES.md` (one bullet)

**Interfaces:**
- Consumes: Task 2's bullet under `## v6.7.0 (unreleased)`.
- Produces: `process-review` step numbers 1–9, with the watchlist step at 5 and the synthesis at 6. Task 4 edits steps 3 and 6 by their text, not their numbers.

- [ ] **Step 1: Rewrite the `notes.md` header**

In `docs/superpowers/process-reviews/notes.md`, replace:

```
Append-only log. Each entry marks one finding a review catches on its
first pass (spec-compliance, code-quality, or the final whole-branch
review), tagged `Catch`. `process-review` reads this log,
cross-references `git log`, and may surface `Miss`, `Friction`, or
`Gap` patterns across entries when it synthesizes a review file.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <check that caught it> | <one-line finding>`
```

with:

```
Append-only log. Each entry records one finding, tagged with one of the
five types below. A finding a review catches on its first pass
(spec-compliance, code-quality, or the final whole-branch review) gets
`Catch`. `process-review` reads this log, cross-references `git log`,
and routes each type to one section of its review file.

Format: `- <YYYY-MM-DD> | <type> | <task/spec label> | <field 4> | <field 5>`

| Type | Records | Field 4 | Field 5 |
|---|---|---|---|
| `Catch` | A defect found before it shipped | The check that caught it | The finding |
| `Miss` | A defect that got past a check that should have caught it | The check that missed it | The finding |
| `Gap` | A class of defect that no check covers | The mechanism it wants, or `(no mechanism proposed)` | The finding |
| `Friction` | Process cost with no defect behind it | The step that cost too much | The finding |
| `Watch` | A condition to watch, with a pre-decided action | `trigger: <condition>` | `action: <pre-decided action>` |

A literal `|` inside a field gets written as `\|`. A reader splits an
entry on unescaped `|` only. Entries written before 2026-10-15 stay as
written, including any unescaped `|` inside a finding.
```

The paragraphs about the fourth field and about four-field entries stay unchanged below it.

Run: `grep -c "^| \`" docs/superpowers/process-reviews/notes.md; grep -c "splits an" docs/superpowers/process-reviews/notes.md; git diff -U0 -- docs/superpowers/process-reviews/notes.md | grep -c '^[-+]- 20'`
Expected: `5`, `1`, `0`. The last count shows that no entry line changed.

- [ ] **Step 2: Create `watchlist.md` with the six seed entries**

Create `docs/superpowers/process-reviews/watchlist.md`:

````markdown
# Watchlist

Durable store for `Watch` entries. A session logs a `Watch` entry to
`notes.md`. Each process review appends the window's `Watch` entries
here, then evaluates every entry's trigger (`process-review` step 5).

Entry format:

```markdown
- **<kebab-slug>** (added YYYY-MM-DD, <origin spec or discussion>)
  - Watching: <the thing under watch>
  - Trigger: <observable condition>
  - Action when tripped: <pre-decided action>
```

<!-- entries below this line -->
- **item-10-accretion** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: `writing-plans` Self-Review item 10's duties.
  - Trigger: any change gives item 10 a fourth duty. It carries three today: run the `Expected:` count commands, check budget arithmetic, and run the drafted-insertion grep.
  - Action when tripped: split item 10 into separate items through its own spec. The drafted-insertion sentence passed a trial, so it moves verbatim and never gets reworded.
- **executing-plans-finish-pointers** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: `executing-plans` Step 3 pointers into SDD's Finish section.
  - Trigger: any restructure of SDD's Finish section — a heading rename, a split, or the removal of the lesson-promotion or concept-index trigger text.
  - Action when tripped: check that `executing-plans` Step 3 items 6 and 8 still point at text that exists and says what they claim. `writing-plans` item 8 catches this only when a plan touches those files.
- **plugin-wide-bump-trigger** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: the `plugin/`-wide version-bump trigger.
  - Trigger: a review window where doc-only patch bumps under `plugin/docs` or `plugin/README` outnumber content bumps, or bump churn shows in the log.
  - Action when tripped: rescope the gate's trigger to `plugin/skills/`, `plugin/scripts/`, and the manifests. Edit both wording copies together, because they must stay identical.
- **g1-title-based-overlap** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G1)
  - Watching: claims that two checks overlap.
  - Trigger: a spec or review asserts that two checks overlap from their titles or first sentences alone.
  - Action when tripped: raise a Recommendation for a spec-time check — an overlap claim cites the record of what each check caught, per `docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md`.
- **g2-plan-less-shipping** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G2)
  - Watching: specs that ship through spec → trial → ship, with no plan.
  - Trigger: a spec ships that way again.
  - Action when tripped: hold its Finish until the G2 ownership design conversation happens.
- **g3-attribution-coverage** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G3)
  - Watching: attribution coverage of `Catch` entries.
  - Trigger: a review window where unattributed catches again dominate, which blocks Zero-yield.
  - Action when tripped: raise a Recommendation that targets each write site that produced the unattributed entries, so it writes field 4.
````

Run: `grep -c "^- \*\*[a-z0-9-]*\*\* (added 20" docs/superpowers/process-reviews/watchlist.md; grep -c "^  - Action when tripped: [^<]" docs/superpowers/process-reviews/watchlist.md`
Expected: `6`, `6`. Both patterns skip the format example, whose values start with `<`.

- [ ] **Step 3: Rewrite `process-review` step 2**

In `plugin/skills/process-review/SKILL.md`, replace step 2 in full:

```
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

with:

```
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet"). Split each entry on unescaped `|`
   only, and read `\|` as a literal pipe. Field 2 names the entry's
   type, per the type table in the file's header: `Catch`, `Miss`,
   `Gap`, `Friction`, or `Watch`. A `Catch` entry carries either four
   fields (date, Catch, label, finding) or five (date, Catch, label,
   check, finding). Read a four-field entry as carrying no
   attribution: it predates the attribution field, and nothing
   reconstructs which check found it. Read the literal value
   `none — found ad hoc` in a five-field entry the same way — a real
   record that no check produced that Catch, not a missing value.
   Route each type to one destination:
   - `Catch` — the Catch synthesis in step 6.
   - `Miss` — step 6's Misses section directly, without the
     recurrence threshold.
   - `Gap` — step 6's Gaps section, with its field-4 disposition.
     Read an empty field 4 as `(no mechanism proposed)`.
   - `Friction` — step 6's Friction section.
   - `Watch` — the watchlist in step 5.
```

- [ ] **Step 4: Insert the watchlist step and renumber**

Replace:

```
   entry, treat it as a Catch the running log missed, and include it.
5. Synthesize the collected Catches and outcomes entries into the
   review's sections:
```

with:

```
   entry, treat it as a Catch the running log missed, and include it.
5. Append the window's `Watch` entries to
   `docs/superpowers/process-reviews/watchlist.md`, in that file's
   entry format. Then, for every watchlist entry, evaluate its trigger
   against this window's evidence. A tripped entry becomes a
   Recommendation that names the entry's pre-decided action. A
   resolved or obsolete entry leaves the file, with a one-line removal
   note in the review. Every other entry stays. The review names how
   many entries it checked, so an unread watchlist shows up as a zero.
6. Synthesize the collected entries and outcomes entries into the
   review's sections:
```

Then renumber the three later steps. Replace `6. Write the review to` with `7. Write the review to`. Replace `7. Update \`docs/superpowers/process-reviews/tracker.md\`` with `8. Update \`docs/superpowers/process-reviews/tracker.md\``. Replace:

```
8. Commit the review file and the tracker update together.
```

with:

```
9. Commit the review file, the watchlist update, and the tracker
   update together.
```

- [ ] **Step 5: Admit the logged types in the synthesis sections**

Replace:

```
     outcomes-reported divergence that recurs across 2 or more of the
     reviewed specs joins this section too, the same recurrence
     threshold.
```

with:

```
     outcomes-reported divergence that recurs across 2 or more of the
     reviewed specs joins this section too, the same recurrence
     threshold. A logged `Miss` entry joins this section directly,
     without the recurrence threshold, and its Recommendation targets
     the check its field 4 names.
```

Replace:

```
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect.
```

with:

```
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect. A logged `Friction` entry joins this
     section too.
```

Replace:

```
     follow-up too vague to act on yet joins this section too, as a
     candidate needing more definition.
```

with:

```
     follow-up too vague to act on yet joins this section too, as a
     candidate needing more definition. A logged `Gap` entry joins this
     section too, with its disposition.
```

- [ ] **Step 6: Check the step numbering and the new text (spec criteria 2 and 10)**

```bash
grep -n -E "^[0-9]+\. " plugin/skills/process-review/SKILL.md
for p in "the watchlist in step 5" "many entries it checked" "A logged \`Miss\` entry joins" "A logged \`Friction\` entry joins" "A logged \`Gap\` entry joins" "Split each entry on unescaped"; do echo "$(grep -c -- "$p" plugin/skills/process-review/SKILL.md) $p"; done
grep -n -i -E "\bstep [0-9]" plugin/skills/process-review/SKILL.md
```

Expected: steps `1.` through `9.`, each once, in order, at lines 31, 34, 54, 72, 77, 85, 135, 139, 144. (Task 4 later shifts steps 4–9 down.) Each of the six phrases returns `1`. The last grep prints exactly 5 lines, all inside step 2's route list or the step-6 reference: `step 6` four times and `step 5` once. No other numbered step reference exists in the file.

- [ ] **Step 7: Cross-section check (Self-Review item 8)**

Run: `grep -n -E "Catch|Miss|Gap|Friction|Watch" plugin/skills/process-review/SKILL.md | head -40`

Read each hit. A hit that states `notes.md` holds only `Catch` entries contradicts the new step 2. Fix any such hit in this step. At plan time the frontmatter description, the Core principle, and the No Placeholders section name the review sections only, and none makes that claim.

- [ ] **Step 8: Add this task's bullet**

In `plugin/RELEASE-NOTES.md`, directly after the bullet that begins `- **Every version bump writes a RELEASE-NOTES entry.**`, insert:

```
- **`notes.md` admits five entry types, and `process-review` routes each one.** `Catch`, `Miss`, `Gap`, `Friction`, and `Watch` each reach their own review section. `Watch` entries move to a durable `watchlist.md`, and every review checks each watchlist trigger.
```

- [ ] **Step 9: Commit and run the docs check**

```bash
git add docs/superpowers/process-reviews/notes.md docs/superpowers/process-reviews/watchlist.md plugin/skills/process-review/SKILL.md plugin/RELEASE-NOTES.md
git commit -m "feat(process-review): add five notes.md entry types, typed routing, and a durable watchlist

Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.

---

### Task 4: The `**Spec:**` plan-header field (spec part F)

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md:128` (header template), `:268` (item 11)
- Modify: `plugin/skills/process-review/SKILL.md` (step 3 third rule; step 6 Specs Reviewed)
- Modify: `plugin/skills/subagent-driven-development/SKILL.md:509-511` (Final Review), `:560-562` (Finish)
- Modify: `plugin/skills/executing-plans/SKILL.md:40-41` (Step 2.5 item 1)
- Modify: `plugin/RELEASE-NOTES.md` (one bullet)

**Interfaces:**
- Consumes: Task 3's step 6 text (`- **Specs Reviewed** — ...`), edited by its text.
- Produces: the header line `**Spec:** <path or "none">`, which this plan's own header already carries (spec criterion 9).

- [ ] **Step 1: Add the field to the `writing-plans` header template and item 11**

In `plugin/skills/writing-plans/SKILL.md`, replace:

```
**Tech Stack:** [Key technologies/libraries]
```

with:

```
**Tech Stack:** [Key technologies/libraries]

**Spec:** [Path to the design spec this plan implements, or "none"]
```

Replace:

```
(Goal, Architecture, Tech Stack, Global Constraints)? A required
```

with:

```
(Goal, Architecture, Tech Stack, Spec, Global Constraints)? A required
```

Run: `grep -c "^\*\*Spec:\*\* \[Path" plugin/skills/writing-plans/SKILL.md; grep -c "Tech Stack, Spec, Global Constraints" plugin/skills/writing-plans/SKILL.md`
Expected: `1`, `1`.

- [ ] **Step 2: Add the third outcomes rule and the Specs Reviewed listing**

In `plugin/skills/process-review/SKILL.md`, replace:

```
   ambiguity — name the candidate filenames in the review's Gaps
   section and skip reading any of them, rather than guessing. Collect
```

with:

```
   ambiguity — name the candidate filenames in the review's Gaps
   section and skip reading any of them, rather than guessing. Then,
   however many files the two rules above matched, read the outcomes
   file of every plan whose `**Spec:**` header field names this spec.
   A spec that shipped through more than one plan has more than one
   outcomes file, and its later plans carry dates no spec shares. Collect
```

Replace:

```
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers.
```

with:

```
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers. Under
     each spec, name every outcomes file this review read for it, or
     `none`.
```

Run: `grep -c "header field names this spec" plugin/skills/process-review/SKILL.md; grep -c "outcomes file this review read" plugin/skills/process-review/SKILL.md`
Expected: `1`, `1`.

- [ ] **Step 3: Name the field in the three spec-trace definitions**

In `plugin/skills/subagent-driven-development/SKILL.md`, replace (Final Review):

```
Before dispatching the final reviewer, check whether this plan traces to
a design spec (named in the plan's Goal line or a task's commit trailer,
e.g. "Part of docs/superpowers/specs/..."). If it does, run `python
```

with:

```
Before dispatching the final reviewer, check whether this plan traces to
a design spec (named in the plan's `**Spec:**` field, its Goal line, or a
task's commit trailer, e.g. "Part of docs/superpowers/specs/..."). If it
does, run `python
```

Replace (Finish):

```
`finishing-a-development-branch` handles afterward — check whether this
plan traces to a design spec (named in the plan's Goal line or a task's
commit trailer, e.g. "Part of docs/superpowers/specs/..."). If it does,
```

with:

```
`finishing-a-development-branch` handles afterward — check whether this
plan traces to a design spec (named in the plan's `**Spec:**` field, its
Goal line, or a task's commit trailer, e.g. "Part of
docs/superpowers/specs/..."). If it does,
```

In `plugin/skills/executing-plans/SKILL.md`, replace:

```
1. **Documentation check:** If this plan traces to a design spec (named
   in the plan's Goal line or a task's commit trailer), run `python
```

with:

```
1. **Documentation check:** If this plan traces to a design spec (named
   in the plan's `**Spec:**` field, its Goal line, or a task's commit
   trailer), run `python
```

- [ ] **Step 4: Check the three definitions side by side (Self-Review item 6)**

```bash
python - <<'EOF'
import re
for f in ['plugin/skills/subagent-driven-development/SKILL.md', 'plugin/skills/executing-plans/SKILL.md']:
    flat = re.sub(r'\s+', ' ', open(f, encoding='utf-8').read())
    for m in re.finditer(r'traces to a design spec \(named in ([^)]*?)(?:, e\.|\))', flat):
        print(f.split('/')[2], '|', m.group(1))
EOF
```

Expected: exactly 3 lines, each ending `the plan's \`**Spec:**\` field, its Goal line, or a task's commit trailer`. Two lines name `subagent-driven-development`, and one names `executing-plans`.

- [ ] **Step 5: Run the two-plan fixture (spec criterion 8)**

```bash
F="$TMPDIR/specfix"; rm -rf "$F"; mkdir -p "$F/docs/superpowers/specs" "$F/docs/superpowers/plans" && cd "$F"
S=docs/superpowers/specs/2026-01-01-widget-design.md; echo "# Widget" > $S
for p in 2026-01-01-widget-surface 2026-01-03-widget-handlers; do
  printf '# Plan\n\n**Goal:** x\n\n**Spec:** `%s`\n\n## Global Constraints\n\n---\n' "$S" > docs/superpowers/plans/$p.md
  echo "- outcome" > docs/superpowers/plans/$p-outcomes.md
done
printf '# Other\n\n**Spec:** none\n\nSee 2026-01-01-widget-design.md for background.\n' > docs/superpowers/plans/2026-01-05-other.md
echo other > docs/superpowers/plans/2026-01-05-other-outcomes.md
echo "== date rule"; ls docs/superpowers/plans/2026-01-01-*-outcomes.md
echo "== spec-field rule"
for p in $(grep -l "^\*\*Spec:\*\* .*2026-01-01-widget-design\.md" docs/superpowers/plans/*.md | grep -v -- "-outcomes\.md$"); do
  o="${p%.md}-outcomes.md"; [ -f "$o" ] && echo "$o"
done
cd - > /dev/null; rm -rf "$F"
```

Expected: the date rule lists only `2026-01-01-widget-surface-outcomes.md`. The spec-field rule lists `2026-01-01-widget-surface-outcomes.md` and `2026-01-03-widget-handlers-outcomes.md`, and leaves out `2026-01-05-other-outcomes.md`, which cites the spec only as background.

- [ ] **Step 6: Check this plan's own header (spec criterion 9)**

Run: `grep -c "^\*\*Spec:\*\* \`docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md\`" docs/superpowers/plans/2026-10-15-watchlist-and-findings-batch.md`
Expected: `1`.

- [ ] **Step 7: Add this task's bullet**

In `plugin/RELEASE-NOTES.md`, directly after the bullet that begins `- **\`notes.md\` admits five entry types`, insert:

```
- **Plans name their spec in a `**Spec:**` header field.** `process-review` reads the outcomes file of every plan that names a spec, so a spec shipped through two plans keeps both plans in its review.
```

Run: `sed -n '/^## v6.7.0/,/^## v6.6.0/p' plugin/RELEASE-NOTES.md | grep -c "^- "`
Expected: `4`.

- [ ] **Step 8: Commit and run the docs check**

```bash
git add plugin/skills/writing-plans/SKILL.md plugin/skills/process-review/SKILL.md plugin/skills/subagent-driven-development/SKILL.md plugin/skills/executing-plans/SKILL.md plugin/RELEASE-NOTES.md
git commit -m "feat(writing-plans): add a **Spec:** plan-header field, and read every plan that names a spec in process-review

Part of docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md"
python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-10-15-watchlist-and-findings-batch-design.md <task-base-sha> HEAD
```

Expected: `ALREADY_UPDATED: plugin/RELEASE-NOTES.md`, exit 0.
