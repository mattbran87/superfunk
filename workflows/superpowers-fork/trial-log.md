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
