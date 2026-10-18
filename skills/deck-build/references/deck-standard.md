# Deck Standard (the house bar for a Bison Fund pitch)

Every Bison Fund pitch deck meets this standard, so decks are consistent across analysts and across
tools (Hermes, Claude Code, Codex, Cowork, plain chat). This file is the whole bar: what each slide
must carry and what good looks like on it, so a deck can be built and judged without any other deck
in hand. It is a floor, not a ceiling. A deck may run longer with creative slides, but it must not
run thinner than this.

## What the standard requires

- The full five-section arc, each section opened by a dark divider slide with a big section number.
- A chart or a table on every analytical slide, not paragraphs of text.
- The analyst's judgment shown plainly: a Recommendation slide, a bull case, a bear case, a risk
  matrix, and an investment-thesis slide with three pillars, each pillar carrying its evidence.
- An "analyst owns this" box on any slide where a judgment call is still open.
- A Verification pass slide with sign-off blanks, and a Sources slide.
- Roughly 30 to 41 slides for a full five-section arc. The short-form Alphabet deck (23 slides)
  is the accepted leaner variant; a full-arc deck under 25 slides is under-built.

## The standard slide inventory, with what good looks like

Three of these slides carry a different name in `templates/deck-skeleton.html`, so a deck built from
it can still be checked row by row: its light title slide is `Plain Title`, "A differentiating asset"
is `Flagship asset`, and "The strategy behind the deals" is `The deal strategy`.

Overview. No eyebrow, except the Recommendation slide, which carries "Overview".

| Slide | Must carry | What good looks like |
|---|---|---|
| Title (dark) | Company name, exchange and ticker, a one-line thesis in the presenter's voice, and a data-as-of line | One thesis line a reader could repeat from memory, and a date that matches the freshest figure in the deck. Exactly one title element on the slide |
| Executive Summary | A four-card key-metrics strip, a market-sentiment card, and a thesis box | Four metrics that are the numbers the rest of the deck argues about, each with its source and as-of date. The thesis box states the belief, not the plan |
| What the market says | Consensus target and dispersion, ratings, valuation multiples, and the disagreement | The street's view stated plainly, then the specific point where it differs from the analyst's. Multiples compared against the company's own history or named peers, never in the abstract |
| Recommendation | Recommendation, current price, price target, implied upside, and a Key risk card | The label and the target agree with each other. The current price is the most recent trading figure, the target is the fund's discounted cash flow output, and consensus sits in the takeaway text as a cross-check, never in the target box |
| The big idea | One sentence, the emotional open | A conviction stated in the presenter's voice, with no quotation marks and no attribution. Short enough to read aloud in one breath |

Section 01 Business. The divider carries the section label as its eyebrow.

| Slide | Must carry | What good looks like |
|---|---|---|
| Who is the company | What the business does, its founding and scale, and where it sits in the industry | A reader who knows nothing about the company can say what it sells and to whom after one slide |
| Products and services | The revenue lines, by product or segment, with the share each contributes | Every line tied to a reported figure, and the mix shown as it is rather than as the company describes it |
| Platform key metrics | The operating metric the company runs on, trended | Real reported values with dates, and a comparison against the company's own prior year |
| Industry outlook | Market size, growth rate, and the driver behind the growth | A named driver, not "growth in the sector". Every projection labelled an estimate |
| The market opportunity | The addressable market the thesis depends on | The bottom-up build shown, with its assumptions visible, not a top-down percentage of a large number |
| Where it operates | Geography, and the revenue split by region | Named regions with reported shares, and a note on where the growth is coming from |

Section 02 Competition. The divider carries the section label.

| Slide | Must carry | What good looks like |
|---|---|---|
| Revenue diversification | Revenue by segment or line, and how concentrated it is | The concentration stated as a number, and the risk of that concentration named |
| Competitive landscape | The two or three closest competitors, compared on the metrics that decide the market | A table a reader can scan, with the same metrics for each company, all sourced and dated |
| A differentiating asset | The one thing the company has that the others do not, whether a product, a programme, or a network | The asset named, its advantage argued from evidence, and the case where it stops mattering |
| Regulatory landscape | The rules that touch the business, and the open matters | Actual policy or proceeding names with dates, never "subject to regulation" |
| Competitive moat | The source of the defence and its durability | The moat argued from a mechanism, such as switching costs or scale economics, with the evidence that it is holding or eroding |
| Recent acquisitions | What was bought, for how much, when, and why | The headline deal's price and date, and the strategic reason in one line |
| Management and compensation | Who runs it, tenure, ownership, and how they are paid | Compensation tied to the metrics the thesis depends on, stated plainly |

Section 03 Key Deals. The divider carries the section label.

| Slide | Must carry | What good looks like |
|---|---|---|
| The strategy behind the deals | The pattern across the transactions | One plain statement of what the company is buying, with two or three deals as the evidence |
| The headline deal | The largest or most thesis-relevant transaction: price, date, rationale, and what it changed | The figure, the date, and what it does to the numbers the deck already showed |
| The rest of the portfolio | The remaining transactions and partnerships, briefly | A dated list rather than prose, with the deals that do not matter to the thesis left short |

Section 04 Financials. The divider carries the section label. One chart per slide, each with a Key
takeaway box.

| Slide | Must carry | What good looks like |
|---|---|---|
| Revenue | Revenue trend and the company's core operating metric | Both over the same period, with the growth rate stated and its driver named |
| Unit economics | The revenue and cost per unit that drives the model | Actual reported inputs, and a clear statement of which inputs the model extends |
| Margins | Gross, operating, and the trajectory | The line the thesis depends on, with the reason it moves |
| Profitability | GAAP against non-GAAP, and what the difference is | The reconciling items named, and no non-GAAP figure standing in for a reported one |
| Cash flow | Operating cash flow, capital expenditure, free cash flow | The conversion from earnings shown, so the deck does not rest on an earnings figure alone |
| Balance sheet and quality of earnings | Debt, cash, maturities, and the items that need a second look | Net debt or net cash stated, the nearest maturity dated, and any accounting choice that flatters the result flagged |

Section 05 Valuation and Outlook. The divider carries the section label. The trailing slides carry
the "Outlook" eyebrow.

| Slide | Must carry | What good looks like |
|---|---|---|
| Capital allocation | Buybacks, dividends, reinvestment, and debt reduction | The specific authorisations with their amounts and dates, never "returns capital to shareholders" |
| Share performance | The price series against a benchmark and the peer set | The period named, and the comparison the thesis actually rests on |
| Discounted cash flow | Inputs, projection, and sensitivity on one slide | The discount rate, the terminal growth, and the sensitivity grid all visible, with the model record behind every figure |
| The bull case | The case for the thesis, drawn from evidence already shown | Three to five points, each one pointing at a figure elsewhere in the deck |
| The bear case | The strongest case against the thesis, and what would break it | Written to persuade, with the assumptions the thesis depends on attacked directly |
| Risk matrix | Three by three, probability against impact, populated | Named risks placed by judgement, with the ones that would kill the thesis in the top rows |
| Investment thesis | Three pillar cards, each with its evidence | Each pillar is a belief with a figure behind it, not a theme |
| Upcoming milestones and catalysts | The dated events that move the story, eyebrow "Outlook" | Real dates from the company's own calendar, each tied to the part of the thesis it tests |

Closing. No eyebrow.

| Slide | Must carry | What good looks like |
|---|---|---|
| Verification pass | The analyst's checks, what remains open, and a sign-off box with blank lines | Each check states what was reopened and confirmed. Blank means blank |
| Sources | The full list behind every figure, with dates | Ordered as the deck reads, and every figure in the deck resolves to a line here |

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
4. Run `scripts/deck_audit.py` on the deck and fix everything it reports. It must exit 0.
5. Run the browser audit in `references/deck-build-checklist.md`, which covers the layout checks the
   script cannot read from the file: overflow and note collisions.
6. Run the review loop in the `pitch-review` skill until zero blockers.
7. Hand it to the analyst for the Phase 6 sign-off (the Verification pass slide).

## Relationship to the required sections

The five `pitch-*` section skills define the content each of the five sections must carry. This
file defines the deck that presents them. Where they overlap, the section method wins on content
and this file wins on structure, slide inventory, and design.
