# FMP API reference (cheatsheet)

The calls this package makes, one page. For anything not listed here, open FMP's full, current
developer docs: https://financialmodelingprep.com/developer/docs

Base URL: `https://financialmodelingprep.com/stable/`. Append `?apikey=KEY`, or `&apikey=KEY`
when other parameters are already present. Only the current `stable` API exists; the legacy v3
and v4 paths are discontinued.

## Endpoints this package uses (scripts/fmp_dcf.py)

`stable/quote?symbol=<SYMBOL>`
  - `price`, `yearHigh`, `yearLow`

`stable/income-statement?symbol=<SYMBOL>&period=annual&limit=3`
  - `revenue`, `weightedAverageShsOutDil`

`stable/cash-flow-statement?symbol=<SYMBOL>&period=annual&limit=3`
  - `operatingCashFlow`, `capitalExpenditure`

`stable/balance-sheet-statement?symbol=<SYMBOL>&period=annual&limit=1`
  - `totalDebt`, `cashAndShortTermInvestments`

`stable/discounted-cash-flow?symbol=<SYMBOL>`
  - `dcf` (a cross-check only, never the analyst's price target)

## Endpoints the manual method references (dcf-method.md)

`stable/analyst-estimates?symbol=<SYMBOL>`: `revenueAvg`, `ebitdaAvg`
`stable/price-target-summary?symbol=<SYMBOL>`: `lastYearAvgPriceTarget`, `lastYearCount`
`stable/key-metrics` or `stable/financial-ratios?symbol=<SYMBOL>`: beta

## Notes

- Rows come back newest first; index 0 is the latest period.
- Free tier is rate-limited to about 250 calls a day, so one key per analyst.
