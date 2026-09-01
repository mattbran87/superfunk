# BUG-0001: check_docs.py doesn't recognize nested README.md/CHANGELOG.md paths

**Severity:** Important
**Status:** Open
**Origin:** Reported 2026-08-28 by session (found during superfunk-rebrand's Task 6 verification)
**External ID:** (blank until synced to an external tracker)

## Description

`check_docs.py`'s `ALREADY_UPDATED` check does an exact bare-filename
match: `doc_files = [f for f in files if f in ("README.md", "CHANGELOG.md")]`.
This only matches a doc file sitting at the repository root. Any
project whose README/CHANGELOG lives in a subdirectory — including
this project's own plugin, at `plugin/README.md` — never matches,
so the tool reports `ACTION_NEEDED` even when the relevant doc file
genuinely already changed in the commit range.

## Reproduction

1. In this repo, on a branch that already modified `plugin/README.md`
   as part of a user-facing change.
2. Run `python plugin/skills/documentation/scripts/check_docs.py
   <a User-Facing: Yes spec file> <base_sha> <head_sha>`, where the
   commit range includes the `plugin/README.md` edit.
3. Observe: the tool prints `ACTION_NEEDED` and exits 1, instead of
   `ALREADY_UPDATED: plugin/README.md` and exiting 0.

Concretely reproduced 2026-08-28 running `check_docs.py` against
`docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md` over
a range that included the Task 5 `plugin/README.md` edit.

**Second occurrence, 2026-09-01.** Reproduced again running
`check_docs.py` against
`docs/superpowers/specs/2026-09-01-research-skill-adoption-design.md`
over a range that included a `plugin/README.md` edit. A fresh
implementer with no knowledge of this bug hit the same
`ACTION_NEEDED`, independently diagnosed the same root cause at line
47, and escalated rather than treating the result as a real gap. Two
occurrences in five days, both costing an implementer time to
re-derive a known defect.

## Resolution
(filled in when Status becomes Fixed or Won't Fix — what changed, commit SHA)
