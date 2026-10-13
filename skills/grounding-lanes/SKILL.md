---
name: grounding-lanes
description: "Use when gathering what the business, the street, and the news have independently said about a company, before any thesis exists."
version: 2.0.0
author: Jacob Radke
license: MIT
---

# Grounding Lanes

Phase 1 of the pitch loop. Four lanes of independent research, run before the analyst has stated a
view, so the record is on the table before anyone forms an opinion.

The rule that makes this phase worth its cost: **no thesis, no judgment, no recommendation.** Each
lane returns what was said and when it was said. The analyst forms the view afterward, after reading
the record and before seeing what the street concluded.

## Triggers

- The hub routes Phase 1 here.
- A request to find out what the street says, what management said last quarter, what the news flow
  has been, or who the close competitors are.

## Inputs

- Company name, ticker, and exchange.
- The analyst's one-line reason for interest, when there is one.
- Public sources: filings, transcripts, investor materials, dated news, and market-data providers.

## The four lanes

1. **Business reality.** Earnings call transcripts and filings. What management says the business is,
   what the segments earn, what changed since the last call.
2. **News flow.** The trailing 6 to 12 months, every item dated. Material events, not coverage volume.
3. **Peer intelligence.** The two or three closest competitors, on the metrics that matter to this
   thesis, from each peer's own filings.
4. **Market view.** Consensus estimates, analyst price targets, valuation commentary.

Full briefs, the sub-agent contracts, and the merge rules: `references/grounding-method.md`.

## How to run it

- Parallel sub-agents when the harness has them, one lane each, so the lanes cannot contaminate each
  other. Sequential when it does not; keep the lanes separate either way.
- **Read order for the analyst:** business reality first, then news and peers, and the market view
  digest last. Forming a view from the record before seeing the street's conclusion is the whole point
  of the ordering.
- Every line in every digest carries a source and an as-of date, in the tag shape from
  `sourcing-standard`.

## Merging

The analyst merges, not the assistant: deduplicate, tag which voice said what (company, street, or
press), and turn contested claims into questions for the Phase 2 Socratic gate. A contradiction
between lanes is a finding to carry forward, never something to smooth over.

## Output

Four cited digests, plus the analyst's merged read of them. Contested claims become Phase 2 questions.

## Pitfalls

- **Researching past the lane.** A lane that starts arguing the case has failed the phase. Collect
  what was said; the argument is Phase 4.
- **Undated news.** A news lane without dates is unusable in a pitch, because a two-year-old item read
  as current changes the thesis.
- **Reading the market view first.** It anchors the analyst on the street's conclusion, which is
  exactly the thinking this package exists to prevent.
- **One vendor's summary standing in for the record.** Consensus feeds and aggregator pages are the
  street's interpretation. Filings and transcripts are the record.
