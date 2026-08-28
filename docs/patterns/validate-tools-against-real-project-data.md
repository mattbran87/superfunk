# Validate a shipped tool against real project data, not just its own fixtures

A tool's fixture-based unit tests prove its branches execute correctly against the data its author imagined. They don't prove it works against the actual paths and text the tool will meet in production.

## Context

A fixture gets built to exercise a tool's logic: one case per branch, enough variation to hit each code path. Building a fixture for coverage naturally produces data shaped like whatever's easiest to set up — a doc file at the fixture's own root, ASCII-only sample text — rather than data shaped like the real target environment. Every unit test can pass while the tool still fails the moment it meets a real project's nested directory structure, non-ASCII prose, or platform-specific behavior (like a terminal's default text encoding) that the fixture never modeled.

## Pattern

Before treating a newly-shipped tool's passing test suite as proof it works, run it at least once against the real project it's meant to operate on — its actual file paths, its actual prose, on the actual platform it'll run on. This is a distinct check from the unit tests: it validates fit against the real environment, not correctness of the tool's own logic.

## Example

- `check_docs.py` shipped with 10 passing unit tests, including a real-git-fixture test. Its first invocation against this project's own real spec and branch returned the wrong result and then crashed. The fixture's doc file sat at fixture-root, so an exact-bare-filename match never got tested against a nested real path (`plugin/README.md`). The fixture's spec text used only ASCII, so printing it never exercised Windows' default stdout encoding against the em dashes and arrows this project's specs use throughout.

## Originating lessons

- "A tool's passing fixture-based unit tests don't prove it works against a real project's actual paths and text" (2026-08-28-superfunk-rebrand)
