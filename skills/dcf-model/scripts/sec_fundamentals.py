#!/usr/bin/env python3
"""Build the DCF inputs with no API key, from SEC EDGAR and the US Treasury.

Usage:
  python3 sec_fundamentals.py UBER                 # keyless: SEC XBRL + Treasury
  python3 sec_fundamentals.py UBER --price 62.40   # adds the reverse DCF
  python3 sec_fundamentals.py --demo               # offline: verifies the math

Why this exists: a pitch should not dead-end because a machine has no market-data
key. Every number this script prints comes from a free, keyless, citable source:

  - SEC EDGAR XBRL company facts  (https://data.sec.gov/api/xbrl/companyfacts/)
  - SEC EDGAR ticker to CIK map   (https://www.sec.gov/files/company_tickers.json)
  - US Treasury daily yield curve (10-year, the risk-free rate the method asks for)

Sources need a User-Agent that identifies the caller, per SEC policy. Set
BISON_CONTACT to your email, or SEC may throttle you.

Field names differ from FMP's: the SEC tag for operating cash flow is
NetCashProvidedByUsedInOperatingActivities, not operatingCashFlow. That mapping
is why this file exists rather than asking the assistant to improvise tags.

Every model output is an estimate. The price target is the analyst's, not this script's.
"""
import argparse, csv, datetime, io, json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fmp_dcf import report  # noqa: E402  (same math and output as the FMP path)

CACHE = os.path.expanduser("~/.config/bison/company_tickers.json")
UA = "bison-fund-research/1.0 (contact: %s)" % os.environ.get("BISON_CONTACT", "student@example.edu")

# The XBRL tags this model needs, per concept, in preference order.
TAGS = {
    "revenue":    ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                   "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "ocf":        ["NetCashProvidedByUsedInOperatingActivities",
                   "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex":      ["PaymentsToAcquirePropertyPlantAndEquipment",
                   "PaymentsToAcquireProductiveAssets"],
    "shares":     ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "cash":       ["CashAndCashEquivalentsAtCarryingValue"],
    "short_inv":  ["MarketableSecuritiesCurrent", "ShortTermInvestments"],
    "debt_nc":    ["LongTermDebtNoncurrent", "LongTermDebt"],
    "debt_c":     ["LongTermDebtCurrent", "DebtCurrent"],
    "d_and_a":    ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization"],
    "op_income":  ["OperatingIncomeLoss"],
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def ticker_to_cik(ticker):
    """SEC's own ticker map. Cached for a day so repeated runs cost one request."""
    data = None
    if os.path.exists(CACHE):
        age = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(CACHE))
        if age.days < 1:
            data = json.load(open(CACHE))
    if data is None:
        data = fetch("https://www.sec.gov/files/company_tickers.json")
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(data, open(CACHE, "w"))
    for row in data.values():
        if row["ticker"].upper() == ticker.upper():
            return str(row["cik_str"]).zfill(10), row["title"]
    sys.exit("No SEC filer with ticker %s. Check the ticker, or the company may file "
             "outside the US." % ticker)


def annual(gaap, concept):
    """Annual 10-K values for one concept, oldest first, as [(end_date, value)].

    Quarterly facts and amendments share the same concept, so filter to 10-K and
    to durations of about a year; instantaneous items (balance sheet) have no
    start date and are kept as filed.
    """
    for tag in TAGS[concept]:
        if tag not in gaap:
            continue
        units = gaap[tag]["units"]
        unit = "USD" if "USD" in units else ("shares" if "shares" in units else list(units)[0])
        seen = {}
        for o in units[unit]:
            if o.get("form") not in ("10-K", "10-K/A"):
                continue
            if o.get("start"):
                d0 = datetime.date.fromisoformat(o["start"])
                d1 = datetime.date.fromisoformat(o["end"])
                if not 300 <= (d1 - d0).days <= 400:
                    continue
            seen[o["end"]] = o["val"]
        if seen:
            return sorted(seen.items()), tag
    return [], None


def treasury_10y():
    """The dated 10-year Treasury yield: the method's risk-free rate. Keyless CSV."""
    year = datetime.date.today().year
    url = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
           "daily-treasury-rates.csv/%d/all?type=daily_treasury_yield_curve"
           "&field_tdr_date_value=%d&page&_format=csv" % (year, year))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        rows = list(csv.DictReader(io.StringIO(r.read().decode())))
    rows = [x for x in rows if x.get("10 Yr")]
    if not rows:
        return None, None
    latest = max(rows, key=lambda x: datetime.datetime.strptime(x["Date"], "%m/%d/%Y"))
    d = datetime.datetime.strptime(latest["Date"], "%m/%d/%Y").date()
    return float(latest["10 Yr"]) / 100.0, d.isoformat()


def run(symbol, wacc, tg, years, price):
    if tg >= wacc:
        sys.exit("Terminal growth (%.0f%%) must stay below the discount rate (%.0f%%)."
                 % (tg * 100, wacc * 100))
    cik, name = ticker_to_cik(symbol)
    facts = fetch("https://data.sec.gov/api/xbrl/companyfacts/CIK%s.json" % cik)
    gaap = facts["facts"].get("us-gaap", {})
    if not gaap:
        sys.exit("%s files no us-gaap XBRL facts. A foreign filer using IFRS may need "
                 "the ifrs-full taxonomy, or use the FMP path." % symbol)

    got = {c: annual(gaap, c) for c in TAGS}
    rev, rev_tag = got["revenue"]
    ocf, ocf_tag = got["ocf"]
    capex, capex_tag = got["capex"]
    shares, shares_tag = got["shares"]
    if not rev:
        sys.exit("No annual revenue concept found for %s in SEC XBRL." % symbol)
    if not ocf or not capex:
        sys.exit("No operating-cash-flow or capex concept found for %s. "
                 "Pass --fcf-margin and build from revenue instead." % symbol)
    if not shares:
        sys.exit("No diluted share count found for %s in SEC XBRL." % symbol)

    # Pair the last three years that have all three cash-flow facts.
    oc = dict(ocf)
    cx = dict(capex)
    rv = dict(rev)
    common = sorted(set(oc) & set(cx) & set(rv))[-3:]
    if len(common) < 1:
        sys.exit("SEC facts for %s do not line up by fiscal year across revenue, "
                 "operating cash flow, and capex." % symbol)
    rev_hist = [rv[d] for d in common][::-1]
    fcf_hist = [(oc[d] - cx[d]) for d in common][::-1]
    base_rev = rev_hist[0]
    margin = sum(f / r for f, r in zip(fcf_hist, rev_hist)) / len(fcf_hist)

    cash = (got["cash"][0] or [("", 0)])[-1][1] if got["cash"][0] else 0
    short_inv = (got["short_inv"][0] or [("", 0)])[-1][1] if got["short_inv"][0] else 0
    debt = 0
    for c in ("debt_nc", "debt_c"):
        series, _ = got[c]
        if series:
            # these are instantaneous: take the value at the latest balance date
            debt += series[-1][1]
    net_debt = debt - (cash + short_inv)
    shares_val = shares[-1][1]

    rf, rf_date = treasury_10y()
    note = ("inputs: SEC EDGAR XBRL 10-K, fiscal years %s; %s; %s; %s"
            % (", ".join(common), rev_tag, ocf_tag, capex_tag))
    if rf is not None:
        note += "; risk-free 10Y %.2f%% (%s)" % (rf * 100, rf_date)
        if wacc < rf:
            note += "  WARNING: your discount rate is below the risk-free rate"
    note += "; FCF = operating cash flow minus capex"

    print("\n%s (CIK %s) via SEC EDGAR, no API key." % (name, cik))
    print("  annual revenue   %s" % ["{:,.0f}".format(x) for x in rev_hist])
    print("  FCF history      %s  (margin %.1f%%)" % (
        ["{:,.0f}".format(x) for x in fcf_hist], margin * 100))
    print("  net debt         %s  (debt %s less cash and short-term investments %s)" % (
        "{:,.0f}".format(net_debt), "{:,.0f}".format(debt), "{:,.0f}".format(cash + short_inv)))
    print("  diluted shares   %s  (%s)" % ("{:,.0f}".format(shares_val), shares_tag))

    stream = [base_rev * (1 + 0.12) ** (i + 1) * margin for i in range(years)]
    report(symbol.upper(), "data.sec.gov (SEC EDGAR XBRL)",
           base_rev, margin, stream, wacc, tg, net_debt, shares_val, price, note=note)


def demo():
    """Offline check of the SEC path's parsing, no network."""
    gaap = {"Revenues": {"units": {"USD": [
        {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K", "val": 100.0},
        {"start": "2022-01-01", "end": "2022-12-31", "form": "10-K", "val": 90.0},
        {"start": "2023-04-01", "end": "2023-06-30", "form": "10-Q", "val": 40.0}]}}}
    series, tag = annual(gaap, "revenue")
    assert [v for _, v in series] == [90.0, 100.0], series      # quarterly dropped, oldest first
    assert tag == "Revenues"                                    # fallback tag used
    gaap2 = {"PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": [
        {"end": "2023-12-31", "form": "10-K", "val": 5.0}]}}}
    series2, _ = annual(gaap2, "capex")
    assert series2 == [("2023-12-31", 5.0)], series2            # instantaneous item kept
    print("SEC parsing verified offline: quarterly facts dropped, fallback tag used, "
          "instantaneous facts kept.\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", nargs="?", default=None)
    ap.add_argument("--wacc", type=float, default=0.09)
    ap.add_argument("--terminal-g", type=float, default=0.025)
    ap.add_argument("--years", type=int, default=5)
    ap.add_argument("--price", type=float, default=0.0)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        demo()
    elif a.symbol:
        run(a.symbol, a.wacc, a.terminal_g, a.years, a.price)
    else:
        ap.print_help()
