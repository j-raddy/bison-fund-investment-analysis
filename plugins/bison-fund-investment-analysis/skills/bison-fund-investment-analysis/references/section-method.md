# Section Method, What Goes in Each Section

The pitch runs five sections in this fixed order. This file lists the required elements
for each one, the deck slides it feeds, and the judgment calls that stay with the analyst.
Work top to bottom. Do not jump ahead to Valuation before the earlier sections are sourced.

Grounding rule: every section reads public record first, then the analyst's overlay as its
Key takeaway. The takeaway is the analyst's take *on* what the record says (see
`grounding-method.md`), never a standalone opinion floating without the market view.

## Standard evidence tag

Every figure, everywhere, uses this shape:

```
<value>, source: <document/site + link>, as-of: <date>, [fact | estimate | opinion]
```

A line that cannot carry a source is tagged `[UNVERIFIED]` and stays out of the deck.

## Section map

| Section | Slides | Core question it answers |
|---|---|---|
| 01 Business, Products & Industry | 01–10 | What is this business and is its market growing? |
| 02 Competition, M&A & Leadership | 11–18 | Who does it compete with and who runs it? |
| 03 Key Deals | 19–21 | What transactions or partnerships shape the thesis? |
| 04 Financials | 22–28 | Does the money work, revenue, margins, returns, cash? |
| 05 Valuation & Outlook | 29–40 | What is it worth, what could go wrong, why own it? |

---

## Section 01, Business, Products & Industry Outlook (slides 01–10)

Required elements:
- One-line company description and headline scale metrics (revenue, customers, assets).
- Products and services, segment by segment, each with its revenue contribution where disclosed.
- Platform / operating KPIs the market actually trades on (users, net deposits, assets under custody).
- Industry outlook and the structural drivers (wealth transfer, mobile-first behavior, fee compression).
- Market opportunity: TAM / SAM sizing **with a cited source and a stated CAGR**.
- Geographic and product footprint.

Analyst owns: the narrative of *why this business is durable*, not just what it sells.

## Section 02, Competition, M&A & Leadership (slides 11–18)

Required elements:
- A peer comparison table on consistent metrics: net revenue, growth, net income, margin,
 accounts, client assets, revenue per account, market cap, P/E.
- Revenue diversification: how the mix shifts across periods, and what it means.
- Regulatory landscape that shapes the business model.
- The competitive moat, evidenced (e.g. recurring subscription revenue vs. volume-dependent revenue).
- Recent M&A and the rationale for each deal.
- Management team: tenure, background; executive compensation vs. peers.

Analyst owns: whether the moat is real and whether management is aligned.

## Section 03, Key Deals (slides 19–21)

Required elements:
- The transactions and partnerships that matter most to the thesis.
- For each: target, consideration, strategic rationale, and what it changes about the story.

Analyst owns: which deals are thesis-relevant vs. noise.

## Section 04, Financials (slides 22–28)

Required elements:
- Revenue trajectory with CAGR / YoY and the named drivers.
- Unit economics and ARPU, what each customer is worth, and cost to acquire.
- Return metrics: ROA, ROE, ROIC, with peak callouts.
- Margin structure over time: gross, operating, EBITDA, net.
- Liquidity and balance-sheet strength: current/quick ratios, cash, undrawn credit.
- Cash flows: CFO, capex, free cash flow.

Analyst owns: which financial trend is the one that actually drives the valuation.

## Section 05, Valuation & Outlook (slides 29–40)

Required elements:
- Capital allocation: where the company puts its money (M&A, R&D, buybacks, balance sheet).
- DCF: FCF projection, WACC, terminal value, implied share price, with every assumption stated.
- Bull / bear scenarios with implied values.
- Valuation summary: triangulated fair value and the conclusion.
- Risk register and a probability × impact matrix.
- Catalysts timeline and recent news.
- Investment thesis pillars and the recommendation.

**Analyst owns, and the assistant must never fill in for them:**
- the **price target** and the implied upside;
- the **thesis pillars** (the reason to own it, in the analyst's words);
- the **recommendation** (buy / hold / sell) and its confidence.

Build the valuation with the fund's DCF method: `references/dcf-method.md` for the steps,
`scripts/fmp_dcf.py` for the working model. Consensus fills the earnings base; the analyst owns
the discount rate, terminal growth, and the final number.

The assistant's job in this section is to lay out the inputs, the range, and the
assumptions, then hand the pen back.

### Using consensus estimates (DCF-anchored funds)

When the fund's method is DCF, consensus estimates (e.g. Financial Modeling Prep's
`analyst-estimates`, `price-target-summary`, and `discounted-cash-flow` endpoints) are a
legitimate way to fill the earnings base fast, with three rules:

1. **Label every consensus figure as an estimate** and carry its source and as-of date.
2. **Consensus is the cross-check, not the answer.** The DCF sets the view; consensus sets
  the yardstick. A large gap between the analyst's DCF and consensus is a finding to
  defend, not a number to average away.
3. **Terminal growth and WACC stay with the analyst.** No consensus feed sets the discount
  rate for the fund.

Keys are read from the `FMP_API_KEY` environment variable, or a local secrets file, at runtime
and never hardcoded, printed, or committed into a deck or handout.
