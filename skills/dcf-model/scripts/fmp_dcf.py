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

The API key is read from $FMP_API_KEY, else the file setup.py writes
(~/.config/bison/keys/fmp.key), else a legacy path (~/.hermes/secrets/fmp_api_key or
~/.config/fmp/api_key). Never printed.
No key? Run `python3 setup.py` once, or use the keyless path: sec_fundamentals.py.
Endpoint paths and field names come from references/fmp-api-docs.md (a cheatsheet of the
calls this script makes, linked to FMP's full current docs). Only the stable API exists now;
legacy v3/v4 paths are discontinued.
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
        for p in ("~/.config/bison/keys/fmp.key", "~/.config/bison/fmp_api_key",
                  "~/.hermes/secrets/fmp_api_key", "~/.hermes/secrets/.fmp_api_key",
                  "~/.config/fmp/api_key"):
            fp = os.path.expanduser(p)
            if os.path.exists(fp):
                key = open(fp).read().strip()
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


def reverse_g(stream, wacc, net_debt, shares, price):
    """Terminal growth the current price implies, solving the model backwards.

    market value = PV(free cash flows) + PV(terminal value) + net_debt_passed.
    Solve the Gordon term for g. Returns None when the price supports no finite
    positive terminal value.
    """
    pv_fcf = dcf(stream, wacc, 0.0, 0, shares)["pv_fcf"]
    fcf_n = stream[-1]
    tv_pv = price * shares - pv_fcf - net_debt
    tv = tv_pv * (1 + wacc) ** len(stream)
    if tv <= 0 or abs(fcf_n + tv) < 1e-9:
        return None
    return (tv * wacc - fcf_n) / (fcf_n + tv)


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


def grid(stream, waccs, gs, net_debt, shares):
    """Sensitivity: value per share across WACC x terminal growth.

    The projected FCF stream is fixed -- it does not change with the discount
    rate or the terminal growth. Only the discounting and the terminal value
    vary, so the grid's center cell equals the headline per-share value.
    """
    out = {}
    for w in waccs:
        row = []
        for g in gs:
            row.append(round(dcf(stream, w, g, net_debt, shares)["per_share"], 2))
        out["%.2f" % w] = row
    return out


def report(symbol, src, base_rev, margin, stream, wacc, tg, net_debt, shares, price,
           cross=None, note=None):
    """Print the model record, the grid, and the reverse DCF.

    Shared by the FMP path (`run`) and the keyless SEC path (`sec_fundamentals.py`),
    so the two sources cannot print different-looking models.
    """
    nd = -net_debt if net_debt else 0
    r = dcf(stream, wacc, tg, nd, shares)
    implied_g = reverse_g(stream, wacc, nd, shares, price) if price else None
    print("\nDCF build for %s (source: %s)" % (symbol, src))
    if note:
        print("  %s" % note)
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
    if implied_g is not None:
        print("  implied terminal growth at the current price  %.2f%%  (reverse DCF, cross-check only)"
              % (implied_g * 100))
    print("\nSensitivity, value per share (WACC rows, terminal growth cols):")
    g = grid(stream, [wacc - 0.02, wacc, wacc + 0.02], [tg - 0.01, tg, tg + 0.01], nd, shares)
    print("        " + "".join("%9s" % c for c in g.keys()))
    for w, row in g.items():
        print("  %5s" % w + "".join("%9s" % x for x in row))
    print("\nThe price target is yours. This model is an input, not an answer.\n")
    return r


def run(symbol, wacc, tg, fcf_margin, years):
    if tg >= wacc:
        sys.exit("Terminal growth (%.0f%%) must stay below the discount rate (%.0f%%)."
                 % (tg * 100, wacc * 100))
    key = load_key()
    if not key:
        sys.exit("No FMP key. Run `python3 setup.py` to set one up, or use the keyless "
                 "SEC path: python3 sec_fundamentals.py %s" % symbol)
    try:
        quote, src = get(key, "stable/quote?symbol=%s" % symbol)
    except RuntimeError as e:
        sys.exit("FMP rejected the call with the stored key: %s\n"
                 "Fix the key with `python3 setup.py`, or use the keyless path: "
                 "python3 sec_fundamentals.py %s" % (str(e)[:120], symbol))
    q = quote[0] if isinstance(quote, list) and quote else quote
    price = float((q or {}).get("price") or 0)
    cf, _ = get(key, "stable/cash-flow-statement?symbol=%s&period=annual&limit=3" % symbol)
    inc, _ = get(key, "stable/income-statement?symbol=%s&period=annual&limit=3" % symbol)
    bs, _ = get(key, "stable/balance-sheet-statement?symbol=%s&period=annual&limit=1" % symbol)
    rev_hist = [float(r.get("revenue", 0)) for r in (inc if isinstance(inc, list) else [])]
    if not rev_hist:
        sys.exit("No income-statement revenue returned for %s. The model needs it." % symbol)
    fcf_hist = []
    for r in (cf if isinstance(cf, list) else []):
        fcf_hist.append(float(r.get("operatingCashFlow", 0)) - float(r.get("capitalExpenditure", 0)))
    if not fcf_hist:
        if fcf_margin is None:
            sys.exit("No cash-flow history for %s and no --fcf-margin given. "
                     "Pass --fcf-margin to build from revenue instead." % symbol)
        fcf_hist = [rev_hist[0] * fcf_margin]
    margin = fcf_margin if fcf_margin else sum(f / r for f, r in zip(fcf_hist, rev_hist)) / len(fcf_hist)
    b = (bs[0] if isinstance(bs, list) else bs)
    net_debt = (float(b.get("totalDebt", 0)) - float(b.get("cashAndShortTermInvestments", 0)))
    shares = float((inc[0] if isinstance(inc, list) else inc).get("weightedAverageShsOutDil", 0) or 0)
    if not shares:
        sys.exit("No diluted share count in the income statement for %s. The model needs it." % symbol)
    base_rev = rev_hist[0]
    stream = [base_rev * (1 + 0.12) ** (i + 1) * margin for i in range(years)]
    try:
        fmp_dcf, _ = get(key, "stable/discounted-cash-flow?symbol=%s" % symbol)
        x = fmp_dcf[0] if isinstance(fmp_dcf, list) and fmp_dcf else fmp_dcf
        cross = x.get("dcf")
    except Exception:
        cross = None
    report(symbol, src, base_rev, margin, stream, wacc, tg, net_debt, shares, price, cross,
           note="inputs: Financial Modeling Prep, stable API")


def demo():
    """Offline check of the math with canned inputs."""
    stream = [100, 115, 130, 145, 160]
    r = dcf(stream, 0.09, 0.025, 500, 100)
    assert abs(r["terminal_value"] - 160 * 1.025 / (0.09 - 0.025)) < 1
    assert r["per_share"] > 0 and 0 < r["tv_share"] < 1
    g = grid(stream, [0.09], [0.025], 500, 100)
    assert abs(g["0.09"][0] - r["per_share"]) < 0.01, "grid center cell must equal per_share"
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
