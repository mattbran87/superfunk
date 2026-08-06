# Brainstorm — Changelog Entry Workflow (example)

**Date:** 2026-08-05
**Stage:** 0 — Brainstorm

## Prior Art Reviewed

Casita required a full changelog entry at Acceptance, written by hand with no template. Spec-kit does not define a changelog step. This example explores a minimal, templated alternative.

## Approaches Considered

### Approach A

A single-line template: date, one-sentence summary, link to the commit.

### Approach B

A structured template with separate fields for change type, motivation, and impact.

## Anti-Pattern Check

- Phase gate ceremony: Approach B adds a review gate before the entry counts as complete. That gate does not earn its ceremony for a one-line record.
- Dedicated SME or agent: Neither approach needs one; a template fills this need.

## Recommendation

Approach A. It captures the minimum useful record and adds no gate.

## Rejected Approaches

Approach B: the extra fields and gate cost more effort than the entries deliver in value, for a change this small.
