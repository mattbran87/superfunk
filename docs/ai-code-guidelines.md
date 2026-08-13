# AI Code Guidelines

Code conventions for AI-assisted development. Each principle includes the engineering rationale and the specific reason it matters for AI context and generation quality.

---

## File Organization

Each file has a single, clearly defined responsibility. Keep files focused and small enough to read in one pass. Co-locate related code — things that change together should live together.

**Engineering:** Separation of concerns makes code easier to navigate, test, and change in isolation. A file with a clear purpose is easier to review and harder to misuse.

**AI:** Claude reads files to build a mental model of what belongs where. A focused file gives it a clear, unambiguous signal about the patterns in use. Files that mix responsibilities create competing patterns — Claude generates code that conflates those responsibilities or places logic in the wrong location.

---

## Naming

Names should describe what a thing *is* or *does*, not how it does it. Use vocabulary from the problem domain. A name that accurately represents behavior is worth more than a comment explaining the mismatch.

**Engineering:** Self-documenting names reduce the cognitive load for new contributors and make code reviewable without running it.

**AI:** Claude reads names before reading bodies. A name that misrepresents behavior is a generation trap — Claude will generate call sites based on the name and not account for the actual behavior. `getUserById` that also updates a cache generates incorrect usage every time Claude writes a call to it. Accurate names are the primary signal for correct generation.

---

## Explicit Over Implicit

Make behavior visible in the code. Avoid magic, implicit state, side effects hidden behind innocent-looking calls, and overloaded semantics. If something non-obvious happens, it should be visible at the call site.

**Engineering:** Explicit code is predictable, testable, and easier to debug. Implicit behavior produces surprises for contributors who haven't memorized the codebase.

**AI:** Implicit behavior is invisible to Claude. It cannot inspect runtime state, follow hidden wiring, or infer side effects that aren't expressed in the code it reads. Code that looks one way but behaves another generates code that looks correct but misbehaves. Explicit code generates correct code.

---

## Flat Control Flow

Use early returns and guard clauses to keep the happy path at the lowest indentation level. Avoid deep nesting. A function that can be read top-to-bottom without tracking multiple levels of conditional context is preferable to one that requires backtracking.

**Engineering:** Flat control flow reduces cyclomatic complexity, is easier to read, and makes the primary path of execution immediately obvious.

**AI:** Deeply nested code makes it hard for Claude to track which conditions are in effect at any given point. When generating a continuation inside a nested block, Claude must reason about all enclosing conditions simultaneously — and can misattribute which context it's in. Flat flow lets Claude read a function linearly and generate correct continuations.

---

## Zero Dead Code Policy

Remove unused code immediately. This includes: unused functions, unused variables, commented-out blocks, dead branches, unreachable paths, and deprecated helpers that are no longer called. Do not leave code "just in case."

**Engineering:** Dead code creates maintenance confusion — future contributors cannot tell whether something is unused by design or by accident. It inflates file size and makes the actual behavior harder to follow.

**AI:** Claude cannot distinguish live code from dead code without executing it. Unused functions, commented-out blocks, and dead branches all appear as patterns worth following. Dead code generates more dead code — Claude treats the pattern as an established convention and produces more of it. A codebase with zero dead code gives Claude only patterns that are actually in use.

---

## Side Effect Isolation

A function either computes a value or performs an action — not both. Keep pure functions and effectful operations separate. Name effectful functions to make their nature clear.

**Engineering:** Pure functions are trivially testable and composable. Isolating side effects to clearly-bounded functions makes it possible to reason about what a call does without tracing through the whole call stack.

**AI:** A function that looks like a query but mutates state is a generation trap. Claude generates calls to it in query contexts, producing bugs that are invisible until runtime. When side effects are isolated to explicitly-named effectful functions, Claude generates correct call sites — it can see from the function's context and name that the call has consequences.

---

## Retrieval-Oriented Documentation

Write comments and documentation so they can be found and used by AI during generation — not just read by humans during review. Co-locate context with the code it describes. Explain *why*, not *what*.

**Engineering:** Comments that explain the reasoning behind a decision are more durable than comments that describe what the code does (which the code already shows). Co-location prevents doc/code drift — a comment next to the code it describes is updated when the code changes.

**AI:** Claude only sees what is in its context window. Documentation in a separate wiki, PR description, or README that isn't read during a session is invisible. A comment placed next to the code it describes is always in context when that code is read. Dense, specific, co-located documentation is retrieved automatically. Narrative documentation in external systems is not. Write as if the only reader is a model with a limited context window — because it often is.

---

## Why Comments

Mark non-obvious constraints with a `// why:` comment (or language equivalent: `# why:`, `-- why:`, etc.) placed inline at the point of the constraint. The `why:` prefix is the signal; the comment delimiter varies by language. Use it when the code looks like it should be written differently but can't be — the comment explains the constraint that prevents the obvious rewrite.

Common cases: compliance or regulatory limits, workarounds for historical bugs, external API quirks, specific timeout or retry values chosen for a non-obvious reason, disabled behavior that must stay disabled.

```python
# why: GDPR Art. 17 requires hard delete within 30 days — soft delete is not sufficient here
user.hard_delete()

# why: payment processor returns 422 for duplicate requests within 60s — not an error
if response.status == 422:
    return existing_transaction

# why: 3 retries matches the SLA window; 4+ causes duplicate charges on slow networks
MAX_RETRIES = 3
```

**Engineering:** A constraint without a comment looks like a mistake to any reviewer who doesn't know the history. The next contributor — or a future refactor — will change it. A `// why:` comment makes the constraint explicit and prevents the regression.

**AI:** Non-obvious constraints are exactly what Claude optimizes away. A magic number looks like a placeholder. An unusual conditional looks like a bug. A specific timeout looks arbitrary. Claude will "fix" these — and produce a correct-looking change that breaks a non-obvious invariant. A `// why:` comment makes the constraint visible in the context window. Claude reads it, understands that the pattern is intentional, and preserves it. Without the comment, the constraint is invisible.

---

## Signal Clarity

Use consistent patterns across the codebase. When similar problems are solved differently in different places, AI cannot know which pattern is intentional. One pattern per concern, applied consistently, is the highest-leverage code quality investment for AI-assisted development.

**Engineering:** Consistency reduces cognitive load for contributors and enables automated enforcement. A codebase where similar problems are solved similarly is easier to onboard into and easier to audit.

**AI:** Claude generates code that matches the pattern most prominent in its current context window. If the codebase has two competing patterns for the same problem — say, some functions throw on error while others return error objects — Claude follows whichever appeared most recently, not necessarily the intended one. Inconsistent patterns create *signal conflict*: the model has no reliable prior for which convention to follow, so generation becomes unpredictable. The more consistent the patterns in a codebase, the more consistently Claude generates code that belongs in it.

---

## Behavioral Test Naming

Test names are requirements, not implementation descriptions. A test name should state what the system does under specific conditions — readable as a specification by someone who has never seen the implementation.

**Engineering:** Test suites with behavioral names form living documentation. When a test fails, the name tells you which requirement was violated — not which function was called. A suite of behaviorally-named tests can be read as a specification, making gaps and redundancies visible without running the tests.

**AI:** Claude reads test names to understand what the system is supposed to do. An implementation-description name (`testRetryLogic`, `test_handle_response`) tells it nothing about the contract — it could pass or fail for any reason. A behavioral name (`retries up to three times before returning an error`, `returns 404 when the resource does not exist`) gives Claude a requirements-level specification it can reason against. When generating new tests, Claude mirrors the naming pattern it sees — behavioral names generate behavioral names; vague names generate vague names.

### Rule

Name tests as requirement statements: **given some condition, the system does something specific.**

| ✓ Behavioral | ✗ Implementation description |
|---|---|
| `returns 404 when user does not exist` | `testUserLookupQuery` |
| `rejects login when password is expired` | `test_handle_expired_password` |
| `retries up to three times before returning an error` | `testRetryLogic` |
| `sends a confirmation email after successful registration` | `testRegistrationFlow` |
| `returns an empty list when no results match the query` | `it('works')` |

The pattern applies across all test frameworks and languages — the format of the name varies, but the principle does not:

```js
// Jest
it('returns 404 when user does not exist', ...)
test('rejects login when password is expired', ...)
```

```python
# pytest
def test_returns_404_when_user_does_not_exist(): ...
def test_rejects_login_when_password_is_expired(): ...
```

```go
// Go testing
func TestReturns404WhenUserDoesNotExist(t *testing.T) { ... }
func TestRejectsLoginWhenPasswordIsExpired(t *testing.T) { ... }
```

---

## Per-Directory Context Files

Each significant directory contains a `.context.md` file describing the directory's purpose, key design decisions, and what to be careful about. Claude reads this file before working in the directory.

**Engineering:** Directory-level documentation captures the "why" behind a directory's structure — decisions that are invisible in individual files. This context is useful for new contributors, code reviewers, and anyone making changes that span multiple files in an area.

**AI:** Claude does not carry context about a directory's intent between sessions or tasks. Without a `.context.md`, it infers purpose from filenames and code patterns, which may be incomplete or wrong. A `.context.md` file gives Claude the constraints, conventions, and watch-outs that are specific to that area — before it generates code that might violate them. This is not hypothetical for superfunk: the `human-in-the-loop-review-checkpoint` work depended on one subtle, easy-to-violate constraint — never make `plugin/` the active session plugin, always test fork changes via disposable `--plugin-dir` sessions — that a `.context.md` in `plugin/` would have surfaced immediately to a fresh session, instead of relying on it being remembered from earlier in a long conversation.

### Significant Directory

A directory is significant if it has a discrete purpose that contains files Claude would touch during implementation. Exclude version-control and generated directories: `.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`.

Unlike Casita's own rule, a dot-prefixed directory is not automatically excluded — `.superfunk/` is a real example: a hand-authored, significant directory (holds `add_feature.py`, `rebuild_index.py`, `split_roadmap.py`) that happens to use a dot prefix by naming convention, not because it's generated or hidden tooling state.

A practical threshold: any directory with 3 or more non-generated files, or any top-level directory whose purpose is not evident from its name alone.

### Format

```markdown
# [Directory Name]

**Purpose:** One sentence — what this directory contains and why it exists.

## Key Design Decisions

- [Decision and why it was made]

## What to Be Careful About

- [Watch-out — constraint, invariant, or common mistake to avoid]
```

### Loading Model

`.context.md` files are loaded explicitly — Claude does not auto-load them. superfunk doesn't run numbered phase prompts the way Casita does, so this ties into the existing skill chain instead: `brainstorming`'s "explore project context" step reads the `.context.md` for any directory it examines; `writing-plans`' File Structure step reads it for every directory a task will touch, before writing that task; and when dispatching an implementer subagent, the coordinator reads the relevant `.context.md` first and folds its contents into the subagent's scene-setting context — subagents never read it themselves, since they get curated context, not raw file access to figure out on their own. When creating a new significant directory, create `.context.md` as the first file written into it.

### Keeping It Current

Create `.context.md` when a new significant directory is created — write it as the first file in that directory. Update it when changes alter the directory's purpose, add a new design constraint, or introduce a new watch-out. Stale `.context.md` files are worse than missing ones — outdated guidance actively misleads.

---

## Confidence-Calibrated Recommendations

When a real decision needs to weigh named alternatives — not casual conversation — use `multi-lens-research` or `branching-research`. Both invoke `calibrating-recommendations` as a required sub-skill: a pre-mortem on the recommendation, a confidence level grounded in named project-specific evidence (not reasoning depth or familiarity), and a steelmanned case for the strongest rejected alternative.

This discipline stays skill-scoped in superfunk, not a standing rule for every recommendation Claude makes. Applying pre-mortem/confidence/steelman ceremony to every casual suggestion in ordinary conversation would spend real bias-mitigation cost where it doesn't earn it — reach for the research skills when a decision actually needs that rigor, and let them carry this behavior automatically once invoked.

