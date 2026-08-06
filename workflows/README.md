# Workflow Validation Process

This directory holds the working files for the Workflow Validation Process, defined in `docs/superpowers/specs/2026-08-05-workflow-validation-process-design.md`. Read that spec first — this README only summarizes it.

## Starting a New Candidate Workflow

1. Create a directory: `workflows/<workflow-name>/`.
2. Copy each file from `workflows/_template/` into the new directory.
3. Work through the stages in order: Brainstorm, Diagram, Success Criteria, Test Plan, Trials + Trial Log, Verdict.
4. Check every approach in `brainstorm.md` against `workflows/anti-patterns.md`.
5. On a Ship verdict, promote `diagram.md` and `criteria.md` into the workflow's canonical spec.
6. On a Kill verdict, return to `brainstorm.md` and revise the approach.

## Example

See `workflows/_example/` for a filled-out dry run of this process against a trivial toy workflow.

## Files

| File | Stage |
|---|---|
| `brainstorm.md` | 0 |
| `diagram.md` | 1 |
| `criteria.md` | 2 |
| `test-plan.md` | 3 |
| `trial-log.md` | 4 |
