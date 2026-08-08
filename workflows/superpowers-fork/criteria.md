# Success Criteria — Superpowers Fork

**Date:** 2026-08-08
**Stage:** 2 — Success Criteria

## Falsifiable Criteria

1. **Import safety** — `git subtree add` merges the fork into `superfunk` with zero loss or corruption of existing `docs/` and `workflows/` content. The team rehearses this once on a disposable clone before it runs on the real repo.
2. **Local install works** — a session in a disposable test project installs an in-progress `superfunk` build from a local path. That session then actually runs on the build's skills, not the global `superpowers` plugin. Confirmed in at least 2 of 2 install trials.
3. **Isolation holds** — across every trial in the test plan, no `superfunk` dev session ever loads its own in-repo fork content as its active plugin. The criteria tolerate zero occurrences.
4. **Upstream sync works** — `git subtree pull` completes cleanly, or a session resolves any conflicts without losing prior `superfunk`-side edits. Confirmed in at least 1 of 1 sync trial.

## Minimum Trial Coverage

The workflow needs at least 4 trials:

- one import rehearsal on a disposable clone
- two local-install checks, using different skill files, to rule out a fluke
- one upstream-sync check, performed after local edits already exist
