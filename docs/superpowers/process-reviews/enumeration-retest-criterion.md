# Rule-enumeration re-test — criterion, registered before the arms run

## Fixture

superfunk at `0dc8e45`, rebuilt as a single-commit repository. 17 Rule
sentences. Entry "Writing a check for unverified numeric claims doesn't exempt
the document writing it" does not yet exist. Entry "A newly-shipped
cross-section check doesn't apply itself to the fixes that ship it" and its
pattern `self-apply-cross-section-check-to-hand-fixes.md` both exist already.

## Arms

| Arm | The promotion step carries |
|---|---|
| 1 · Control | the wording that shipped before `5c2ea7c` |
| 2 · Enumeration | the wording `5c2ea7c` shipped |

## Scored criterion — process, not answer

Does the output show that it compared the new Rule sentence against the
existing entries **as a set** — by enumerating them, by stating how many it
compared, or by explicitly ruling out named non-matches — rather than naming a
single adjacent pattern from recall?

Score NO when the output names one neighbouring pattern or lesson without
evidence that it examined the others. Naming a neighbour alone does not count:
the shipped entry for this sub-project did exactly that, and named
`validate-tools-against-real-project-data.md` while
`self-apply-cross-section-check-to-hand-fixes.md` already covered the act more
closely.

## Recorded, not scored

Which existing entry or pattern each arm names as the closest match. The
shipped history named `validate-tools-against-real-project-data.md`. This
re-test measures whether the enumeration happens, and reports the answer each
arm reaches as an observation rather than as a pass condition.

## Decision rule

1. Arm 1 enumerates → the enumeration wording adds nothing here; record and
   keep `5c2ea7c` on its single existing fixture's evidence.
2. Arm 2 enumerates and arm 1 does not → `5c2ea7c` holds on a second fixture.
3. Neither enumerates → `5c2ea7c` fails to replicate; reopen it.
