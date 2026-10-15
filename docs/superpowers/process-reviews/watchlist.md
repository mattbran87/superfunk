# Watchlist

Durable store for `Watch` entries. A session logs a `Watch` entry to
`notes.md`. Each process review appends the window's `Watch` entries
here, then evaluates every entry's trigger (`process-review` step 5).

Entry format:

```markdown
- **<kebab-slug>** (added YYYY-MM-DD, <origin spec or discussion>)
  - Watching: <the thing under watch>
  - Trigger: <observable condition>
  - Action when tripped: <pre-decided action>
```

<!-- entries below this line -->
- **item-10-accretion** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: `writing-plans` Self-Review item 10's duties.
  - Trigger: any change gives item 10 a fourth duty. It carries three today: run the `Expected:` count commands, check budget arithmetic, and run the drafted-insertion grep.
  - Action when tripped: split item 10 into separate items through its own spec. The drafted-insertion sentence passed a trial, so it moves verbatim and never gets reworded.
- **executing-plans-finish-pointers** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: `executing-plans` Step 3 pointers into SDD's Finish section.
  - Trigger: any restructure of SDD's Finish section — a heading rename, a split, or the removal of the lesson-promotion or concept-index trigger text.
  - Action when tripped: check that `executing-plans` Step 3 items 6 and 8 still point at text that exists and says what they claim. `writing-plans` item 8 catches this only when a plan touches those files.
- **plugin-wide-bump-trigger** (added 2026-09-02, process-review-batch-r1-r4)
  - Watching: the `plugin/`-wide version-bump trigger.
  - Trigger: a review window where doc-only patch bumps under `plugin/docs` or `plugin/README` outnumber content bumps, or bump churn shows in the log.
  - Action when tripped: rescope the gate's trigger to `plugin/skills/`, `plugin/scripts/`, and the manifests. Edit both wording copies together, because they must stay identical.
- **g1-title-based-overlap** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G1)
  - Watching: claims that two checks overlap.
  - Trigger: a spec or review asserts that two checks overlap from their titles or first sentences alone.
  - Action when tripped: raise a Recommendation for a spec-time check — an overlap claim cites the record of what each check caught, per `docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md`.
- **g2-plan-less-shipping** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G2)
  - Watching: specs that ship through spec → trial → ship, with no plan.
  - Trigger: a spec ships that way again.
  - Action when tripped: hold its Finish until the G2 ownership design conversation happens.
- **g3-attribution-coverage** (added 2026-09-01, review-after-2026-09-01-behavioral-claim-verification-design.md G3)
  - Watching: attribution coverage of `Catch` entries.
  - Trigger: a review window where unattributed catches again dominate, which blocks Zero-yield.
  - Action when tripped: raise a Recommendation that targets each write site that produced the unattributed entries, so it writes field 4.
