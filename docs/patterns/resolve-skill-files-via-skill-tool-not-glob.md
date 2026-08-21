# Resolve a skill's own referenced files via the Skill tool, not a filesystem search

In a `--plugin-dir` trial, tell the agent to invoke the Skill tool first and resolve any file the skill references as a sibling of what it just loaded — never tell it to Glob or broadly search the filesystem for that file.

## Context

A `--plugin-dir` trial runs a fresh Claude Code session against a fork's plugin, so the trial can verify a skill-file edit actually takes effect. When the fork's plugin shares its name with an already-installed plugin (common when testing a fork of an existing plugin), a file that exists under both — like a skill's own reference template — has no principled path for a broad filesystem search to prefer one copy over the other. The agent can resolve to the wrong (globally-cached) copy, report the file it needed doesn't exist, and improvise instead of exercising the change under test.

This differs from `seed-trial-fixtures-with-real-docs.md`: that pattern covers *project* docs the fixture must copy in (files the skill instructs an implementer to read from the repo it's working in). This pattern covers a *skill's own* files (like a dispatch-template reference) — those are never copied into a fixture; they must resolve through the loaded plugin itself.

## Pattern

1. In the trial prompt, tell the agent to use the Skill tool to invoke the relevant skill by name first — this loads the fork's actual current content, not any other installed copy.
2. When the skill references a sibling file (a dispatch template, a reviewer prompt), tell the agent to resolve it "using whatever path resolution you would naturally use for a skill's own referenced files" — relative to the skill it just loaded.
3. Never instruct the agent to Glob or search broadly for a skill file by name. A broad search has no way to know which of two identically-named, differently-located plugins is the one under test.
4. If a trial reports a skill file "doesn't exist," treat that as a trial-design defect before concluding the wiring itself is broken — confirm with a minimal, direct diagnostic (ask the agent to use the Skill tool and quote back a phrase that only exists in the fork's edited version) that the fork's content loads correctly at all.

## Example

- A trial telling a simulated implementer to "follow the implementer-prompt.md instructions exactly" (implying it should locate the file itself) resolved to the globally-cached `superpowers` plugin's copy, not the fork's, and the resulting status report had no Outcome field at all — even though the fork's `implementer-prompt.md` had already been edited to require one. A direct diagnostic confirmed the fork's content loads correctly when the agent uses the Skill tool first: told to invoke `subagent-driven-development` and then "open that referenced sibling file using whatever path resolution you would naturally use," it opened the fork's exact copy and quoted the new field verbatim. Rewriting the trial prompt to lead with the Skill tool invocation fixed it on the next attempt.

## Originating lessons

- "A --plugin-dir trial that tells the agent to hunt for a skill's own file breaks under a plugin name collision" (2026-08-21-per-task-outcome-capture)
