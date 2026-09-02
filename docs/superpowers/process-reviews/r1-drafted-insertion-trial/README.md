# R1 drafted-insertion A/B trial — 2026-09-02

Pre-registered criterion and decision rule: spec commits 2f68049 / 5060812
(docs/superpowers/specs/2026-09-02-process-review-batch-r1-r4-design.md),
committed before any arm ran.

Dispatch prompt (byte-identical, both arms):
"Read docs/specs/error-message-rules-design.md and write the implementation
plan for it using your writing-plans skill. Save the plan to docs/plans/."

Arms: full plugin copies differing in exactly one file
(skills/writing-plans/SKILL.md, item 10 tail — diff -rq output: 1 line).
Marketplace plugins disabled via trial-settings.json (enabledPlugins false).

Blinding: labels assigned by $RANDOM parity, mapping sealed to a file and
read only after the verdict. Mapping: arm1(control)=B, arm2(treatment)=A.

Judge prompt: verbatim quote required per pattern Rule 4; see judge-verdict.txt.
Verdict: A(=arm2) YES with a quoted scratch-file grep of drafted text;
B(=arm1) NO — its only greps ran against the pre-existing target, which the
criterion excludes. Both quotes checked against the criterion wording before
acting (Rule 4).

Decision-rule branch reached: arm1 no / arm2 yes -> SHIP the exact string.
