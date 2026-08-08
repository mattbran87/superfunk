# Trial Log — Superpowers Fork

**Stage:** 4 — Trials + Trial Log

Append-only. Add a new entry per trial; do not edit past entries.

## Trial 1

<!-- Add one "## Trial N" heading per trial, incrementing N. Never edit a previous entry's fields. -->

**Date:** 2026-08-08
**Environment:** Disposable clone of `superfunk`
**Driver:** Hands-on
**Outcome:** The first attempt failed with Windows "Filename too long" errors on several deeply-nested fork files. The disposable clone's scratchpad path, combined with the `superpowers/` prefix, exceeded Windows' 260-character path limit. A second attempt, at a short path with `core.longpaths` enabled, completed cleanly. A git-level diff confirmed zero loss or corruption of `docs/`, `workflows/`, and `CLAUDE.md` content. Criterion 1 passes, with `core.longpaths` as a new prerequisite this trial surfaced.
**Friction:** The scratchpad location Claude Code provides for temporary files sits about 200 characters deep already. Adding the fork's own nested paths pushed several files past Windows' path-length limit, forcing a retry at a shorter location. `core.longpaths` stayed off by default; the rehearsal needed manual configuration to turn it on. The real repo's shorter path likely avoids this specific failure. Future setup instructions should enable `core.longpaths` regardless, as cheap insurance. Separately: the `superpowers/` prefix, combined with the fork's own `docs/superpowers/...` layout, produces a redundant nested path — `superpowers/docs/superpowers/...`. This causes no failure. A future revision should reconsider the prefix name to avoid the redundancy.

## Trial 2

**Date:** 2026-08-08
**Environment:** Fresh disposable local test project
**Driver:** Autonomous agent run
**Outcome:** A separate `claude -p` process, launched with `--plugin-dir` pointed at a marked clone of the fork, correctly loaded the modified skill. The session's skill listing showed the planted marker attached to `superpowers:brainstorming`'s description, exactly as edited. Criterion 2 passes for this trial.
**Friction:** The isolated session also inherited every globally-configured plugin beyond the one under test — `--plugin-dir` adds a plugin; it does not create a clean room. A `superfunk` session pointed the same way at its own in-repo fork content would start running on it immediately, mixed in with everything else already active. This reinforces why Criterion 3 (isolation) matters. A future trial could test whether `--bare` combined with `--plugin-dir` produces a true clean-room session, if that ever matters for a specific validation.

## Trial 3

**Date:** 2026-08-08
**Environment:** Fresh disposable local test project
**Driver:** Autonomous agent run
**Outcome:** A second isolated `claude -p` session used `--plugin-dir`, pointed at a fork clone with a marker planted in the `session-start` hook script rather than a skill file. That session received the marker verbatim in its initial hook-injected context. The install mechanism generalizes to hook changes, not just skill-file edits. Criterion 2 passes again, on a different kind of change, per the Test Plan's intent.
**Friction:** The isolated session flagged the hook's own injected `<EXTREMELY_IMPORTANT>` block as a likely prompt injection before it followed any part of it. Out of conversation context, superpowers' emphatic, mandatory-sounding hook injection reads identically to an adversarial injection attempt. This observation falls outside this workflow's scope. It belongs to a future workflow about how a reworked framework enforces skill usage without looking indistinguishable from an attack.

## Trial 4

**Date:** 2026-08-08
**Environment:** Disposable clone of `superfunk` (post-import, with sample local edits already applied)
**Driver:** Hands-on
**Outcome:** A local commit and a simulated upstream commit both changed the same line in a subtree-imported file. `git subtree pull` correctly detected the conflict and stopped for manual resolution, instead of silently picking a side. A hands-on resolution completed the merge; the resulting commit history and content stayed coherent. Criterion 4 passes.
**Friction:** The simulated upstream commit lived in a local stand-in clone rather than the real GitHub fork. To force a genuine upstream conflict, a session would need to push a conflicting commit to the shared fork first. The stand-in reproduces the same subtree-pull mechanics `git` uses, regardless of remote location. The trial still validates the real behavior. A future trial could repeat this against the actual GitHub fork, once real upstream changes accumulate there. That would confirm no gap exists between a local remote and a hosted one.
