# Success Criteria — Project Definition Skill

**Date:** 2026-08-11
**Stage:** 2 — Success Criteria

## Falsifiable Criteria

1. **Tier respected** — the skill asks explicitly which tier before generating anything, then produces exactly that tier's output: lightweight produces 3 sections in one file (`docs/architecture/project-definition.md`); full produces all 12 sections as separate files (`docs/architecture/NN-section-name.md`). Either way, zero extra or missing sections.
2. **Codebase-derived content stays accurate** — for a codebase-answerable section (for example, Building Block View), the generated content matches the actual explored codebase structure, verified by comparing it against the real directory and file layout. The content does not fabricate modules or components that don't exist.
3. **Building Block View solves module-assignment** — the core goal this workflow exists for. Given a generated Building Block View for a test codebase, a separate, fresh session with no other context correctly determines, using only that document, which module a new hypothetical feature belongs to. The determination matches what someone with full codebase knowledge would decide.
4. **Update mode does not silently clobber hand-edited content** — re-running the skill after a user hand-edits a section either preserves that edit or explicitly flags the conflict. It never silently overwrites the edit.

## Minimum Trial Coverage

At least 4 trials:

- one lightweight-tier generation trial, against a synthetic codebase
- one full-tier generation trial, against a synthetic codebase
- one module-assignment trial, using a generated Building Block View to route a new feature (this is the core validation, criterion 3)
- one update-mode trial, with a hand-edited section already in place before the skill re-runs
