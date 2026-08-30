# Re-verify quotes and document state against the source before citing

A source read once, earlier in a session, is a memory — not a live view. Before citing it again, especially inside quotation marks, check it fresh.

## Context

Building a second artifact (a design spec, a plan) from a document read earlier in the same session invites two related failures. First, the document itself may have changed — a living report another process can append corrections to, a file another agent edited, a tracker that moved on — so treating an earlier read as still-current risks building on a retracted finding. Second, even an unchanged document gets misquoted from memory: a paraphrase close enough to feel faithful, or a sentence invented from the general shape of a nearby passage, both read naturally once written down and are easy to mistake for something actually copied from the source.

## Pattern

Before citing a source document's *content* as fact, or *wording* inside quotation marks, re-read the source fresh rather than relying on an earlier pass — full-document reads for "has anything here changed," and a direct grep for the exact phrase whenever presenting something as a quotation. A quotation mark makes a stronger claim than a summary: it asserts the words themselves came from the source, not a close reasonable restatement of it. If a grep for the quoted phrase finds no match, the quote is wrong regardless of how plausible it reads.

## Example

- A design spec's Context section treated an external trial report's original finding as settled fact, missing a same-day correction embedded later in the same file that retracted it — caught only because an unrelated numeric claim needed checking against the same document, and reading enough context to fix that number surfaced the correction too.
- The very next spec presented two "direct quotes" from a different source file, both reconstructed from memory: one substituted near-synonyms for the real wording ("cap" for "rule," "stop" for "prevent"), the other didn't exist verbatim anywhere in the file. Grepping the source for the quoted phrases before finalizing found no match for either.

## Originating lessons

- "A source document can change after you've already read it once" (2026-08-30-pattern-template-and-convention-bootstrap)
- "A quoted 'direct quote' needs the same verification as a numeric claim" (2026-08-30-fix-wave-regression-amendment)
