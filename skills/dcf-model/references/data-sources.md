# Market data sources

Where the numbers in a pitch come from, and how a machine gets them. The setup
script (`python3 setup.py`, run once after installing) walks through these
choices and records the result in `~/.config/bison/config.json`.

## The four choices

1. **Financial Modeling Prep.** A keyed API. The free tier allows about 250
   calls a day, end of day data, roughly 5 years of history. This is the one
   source with a ready model script (`fmp_dcf.py`). Get a key at
   financialmodelingprep.com.
2. **SEC EDGAR plus the US Treasury.** No key, nothing to install. SEC EDGAR
   serves every US filing and the XBRL financial facts as machine-readable
   JSON; the Treasury serves the daily yield curve, which is the dated
   risk-free rate the DCF method asks for. `sec_fundamentals.py` builds the
   DCF inputs from these two, keylessly.
3. **Another provider you already have a key for.** School-issued keys,
   Finnhub, Alpha Vantage, Polygon, Tiingo, EODHD, Twelve Data, and similar
   services each have their own endpoint shapes. Setup stores the key so no
   secret is hardcoded in a file or transcript; the analyst pulls data with
   the provider's own docs. Setup cannot verify an arbitrary provider, so a
   human confirms the key works.
4. **Bloomberg Terminal.** Only for analysts with a logged-in terminal and
   entitlements. There is no public Bloomberg API. The terminal path is
   covered in `bloomberg-terminal.md`.

## Where students get this data

- The finance lab. Most business schools run Bloomberg terminals and hold
  seats for S&P Capital IQ, Morningstar Direct, and Wharton Research Data
  Services (WRDS), which carries Compustat and CRSP. These are the strongest
  sources on campus, and they are licensed for coursework, so the student
  pays nothing.
- The free sources above. FMP's free tier, SEC EDGAR, the Treasury yield
  curve, and yfinance (an unofficial Yahoo Finance wrapper: fine for a
  personal draft, not a citable source for a slide).
- The school's library guide. Most business schools publish a finance data
  guide that lists which databases the campus subscribes to and how to
  request an account. That is the fastest route to the school's paid tools.

The package rule still applies to every one of these: a figure on a slide
needs a source a reviewer can reopen. A Bloomberg pull is licensed for
internal use, so it gets re-checked against the filing or a public source
before it ships.

## The keyless endpoints

SEC EDGAR asks for a User-Agent that names the caller. Set `BISON_CONTACT` to
your email so the request identifies itself.

- Ticker to CIK: `https://www.sec.gov/files/company_tickers.json`
- Company facts (all XBRL for one company): `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- One fact across all filers, for peer screening: `https://data.sec.gov/api/xbrl/frames/us-gaap/<tag>/USD/CY<year>.json`
- Treasury daily yield curve: `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv`

The XBRL tag names differ from FMP's field names. The mapping
`sec_fundamentals.py` uses, verified against Apple's 10-K: operating cash flow
is `NetCashProvidedByUsedInOperatingActivities`, revenue is
`RevenueFromContractWithCustomerExcludingAssessedTax`, capex is
`PaymentsToAcquirePropertyPlantAndEquipment`, diluted shares is
`WeightedAverageNumberOfDilutedSharesOutstanding`.

## Choosing

- A machine with no key: choose option 2 and run `sec_fundamentals.py`.
- A class that assigns FMP: choose option 1 and run `fmp_dcf.py`.
- A lab with Bloomberg or Capital IQ: use those for the deep pulls, and keep
  the model record citing the filing or a public source.
