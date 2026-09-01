Self-review complete. I checked all seven steps of brainstorming's Spec Self-Review against the real files rather than from memory. **14 findings**, listed below. I have not edited the committed spec — you asked for the report.

## Blocking

**1. The `notes.md` five-field change misses its real producers** (consistency / rule-membership)
Decision 1 says only "`notes.md`'s header gains this format line, replacing the current one." But the header is not what writes entries — `subagent-driven-development/SKILL.md` is, and it carries two four-field templates of its own:
- `SKILL.md:365` — `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <one-line finding>`
- `SKILL.md:535` — `- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`

A plan implementing this spec literally would update the header and leave both templates, so every future entry still lands with four fields and the attribution field never appears. `docs/superpowers/plans/2026-08-19-process-review.md:40,435` also restates the old format (historical artifact, no action). This is `docs/patterns/cross-check-shared-rule-restatements.md`.

**2. "Five output sections" is wrong, and it is a repeat of a previously-caught error**
`process-review/SKILL.md` Step 5 emits **six** sections: Specs Reviewed, Catches, Misses, Friction, Gaps, Recommendations. The Confidence paragraph says it "already emits five output sections, so a sixth section reuses a proven shape" — Retirements would be the seventh. `notes.md`'s second entry (2026-08-19) records this exact failure: a stale "five sections" count surviving a correction to six. Context's "All five of its output sections … add" is defensible (Specs Reviewed adds no rules), but the Confidence sentence is not.

**3. The "No Placeholders" enforcement does not reach the new section**
Decision 4 claims `process-review`'s No Placeholders rule "extends to cover" Retirements. The rule's actual text is Recommendation-scoped: *"Every Recommendation names a real target file and a real, specific change."* Nothing in it generalizes; the plan must widen it explicitly or the enforcement is asserted, not real.

**4. Two of the three enforcement mechanisms name no runner** (Mechanisms, Not Goodwill)
- `process-review/SKILL.md` has **no Self-Review section at all** (grep: 0 hits). Decision 4's "counts as a review defect" therefore names no step that would ever catch it.
- The `notes.md` field is "visible to `grep`" — but no gate runs that grep. SDD's existing gate greps `Task <N> (<plan-slug>)`, which counts entries and is blind to field count.

**5. A requirement lives only in Consequences**
Consequences states the Retirements section "reports the ratio of attributed to unattributed entries in its window" and "states its own attribution coverage on every run." Decision 2 does not require it, and Falsifiable Criterion 2 does not check it. As written, an implementer would not build it.

## Numeric claims that do not reproduce

**6. "All 24 skill files"** — actual: **22** `plugin/skills/*/SKILL.md`. The 24 carried over verbatim from `2026-09-01-research-skill-adoption-design.md:34`, where it meant 19 plugin + 5 user-level skills. Stripped of that context it contradicts the next paragraph's "Skill count grew from 14 to 22," and Alternative B's "a 23rd skill."

**7. "30,959 words on 2026-09-01"** — does not reproduce under any scope I tried: 30,609 (`plugin/skills/*/SKILL.md`), 31,864 (+ references), 50,157 (all `.md` under skill dirs). The measurement's scope is not recorded in the spec.

**8. The whole historical series is unverifiable in this repo** — 19,031 words on 2026-08-08, skill count 14, the `writing-plans` sequence 3→4→6→7→8→9→11→12→14, and "monotonically increasing on every day that recorded a change." This repo has **one commit** (`d74eac2`), and `C:/sf-bcv-plugins/arm1` is not a git repo. The measurements may be correct, but nothing here can re-derive them, and Context presents them as the spec's central evidence.

**9. "Task 1" 13 times** — 13 matches `| Task 1 (`, but two further entries carry the label `Task 1 code quality review (research-skill-adoption)` (`notes.md:95,96`). Actual: **15**.

**10. "Only 18 of its 88 entries name a specific numbered check"** — 11 entries name an `item N`; 27 name any numbered `item`/`check`/`step`/`rule`. Neither is 18.

## Quote and source freshness

**11. The LeCunSkills origin misstates its source.** The spec says "rejected eight of its nine skills. The ninth, `lecun-first-principles`, contributed its assumption-autopsy step." `2026-09-01-research-skill-adoption-design.md:29-34` says: *"Six of the nine duplicate existing coverage or state it more weakly. A seventh, `lecun-first-principles`, contributed the deferred item at the end of this document."* Two other mechanisms survived into that design. Also, **"assumption-autopsy" appears nowhere outside this spec** — the source attributes a deferred item to that skill, not a named step.

**12. Criterion 8's Rule 2 citation is incomplete.** Rule 2 of `ab-test-live-trials-for-behavior-change.md` (don't hand the agent the answer) does cover the un-seeded fixture. But Rule 3 governs the outcome Criterion 6 can actually produce — a trial returning zero retirements — and the spec says nothing about what a zero-finding run means. Criterion 7 treats a bad retirement as falsifying; nothing treats an empty run as inconclusive-and-re-run.

## Minor

**13. `Status: Draft`** is outside the required vocabulary. Brainstorming allows `Proposed`, `Approved`, or `Superseded by <filename>`, never free text.

**14. Criterion 5's "88 pre-existing entries" is a snapshot that will drift** before implementation — this session alone may add entries. Better phrased as "every entry existing when the plan starts."

## Clean

No TBD/TODO/placeholder text. Scope fits one plan. Verified correct: `writing-plans/SKILL.md:270-278` (item 14, exact line range); the item 11 quote *"same class of gap as a missing task for a spec requirement"* (`writing-plans/SKILL.md:253`, verbatim); `writing-plans` Self-Review holds 14 items; 88 `notes.md` entries; "Final review" 29; "Plan self-review" 7; tracker sits at 2 specs; `docs/principles.md` "Mechanisms, Not Goodwill"; `brainstorming` item 6 / `writing-plans` item 10 both numeric-verification; the prior spec's deferral of this work.

Findings 1–5, 6, 13 and 14 are mechanical fixes I can apply and amend into the commit. Findings 7–10 need you to either re-run the measurements or record where they came from; finding 11 needs the origin paragraph rewritten from the source's actual wording. Say the word and I'll apply what's fixable.
