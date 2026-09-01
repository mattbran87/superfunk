Self-review complete. All seven checks ran; checks 6 and 7 required re-running every count and grepping each quote against source rather than trusting the spec's text.

## What passed

Every count and quote in the spec verifies against the real thing:

- 43 prior specs (44 files minus this one; the extra `Status:` line in the uniq output is a template block inside the bug-tracking spec), **zero** containing `## Alternatives Considered` ✓
- 19 plugin skills + 5 user skills = 24 ✓
- `adhd-research` on exactly 6 lines of `branching-research/SKILL.md` — 10, 12, 17, 39, 77, 90 — and the positioning/provenance split is correct member-by-member ✓
- Quotes exact: `SKILL.md:27` step 4 wording, `branching-research:90` "confirmed failure mode from `adhd-research` testing", `process-review:13` "real evidence over vibes", `calibrating-recommendations:48` `**What would lower it:**` ✓
- Install state: `enabledPlugins` has `superpowers@claude-plugins-official`; `plugins/config.json` is `{"repositories": {}}` ✓
- `6.2.0` in both JSON files ✓; `docs/architecture/` does not exist ✓; the keyword probe and the retirement probe both return zero ✓
- The `2026-08-30-checkpoint-priority-and-conditional-gate` spec did make a gate conditional by hand (`:50`) ✓

Scope is right for one plan. No placeholders.

Supporting the design: `adhd-research/SKILL.md:72` already reads "confirmed failure mode from testing" — the exact de-named provenance form Decision 2 proposes, working in a sibling file.

## Eight findings

**1. Overstated claim — a lens *can* defer** (line 39, check 6)
The spec says lenses "must propose an approach; none may return 'defer.'" `multi-lens-research/SKILL.md:53` says the opposite: "If a lens doesn't meaningfully apply to the problem, the agent should say so in its proposal." Step 1 also permits deferring the whole fan-out. Decision 6 survives on the narrow reading (the lens prompt does demand one approach, so no lens carries a *null option*) — the Context wording needs narrowing to that.

**2. `writing-controlled-documents` never appears in the adopt/exclude analysis** (check 2, rule membership)
`~/.claude/skills/` holds five skills. The spec adopts three and explicitly excludes `adhd-research` with a reason. The fifth is absent from both lists — yet `CLAUDE.md:17` mandates it for *all* specs in this project and hardcodes `C:\Users\marko\.claude\skills\writing-controlled-documents`. It has the identical portability defect this spec exists to fix, and `grep -rn writing-controlled-documents plugin/` returns nothing. Adopt it or state why not.

**3. Decision 5 does not reach the omission contract** (check 2, rule membership)
`calibrating-recommendations` protects its required fields by *enumerating* them in three places — `:14` ("the pre-mortem, the confidence breakdown, or the steelman"), `:16` (the disclosure-note example), `:78` (Common Mistakes). Decision 5 asserts "the skill's existing contract governs this field like the others," but the contract is a list, and `**What would flip the ranking:**` joins none of the three producers. Criterion 6 checks only the output line and the new table row. This is the exact shape the rule-membership check targets: a list gains a member silently — here it fails to.

**4. Line references go stale inside the spec's own edit sequence** (checks 2, 4)
Decision 3 replaces one line at `:27` with ten, shifting everything below by +9. So `:91-94` becomes ~`:100-103` and the `:139` bullet Decision 4 targets becomes ~`:148`. Criterion 4 ("`SKILL.md:27` matches the step 4 wording... exactly") then fails on its face — the new step 4 spans ten lines. Criteria 4 and 5 need anchoring to quoted text, not line numbers.

**5. Criterion 3 is not scriptable as written** (check 5)
It says "every backtick-quoted skill name... checked by script rather than by reading." The three files' backticked tokens are `adhd-research`, `calibrating-recommendations`, `dispatching-parallel-agents`, `general-purpose`, `multi-lens-research`, `Agent`, `<constraint>`, `subagent_type: general-purpose`, `What would lower it:`. `general-purpose` is kebab-case and pattern-identical to a skill name but is an agent type — Decision 2 says so in prose, which a script cannot read. The criterion needs an explicit extraction rule or allowlist.

**6. Decision 6's `branching-research` exemption names no mechanism** (check 5)
"Can reach the null option through its Inversion or Remove-assumption frames, so it takes no equivalent change." Both frames exist (`:36`, `:37`) — but frames are selected per-problem, so neither is guaranteed to run, and `:39` notes that Boundary-tagged frames (both of these) "often produce ideas that get trapped by the critic." The spec's own Context invokes Mechanisms, Not Goodwill against exactly this shape. Either flag it as a gap or give `branching-research` the equivalent change.

**7. "The branch has never fired once" claims more than the count shows** (line 18, check 6)
Zero specs carry the heading — that proves the *output* never appeared. It does not establish which branch fired; nothing in `docs/superpowers/` records which brainstorms dispatched a research skill. The defensible claim is the one the count supports.

**8. The LeCunSkills review is unverifiable from the repo** (check 7)
"Six of the nine duplicate existing coverage or state it more weakly" cites `github.com/AminBlg/LeCunSkills`; no local copy exists anywhere on this machine, and the spec names none of the six. A reader cannot check it. Name the six, or attribute it to the session that did the reading.

## One judgment call, not a defect

The spec frames itself as "the forty-fourth consecutive spec" to skip `Alternatives Considered` (lines 55-60). Correct under the current `:139` rule — but the spec records at least four choices between approaches (copy vs. move at 47-53; adopt vs. leave `adhd-research` at 77-80; lens vs. Synthesize at 174-177; and the Decision 6 exemption). Under the rule Decision 4 ships in the same commit, this spec would owe the short form. Applying its own new rule to itself is available and would demonstrate the change; keeping the skip preserves the rhetorical point. Your call.

Findings 1, 4, 5, 7, and 8 are mechanical text fixes. Findings 2, 3, and 6 change scope or add work — I'd rather not amend a committed spec on those without your ruling. Want me to apply the mechanical five now and hold the rest?
