# Deck Standard (the house bar for a Bison Fund pitch)

Every Bison Fund pitch deck meets this standard, so decks are consistent across analysts and
across tools (Hermes, Claude Code, Codex, Cowork, plain chat). The bar is set by the fund's
reference deck, the **Uber equity pitch** (41 slides, October 2026). The **Alphabet pitch**
(23 slides) is the second reference. The standard is a floor, not a ceiling: a deck may run
longer with creative slides, but it must not run thinner than this.

## What "Uber grade" means

- The full five-section arc, each section opened by a dark divider slide with a big section number.
- A chart or a table on every analytical slide, not paragraphs of text.
- The analyst's judgment shown plainly: a Recommendation slide, a bull case, a bear case, a risk
  matrix, and an investment-thesis slide with three pillars, each pillar carrying its evidence.
- An "analyst owns this" box on any slide where a judgment call is still open.
- A Verification pass slide with sign-off blanks, and a Sources slide.
- Roughly 30 to 41 slides for a full five-section arc. The short-form Alphabet deck (23 slides)
  is the accepted leaner variant; a full-arc deck under 25 slides is under-built.

## The standard slide inventory (in order)

Overview (no eyebrow except the Recommendation slide's "Overview"):
1. Title (dark): company name, exchange and ticker, one-line thesis, data-as-of line.
2. Executive Summary: a 4-card key-metrics strip, a market-sentiment card, and a thesis "own" box.
3. What the market says: consensus target and dispersion, ratings, valuation multiples, the disagreement.
4. Recommendation: recommendation, current price, price target, implied upside; a Key risk card.
5. The big idea: one sentence in the analyst's words, the emotional open.

Section 01 Business (divider, then slides):
- Who is the company
- Products and services
- Platform key metrics
- Industry outlook
- The market opportunity
- Where it operates

Section 02 Competition:
- Revenue diversification
- Competitive landscape
- A differentiating asset (for example, a flagship product or program)
- Regulatory landscape
- Competitive moat
- Recent acquisitions
- Management and compensation

Section 03 Key Deals:
- The strategy behind the deals
- The headline deal
- The rest of the portfolio

Section 04 Financials:
- Revenue (and the company's core operating metric, for example gross bookings or annual recurring revenue)
- Unit economics
- Margins
- Profitability (GAAP versus non-GAAP)
- Cash flow
- Balance sheet and quality of earnings

Section 05 Valuation and Outlook:
- Capital allocation
- Share performance
- Discounted cash flow (inputs, projection, sensitivity, all on one slide)
- The bull case
- The bear case
- Risk matrix (3 by 3, probability x impact)
- Investment thesis (three pillar cards, each with its evidence)
- Upcoming milestones/catalysts (eyebrow "Outlook")

Closing:
- Verification pass (analyst checks, what remains open, a sign-off box with blank lines)
- Sources

## Design system

Use `templates/deck-house.css` verbatim as the deck stylesheet. It is the fund's shared design
system: tokens, `.slide` and `.slide.dark`, `.eyebrow`, `h2.title`, `p.sub`, `.content`, the
`.grid` / `.g2` `.g3` `.g4` card grids, `.card` with `.v` and `.d` (plus `.card.y` yellow and
`.card.g` green variants), `.bullets`, `.note`, tables, CSS bar `.chart` / `.bar` / `.col`,
`.divider-num` / `.divider-list`, the `.own` analyst-owns box, `.blank` sign-off rule, `.deal`,
`.pill`, and `.badge-buy`. Palette and typeface rationale: `references/brand-and-design-tokens.md`.

Conventions:
- Footer on every slide: `<div class="foot"><span>Bison Fund Equity Pitch</span><span class="pageno">NN / TOTAL</span></div>`.
  One name per slide, in the footer. The page total must equal the real slide count.
- Eyebrow is the section label ("01 Business", "05 Valuation"); Overview slides have none except
  Recommendation ("Overview"); closing slides have none.
- Charts are CSS bar charts (`.chart` > `.bar` > `.col` with `.lab` for the value and `.cat` for
  the category), with bar heights proportional to value. Bars need real height.
- A `.note` line carries inline sources on a slide; the Sources slide carries the full list.

## Build workflow

1. Build the plain deck as one html file using `templates/deck-house.css`. Start from
   `templates/deck-skeleton.html`, which ships the full inventory with placeholders and correct footers.
2. Fill each placeholder from the fact sheet. No unsourced figure enters a slide.
3. Wrap it in the commentable harness (`templates/commentable-deck-harness.html`), one screen per
   section plus Overview, with `data-region` on slides and key cards.
4. Run the browser audit in `references/deck-build-checklist.md`.
5. Run the review loop in the `pitch-review` skill until zero blockers.
6. Hand it to the analyst for the Phase 6 sign-off (the Verification pass slide).

## Relationship to the required sections

The five `pitch-*` section skills define the content each of the five sections must carry. This
file defines the deck that presents them. Where they overlap, the section method wins on content
and this file wins on structure, slide inventory, and design.
