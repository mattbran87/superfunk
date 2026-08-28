# BUG-0002: check_docs.py crashes with UnicodeEncodeError on Windows console

**Severity:** Critical
**Status:** Open
**Origin:** Reported 2026-08-28 by session (found during superfunk-rebrand's Task 6 verification)
**External ID:** (blank until synced to an external tracker)

## Description

`check_docs.py`'s `ACTION_NEEDED` branch prints the spec's extracted
Context/Decision/Consequences sections directly via `print()`. On
Windows, Python's default stdout encoding is `cp1252`, which cannot
encode common Markdown characters this project's specs use throughout
— em dashes (`—`), right arrows (`→`), curly quotes. The process
crashes with `UnicodeEncodeError` partway through printing, instead
of completing and exiting 1 as designed. Since virtually every spec
in this project uses em dashes, this makes the `ACTION_NEEDED` branch
unusable on Windows for any real (non-ASCII-only) spec — a higher
severity than BUG-0001 because it crashes instead of just misreporting.

## Reproduction

1. On Windows, with a spec file containing an em dash or `→` character
   in its Context, Decision, or Consequences section.
2. Run `python plugin/skills/documentation/scripts/check_docs.py
   <spec_file> <base_sha> <head_sha>` where the `ACTION_NEEDED` branch
   fires (User-Facing: Yes, no README/CHANGELOG in the diff).
3. Observe: `UnicodeEncodeError: 'charmap' codec can't encode
   character '→' in position ...` (or similar for `—`/curly
   quotes), raised from `codecs.charmap_encode`, instead of a clean
   `ACTION_NEEDED` printout and exit code 1.

Concretely reproduced 2026-08-28 running `check_docs.py` against
`docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md`, which
uses `→` and `—` throughout its Context section.

## Resolution
(filled in when Status becomes Fixed or Won't Fix — what changed, commit SHA)
