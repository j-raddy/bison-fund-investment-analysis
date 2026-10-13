# Grounding Method (Phase 1, runs before any thesis exists)

Grounding is the first analytical step. The deck is built from it: the public record of what the
business, the street, and the news have said, and the analyst's overlay goes on top of that record
rather than in front of it.

**Read order matters for anchoring.** The analyst reads the digests in this sequence: business
reality first, then news and peers, then the market view digest last. The point is to form a view
from the record before seeing what the street concluded, so the overlay is a position, not an echo.
Only after reading does the analyst answer the Socratic gate (Phase 2) and state a thesis.

The deliverable is four cited digests, not analysis. Analysis happens in Phase 4 with the analyst.

## The four lanes

Run them in parallel if the harness has sub-agents; sequentially in the main session if it does not.
The skill works either way; the lanes and contracts are identical. The lanes collect the evidence
base itself, including the numeric pulls, so there is no separate evidence phase later.

| Lane | Question it answers | Sources and pulls |
|---|---|---|
| 1. Business reality | What has management actually said, guided, and shipped? | Earnings call transcripts, press releases, 10-K/10-Q, investor presentations, segment revenue, statements via the data provider |
| 2. Market view | What does the street think, and where does it disagree with itself? | Consensus estimates, price-target dispersion, ratings, valuation commentary, the provider's own DCF as a cross-check |
| 3. News flow | What has happened in the trailing 6 to 12 months? | Dated headlines: deals, regulatory moves, executive changes, litigation, product events |
| 4. Peer intelligence | How does the market read the two or three closest competitors? | The same grounding for each peer, scaled down (one page each) |

Each lane's brief carries the evidence-tag standard (`references/citation-rules.md`) and the
provider key rule: read the key at runtime from the secrets path, never print it.

## The brief (one per lane, fully self-contained)

Sub-agents cannot ask the analyst questions, so the brief must carry everything. A brief names the
lane's role, the exact deliverable, the output location, and the rules. Nothing else.

```
Lane: [1-4]
Company: [name, ticker, exchange]
Scope: [the lane's question, in one sentence]
Timeframe: [e.g. trailing 12 months]
Deliverable: a markdown digest, maximum [N] lines, every line tagged:
  <claim or figure>, source: <document or link>, as-of: <date>, [fact | estimate | opinion]
No thesis. No judgment. No recommendation. If a line cannot carry a source and a date, drop the line.
Write the digest to: <workspace>/grounding-<lane>.md
Return: the file path and a one-line summary of coverage. Nothing else.
```

Practical rules for the runner:
- Dispatch all lanes in one batch, in parallel. Each gets its own sub-agent; no shared state.
- Sub-agents cannot make judgment calls, so never ask a lane for a recommendation.
- Sub-agents read API keys at runtime from the secrets path (same rule as the main session) and
  never print a key. If a lane has no web or data access, it says so in one line rather than
  filling the digest with plausible text.
- If a lane returns fewer than a third of its requested lines, rerun it with a narrower scope
  before drafting.

## Merge rules (main session, with the analyst)

1. Read all four digests. Tag anything the lanes left unlabeled.
2. Deduplicate: the same claim in two lanes keeps the better source, not both.
3. Separate the three voices explicitly:
   - **The company says** (lane 1, company-reported: fact)
   - **The market says** (lane 2, sell-side and data providers: estimate)
   - **The world says** (lane 3 and 4, news and peers: fact for events, opinion for commentary)
4. Anything contested between lanes becomes a red-team question in Phase 4, not a slide fact.
5. Anything the analyst disagrees with is not deleted. It is written down as the overlay target:
   the deck's job is to say why the analyst sees it differently.

## How grounding changes the deck

- New early slide, **"What the market says"**: consensus target with dispersion, the two or three
  dominant street narratives, each cited. Placed in the Overview, before the recommendation.
- Every core section reads public record first, then the analyst's overlay as its Key takeaway.
  The takeaway is the analyst's take *on* what the record says, not a standalone opinion.
- Disagreement is a feature: "the market says X, we say Y, here is why" is the strongest move a
  student pitch can make. But it must name the source it is disagreeing with.

## Anti-goals

- No lane writes the thesis. The analyst forms it in Phase 2, from the record, in their own words.
- No unsourced lines ship from a digest into a slide. Same gate as everywhere else.
- No aggregator-blog citations (same source-quality rule as the main skill).
- No lane output goes into the deck unread. The analyst reads and merges; shipping lane output
  straight to slides is how a deck becomes a quote collection.
