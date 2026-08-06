# Diagram — Changelog Entry Workflow (example)

**Date:** 2026-08-05
**Stage:** 1 — Diagram

## Flow / State Diagram

```mermaid
flowchart TD
    A[Finish a task] --> B[Write one-line summary]
    B --> C[Append to CHANGELOG.md]
    C --> D[Commit]
```

## Notes

The diagram assumes CHANGELOG.md already exists. A missing file needs a setup step this example does not cover.
