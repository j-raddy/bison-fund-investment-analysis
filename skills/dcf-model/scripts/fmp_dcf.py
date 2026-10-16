#!/usr/bin/env python3
"""Build a DCF from FMP data, the Bison Fund way.

Usage:
  python3 fmp_dcf.py UBER                 # live: pulls from FMP, builds the model
  python3 fmp_dcf.py --demo               # offline: runs the same math on canned inputs

Options:
  --wacc 0.09            discount rate (analyst's call; default 0.09)
  --terminal-g 0.025     terminal growth (must be < long-run nominal GDP)
  --fcf-margin 0.30      FCF margin of revenue (default: trailing 3-year average)
  --years 5              forecast horizon

The API key is read from $FMP_API_KEY, else a secrets file (~/.hermes/secrets/fmp_api_key or
~/.config/fmp/api_key), and is never printed.
Endpoint paths come from references/fmp-api-docs.md (the official api-docs.md). Only the
stable API exists now; legacy v3/v4 paths are discontinued.
Every model output is an estimate. The price target is the analyst's, not this script's.
"""
import argparse, json, os, sys

try:
    import urllib.request, urllib.parse
except ImportError:
    sys.exit("python 3 required")


def load_key():
    """Read the FMP key at runtime. Handles a bare key file or a VAR=... wrapper line,
    and both the documented path and a dotfile variant. Never prints the key."""
    key = os.environ.get("FMP_API_KEY", "")
    if not key:
        for p in ("~/.hermes/secrets/fmp_api_key", "~/.hermes/secrets/.fmp_api_key",
                  "~/.config/fmp/api_key"):
            fp = os.path.expanduser(p)
            if os.path.exists(fp):
                with open(fp) as fh:
                    key = fh.read().strip()
                break
    key = key.strip()
    if "=" in key and key.split("=", 1)[0].strip().upper().endswith("API_KEY"):
        key = key.split("=", 1)[1].strip()
    return key


def get(key, path, **params):
    """GET from FMP's stable API. Legacy v3/v4 paths are discontinued. Never prints the key."""
    url = "https://financialmodelingprep.com/" + path
    try:
        req = urllib.request.Request(url + ("&" if "?" in url else "?") + "apikey=" + key)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        if isinstance(data, dict) and data.get("error-message"):
            raise RuntimeError(str(data.get("error-message"))[:120])
        return data, url.split("?")[0]
    except Exception as e:
        raise RuntimeError("FMP request failed: %s" % str(e)[:120])


def dcf(fcf_stream, wacc, terminal_g, net_debt, shares):
    """Core math. Returns dict; pure, so it can be tested offline."""
    pv = sum(f / (1 + wacc) ** (i + 1) for i, f in enumerate(fcf_stream))
    final = fcf_stream[-1]
    tv = final * (1 + terminal_g) / (wacc - terminal_g)
    pv_tv = tv / (1 + wacc) ** len(fcf_stream)
    ev = pv + pv_tv
    equity = ev + net_debt
    return {"pv_fcf": pv, "terminal_value": tv, "pv_terminal": pv_tv,
            "enterprise_value": ev, "equity_value": equity, "per_share": equity / shares,
            "tv_share": pv_tv / ev}


def grid(fcf_base, waccs, gs, net_debt, shares):
    """Sensitivity: value per share across WACC x terminal growth."""
    out = {}
    for w in waccs:
        row = []
        for g in gs:
            stream = [fcf_base * (1 + g * 4) ** (i + 1) for i in range(5)]
            row.append(round(dcf(stream, w, g, net_debt, shares)["per_share"], 2))
        out["%.2f" % w] = row
    return out


def run(symbol, wacc, tg, fcf_margin, years):
    key = load_key()
    if not key:
        sys.exit("No FMP key. Set $FMP_API_KEY, or store it (chmod 600) at "
                 "~/.hermes/secrets/fmp_api_key or ~/.config/fmp/api_key.")
    quote, src = get(key, "stable/quote?symbol=%s" % symbol)
    q = quote[0] if isinstance(quote, list) and quote else quote
    cf, _ = get(key, "stable/cash-flow-statement?symbol=%s&period=annual&limit=3" % symbol)
    inc, _ = get(key, "stable/income-statement?symbol=%s&period=annual&limit=3" % symbol)
    bs, _ = get(key, "stable/balance-sheet-statement?symbol=%s&period=annual&limit=1" % symbol)
    rev_hist = [float(r.get("revenue", 0)) for r in (inc if isinstance(inc, list) else [])]
    fcf_hist = []
    for r in (cf if isinstance(cf, list) else []):
        fcf_hist.append(float(r.get("operatingCashFlow", 0)) - float(r.get("capitalExpenditure", 0)))
    if not fcf_hist:
        fcf_hist = [rev_hist[0] * fcf_margin]
    margin = fcf_margin if fcf_margin else sum(f / r for f, r in zip(fcf_hist, rev_hist)) / len(fcf_hist)
    b = (bs[0] if isinstance(bs, list) else bs)
    net_debt = (float(b.get("totalDebt", 0)) - float(b.get("cashAndShortTermInvestments", 0)))
    shares = float((inc[0] if isinstance(inc, list) else inc).get("weightedAverageShsOutDil", 0)
                   or (inc[0] if isinstance(inc, list) else inc).get("weightedAverageShsDil", 0))
    base_rev = rev_hist[0]
    stream = [base_rev * (1 + 0.12) ** (i + 1) * margin for i in range(years)]
    r = dcf(stream, wacc, tg, -net_debt if net_debt else 0, shares)
    try:
        fmp_dcf, _ = get(key, "stable/discounted-cash-flow?symbol=%s" % symbol)
        x = fmp_dcf[0] if isinstance(fmp_dcf, list) and fmp_dcf else fmp_dcf
        cross = x.get("dcf")
    except Exception:
        cross = None
    print("\nDCF build for %s (source: %s)" % (symbol, src))
    print("  revenue base      %s" % "{:,.0f}".format(base_rev))
    print("  FCF margin used   %.1f%%" % (margin * 100))
    print("  projected FCF     %s" % ["{:,.0f}".format(f) for f in stream])
    print("  WACC / terminal g %.2f%% / %.2f%%" % (wacc * 100, tg * 100))
    print("  PV of FCF         %s" % "{:,.0f}".format(r["pv_fcf"]))
    print("  terminal value    %s (PV %s, %.0f%% of EV)" % (
        "{:,.0f}".format(r["terminal_value"]), "{:,.0f}".format(r["pv_terminal"]), r["tv_share"] * 100))
    print("  enterprise value  %s" % "{:,.0f}".format(r["enterprise_value"]))
    print("  equity value      %s" % "{:,.0f}".format(r["equity_value"]))
    print("  per share         %s" % "{:,.2f}".format(r["per_share"]))
    if cross:
        print("  FMP's own DCF     %s (cross-check only)" % "{:,.2f}".format(float(cross)))
    print("\nSensitivity, value per share (WACC rows, terminal growth cols):")
    g = grid(fcf_hist[0] * margin, [wacc - 0.02, wacc, wacc + 0.02], [tg - 0.01, tg, tg + 0.01],
             -net_debt if net_debt else 0, shares)
    print("        " + "".join("%9s" % c for c in g.keys()))
    for w, row in g.items():
        print("  %5s" % w + "".join("%9s" % x for x in row))
    print("\nThe price target is yours. This model is an input, not an answer.\n")


def demo():
    """Offline check of the math with canned inputs."""
    stream = [100, 115, 130, 145, 160]
    r = dcf(stream, 0.09, 0.025, 500, 100)
    assert abs(r["terminal_value"] - 160 * 1.025 / (0.09 - 0.025)) < 1
    assert r["per_share"] > 0 and 0 < r["tv_share"] < 1
    print("\nDemo DCF (canned inputs, FCF 100..160, WACC 9%, g 2.5%):")
    for k in ("pv_fcf", "terminal_value", "enterprise_value", "equity_value", "per_share", "tv_share"):
        print("  %-17s %s" % (k, round(r[k], 2)))
    print("  math verified\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", nargs="?", default=None)
    ap.add_argument("--wacc", type=float, default=0.09)
    ap.add_argument("--terminal-g", type=float, default=0.025)
    ap.add_argument("--fcf-margin", type=float, default=None)
    ap.add_argument("--years", type=int, default=5)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        demo()
    elif a.symbol:
        run(a.symbol.upper(), a.wacc, a.terminal_g, a.fcf_margin, a.years)
    else:
        ap.print_help()
