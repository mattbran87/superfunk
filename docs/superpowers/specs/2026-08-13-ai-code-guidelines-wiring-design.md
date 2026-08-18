# AI Code Guidelines Wiring — Design

**Date:** 2026-08-13
**Status:** Shipped

## Context

`docs/ai-code-guidelines.md` (shipped in the prior sub-project) has no wired trigger point anywhere in the skill chain. Loaded ambiently at session start, it would compete for context against everything else and apply as framing rather than at a specific moment — the same failure `claude-spec-framework`'s own `code-standards.md` names directly: *"Placing an imperative rule in Conversation Guidelines makes it present but not enforced."* The document's own "Retrieval-Oriented Documentation" section states the same thing about any documentation Claude doesn't read at the right moment. This spec closes that gap: it wires explicit read/check instructions into the specific skill-chain points where each rule actually applies, instead of relying on ambient loading.

While mapping these points, `plugin/skills/subagent-driven-development/`'s real current content turned out to hold a considerably more advanced version (a progress ledger, workspace-management scripts, a combined spec-and-quality `task-reviewer-prompt.md`) than the globally-installed Superpowers plugin this session runs on. `git log` confirms this content never changed since the original `git subtree add` — it came in this way from upstream. This doesn't change the established dev/test split (this session always runs on the global plugin; fork changes get validated via disposable `--plugin-dir` sessions) — it only means this spec's edits target the fork's actual current file content, not the simpler two-separate-reviewer shape this session has operated with all along.

## Decision

- **`plugin/skills/subagent-driven-development/implementer-prompt.md`** — adds a standing instruction, baked into the template rather than left to the coordinator to remember: read `docs/ai-code-guidelines.md` before writing any code. Baked in because the alternative — coordinator-curated inclusion, the same approach `.context.md` uses below — has no natural per-task variation to curate; the whole document applies to every implementer, every time.
- **`plugin/skills/subagent-driven-development/task-reviewer-prompt.md`** — extends the existing "Part 2: Code Quality" section with an explicit check against `docs/ai-code-guidelines.md`, using the template's own established file:line evidence convention for any violation found. This is the single highest-leverage point: code-quality review is exactly where "does this follow the project's AI-code conventions" gets judged, and a fresh-context subagent dispatch costs nothing extra to extend.
- **`plugin/skills/subagent-driven-development/SKILL.md`, "① Dispatch the implementer"** — adds a bullet instructing the coordinator to read the `.context.md` for any directory the task touches and fold a summary into the dispatch's Context section, before dispatching. This is the one point `.context.md` needs coordinator curation rather than a baked-in instruction, since which directories apply varies per task — matching what `ai-code-guidelines.md`'s own Loading Model section already describes as the intended mechanism.
- **`plugin/skills/brainstorming/SKILL.md`, step 1 ("Explore project context")** — adds explicit `.context.md` reading for any directory the exploration touches, alongside the existing "check files, docs, recent commits" instruction.
- **`plugin/skills/writing-plans/SKILL.md`, "File Structure"** — adds explicit `.context.md` reading for each directory before mapping its role in the plan, at the point decomposition decisions get locked in.

No changes reach `re-review-prompt.md`: re-reviews verify fixes against a specific findings list, not a fresh code-quality pass — the original `task-reviewer-prompt.md` check already covered the code once, and repeating it doesn't fit that template's narrower scope.

## Testing

Same disposable `--plugin-dir` scratch approach validated for the human-in-the-loop-review-checkpoint work: a baseline trial confirming each new instruction actually surfaces in a live session, not the full adversarial pressure-test battery `writing-skills` reserves for discipline-under-pressure rules (these are structural additions — a required read, a required check — not rules an agent might rationalize skipping).

Because a `--plugin-dir` scratch session runs against a throwaway git repo with none of superfunk's own files present, a meaningful trial needs `docs/ai-code-guidelines.md` and at least one `.context.md` copied into the scratch fixture first, so the wired instructions have something real to read.

## Deferred

- `docs/principles.md` and `docs/code-standards.md` — sub-projects 2 and 3, not started.
- The continuous-improvement mechanism — sub-project 4, not started.
- The two sections cut from `ai-code-guidelines.md` ("Audit Step-Number References," "New Mechanisms Require an Action Step") remain candidates for `principles.md` or `code-standards.md`.
