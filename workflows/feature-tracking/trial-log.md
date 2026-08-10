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

## Trial 2

**Date:** 2026-08-10
**Environment:** Synthetic test project
**Driver:** Autonomous agent run
**Outcome:** A second isolated `claude -p` session received the same procedure, but a fresh project with no existing modules. It correctly created the new auth module, the Login Security bundle, and all four feature files, with Status set to Planned. A fix to the roadmap template closed a gap the first attempt exposed (see Friction). Criterion 1 passes for this scenario after the fix.
**Friction:** The first attempt surfaced two real defects, both traced to the same root cause: without an existing entry to mimic, the agent had nothing to anchor its choices to. It left the template's own instructional comment sitting in the generated roadmap.md permanently, since nothing told it to remove that comment. It also invented an inconsistent link format. It pointed at spec.md directly instead of the feature directory, and it dropped the leading `./` that Trial 1's pre-existing example used. Updating the roadmap template to show an explicit link format, and to instruct comment removal, fixed both. A re-run against the corrected template produced a clean result, verified independently. This finding only surfaced because Trial 2 specifically exercised the no-existing-example branch — Trial 1's fixture already had a real entry to copy, which papered over the same ambiguity.

## Trial 3

**Date:** 2026-08-10
**Environment:** Synthetic test project (multi-module, multi-status fixture)
**Driver:** Hands-on
**Outcome:** The rebuild script processed a fixture of 5 features across 2 modules and 3 bundles, spanning 4 distinct status values, in 0.12 seconds. Every query result matched its feature's actual `spec.md` Status line exactly, with zero mismatches. A direct completion query ("is Process Refund Request complete") correctly returned `Done`. Criteria 2 and 3 both pass.
**Friction:** None. The `_template` directory's own `spec.md` never appeared in the index. The two-level glob pattern (`specs/<module>/<feature>/spec.md`) naturally excludes it, without needing the explicit module-name guard the script also carries as a defense. `git status` stayed empty after the rebuild, and `git status --ignored` confirmed `.gitignore` correctly excludes `.superfunk/tracking.db`.
