# Process Review — Running Notes

Append-only log. Each entry marks one finding a review catches on its
first pass (spec-compliance, code-quality, or the final whole-branch
review), tagged `Catch`. `process-review` reads this log,
cross-references `git log`, and may surface `Miss`, `Friction`, or
`Gap` patterns across entries when it synthesizes a review file.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`

<!-- entries below this line -->
