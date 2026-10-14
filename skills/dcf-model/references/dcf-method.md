# DCF Method (the fund's valuation standard)

The Bison Fund values with a discounted cash flow model. This file is the build guide;
`scripts/fmp_dcf.py` is the working implementation that pulls from FMP and produces the model.
Write the model yourself or run the script, then defend every assumption. Consensus feeds the
earnings base; the analyst owns the discount rate, terminal growth, and the final number.

## The model in one line

    equity value = PV(free cash flows, years 1..N) + PV(terminal value), then bridge
                   enterprise value to equity value and divide by diluted shares

## Step 1. Inputs

| Input | Source | Notes |
|---|---|---|
| Revenue history | `stable/income-statement` | field `revenue`; 3 to 5 years |
| Revenue forecast | `stable/analyst-estimates` (field `revenueAvg`) or your own drivers | consensus is an estimate; your own build is preferred for a pitch |
| EBITDA forecast | `stable/analyst-estimates` (field `ebitdaAvg`) | useful for the exit-multiple cross-check |
| Free cash flow history | `stable/cash-flow-statement` | `operatingCashFlow` minus `capitalExpenditure` |
| Net debt | `stable/balance-sheet-statement` | `totalDebt` minus `cashAndShortTermInvestments` |
| Diluted shares | `stable/income-statement` (field `weightedAverageShsOutDil`) or the latest 10-Q | use the most recent diluted count |
| Current price | `stable/quote` | fields `price`, `yearHigh`, `yearLow` |
| Consensus price target | `stable/price-target-summary` | fields `lastYearAvgPriceTarget`, `lastYearCount`; cross-check only |
| FMP's own DCF value | `stable/discounted-cash-flow` | field `dcf`; another cross-check, not your answer |
| Beta | `stable/key-metrics` or `stable/financial-ratios` | for the WACC build |

Endpoint paths and field names come from `references/fmp-api-docs.md`, a cheatsheet of the
calls this package makes, with a link to FMP's full current docs for anything not listed there.
Only the stable base (`https://financialmodelingprep.com/stable/`) exists; the legacy v3 and v4
paths are discontinued. If a call returns an error, check the path against the cheatsheet (and
the linked docs) before assuming the data does not exist.

## Step 2. Forecast revenue

Either use the consensus revenue path from `analyst-estimates`, or build your own from drivers
(bookings growth, take rate, member growth). For a student pitch, a two-scenario build is more
defensible than one line: a base case near consensus and one alternate case you can argue.

## Step 3. Convert revenue to free cash flow

    EBIT (operating income)
      + depreciation and amortization
      - capital expenditures
      - change in net working capital
      - taxes on EBIT (EBIT x tax rate)
    = unlevered free cash flow (UFCF)

Practical shortcut when statement detail is thin: use a trailing FCF margin (FCF over revenue,
averaged over the last three years) and hold or fade it across the forecast. State the margin
you chose and why. Do not mix adjusted EBITDA into a GAAP-based FCF build; pick one basis.

## Step 4. Discount rate (WACC)

    WACC = (E / V) x Re + (D / V) x Rd x (1 - tax rate)
    Re   = risk-free rate + beta x equity risk premium        (CAPM)

- Risk-free rate: the 10-year Treasury at your valuation date. Date it.
- Beta: 5-year monthly beta is the common student choice.
- Equity risk premium: pick a published estimate (Damodaran's is the usual student source) and cite it.
- Cost of debt: the company's recent borrowing rate or yield on its bonds, tax-affected.

The analyst sets these. Sensible ranges for a platform business: beta roughly 0.8 to 1.4,
WACC roughly 7% to 12%. Never let a consensus feed pick the discount rate.

## Step 5. Terminal value

    Gordon growth: TV = FCF(N) x (1 + g) / (WACC - g)

- Terminal growth must be below long-run nominal GDP growth; a ceiling near 2.5% is the usual discipline.
- Cross-check with an exit multiple: TV implied EV/EBITDA or EV/FCF should sit in a range you can
  defend against comparables. If the Gordon-growth TV implies a silly exit multiple, the model is
  telling you the terminal growth or WACC is off.

## Step 6. Bridge to equity value

    enterprise value
      + cash and equivalents (non-operating)
      - total debt
      - minority interest and preferred
      + value of equity investments (e.g. Uber's stakes)
    = equity value
      / diluted shares outstanding
    = value per share

For a company holding public stakes (Lucid, for example), decide whether to mark them to market
and add. State the treatment; do not leave it silent.

## Step 7. Sensitivity

Always produce a grid, at minimum WACC (rows) by terminal growth (columns), showing value per
share. It answers the only question that matters: how much of the answer hangs on two inputs.
A sensitivity grid is where most DCF mistakes get caught.

## Common errors to catch before presenting

- Discounting a negative or SBC-inflated FCF without saying which basis it is on.
- Terminal value over 70% of enterprise value without a defense.
- Using adjusted EBITDA as FCF.
- Forgetting the share count is diluted, or using a stale count.
- Terminal growth above nominal GDP growth.
- WACC below the risk-free rate.
- Double counting equity stakes (in FCF and again in the bridge).

## Cross-checks

1. Your value per share vs the consensus price target.
2. Your value vs FMP's `discounted-cash-flow` output.
3. Your implied exit multiple vs comparables.
A large gap from consensus is a finding. State why you differ or change your mind.

## Bloomberg Terminal (for analysts who have access)

There is no public or free Bloomberg market-data API. BLPAPI (the client library, plus Python
`blpapi` or the `xbbg` wrapper) and the Excel `=BDP()` / `=BDH()` functions all require a logged-in
Bloomberg Terminal and entitlements on the machine making the call. Enterprise routes (Data License,
B-PIPE, SAPI) are contract products. OpenFIGI is free and public but only maps identifiers.

See `references/bloomberg-terminal.md` for the API library link (where Bloomberg publishes the
BLPAPI guides), the mnemonics to pull for each model input, and the redistribution caveat. FMP remains
the automatable path; Bloomberg is the terminal-side path.
