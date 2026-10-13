# Section 05, Valuation and Outlook

Slides 29 to 40. Core question: what is it worth, what could go wrong, and why own it?

## Required elements

- Capital allocation: where the company puts its money (M&A, research and development, buybacks,
  balance sheet).
- A discounted cash flow: free cash flow projection, discount rate, terminal value, implied share
  price, with every assumption stated.
- Bull and bear scenarios with implied values.
- Valuation summary: triangulated fair value and the conclusion.
- Risk register and a probability by impact matrix.
- Catalysts timeline and recent news.
- Investment thesis pillars and the recommendation.

## Analyst owns, and the assistant must never fill in

- the price target and the implied upside;
- the thesis pillars, the reason to own it, in the analyst's words;
- the recommendation, buy, hold, or sell, and the conviction behind it.

The assistant's job in this section is to lay out the inputs, the range, and the assumptions, then
hand the pen back.

## Using consensus estimates

When the fund's method is DCF, consensus estimates (for example Financial Modeling Prep's
analyst-estimates, price-target-summary, and discounted-cash-flow endpoints) are a legitimate way to
fill the earnings base fast, with three rules:

1. Label every consensus figure as an estimate, and carry its source and as-of date.
2. Consensus is the cross-check, not the answer. The DCF sets the view; consensus sets the yardstick.
   A large gap between the two is a finding to defend, not a number to average away.
3. Terminal growth and the discount rate stay with the analyst. No consensus feed sets the discount
   rate for the fund.

Build the model with `dcf-model`: that skill holds the method, the working script, and the market
data keys.

## Evidence

Every figure carries the tag shape from `sourcing-standard`. Record every model run, inputs, case
outputs, and sensitivity grid, in a dated model record beside the fact sheet, so every slide figure
resolves to a source.
