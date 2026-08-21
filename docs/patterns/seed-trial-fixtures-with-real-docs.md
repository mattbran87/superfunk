# Seed --plugin-dir trial fixtures with the real docs they depend on

Before running any `--plugin-dir` trial that depends on a project convention doc, copy that doc into the scratch fixture as part of building it.

## Context

A `--plugin-dir` trial runs against a throwaway scratch repository with none of the real project's files present. When the trial's whole purpose is verifying that a skill correctly reads and applies a specific convention doc, an empty scratch repo gives the AI nothing real to read — it falls back to generic, plausible-looking conventions instead of the specific ones under test. The trial can still "pass" in the sense of producing sensible output, while testing nothing about the actual wiring.

## Pattern

When building a scratch fixture for a trial that exercises a skill instructed to read a specific doc (`docs/ai-code-guidelines.md`, `docs/code-standards.md`, or similar):
1. Copy the real doc — or the real repo's current version of it — into the fixture at the same relative path the skill expects.
2. Only then run the trial.
3. If the trial's own output reports a file it expected to read doesn't exist, treat that as a fixture-construction failure, not a skill failure — rebuild the fixture rather than reinterpreting the result.

## Example

- A trial dispatched a scratch session to read `docs/ai-code-guidelines.md` and `docs/code-standards.md` and apply the Hazard Signal Words / commit-trailer conventions. The fixture only had a bare `README.md`. The session correctly reported it couldn't find either file, then produced generic hazard/commit conventions instead of the specific ANSI Z535 vocabulary under test — a result that looked plausible but verified nothing. Rebuilding the fixture with both docs copied in produced a trial that actually exercised the wiring.
- The same requirement had already been written down once, in an earlier sub-project's own Testing section, and still got missed on the next trial that needed it — confirming this needs an explicit checklist step, not just a one-time note.

## Originating lessons

- "A --plugin-dir trial fixture needs the real convention docs it's testing copied in, not just the scratch structure" (2026-08-21-hazard-signal-words)
