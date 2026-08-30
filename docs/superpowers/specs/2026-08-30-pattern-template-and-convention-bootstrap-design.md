# Dangling Doc References and Convention Bootstrap — Design

**Date:** 2026-08-30
**Status:** Approved
**User-Facing:** No

## Context

The external bookmark-cli trial's findings report carries a correction, added 2026-08-30, to its original D2/D3 finding: `docs/patterns/pattern-template.md`, `docs/ai-code-guidelines.md`, and `docs/code-standards.md` all exist — at the superfunk development repo's own root, not inside `plugin/`. Since the plugin loads via `--plugin-dir <repo>/plugin`, only `plugin/` ships; these paths resolve when superfunk develops itself and dangle for every downstream project. The corrected report also retracts an earlier claim that the framework "invented a format" when promoting a pattern — the trial's three promoted patterns matched the real template exactly, from the model's own prior knowledge, not from anything the framework supplied. Revised severity: low, real, cheap to fix, no damage observed.

**The sharper half:** most references to these three paths carry no "skip if absent" guard, unlike other checks the framework already knows how to degrade (`brainstorming`: "No `docs/lessons-learned.md` yet: skip this check"; concept-index's Step 3: "If the index file doesn't exist yet... skip"). A direct grep of every reference in `plugin/` for these three filenames found:

- **Already self-contained, no fix needed:** `concept-index/SKILL.md:20` and `writing-plans/SKILL.md:30` both inline the actual rule content (the significant-directory threshold; the File Naming rules) rather than depending on the external file at the point of use. `subagent-driven-development/SKILL.md:225-231` and its sibling `.context.md` citations in `writing-plans`/`brainstorming` already guard the real action (reading `.context.md`) independently of whether `ai-code-guidelines.md` exists.
- **Genuinely unguarded — the fix targets these three sites:** `implementer-prompt.md:18` tells every implementer subagent to read both files unconditionally; `task-reviewer-prompt.md:127-136` tells every task reviewer the same; `brainstorming/SKILL.md:112` instructs checking a spec against `docs/code-standards.md`'s Spec File Conventions section with no fallback. In the trial, the unconditional implementer instruction alone reached roughly 20 subagents pointed at a file that never existed for that project.

`docs/patterns/pattern-template.md` needs a different fix than a guard: `subagent-driven-development/SKILL.md`'s Finish step doesn't just read this file, it writes a new file *from* it as a template — there's no "skip if absent" that makes sense for a promotion step that's supposed to produce a Pattern file. The report's own suggested fix applies here: inline the four section names directly into the instruction, so no external template file exists to dangle in the first place.

This leaves D8 (no session ever offers to create a `CLAUDE.md`) as the one finding in this cluster the report explicitly flags as needing a ruling rather than asserting as a bug — already resolved: this project's earlier ruling on this exact trial treated it as a real gap to fix. That decision stands independently of the D2/D3 mechanism above; the fix below (brainstorming offers to scaffold `CLAUDE.md` and `docs/ai-code-guidelines.md`) also has the side effect of giving a project real content for the guarded `ai-code-guidelines.md` reads above, once a project accepts the offer.

## Decision

**`subagent-driven-development/SKILL.md`'s Finish-step Lessons-learned paragraph stops referencing a separate template file.** Its pattern-promotion sentence changes from:

```markdown
On promotion, write `docs/patterns/<slug>.md`
from `docs/patterns/pattern-template.md`, and add `*Pattern promoted
— see docs/patterns/<slug>.md*` after the entry.
```

to:

```markdown
On promotion, write `docs/patterns/<slug>.md` with this structure: a
`# <Pattern Name>` title and one-line description, then `## Context`
(what situation makes this pattern apply), `## Pattern` (the rule
itself, as an imperative instruction), `## Example` (one or more
worked examples), and `## Originating lessons` (one bullet per
lesson: `- "<title>" (<spec-slug>)`). Add `*Pattern promoted — see
docs/patterns/<slug>.md*` after the entry.
```

This repo's own `docs/patterns/pattern-template.md` gets deleted — nothing references it anymore, in the plugin or in this repo's own Finish step, which now follows the same inlined instruction every downstream project does.

**`implementer-prompt.md`'s conventions-reading instruction gains a guard.** Changes from:

```markdown
Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md`
before you begin — together they hold this project's code
conventions (naming, control flow, dead code, side effects,
comments, tests), which apply as you write, and file/commit
conventions (file naming, git message format), which apply when
you commit.
```

to:

```markdown
Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md`
before you begin, if they exist — together they hold this project's
code conventions (naming, control flow, dead code, side effects,
comments, tests), which apply as you write, and file/commit
conventions (file naming, git message format), which apply when
you commit. Either file missing: skip reading it and follow the
category list above as general best practice instead.
```

**`task-reviewer-prompt.md`'s Project Conventions checklist gains the same shape of guard.** Changes from:

```markdown
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
```

to:

```markdown
**Project conventions:**
- Read `docs/ai-code-guidelines.md`, if it exists, and check whether
  the diff follows it — in particular: naming, explicit-over-implicit,
  flat control flow, dead code, side-effect isolation, why-comments,
  hazard signal words, signal clarity, behavioral test naming. File
  missing: skip this check — the categories above still apply as
  general best practice, but cite specific evidence only from a
  document you actually read.
- Read `docs/code-standards.md`, if it exists, and check whether the
  diff and its commit messages follow it — in particular: file
  naming, commit message format, and the severity-trailer rule for
  risky changes. File missing: skip this check, for the same reason.
- A violation is a Code Quality finding like any other, cited by
  file:line.
```

**`brainstorming/SKILL.md`'s spec-review bullet gains the same guard.** Changes from:

```markdown
- Check the written spec against `docs/code-standards.md`'s Spec File
  Conventions section before committing — self-contained (readable
  without external context beyond `CLAUDE.md`), testable acceptance
  criteria (observable and binary for Falsifiable Criteria, or quoted
  evidence from disposable scratch trials for a Testing section).
  That section's Status-line and template rules target
  feature-tracking's `spec.md`, not this design-spec system — the
  next bullet's `Status` vocabulary governs here instead.
```

to:

```markdown
- Check the written spec against `docs/code-standards.md`'s Spec File
  Conventions section before committing, if that file exists —
  self-contained (readable without external context beyond
  `CLAUDE.md`), testable acceptance criteria (observable and binary
  for Falsifiable Criteria, or quoted evidence from disposable scratch
  trials for a Testing section). That section's Status-line and
  template rules target feature-tracking's `spec.md`, not this
  design-spec system — the next bullet's `Status` vocabulary governs
  here instead. No `docs/code-standards.md` yet: apply the two named
  criteria directly, without the file.
```

**`brainstorming/SKILL.md`'s "Explore project context" step gains a new bullet**, inserted after the existing lessons-learned/patterns check and before the scope-assessment bullet — this fixes D8, unchanged from the earlier draft of this spec:

```markdown
- Check for a `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` at the project
  root, and for `docs/ai-code-guidelines.md`. If either is missing,
  offer once (ask-don't-force, never blocking): "This project has no
  [instructions file for AI agents / coding conventions doc] yet.
  Want me to scaffold a starter version from a few quick questions
  before we continue?" If accepted, ask up to three questions, one at
  a time: the project's language/stack (skip if already evident from
  existing files), any coding conventions already followed informally,
  and anything future sessions should know upfront (build/test
  commands, architecture notes). Draft whichever file(s) were missing
  from the answers, commit them, then continue. If declined, or both
  files already exist, proceed without further mention.
```

**The `CLAUDE.md` scaffold** drafts from the interview's third answer (and the language/stack answer, for Commands):

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project status

<one-line project description drawn from the interview>

## Commands

<build/test/lint commands from the interview, or, if none exist yet:
"No build/test tooling yet — update this section once one exists.">

## Architecture notes

<anything else the interview surfaced; omit this section entirely if
the interview surfaced nothing beyond Project status and Commands>
```

**The `docs/ai-code-guidelines.md` scaffold** covers exactly the nine categories `task-reviewer-prompt.md` already checks a diff against, each a single `**Rule:**` line — a lighter version of this repo's own file, which additionally carries a two-paragraph Engineering/AI rationale per section; that fuller shape stays this project's own enhancement, not a baseline requirement:

```markdown
# AI Code Guidelines

Code conventions for AI-assisted development in this project.

## Naming

**Rule:** <the interview's conventions answer, if it addresses naming;
otherwise: Names describe what a thing does, not how it does it.>

## Explicit Over Implicit

**Rule:** <interview answer if applicable, otherwise: Make behavior
visible in the code — avoid hidden state and side effects.>

## Flat Control Flow

**Rule:** <interview answer if applicable, otherwise: Use early
returns and guard clauses; avoid deep nesting.>

## Dead Code

**Rule:** Remove unused code immediately — no commented-out blocks, no unreachable paths.

## Side Effect Isolation

**Rule:** <interview answer if applicable, otherwise: A function
either computes a value or performs an action, not both.>

## Why Comments

**Rule:** Mark non-obvious constraints with a `// why:` comment at the point of the constraint.

## Hazard Signal Words

**Rule:** Mark hazards inline with DANGER, WARNING, CAUTION, or NOTICE by severity.

## Signal Clarity

**Rule:** <interview answer if applicable, otherwise: Use one
consistent pattern per concern across the codebase.>

## Behavioral Test Naming

**Rule:** Name tests as requirement statements (what the system does under specific conditions), not implementation descriptions.
```

Four sections (Dead Code, Why Comments, Hazard Signal Words, Behavioral Test Naming) always use the fixed default — these describe universal practices, not stack-specific conventions, so no interview answer could meaningfully change them. The other five draw from the interview's conventions answer where it addresses that category, and fall back to the stated default otherwise.

`docs/code-standards.md` stays out of the bootstrap offer's scope — the guard added above already makes every reference to it degrade gracefully, and no evidence from the trial suggests a project needs it scaffolded proactively the way `ai-code-guidelines.md` and `CLAUDE.md` do.

## Falsifiable Criteria

1. A direct read-through of `subagent-driven-development/SKILL.md`'s Finish section confirms the pattern-promotion sentence inlines the four section names and no longer references `docs/patterns/pattern-template.md`. `docs/patterns/pattern-template.md` no longer exists in this repo.
2. A direct read-through of `implementer-prompt.md`, `task-reviewer-prompt.md`, and `brainstorming/SKILL.md`'s spec-review bullet confirms each of the three guard additions exists, worded identically to the Decision block above.
3. A direct read-through of `brainstorming/SKILL.md`'s "Explore project context" step confirms the new convention-bootstrap bullet exists, worded identically to the Decision block above, positioned between the lessons-learned/patterns bullet and the scope-assessment bullet.
4. A disposable `--plugin-dir` trial creates a fresh git repo with no `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` and no `docs/ai-code-guidelines.md`, then starts a brainstorming session. The session offers to scaffold both files, and — when accepted and given real answers to the three questions — drafts both files with real content (not placeholder text) matching the templates above, then commits them before continuing to the actual brainstorming topic.
5. A second disposable trial repeats Criterion 4 but declines the offer. The session proceeds directly to clarifying questions with no files created and no further mention of the offer.
6. A third disposable trial runs a task through `subagent-driven-development` in a project with no `docs/ai-code-guidelines.md` or `docs/code-standards.md`. The implementer and task reviewer both proceed without error, and the task reviewer's report cites no finding attributed to either file.

## Consequences

A future pattern promotion produces a correctly-structured Pattern file in every project, including ones that never had a copy of the old template — closing the actual mechanism gap, more simply than shipping a file would have. A future implementer or task reviewer in a project without `ai-code-guidelines.md`/`code-standards.md` degrades the same way the framework's other missing-file checks already do, instead of receiving an unconditional instruction to read something that doesn't exist. A future project starting fresh gets one early opportunity to establish real `CLAUDE.md` and `ai-code-guidelines.md` content, closing D8 and reducing how often the new guards actually fire in practice.

## Deferred

- Scaffolding `docs/code-standards.md` as part of the same bootstrap offer — the guard alone covers it; revisit only if evidence emerges that a project needs it proactively.
- Extending the scaffold offer to also check for a test runner or CI configuration — `using-git-worktrees`'s existing Project Setup step already auto-detects and installs project tooling.
- A fuller Engineering/AI dual-rationale template for `docs/ai-code-guidelines.md` — deferred to manual growth.
- The remaining trial findings (D5, D7, D9/G1, D10/M1) — tracked separately for follow-up sub-projects.
