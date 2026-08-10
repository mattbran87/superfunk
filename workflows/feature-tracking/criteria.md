# Success Criteria — Feature Tracking

**Date:** 2026-08-10
**Stage:** 2 — Success Criteria

## Falsifiable Criteria

1. **Intake correctness** — following the documented procedure creates a feature directory holding all four template files, sets `spec.md`'s Status to `Planned`, and adds exactly one new link under the correct Bundle heading in `roadmap.md`. It leaves every other existing feature's entry and files untouched, confirmed by diffing before and after.
2. **Index accuracy** — after a rebuild, a query against `.superfunk/tracking.db` for a given feature's status returns the exact value from that feature's `spec.md` Status line, for every feature in the test fixture, with zero mismatches. The rebuild itself finishes quickly enough that a human does not notice the wait, across a fixture spanning multiple modules and bundles.
3. **Git-nativeness preserved** — `.superfunk/tracking.db` never appears as a trackable file in `git status` after a rebuild. A `.gitignore` entry excludes it, confirmed by running the rebuild and checking status immediately after.

## Minimum Trial Coverage

At least 3 trials:

- one intake trial into an existing module and bundle
- one intake trial into a brand-new module, where the module and its first bundle don't exist yet
- one index trial: rebuild across a multi-module, multi-status fixture; check query accuracy for every feature; confirm the rebuild finishes quickly; confirm `.superfunk/tracking.db` stays out of `git status`
