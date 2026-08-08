# Test Plan — Superpowers Fork

**Date:** 2026-08-08
**Stage:** 3 — Test Plan

## Trial Scenarios

| # | Environment | Driver | Variation |
|---|---|---|---|
| 1 | Disposable clone of `superfunk` | Hands-on | First-time import of real fork content; watch for root-level collisions |
| 2 | Fresh disposable local test project | Autonomous agent run | Install a build with one trivial, marked skill change; confirm the marker shows up in a running session |
| 3 | Fresh disposable local test project | Autonomous agent run | Install a build with a different kind of skill change (for example, a hook), to confirm the install mechanism generalizes |
| 4 | Disposable clone of `superfunk` (post-import, with sample local edits already applied) | Hands-on | Simulate an upstream change to a file also edited locally, forcing a conflict, to test resolution |
