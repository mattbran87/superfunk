# Seed --plugin-dir trial fixtures with the real docs they depend on

Before running any `--plugin-dir` trial that depends on a project convention doc, copy that doc into the scratch fixture as part of building it.

## Context

A `--plugin-dir` trial runs against a throwaway scratch repository with none of the real project's files present. When the trial's whole purpose is verifying that a skill correctly reads and applies a specific convention doc, an empty scratch repo gives the AI nothing real to read — it falls back to generic, plausible-looking conventions instead of the specific ones under test. The trial can still "pass" in the sense of producing sensible output, while testing nothing about the actual wiring.

## Pattern

When building a scratch fixture for a trial that exercises a skill instructed to read a specific doc (`docs/ai-code-guidelines.md`, `docs/code-standards.md`, or similar):
1. Copy the real doc — or the real repo's current version of it — into the fixture at the same relative path the skill expects.
2. Only then run the trial.
3. If the trial's own output reports a file it expected to read doesn't exist, treat that as a fixture-construction failure, not a skill failure — rebuild the fixture rather than reinterpreting the result.

## Counterpart rule — scrub what must not leak, including from git history

Seeding is only half the job. When a trial tests whether an agent finds
something *on its own*, the fixture must also exclude every document naming
the answer — and a fixture is a git repository, so its history counts as
part of it.

1. Before running, grep the whole fixture for the finding under test, not
   just the directory you expected it in. A design spec's Context section, a
   prior review file, an outcomes entry, or a lessons entry can each name it.
2. After removing a leaking file from the working tree, check whether an
   earlier fixture commit still contains it. `git show <sha>:<path>` remains
   readable to any agent that thinks to look, and an agent establishing a
   review window has a legitimate reason to look.
3. When history carries the leak, rebuild the fixture from scratch rather
   than deleting the file — a fresh `git init` is cheaper than rewriting
   history and leaves no path back to the answer.
4. Treat a run's own disclosure of contamination as a passing behavior worth
   keeping, not a nuisance. A trial that reports "I was handed this answer"
   protects the finding; one that stays quiet lets a leaked result read as
   independent discovery.

## Example

- A trial dispatched a scratch session to read `docs/ai-code-guidelines.md` and `docs/code-standards.md` and apply the Hazard Signal Words / commit-trailer conventions. The fixture only had a bare `README.md`. The session correctly reported it couldn't find either file, then produced generic hazard/commit conventions instead of the specific ANSI Z535 vocabulary under test — a result that looked plausible but verified nothing. Rebuilding the fixture with both docs copied in produced a trial that actually exercised the wiring.
- The same requirement had already been written down once, in an earlier sub-project's own Testing section, and still got missed on the next trial that needed it — confirming this needs an explicit checklist step, not just a one-time note.

- **Counterpart rule:** A trial testing whether `process-review`'s new Retirements section would independently surface subsumption candidates had its fixture built by copying the project's real specs directory — which included the design spec whose own Context names all three candidates. The run detected the contamination and disclosed it unprompted. The spec was deleted and the trial re-run; the leak survived anyway, because the fixture's git history still held the first run's committed review file, which the second run retrieved with `git show` while establishing its review window. It disclosed that too. Two scrub attempts, two surviving leak paths, both found by the trial rather than by its author.

## Originating lessons

- "A --plugin-dir trial fixture needs the real convention docs it's testing copied in, not just the scratch structure" (2026-08-21-hazard-signal-words)
- "Scrubbing a trial fixture means scrubbing its git history too, not only its working tree" (2026-09-01-convention-retirement)
