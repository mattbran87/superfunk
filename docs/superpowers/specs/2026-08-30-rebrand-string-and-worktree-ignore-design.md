# Rebrand String and Worktree Ignore Fix — Design

**Date:** 2026-08-30
**Status:** Approved
**User-Facing:** No

## Context

The same external bookmark-cli trial (`docs/superpowers/process-reviews/external-trial-bookmark-cli-findings.md`) named two further findings, both mechanical and well-specified enough to fix directly.

**D1 — `hooks/session-start` still injects the pre-rebrand skill name.** Every session's bootstrap hook reads `plugin/skills/using-superpowers/SKILL.md` and wraps it in a hardcoded string reading `"You have superpowers... 'superpowers:using-superpowers' skill..."`. Under this fork the skill resolves as `superfunk:using-superpowers` — `superpowers:` names no namespace that exists in a fork-only session. The August 28 rebrand correctly updated every live skill-file cross-reference (confirmed by the trial's own repo-wide grep) but missed this hook, the one place the string lives outside `plugin/skills/`.

**D4 — the worktree lands inside the repo it isolates, with no ignore rule.** `using-git-worktrees/SKILL.md`'s Step 1b (the manual git-worktree fallback) already has a "Safety Verification" step: run `git check-ignore` against the chosen directory, and add a `.gitignore` rule if it isn't covered, before creating anything. Step 1a (the preferred native-tool path) has no equivalent check — it reads "Native tools handle directory placement, branch creation, and cleanup automatically... skip to Step 2," with nothing verifying where the native tool actually put the worktree. In the trial, the harness's native tool placed the worktree at `.claude/worktrees/<branch>`, nested inside the main checkout, and nothing ignored it: the worktree acquired its own `.venv/` (54 KB of vendored library paths visible from the repo root), and `master` sat one `git add -A` away from committing an entire second checkout and virtualenv. The gap only got fixed because the trial's own operator noticed `git status` showing `?? .claude/` and asked for it.

## Decision

**`plugin/hooks/session-start` has six total `superpowers` occurrences** (confirmed via `grep -c`), of which two need to change:

- Line 2, `# SessionStart hook for superpowers plugin`, becomes `# SessionStart hook for superfunk plugin` — a plugin-identity comment, the same class of fix the original rebrand made everywhere else.
- Line 27 (the Decision block below).

Four occurrences stay unchanged: lines 10, 11, and 26 reference the `using-superpowers` skill's own directory name and variable names derived from it, deliberately unrenamed per the original rebrand's scope boundary. Line 37, `# See: https://github.com/obra/superpowers/issues/571`, links to an upstream GitHub issue explaining why the script uses `printf` instead of a heredoc — an attribution/context link to upstream's own issue tracker, not this fork's own identity.

**`plugin/hooks/session-start` line 27's hardcoded string changes:**

```bash
session_context="<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n**Below is the full content of your 'superpowers:using-superpowers' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"
```

becomes:

```bash
session_context="<EXTREMELY_IMPORTANT>\nYou have superfunk.\n\n**Below is the full content of your 'superfunk:using-superpowers' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"
```

The skill's own directory and frontmatter `name: using-superpowers` stay unchanged, per the original rebrand's scope boundary — only the invocation-prefix portion of the quoted string (`superpowers:` → `superfunk:`) and the branding line change.

**`using-git-worktrees/SKILL.md`'s Step 1a gains a Safety Verification paragraph**, placed right after the existing "Native tools handle directory placement, branch creation, and cleanup automatically... Using `git worktree add` when you have a native tool creates phantom state your harness can't see or manage" text and before "Only proceed to Step 1b...":

```markdown
**Safety Verification (before Step 2):** Determine where the native
tool placed the worktree — its own report, or `git worktree list` run
from the main repo. If that path sits inside the main repository's
working tree (its path starts with `git rev-parse --show-toplevel`'s
output from the main repo), verify it's ignored:
`git check-ignore -q <path>`. If NOT ignored, add an ignore rule for it
to `.gitignore` and commit the change, from the main repo, before
proceeding to Step 2. If the native tool placed the worktree entirely
outside the main repository's working tree, skip this check — no
ignore rule applies. A native tool's directory choice needs the same
verification a manually-chosen one already gets in Step 1b below;
without it, a second full checkout (and anything the worktree installs,
like a `.venv/`) sits one `git add -A` away from landing in the
repository it exists to isolate.
```

## Falsifiable Criteria

1. A direct read-through of `plugin/hooks/session-start` confirms line 2 reads `# SessionStart hook for superfunk plugin`, line 27 reads `"You have superfunk."` and `'superfunk:using-superpowers'`, and the file's total `superpowers` occurrence count drops from 6 to 4 — the four remaining occurrences span lines 10, 11, and 26's skill-directory references and line 37's upstream issue link, all deliberately unchanged.
2. A direct read-through of `using-git-worktrees/SKILL.md`'s Step 1a confirms the new Safety Verification paragraph exists, worded identically to the Decision block above, positioned between the phantom-state warning and "Only proceed to Step 1b."
3. A disposable trial creates a fresh git repo, runs a session with a native worktree tool available (or simulates one via a harness that supports it), and confirms: the session-start hook's injected context reads "You have superfunk" and quotes `superfunk:using-superpowers`; and after worktree creation, the main repo's `git status` shows no untracked worktree directory (either because the tool placed it outside the repo, or because an ignore rule now covers it).

## Consequences

A session starting under this fork no longer opens with a self-contradictory bootstrap message naming a skill under a namespace that can't resolve. A future worktree created via a harness's native tool gets the same protection a manually-created one already had, closing the gap that let a real trial come one `git add -A` away from committing a second checkout and a virtualenv into its own repository.

## Deferred

- The remaining trial findings (D2, D3, D5, D7-D10, and the hostile-input-pass/stale-workaround-grep Recommendations) — tracked separately; D2/D3/D8 specifically need a design decision about which skill should own bootstrapping convention docs for a new project, held for a following sub-project.
