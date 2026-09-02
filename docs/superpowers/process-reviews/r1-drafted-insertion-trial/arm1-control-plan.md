# Error-Message Copy Rules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Append an `## Error-Message Copy` section, word for word from the approved design spec, to the end of `docs/code-standards.md`.

**Architecture:** A single documentation edit. The spec (`docs/specs/error-message-rules-design.md`) mandates the exact section text, so the only decisions are placement (end of file, after the existing `## Edit Tool Guidelines` section) and the `---` separator that every other H2 section in the target file already uses. Verification is a byte-exact `diff` of the file's tail against the required text.

**Tech Stack:** Markdown, git, bash (Git Bash — available via the Bash tool on this Windows machine).

## Global Constraints

- The new section must contain exactly this text, per the spec's Design section (line breaks preserved as written there):

  ```
  Error messages must name the failing input and the expected
  format in the same sentence, so a user can correct the mistake
  without reading source code. Log lines above WARN must carry the
  request identifier. Never truncate an identifier in user-facing
  output.
  ```

- Falsifiable criterion from the spec: `docs/code-standards.md` ends with the section above, word for word. Nothing may be appended after it.
- `docs/code-standards.md` Markdown Conventions: H2 (`##`) for major sections; `---` horizontal rules separate major sections.
- `docs/code-standards.md` Git Conventions: conventional commits `type(scope): description`; types `feat|fix|docs|refactor|chore`; scope from `feature-tracking|skills|docs|plugin`; description lowercase, imperative, no trailing period.

---

## File Structure

- **Modify:** `docs/code-standards.md` — append one new H2 section (plus the conventional `---` separator) after the file's current last line (line 139, the `replace_all` preference bullet ending "…before they land in a commit."). No other file changes.

Directory-context check: no `.context.md` exists anywhere in this repository (checked `docs/` and the repo root during plan-writing), so there is no per-directory context to consult. `docs/lessons-learned.md` and `docs/patterns/` also do not exist in this repository.

New-file naming check: this plan file itself (`docs/plans/2026-09-02-error-message-copy-rules.md`) follows the kebab-case, date-prefixed convention from `docs/code-standards.md`'s File Naming section. The task creates no new files.

**Deliberate deviation, recorded here so a reviewer doesn't "fix" it:** existing sections in `docs/code-standards.md` format their content as `[Rule]`/`[Preference]` bullets. The new section is plain prose instead, because the spec's Design section says the section contains *exactly* the quoted text and the Falsifiable Criterion requires a word-for-word match. The spec wins over the file's bullet idiom. The leading `---` separator is added *before* the heading to match every sibling H2 section; it sits outside the section, so the file still "ends with the section" as the criterion requires.

## Pseudocode

- **T1 — API call sites:** Skipped: docs-only change; no external or internal API is called anywhere in this plan.
- **T2 — Handler/pattern reuse:** Skipped: no handler, controller, or code pattern is involved; the only reused shape is the `---`-separated H2 section layout, which File Structure already specifies exactly.
- **T3 — DTO/schema shape:** Skipped: no data shape is defined or consumed; the change is prose in a markdown file.
- **T4 — User-designated:** Skipped: the user requested no pseudocode for any part of this plan.

---

### Task 1: Append the Error-Message Copy section to code-standards.md

**Files:**
- Modify: `docs/code-standards.md` (append after line 139, the current last line)

**Interfaces:**
- Consumes: nothing — this is the only task and it depends on no prior work.
- Produces: nothing consumed by later tasks — this is the final task. Its external contract is the spec's falsifiable criterion: the file ends with the new section, word for word.

- [ ] **Step 1: Run the verification check to confirm it currently fails**

The check compares the last 7 lines of the file against the required section text, byte for byte. Run it from the repo root using the Bash tool:

```bash
diff <(tail -n 7 docs/code-standards.md) <(cat <<'EOF'
## Error-Message Copy

Error messages must name the failing input and the expected
format in the same sentence, so a user can correct the mistake
without reading source code. Log lines above WARN must carry the
request identifier. Never truncate an identifier in user-facing
output.
EOF
) && echo PASS || echo FAIL
```

Expected: `FAIL` (preceded by diff output showing the current tail — the `replace_all` bullet from Edit Tool Guidelines). Verified during plan-writing: the file currently contains zero occurrences of "Error-Message Copy" and zero occurrences of "Never truncate an identifier" (`grep -c` returned 0 for both).

- [ ] **Step 2: Append the section with the Edit tool**

Use the Edit tool on `docs/code-standards.md`. The `old_string` is the file's current last line, which occurs exactly once (verified during plan-writing). The file already ends with a trailing newline (verified with `od -c` during plan-writing), so an Edit that extends the last line's text produces well-formed markdown.

old_string (exact, one line):

```
- `[Preference]` When renaming a symbol across many files, prefer a targeted multi-file search (grep for every call site, then edit each) over `replace_all` — the extra step catches false positives before they land in a commit.
```

new_string (the same line, then a blank line, `---`, blank line, and the section — copy exactly, no trailing whitespace on any line):

```
- `[Preference]` When renaming a symbol across many files, prefer a targeted multi-file search (grep for every call site, then edit each) over `replace_all` — the extra step catches false positives before they land in a commit.

---

## Error-Message Copy

Error messages must name the failing input and the expected
format in the same sentence, so a user can correct the mistake
without reading source code. Log lines above WARN must carry the
request identifier. Never truncate an identifier in user-facing
output.
```

Do not add anything after `output.` — the spec's falsifiable criterion requires the file to *end* with this section.

- [ ] **Step 3: Re-run the verification check to confirm it passes**

Run the identical command from Step 1.

Expected: `PASS` with no diff output above it. If it prints `FAIL`, the appended text differs from the spec — compare the diff output character by character (watch for trailing spaces, a missing blank line after the heading, or re-wrapped lines) and fix with another targeted Edit; do not retype the whole section by hand.

- [ ] **Step 4: Confirm nothing else in the file changed**

```bash
git diff --stat docs/code-standards.md
```

Expected: `1 file changed, 10 insertions(+)` — exactly one file, 10 insertions, 0 deletions. (Verified during plan-writing by applying the append to the working copy, running this command, and restoring the original: git reported exactly `10 insertions(+)` and the Step 1/3 tail check printed `PASS`.) The 10 lines are: 1 blank + `---` + 1 blank + heading + 1 blank + 5 prose lines. Any deletion count above 0, or a second file in the stat, means something unintended changed — investigate before committing.

- [ ] **Step 5: Commit**

```bash
git add docs/code-standards.md
git commit -m "docs(docs): add error-message copy section to code standards"
```

Message follows the repo's conventional-commit rule: type `docs`, scope `docs`, lowercase imperative description, no trailing period. No severity trailer applies — this adds a documentation rule and is trivially reversible.

---

## Self-Review Notes

Run against the spec after drafting; findings and resolutions:

1. **Spec coverage:** The spec has one design action (append the section) and one falsifiable criterion (file ends with it word for word). Task 1 implements the action; Steps 1/3 verify the criterion. No gaps.
2. **Placeholder scan:** No TBDs; every step carries its exact command or exact edit content.
3. **Type consistency:** No code symbols defined; N/A.
4. **Pseudocode coverage:** All four triggers stated, each skipped with a concrete reason.
5. **Sibling-pattern parity:** The `---` separator matches every existing H2 section. The prose-instead-of-bullets deviation is deliberate and documented in File Structure.
6. **Rule-restatement accuracy:** The section text appears three times in this plan (Global Constraints, Step 1's heredoc, Step 2's new_string) and was copied verbatim from the spec each time, including its line breaks. Re-read side by side during self-review; identical.
7. **Lessons-learned check:** `docs/lessons-learned.md` does not exist in this repository; nothing to apply.
8. **Cross-section mechanism consistency:** No routing, trigger, or lifecycle language is edited; N/A.
9. **Worked-example currency:** No multi-step process is changed; the target file's only worked example (the commit-trailer sample) is untouched.
10. **Verified numeric expectations:** Step 1's "currently fails" expectation was verified by running both greps (0 matches each) during plan-writing; the trailing-newline assumption in Step 2 was verified with `od -c`. Step 4's `10 insertions(+)` was verified by a dry run: the append was applied to the working copy, `git diff --stat` was run and reported exactly that value, the Step 1/3 tail check printed `PASS`, and the file was then restored byte-identical to the committed version. No numeric budget exists in Global Constraints.
11. **Template compliance:** Header carries Goal, Architecture, Tech Stack, and Global Constraints.
12. **User-facing documentation timing:** The spec carries no `User-Facing: Yes` marker; N/A.
13. **Hostile-input pass:** The Edit in Step 2 depends on (a) the `old_string` being unique — verified, the line occurs once — and (b) the file ending in a newline — verified via `od -c`. The `diff` check uses a quoted heredoc (`<<'EOF'`), so no shell expansion can corrupt the expected text. Accepted limitation: if `docs/code-standards.md` is edited by someone else between plan-writing and execution such that the last line changes, Step 2's Edit fails loudly (no match) rather than corrupting the file — the executor should re-anchor on the then-current last line and re-verify with Step 1's command.
14. **Stale-workaround grep:** No limitation is being removed; no error message or docstring previously described a missing capability. N/A.
