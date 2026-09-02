# Error-Message Copy Rules — Design

**Date:** 2026-09-02
**Status:** Approved

## Context

Support tickets quote error messages that name neither the failing
input nor the format the tool expected. The style guide in
`docs/code-standards.md` covers naming and file layout and says
nothing about error-message copy.

## Design

Append a new section titled `## Error-Message Copy` to the end of
`docs/code-standards.md`, containing exactly this text:

    Error messages must name the failing input and the expected
    format in the same sentence, so a user can correct the mistake
    without reading source code. Log lines above WARN must carry the
    request identifier. Never truncate an identifier in user-facing
    output.

## Falsifiable Criterion

`docs/code-standards.md` ends with the section above, word for word.
