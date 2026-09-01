## Spec Self-Review — `2026-09-01-convention-retirement-design.md`

Ran all seven steps. Verification note: the loaded `brainstorming` skill (from `C:\sf-bcv-plugins\arm2\skills\brainstorming`) is ahead of the repo's `plugin/skills/brainstorming/SKILL.md` — its item 6 is **Claim verification** (covers behavioral claims, not just counts) where the repo's is **Numeric-claim verification**, and it cites `docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md`, which does not exist in `docs/patterns/`. I ran the broader version.

**12 findings.**

### Blocking

**1. The producer of `notes.md` entries never gets updated — the attribution field would never be written.**
`subagent-driven-development/SKILL.md` writes nearly every entry, and restates the four-field format twice inline:
- `SKILL.md:365` — `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`
- `SKILL.md:536` — `- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`

Decision 1 changes only `notes.md`'s own header ("replacing the current one"), and Falsifiable Criterion 1 verifies only that header. Decision 4's enforcement — "a four-field entry written after this ships stands out against the documented format" — assumes the writer reads `notes.md`'s header, but the writer follows SDD's inline template. Ship as written and every new entry stays four fields, which means zero attribution data, which means the Zero-yield reason never fires at all. This is `docs/patterns/cross-check-shared-rule-restatements.md`. (The Finish gate's `grep -c "Task <N> (<plan-slug>)"` at `SKILL.md:447` survives a fifth field; so does the worked example at `:708`, which is abstract.)

### Internal consistency / claim verification

**2. "All five of its output sections" is wrong — `process-review` emits six.** `process-review/SKILL.md` step 5 lists **Specs Reviewed**, Catches, Misses, Friction, Gaps, Recommendations. The error appears twice (Context, and Confidence's "a sixth section reuses a proven shape" — it would be a seventh). Both were inherited verbatim from `2026-09-01-research-skill-adoption-design.md`. `notes.md:2` logs a Catch for this exact stale "five sections" count in the original `process-review` spec — same error, recurring.

**3. "all 24 skill files" — actual count is 22.** `ls plugin/skills/*/SKILL.md | wc -l` → 22. The 24 came from the prior spec, where it meant *19 plugin + 5 user-level* skills; the qualifier got dropped in the carry-over. It also contradicts this spec's own "14 to 22" and "a 23rd skill". Consequence: the probe backing "no mechanism retires a rule" covered 19 plugin skills, and the three newest (`branching-research`, `multi-lens-research`, `calibrating-recommendations`) were never in it. **I re-ran the probe across all 22 current skills plus both docs — the claim holds** (only hit: `git worktree prune` in `finishing-a-development-branch`). The claim survives; its stated basis does not.

**4. `Status: Draft` is outside the allowed vocabulary.** Brainstorming permits `Proposed`, `Approved`, or `Superseded by <filename>`. Across 45 specs, `Draft` appears exactly once — this one; every other is `Shipped`. Should read `Proposed`.

**5. Word-count figures do not reproduce.** Claimed 30,959 on 2026-09-01. `cat plugin/skills/*/SKILL.md | wc -w` → **30,609**; PowerShell `Measure-Object -Word` → **31,104**. Neither matches. Separately, the 19,031 / 2026-08-08 baseline and "monotonically increasing on every day that recorded a change" cannot be checked here — `git rev-list --count HEAD` is **1** (squashed history). Either name the counter and re-run it, or cite the external source the daily series came from.

**6. "Only 18 of its 88 entries name a specific numbered check" does not reproduce.** 88 total ✓. But `item [0-9]` → 11; `item|step|criterion|rule` → 32; `item|criterion|rule|self-review` → 29. No definition yields 18. The three label tallies **do** verify exactly: Final review 29, Task 1 13, Plan self-review 7.

**7. Subsumption candidate 2 is overstated.** The quote from item 11 verifies verbatim, but its scope claim doesn't: item 11 checks *this plan's own document header* (Goal, Architecture, Tech Stack, Global Constraints); item 1 checks spec-requirement→task coverage; item 2 scans for No-Placeholders patterns. "The same class of gap as a missing task for a spec requirement" is a **severity analogy**, not a scope overlap. Context asserts "Three overlaps exist" as established fact, and Confidence leans on all three being "real work" — while Criterion 7 says an unsupported overlap falsifies the design. Candidates 1 and 3 look defensible; candidate 2 is the kind of invented overlap Criterion 7 exists to reject.

**8. "recorded five times" does not reproduce.** In the research-skill-adoption sub-project I count **4** logged entries of the claim-from-memory class (`notes.md:94–97`), or **6** if entry 97's three predicted-count errors are counted individually. Not 5 under either reading.

**9. LeCunSkills accounting contradicts the prior spec.** This spec: "rejected eight of its nine skills. The ninth, `lecun-first-principles`…". `2026-09-01-research-skill-adoption-design.md:29-33`: *six* of nine duplicate existing coverage, `lecun-first-principles` is *a seventh*, and *two mechanisms survived*. Also "assumption-autopsy step" is a term the prior spec never uses — it says only that the skill "contributed the deferred item."

### Enforcement (Mechanisms, Not Goodwill)

**10. The fixed reason set has no mechanism.** Decision 4 says `process-review`'s "No Placeholders" rule "extends to cover it," but that rule as written governs *Recommendations only* and bans vague content — it says nothing about a closed vocabulary. Nothing stops a fifth invented reason, which is precisely the failure Decision 2 argues the fixed set prevents. Compounding it: no Falsifiable Criterion checks that "No Placeholders" actually gets amended. Criterion 2 checks the Retirements section; the No Placeholders edit is unverified.

**11. A Decision-level requirement lives only in Consequences.** Two obligations appear nowhere else: "the Retirements section states its own attribution coverage on every run," and "reports the ratio of attributed to unattributed entries in its window." Both are behavior `process-review` must implement, both are the stated guard against the degenerate-default failure — and neither has a Decision entry or a Falsifiable Criterion. A requirement stated only in Consequences will not reach an implementation plan.

**12. Criterion 8 cites the wrong rule.** `ab-test-live-trials-for-behavior-change.md` Rule 2 is scoped to the *negative* case ("verifying a trigger correctly does NOT fire"); Criterion 8 describes a *positive* trial seeded with its own answer. Rule 2's clause 2 ("never state the expected answer") applies in spirit, but the pattern that actually governs Criterion 6's fixture is `seed-trial-fixtures-with-real-docs.md`, which the spec doesn't cite.

### Verified clean

No placeholders/TBD/TODO. Scope fits one plan. `User-Facing: No`, `Alternatives Considered`, and `Consequences` all present. `writing-plans/SKILL.md:270-278` is exact (item 14, Stale-workaround grep). Item 11's quoted phrase matches verbatim. Self-Review at 14 items ✓. Tracker's "Specs shipped since" holds 2 entries ✓. 88 entries ✓, three label tallies ✓. `docs/principles.md:35` Mechanisms, Not Goodwill ✓. `none — found ad hoc` consistent between Decision 1 and Criterion 1; "fourth field" is correctly numbered.

---

The skill's next step is to fix these inline. I haven't edited the committed spec — say the word and I'll apply the fixes, or tell me which ones you want to argue with first. Finding 1 is the one that decides whether the mechanism works at all; findings 7 and 10 are the ones that decide whether it does damage.
