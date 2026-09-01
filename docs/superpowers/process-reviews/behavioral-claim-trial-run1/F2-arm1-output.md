Self-review complete. I ran all seven checks against the actual repo files rather than from memory. **Ten findings**, plus what passed.

## Check 1 — Placeholder scan
Clean. No TBD/TODO, no empty sections, no vague requirements.

## Check 6 — Numeric-claim verification (4 findings)

**1. "All five of its output sections" — `process-review` emits six.** Context line 10 and the Confidence paragraph ("already emits five output sections, so a sixth section reuses a proven shape") are both wrong. `plugin/skills/process-review/SKILL.md:60-84` lists **Specs Reviewed, Catches, Misses, Friction, Gaps, Recommendations**, and `review-after-2026-08-30-equality-not-containment-note-design.md` has all six as `##` headings. Retirements would be the **seventh**. This repeats a defect already logged: `notes.md:13` records "*retained a stale 'five sections' count after the Decision section was corrected to six*."

**2. Word count is 30,609, not 30,959.** `cat plugin/skills/*/SKILL.md | wc -w` → `30609`. Off by 350. The "63% in 24 days" figure derives from it.

**3. "all 24 skill files" contradicts the spec's own "22".** There are 22 `SKILL.md` files repo-wide. The 24 came from the prior spec, where it meant 19 plugin + 5 user-level — a framing this spec dropped. Today the same basis would give 27.

**4. "Only 18 of its 88 entries name a specific numbered check" is not reproducible.** `grep -cEi '\bitem [0-9]'` → 11. A broad OR across `item N|check N|step N|self-review|gate` → 37. Nothing yields 18. The claim's *direction* holds (most Catches carry no check attribution), but the number doesn't survive checking.

**5. The historical series cannot be re-derived.** `git log --oneline | wc -l` → **1**. The 19,031-words-on-2026-08-08 baseline, the 14-skill starting count, and the `3, 4, 6, 7, 8, 9, 11, 12, 14` sequence have no verifiable source in this repo. The arithmetic is internally sound (9 values = 8 increases), but Context presents them as measurements.

## Check 7 — Quote and source-freshness (1 finding)

**6. "rejected eight of its nine skills" contradicts the spec it cites.** `2026-09-01-research-skill-adoption-design.md:29-34` says "*Six of the nine duplicate existing coverage or state it more weakly. A seventh, `lecun-first-principles`, contributed the deferred item... Two mechanisms survived into this design.*" So the review rejected six, not eight, and called `lecun-first-principles` "a seventh," not "the ninth." The two survivors were withdrawn later, after the A/B trial (that spec's line 223) — which makes the *outcome* roughly eight-of-nine, but the sentence attributes that to the review.

Verified clean here: the quoted phrase "same class of gap as a missing task for a spec requirement" is at `writing-plans/SKILL.md:253` ✓; `ab-test-live-trials-for-behavior-change.md` Rule 2 exists ✓; `principles.md:35` Mechanisms, Not Goodwill ✓; the label counts 29 / 13 / 7 and 88 entries all reproduce exactly ✓; tracker sits at 2 specs ✓; all three subsumption clusters check out against the real item text ✓.

## Check 2 — Internal consistency + rule membership (2 findings)

**7. The `notes.md` entry format has three producers; the spec updates one.** This is the rule-membership hazard — the format is a list of fields with more than one producer:

- `notes.md`'s header — the spec replaces this ✓
- `subagent-driven-development/SKILL.md:365` — `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>` (fix-loop template)
- `subagent-driven-development/SKILL.md:536` — `- <YYYY-MM-DD> | Catch | Final review | <one-line finding>` (final-review template)

SDD writes the large majority of Catch entries. Left unedited, the framework's own instructions keep emitting four fields, and Decision 4's enforcement ("a four-field entry written after this ships stands out") fires against the framework rather than against a careless writer. `docs/patterns/cross-check-shared-rule-restatements.md` covers exactly this shape.

**8. Consequences imposes a requirement Decision 2 never states.** The last paragraph: "*the Retirements section therefore reports the ratio of attributed to unattributed entries in its window*." Decision section 2 defines the entry format and the four reasons, and says nothing about a ratio. No Falsifiable Criterion covers it. A requirement living only in Consequences will not reach the implementation plan.

## Check 4 — Ambiguity (1 finding)

**9. Retire-vs-merge is undefined.** Decision 2 says "a human decides each removal" and "Removal stays advisory," but Context's first subsumption candidate describes a **merge**: items 5, 6, 8, and 9 "plausibly compress to two checks." Compressing four checks into two is not removal, and the entry field "the proposed action" never enumerates its allowed values. Pick one: either Retirements proposes deletion only (and the 5/6/8/9 cluster yields "delete 2, keep 2"), or it admits a merge action and says what a merged entry looks like.

## Check 5 — Enforcement (1 finding)

**10. The `notes.md` field's enforcement names no runner.** Decision 4's first bullet says a missing attribution stays "visible to `grep`" — but nothing runs that grep. Compare the other two bullets, which attach to real mechanisms (the existing No Placeholders rule; the review-defect class). SDD's Finish step already has a `notes.md` gate that runs `grep -c "Task <N> (<plan-slug>)"` (`SKILL.md:447`) — the natural place to hook a five-field check. As written, this decision relies on goodwill.

## Check 3 — Scope
Passes. Three coupled decisions in two files, eight criteria including a live trial with independent verification. One plan's worth.

---

The spec is committed, so I have not edited it. Findings 1, 2, 3, 6, and 7 are the ones I would fix before the user-review gate — 1 and 7 because they would propagate into the implementation, 7 because it decides whether the mechanism collects any data at all. Want me to apply the fixes and amend the commit?
