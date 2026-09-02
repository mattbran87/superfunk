# Error-Message Copy Rules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfunk:subagent-driven-development (recommended) or superfunk:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Append the approved `## Error-Message Copy` section to the end of `docs/code-standards.md`, word for word per the design spec.

**Architecture:** A single documentation edit: one new H2 section appended to the end of an existing standards document, preceded by the `---` horizontal rule that document's own Markdown Conventions require between major sections. No code, no scripts, no other files change.

**Tech Stack:** Markdown, git, and standard shell tools (`grep`, `tail`, `wc`) for verification. Commands below are POSIX-shell (Git Bash on this Windows machine).

## Global Constraints

- The appended section body must be **exactly** this text from `docs/specs/error-message-rules-design.md` — do not rewrap, restyle, or edit it:

  > Error messages must name the failing input and the expected
  > format in the same sentence, so a user can correct the mistake
  > without reading source code. Log lines above WARN must carry the
  > request identifier. Never truncate an identifier in user-facing
  > output.

- Falsifiable criterion (from the spec): `docs/code-standards.md` **ends** with the section above, word for word. Nothing may come after it.
- Do NOT restyle the body into the file's usual `[Rule]` bullet format. The spec says "exactly this text," and the spec is approved — spec wins over house bullet style. The `---` separator before the heading is still required by the file's own "Use `---` horizontal rules to separate major sections" rule, and it precedes the section, so the file still ends with the section itself.
- Commit message follows the file's own Git Conventions: `type(scope): description`, lowercase imperative, no trailing period. No severity trailer applies (reversible doc addition).

---

## File Structure

- Modify: `docs/code-standards.md` — the project's coding/documentation standards. Currently 138 lines (`wc -l`), ends with the `## Edit Tool Guidelines` section and a trailing newline. Gains one section (10 appended lines including the separator and blank lines), becoming 148 lines.
- No files are created and no other files change. This plan file itself (`docs/plans/2026-09-02-error-message-copy-rules.md`) follows the File Naming rules: kebab-case, date-prefixed.

**`.context.md` check:** Searched the whole repository for `.context.md` files (glob `**/.context.md`) — none exist, so there is no per-directory context to consult for `docs/`.

---

## Pseudocode

- **T1 — API call sites:** Skipped: documentation-only change; no external or internal API is called anywhere in this plan.
- **T2 — Handler/pattern reuse:** Skipped: no handler, controller, or code pattern is implemented; the only "pattern" is the target file's section layout, fully specified in Task 1's literal text.
- **T3 — DTO/schema shape:** Skipped: no data shape is defined or consumed.
- **T4 — User-designated:** Skipped: the user did not request pseudocode for any part of this plan.

---

### Task 1: Append the Error-Message Copy section to code-standards.md

**Files:**
- Modify: `docs/code-standards.md` (append after current last line 138, `- \`[Preference]\` When renaming a symbol across many files...`)
- Test: shell verification commands below (no test framework exists in this repo; markdown changes are verified with `grep`/`tail`)

**Interfaces:**
- Consumes: nothing from other tasks (this is the only task).
- Produces: nothing consumed downstream; the deliverable is the final state of `docs/code-standards.md` itself.

- [ ] **Step 1: Run the failing check — confirm the section is absent**

Run:

```bash
grep -c '## Error-Message Copy' docs/code-standards.md
```

Expected: output `0`, exit code 1 (verified against the current file). This is the "failing test." If it prints `1` or more instead, **stop** — the section already exists (a re-run or someone got there first); do not append a duplicate. Verify the existing section against Step 3's expected output and skip to Step 4 only if it already matches word for word.

- [ ] **Step 2: Append the section**

The file currently ends with a trailing newline, so the appended block starts with one blank line to separate it from the existing last line. Append **exactly** this block to the end of `docs/code-standards.md` (first line below is blank):

```markdown

---

## Error-Message Copy

Error messages must name the failing input and the expected
format in the same sentence, so a user can correct the mistake
without reading source code. Log lines above WARN must carry the
request identifier. Never truncate an identifier in user-facing
output.
```

Use your file-editing tool to append (e.g., Edit with the current final line `- \`[Preference]\` When renaming a symbol across many files — the extra step catches false positives before they land in a commit.` as the anchor, replaced by itself plus the block above), or from a POSIX shell:

```bash
cat >> docs/code-standards.md <<'EOF'

---

## Error-Message Copy

Error messages must name the failing input and the expected
format in the same sentence, so a user can correct the mistake
without reading source code. Log lines above WARN must carry the
request identifier. Never truncate an identifier in user-facing
output.
EOF
```

The heredoc delimiter is quoted (`'EOF'`) so nothing in the text is shell-expanded; the text itself contains no backticks or `$`, so no escaping issues arise either way.

- [ ] **Step 3: Verify the file now ends with the section, word for word**

Run:

```bash
grep -c '## Error-Message Copy' docs/code-standards.md
tail -n 7 docs/code-standards.md
wc -l docs/code-standards.md
```

Expected (all three verified by dry-running the append against a scratch copy of the current file):

1. `grep -c` prints exactly `1`.
2. `tail -n 7` prints exactly:

   ```
   ## Error-Message Copy

   Error messages must name the failing input and the expected
   format in the same sentence, so a user can correct the mistake
   without reading source code. Log lines above WARN must carry the
   request identifier. Never truncate an identifier in user-facing
   output.
   ```

3. `wc -l` prints `148`.

Compare the `tail` output against the block above character by character — "word for word" is the spec's falsifiable criterion. Any mismatch (rewrapped lines, smart quotes, trailing content after `output.`) means the edit is wrong: fix the file and re-run this step.

- [ ] **Step 4: Commit**

```bash
git add docs/code-standards.md
git commit -m "docs(docs): add error-message copy section to code-standards"
```

---

## Self-Review Notes

Run during plan-writing; recorded so the checks stay visible.

- **Spec coverage:** The spec's single requirement (append the exact section; file ends with it) maps to Task 1. The spec has no `User-Facing:` field, so no documentation-timing step applies.
- **Lessons learned:** `docs/lessons-learned.md` does not exist in this repository — nothing to apply.
- **Verified numeric expectations:** The `0`/exit-1 pre-check was run against the real current file; the `1`, the 7-line `tail` output, and the `148` line count were produced by actually appending the drafted block to a scratch copy of the current file and running the verification commands against it — not estimated.
- **Hostile-input pass:** The one input class the append itself can't handle — the section already existing (duplicate append) — is caught by Step 1's mandatory stop condition. The heredoc uses a quoted delimiter, so shell metacharacters in the text are inert.
- **Rule-restatement accuracy:** The section body appears three times in this plan (Global Constraints, Step 2, Step 3) and was copied verbatim from the spec's design block each time, matching its exact five-line wrapping.
