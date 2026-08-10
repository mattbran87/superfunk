# Trial Log — Feature Tracking

**Stage:** 4 — Trials + Trial Log

Append-only. Add a new entry per trial; do not edit past entries.

## Trial 1

<!-- Add one "## Trial N" heading per trial, incrementing N. Never edit a previous entry's fields. -->

**Date:** 2026-08-10
**Environment:** Synthetic test project
**Driver:** Autonomous agent run
**Outcome:** An isolated `claude -p` session received only the documented procedure and the fixture, with no further explanation. It correctly identified the existing billing module and Refunds bundle. It scaffolded all four template files, set Status to Planned, and added exactly one new link under the correct heading in roadmap.md. Independent verification confirmed the sibling feature's spec.md and the template directory both stayed untouched. Criterion 1 passes for this scenario.
**Friction:** The first invocation failed silently on write-permission prompts, since `claude -p` has no way to answer an interactive approval. Adding `--dangerously-skip-permissions` on retry resolved this immediately, safe here since the session ran inside a disposable scratch directory, not the real repo. A production intake procedure run by an agent needs the same consideration. Whatever invokes it must grant write access up front, or it stalls exactly like this trial's first attempt did.
