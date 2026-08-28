---
name: documentation
description: Use when a project needs an initial README/CHANGELOG scaffold, or when subagent-driven-development's Finish step needs to draft a user-facing doc update from a shipped spec. Maintains a project's README.md and CHANGELOG.md, translating a design spec's own Context/Decision/Consequences into the external-facing content a user needs, rather than starting from a blank page.
---

# Documentation

## Overview

Maintains `README.md` and `CHANGELOG.md` in the invoking project's own repository. Every project adopting superfunk gets this same mechanism, operating on its own repo — the same pattern `bug-tracking` and `writing-plans` already use.

Two entry points exist: bootstrapping initial docs for a project with none (Step 1) and drafting a doc update from a shipped, user-facing design spec (Step 2, invoked by `subagent-driven-development`'s Finish step — see that skill's Finish section, not this one, for the trigger logic).

## Step 1: Bootstrap

Invoked by a human or a session for a project with no `README.md` or `CHANGELOG.md` yet.

1. Create `README.md` with a minimal scaffold: a title, a one-paragraph description (ask the user, or infer from the project's existing files), and empty `## Installation` and `## Usage` headings for the user to fill in.
2. Create `CHANGELOG.md` with a minimal scaffold:

```markdown
# Changelog

<!-- entries below this line, newest first -->
```

3. Commit both files together: `git commit -m "docs: scaffold initial README and CHANGELOG"`.

## Step 2: Finish-time drafting

Triggered by `subagent-driven-development`'s Finish step — never run this step standalone; it needs a specific spec file and commit range as input, not a fresh scaffold.

1. Run `python plugin/skills/documentation/scripts/check_docs.py <spec_file> <base_sha> <head_sha>`.
2. If the output starts with `NOT_APPLICABLE` or `ALREADY_UPDATED`: nothing to do, skip the rest of this step.
3. If the output starts with `ACTION_NEEDED`: read the Context/Decision/Consequences content the script printed. Draft:
   - A `CHANGELOG.md` entry, newest-first, in plain language describing what changed and why a user would care — not the internal implementation detail, the user-facing effect.
   - A `README.md` update, only if the change affects something the README already documents (a new feature the Usage section should mention, a changed installation step). Skip the README if the change doesn't affect anything already documented there.
4. Commit both files together, in their own commit separate from Finish's other bookkeeping commits: `git commit -m "docs: update README/CHANGELOG for <short description>"`.

## When check_docs.py Reports ACTION_NEEDED But the Spec Stays Genuinely Unclear

If the spec's Context/Decision/Consequences don't give enough to draft honest user-facing content (e.g., a Consequences section that only discusses internal trade-offs), don't invent user-facing language that isn't grounded in the spec. Report DONE_WITH_CONCERNS instead of fabricating content.
