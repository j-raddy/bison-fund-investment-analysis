# Bloomberg Terminal: the DCF input path for analysts with access

For fund members on a Bloomberg machine. FMP stays the automatable path (`scripts/fmp_dcf.py`);
Bloomberg is the richer terminal-side path and is the standard in industry. There is no public or
free Bloomberg market-data API: every route below requires a logged-in Terminal and entitlements.

## Resources

- API library (downloads, SDKs, developer guides): https://professional.bloomberg.com/support/api-library/
- The BLPAPI Core User Guide and Core Developer Guide download from that page. They are not
  redistributed with this skill: Bloomberg's documentation is licensed to the subscriber and
  this repository is public.

## Three ways in, cheapest first

1. **Excel `=BDP()` and `=BDH()`** on the terminal machine. Fastest for a DCF input sheet.
   - `=BDP("UBER US Equity","PX_LAST")` current price
   - `=BDH("UBER US Equity","PX_LAST","1/1/2025","12/31/2025")` a price series
2. **Python `blpapi`** (the library in the guides above), or the friendlier `xbbg` wrapper.
   ```python
   from xbbg import blp
   blp.bdp(tickers="UBER US Equity", flds=["px_last", "cur_mkt_cap", "net_debt"])
   df = blp.bdh("UBER US Equity", "px_last", "2025-01-01", "2025-12-31")
   ```
   Both need the terminal logged in on the same machine (or Bloomberg Anywhere with the
   entitlement active) and the `blpapi` transport running locally.
3. **Terminal functions**: `FLDS<GO>` to find field mnemonics, `DCF<GO>` for Bloomberg's own
   model, `BEST<GO>` for consensus. Bloomberg's DCF is a prebuilt assumption set. Use it as a
   cross-check, the same way you use FMP's `discounted-cash-flow` value.

## What to pull for the model

| Input | Common mnemonic (verify with `FLDS<GO>`) |
|---|---|
| Price | `PX_LAST` |
| Diluted shares | `EQY_DILUTED_SHARES`, or `BS_SH_OUT` |
| Net debt | `NET_DEBT`, or `BS_TOT_DEBT` minus `BS_CASH_NEAR_CASH_ITEM` |
| Revenue history | `SALES_REV_TURN` |
| Revenue consensus | `BEST_SALES` |
| EPS consensus | `BEST_EPS` |
| Free cash flow | `CF_FREE_CASH_FLOW`, or `CF_CASH_FROM_OPER` minus `CF_CAP_EXPEND` |
| Beta | `BETA_ADJ_OVERRIDABLE` (adjusted) or `BETA_RAW_OVERRIDABLE` |
| Consensus target | `BEST_TARGET_PRICE` |
| Ratings | `BEST_ANALYST_RATING` |

Then run the same DCF steps as `references/dcf-method.md`. The variable names differ; the model
does not.

## Rules and caveats

- **Entitlements vary.** A field that works on one terminal may be blocked on another. If a mnemonic
  fails, check with `FLDS<GO>` before assuming the data does not exist.
- **Redistribution.** Terminal data is licensed to the subscriber for internal use. Do not lift raw
  Bloomberg tables into published decks and handouts; cite the company filing or a public source in
  anything the fund distributes. This matters more than it sounds: pitches leave the building.
- **Never store a Bloomberg login or session token** in a skill file, script, deck, or template.
- **Bloomberg's DCF is not your DCF.** Same rule as FMP: it is a cross-check, not the answer. The
  analyst owns the discount rate, terminal growth, and the final number.
