# Project Principles

superfunk's first principles — the *why* behind the framework's shape. Distinct from the process docs in `docs/superpowers/specs/` (the *what*, decision by decision) and `docs/ai-code-guidelines.md` (code-level conventions).

Each principle follows a fixed structure: a named claim, the mechanisms that implement it, and testable commitments. A principle without mechanisms stays aspirational; a principle without commitments stays decoration.

---

## Continuous Improvement

superfunk's own process stays under iteration, the same way the work it governs does. Rules, templates, and skills count as living artifacts — checked and revised as real evidence arrives, not fixed the day they ship.

**Mechanisms:** `workflows/anti-patterns.md`, a living, append-only checklist checked during every new workflow's brainstorm stage — it already grew from a real incident (the Casita v2-rewrite's shared-live/dev-files failure). The build → review → fix → re-review loop every task in this project runs through, catching real gaps before they ship (the human-in-the-loop review checkpoint and the roadmap split automation each went through multiple real fix rounds this way). Design docs that get revised when new evidence contradicts them — the feature-tracking spec changed multiple times as Casita-comparison findings resolved.

**Commitments:**
- A rule that stops earning its overhead gets removed, not grandfathered.
- A gap a review catches becomes a checklist entry or a design fix, not a one-off patch nobody generalizes from.
- A spec gets revised when real evidence contradicts it, not defended past the point the evidence holds up.

---

## Focused Scope

Work gets planned at three nested scales — task, feature, module — each with one reason to exist. When cohesion looks ambiguous, the fix is splitting into a new feature or module, not absorbing the extra thing into what's already there.

**Mechanisms:** `brainstorming`'s scope-decomposition check (flags a request spanning multiple independent subsystems before design work starts on any of them). Feature-tracking's Module/Bundle structure, which gives every feature exactly one home. `writing-plans`' Task Right-Sizing rule: a task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate — fold setup into the task it serves, split only where a reviewer could reject one task while approving its neighbor.

**Commitments:**
- A feature that grows a second deliverable mid-implementation gets split, not absorbed.
- A module whose bundles share no real theme gets reorganized, not left as-is.
- A bundle that looks like a grab-bag of unrelated small items needs a real reflection process to justify keeping it together — superfunk doesn't have that mechanism yet (it's continuous-improvement territory, not yet built). Until it exists, a grab-bag bundle gets split by default, not excused by convenience.

---

## Mechanisms, Not Goodwill

Every convention in this project gets backed by something that checks it — a review, a script, a derived value — not just stated and hoped-for. A convention with no check might hold on the first feature and drift by the fifth.

**Mechanisms:** the subagent review loop (spec-compliance, then code-quality, now checking diffs against `docs/ai-code-guidelines.md` too) after every implementation task. `rebuild_index.py`'s derived `blocked`/`blocked_reason` columns — never manually typed, always computed fresh from real dependency data. The `.superfunk/*.py` scripts enforcing roadmap structure through regex-parsed markers, instead of trusting a human to remember the format by hand.

**Commitments:**
- A new convention ships with a way to check it, not as a follow-up someone might get to.
- A check that stops catching real issues gets removed, not left running as ceremony.

---

## Artifacts Over Memory

Session context ends — it compacts, and conversations close. Durable files are this project's record of what happened and why. A decision, observation, or commitment that matters lives in a file, not only in a conversation.

**Mechanisms:** `spec.md`, `decisions.md`, `notes.md`, and `tasks.md` per feature (kept unchanged from Casita's format). `docs/superpowers/specs/` for every design decision, with its rationale. `docs/superpowers/plans/` for every implementation plan. `subagent-driven-development`'s progress ledger, built specifically to survive context compaction — a controller that loses its place trusts the ledger and `git log` over its own recollection.

**Commitments:**
- A decision not written into a `decisions.md` entry or a design spec counts as an opinion, not a decision.
- Work that depends on session memory to stay correct is work that breaks the next time context compacts.

---

## User Authority at Decision Points

Claude executes the work and proposes the options. The user holds the real decision points — not checkpoints Claude crosses on its own judgment.

**Mechanisms:** `brainstorming`'s hard gate — no implementation, scaffolding, or code before a design gets presented and approved, regardless of how simple the work looks. The spec-review gate — a written spec gets shown before `writing-plans` runs, and changes get made before proceeding. `finishing-a-development-branch`'s menu — exactly the stated options, presented and waited on, never skipped because an answer looks obvious. The human-in-the-loop review checkpoint — asks before the menu, every time, on every path.

**Commitments:**
- A design never gets implemented without explicit approval, however small it looks.
- `finishing-a-development-branch`'s menu presents exactly its stated options and waits for an answer — it doesn't get bypassed for convenience.
- Automation that erodes one of these decision points gets rejected, however efficient it looks.
