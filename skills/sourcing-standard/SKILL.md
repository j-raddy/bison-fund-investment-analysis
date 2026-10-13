---
name: sourcing-standard
description: "Use when checking or establishing that every figure in the pitch carries a source and an as-of date, or when running the sign-off list."
version: 2.0.0
author: Jacob Radke
license: MIT
---

# Sourcing Standard

The evidence standard for the whole package, in one place. Every other skill points here instead of
restating it. This is the skill the analyst runs at Phase 3 when tagging figures, and at Phase 6 as
the sign-off pass.

## Triggers

- The hub routes Phase 3 gap-fill or Phase 6 verification here.
- A request to check the numbers, confirm a figure, or run the sign-off list.
- Any moment a figure is about to enter the pitch without a source and a date.

## The tag

Every figure, everywhere, uses this shape in the working fact sheet:

```
<value>, source: <document or site and link>, as-of: <date>, [fact | estimate | opinion]
```

A line that cannot carry a source is tagged `[UNVERIFIED]`. Unverified items may exist in working
notes and **may never appear in the final pitch.**

## Rules

1. **Never invent a number.** No plausible-looking figures, no filling a gap to keep moving. If it
   cannot be sourced, it is a question for the analyst or an unverified item.
2. **Every figure carries a source and an as-of date.** A figure without a date is worthless in a
   pitch, because market data drifts.
3. **Label every claim** fact, estimate, or opinion. Revenue projections, market sizing, and growth
   callouts are estimates and are labeled as such.
4. **Primary over secondary.** Cite the filing, the transcript, or the company's own investor
   material. A blog summarizing a filing is not the source; the filing is.
5. **Source quality.** Filings, company investor relations, and established financial data providers
   are acceptable. Aggregator blogs, recap newsletters, and aggregator stock pages are not. If the
   only available source is one of those, mark the figure pending and keep it off the slide.
6. **Provenance stays in the working files.** The tag shape, the words "derived" and "estimate", and
   the unverified marker live in the fact sheet, not on slides. Slide copy rules are in `deck-build`.

## The sign-off pass

Run `references/citation-rules.md` at Phase 6: reopen every source, confirm every number against the
original, confirm no unverified item leaked into the deck, and confirm every judgment call, the price
target, the pillars, and the recommendation, is the analyst's own. The analyst signs off. The
assistant never signs off for them.

## Output

A fact sheet where every line resolves to a source and a date, a list of anything still unverified,
and the analyst's signed-off confirmation. Unverified items are reported as open questions, never
quietly dropped or quietly filled.

## Pitfalls

- **Sourcing to a blog that sources a filing.** Cite the filing. Go to the primary source.
- **Undated figures.** The most common failure after invented numbers. Date everything, including
  quoted prices, which are the most recent trading figure and get refreshed the day of the
  presentation.
- **A forecast presented as a fact.** Label it, or it will be read as reported history.
- **Labels dropping out mid-build.** Tags applied at Phase 3 but dropped when copy moves to slides is
  how unverified figures reach a deck. The review pass checks for exactly this.
