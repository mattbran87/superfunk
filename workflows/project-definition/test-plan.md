# Test Plan — Project Definition Skill

**Date:** 2026-08-11
**Stage:** 3 — Test Plan

## Trial Scenarios

| # | Environment | Driver | Variation |
|---|---|---|---|
| 1 | Synthetic test project (small fake codebase, a few module-like directories) | Autonomous agent run | Lightweight tier: choose Goals + Building Block View + Constraints; verify the single-file output matches the actual codebase structure |
| 2 | Synthetic test project | Autonomous agent run | Full tier: verify all 12 section files get created, correctly named, with no extras or missing sections |
| 3 | Synthetic test project plus the Building Block View generated in Trial 1 or 2 | Autonomous agent run | A separate, fresh session, given only the Building Block View and no other context, decides which module a new hypothetical feature belongs to |
| 4 | Synthetic test project with `docs/architecture/` already generated, one section hand-edited | Hands-on | Re-run the skill; verify the hand-edited section survives, or the conflict gets flagged -- never silently overwritten |

Trial 1 also requires writing `plugin/skills/project-definition/SKILL.md` for the first time, in a disposable copy of the plugin -- reusing the dev/test isolation mechanism the `superpowers-fork` workflow already validated: never `superfunk`'s own in-repo `plugin/`, always `--plugin-dir` against a disposable test copy.
