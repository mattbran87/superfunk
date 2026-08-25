# Process Review — after 2026-08-21-hazard-signal-words-design.md

**Date:** 2026-08-21

## Specs Reviewed

- 2026-08-20-writing-plans-self-review-checks-design.md
- 2026-08-20-checklist-construction-design.md
- 2026-08-21-hazard-signal-words-design.md

## Catches

**2026-08-20-writing-plans-self-review-checks-design.md**
- None logged — shipped clean on its first review, no fix round.

**2026-08-20-checklist-construction-design.md**
- Task 1: wording redundancy — "not once per split sub-checklist" repeated "split" already established one clause earlier.
- Task 2: the per-section instruction said "phase," but two of six groups (Quality Checks, Deployment) don't say "Phase" in their own heading.
- Tasks 1, 2, 3: three separate code-quality findings misapplied a stated rule literally without checking source intent or existing shipped precedent first — all three overridden after independent verification.
- Final review: Falsifiable Criterion 2's literal grep pattern didn't account for tense variation, a false failure if re-run literally.
- Final review: the shipped "5-9 items" rule text itself read ambiguously as a floor, the same ambiguity that had already caused a reviewer override earlier in the same sub-project.

**2026-08-21-hazard-signal-words-design.md**
- Task 3: "before writing any code" inaccurately covered commit-time conventions too, a timing mismatch.
- Task 4: `scripts/review-package`'s `git log --oneline` truncates to subject lines, making the new severity-trailer check impossible to actually perform — a real infrastructure gap, not a wording issue.
- Task 5: the File Naming bullet conflated the Feature Directories rule with a general "dated artifacts" claim and dropped the short-and-descriptive preference entirely.
- Task 6: the acceptance-criteria parenthetical was terse enough to misread as one shared bar for two textually distinct validation tracks.
- Task 7: the first live-trial attempt was invalid — the scratch fixture never had the real convention docs copied in, so the AI fell back to generic conventions instead of testing the actual wiring.
- Task 6: a code-quality finding claiming the template rule "wasn't mentioned" was factually wrong — the shipped bullet named it explicitly; overridden after independent verification, not fixed.

## Misses

- **A code-quality review applying a stated rule too literally, without checking source intent or existing precedent first, and getting overridden rather than fixed.** This recurred across two of the three reviewed specs: checklist-construction (three instances in one review round) and hazard-signal-words (the Task 6 template-rule claim). Both this session's own "verify-against-precedent-before-flagging" Pattern and this recurrence confirm the same reviewer failure mode keeps happening even after the Pattern got recorded — the Pattern names the rule, but nothing yet prompts a reviewer to consult it before firing off a finding.

## Friction

- **hazard-signal-words**: 5 of its 6 editing tasks needed at least one fix round — a high fix-round density, consistent with the pattern the prior review already flagged.
- **checklist-construction**: 3 of its 4 editing tasks needed a fix round.
- Across both sub-projects, no seed-artifact or pure-creation task needed a fix round; every fix round touched a task that edited or extended existing content (a Find/Replace against a live file). This split held again this window, matching the prior review's own observation.

## Gaps

- **No plan-writing check verifies that a bullet summarizing a source rule stays accurate to that rule's real scope.** hazard-signal-words' Task 5 (File Naming) and Task 6 (Spec File Conventions) each summarized a `docs/code-standards.md` rule inaccurately in a single bullet — the same underlying gap `docs/patterns/cross-check-shared-rule-restatements.md` already names for multi-file restatements, just not yet extended to cover a single bullet drifting from its one cited source.
- **The "verify-against-precedent-before-flagging" Pattern has no operational check behind it.** It exists as a recorded Lesson and Pattern, but nothing in the actual review-loop instructions asks a reviewer to consult it before reporting a finding that claims drift from a cited rule.

## Recommendations

- [x] Add a check to `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`: before reporting a finding that claims a diff misrepresents or drifts from a cited source rule, re-read that rule's actual text directly and confirm the claim holds. This operationalizes `docs/patterns/verify-against-precedent-before-flagging.md` as a real pre-finding check, not only a recorded Lesson. (Shipped as the re-read + re-check instruction in `task-reviewer-prompt.md`, commits `41ccefb`/`7a07d10`. Only step 1 of the Pattern's two-step check got operationalized — see `docs/superpowers/specs/2026-08-24-review-recommendations-followup-design.md`'s Deferred section for why step 2 stays out.)
- [x] Extend `plugin/skills/writing-plans/SKILL.md`'s Self-Review item 6 (Cross-file rule restatement) to also cover a single bullet that summarizes one source rule, not only restatements across multiple files — Task 5 and Task 6 of hazard-signal-words each show the narrower single-bullet case item 6's current wording doesn't quite name. (Shipped as the retitled "Rule-restatement accuracy" item 6, commit `b24f018`.)
