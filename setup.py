#!/usr/bin/env python3
"""Set up a market-data source for the Bison Fund investment-analysis skill.

Run once in a terminal after installing the skill:

    python3 setup.py            # pick a source, add your key, verify it
    python3 setup.py --check    # report what this machine already has

It finds what is already here, asks which source to use, takes your own API key if
that source needs one, proves the choice with one live call, and records it in
~/.config/bison/config.json so the skills do not have to guess.

Your key is never printed back. It is stored at ~/.config/bison/keys/<name>.key,
readable only by you (chmod 600). Re-run this any time to add another key or switch
the source; existing keys are kept.

No key at all is a valid answer: option 2 uses SEC EDGAR and the US Treasury, which
need nothing, and the DCF can still be built.
"""
import getpass, json, os, stat, sys, urllib.request

CONFIG = os.path.expanduser("~/.config/bison/config.json")
KEY_DIR = os.path.expanduser("~/.config/bison/keys")
UA = "bison-fund-setup/1.0 (contact: %s)" % os.environ.get("BISON_CONTACT", "student@example.edu")

SOURCES = [
    ("fmp", "Financial Modeling Prep", "needs an API key; free tier about 250 calls a day", True),
    ("free", "SEC EDGAR plus US Treasury", "no key, nothing to install; filings, XBRL facts, risk-free rate", False),
    ("other", "Another provider you already have a key for", "school-issued, Finnhub, Alpha Vantage, Polygon, Tiingo, EODHD, Twelve Data", True),
    ("bloomberg", "Bloomberg Terminal", "only if you have a logged-in terminal with entitlements", False),
]


def read_config():
    if os.path.exists(CONFIG):
        try:
            return json.load(open(CONFIG))
        except ValueError:
            return {}
    return {}


def write_config(cfg):
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=2, sort_keys=True)
        f.write("\n")


def store_key(name, value):
    """Write a key readable only by its owner. Never echoes it."""
    os.makedirs(KEY_DIR, exist_ok=True)
    path = os.path.join(KEY_DIR, "%s.key" % name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(value.strip() + "\n")
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    return path


def stored_key(name):
    path = os.path.join(KEY_DIR, "%s.key" % name)
    if os.path.exists(path):
        return open(path).read().strip()
    return ""


def http(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode()


def verify_fmp(key):
    _, body = http("https://financialmodelingprep.com/stable/quote?symbol=AAPL&apikey=%s" % key)
    data = json.loads(body)
    if isinstance(data, dict) and data.get("error-message"):
        raise RuntimeError(str(data["error-message"])[:120])
    row = data[0] if isinstance(data, list) and data else data
    price = row.get("price") if isinstance(row, dict) else None
    return "AAPL quoted at %s" % price


def verify_free():
    http("https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", timeout=45)
    year = __import__("datetime").date.today().year
    http("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
         "daily-treasury-rates.csv/%d/all?type=daily_treasury_yield_curve"
         "&field_tdr_date_value=%d&page&_format=csv" % (year, year), timeout=45)
    return "SEC EDGAR and the Treasury yield curve both answered"


def detect():
    """What this machine already has. Values are never shown, only presence."""
    found = []
    if os.environ.get("FMP_API_KEY"):
        found.append("$FMP_API_KEY is set")
    if stored_key("fmp"):
        found.append("an FMP key is stored at %s" % os.path.join(KEY_DIR, "fmp.key"))
    for legacy in ("~/.hermes/secrets/fmp_api_key", "~/.config/fmp/api_key"):
        if os.path.exists(os.path.expanduser(legacy)):
            found.append("a key file exists at %s" % legacy)
    cfg = read_config()
    if cfg.get("provider"):
        found.append("a data-source config already exists (using %s)" % cfg["provider"])
    if cfg.get("keys"):
        found.append("stored keys: %s" % ", ".join(sorted(cfg["keys"])))
    return found


def check():
    print("\nBison Fund data source: what this machine has\n")
    found = detect()
    print("\n".join("  - " + f for f in found) if found else "  - nothing yet")
    print("\nRun `python3 setup.py` to configure a source.\n")


def ask(question, default=None):
    suffix = " [%s]" % default if default else ""
    try:
        answer = input("%s%s: " % (question, suffix)).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit("No input. Nothing changed.")
    return answer or default or ""


def main():
    if not sys.stdin.isatty():
        print("No terminal to prompt in. Run this interactively, or set one of:\n"
              "  $FMP_API_KEY                 (Financial Modeling Prep)\n"
              "  nothing at all                (SEC EDGAR and Treasury need no key)\n"
              "Config is written to %s" % CONFIG)
        return 0

    print("\nBison Fund data source setup\n" + "-" * 29)
    for line in detect() or ["nothing found yet"]:
        print("  " + line)
    print("\nWhich source do you want to use?")
    for i, (key, label, blurb, _needs) in enumerate(SOURCES, 1):
        print("  %d) %-44s %s" % (i, label, blurb))
    choice = ask("Number", "1")
    try:
        key, label, _blurb, needs_key = SOURCES[int(choice) - 1]
    except (ValueError, IndexError):
        sys.exit("Not a number from the list. Nothing changed.")

    cfg = read_config()
    cfg.setdefault("keys", {})
    verified = False
    shown = False
    detail = ""

    if key == "fmp":
        existing = os.environ.get("FMP_API_KEY") or stored_key("fmp")
        if existing:
            print("An FMP key is already here. Blank keeps it, or paste a different one.")
        try:
            value = getpass.getpass("Paste your FMP API key (hidden): ").strip() or existing
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit("No input. Nothing changed.")
        if not value:
            sys.exit("No key given. Use option 2 for the keyless path. Nothing changed.")
        path = store_key("fmp", value)
        cfg["keys"]["fmp"] = {"file": path, "verified": False}
        print("  checking key against an AAPL quote ...")
        try:
            detail = verify_fmp(value)
            verified = True
            cfg["keys"]["fmp"]["verified"] = True
        except Exception as e:
            detail = "that key did not work: %s" % str(e)[:120]
            shown = True
            print("  " + detail)
            print("  Keeping it, but the keyless path (option 2) works right now if you need it.")

    elif key == "free":
        print("  checking SEC EDGAR and the Treasury ...")
        try:
            detail = verify_free()
            verified = True
            shown = True
            print("  " + detail)
        except Exception as e:
            detail = "could not reach a free source: %s" % str(e)[:120]
            shown = True
            print("  " + detail)

    elif key == "other":
        cfg.setdefault("providers", [])
        name = ask("Provider name (for example finnhub, capitaliq, school-issued)").lower()
        if not name:
            sys.exit("No provider name given. Nothing changed.")
        try:
            value = getpass.getpass("Paste the %s key (hidden): " % name).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit("No input. Nothing changed.")
        if not value:
            sys.exit("No key given. Nothing changed.")
        path = store_key(name, value)
        cfg["keys"][name] = {"file": path, "verified": False}
        if name not in cfg["providers"]:
            cfg["providers"].append(name)
        detail = ("stored, not verified: setup only knows how to test FMP and the free "
                  "sources, so a human should confirm this key works")

    else:  # bloomberg
        detail = ("recorded. The terminal path needs a logged-in machine with entitlements; "
                  "see the dcf-model skill. Nothing to store.")
        print("  " + detail)

    cfg["provider"] = key
    cfg["provider_label"] = label
    cfg["last_source_supports_keys"] = needs_key
    cfg["configured_at"] = __import__("datetime").datetime.now().isoformat(timespec="seconds")
    write_config(cfg)

    if key != "bloomberg" and not shown:
        print("  %s" % detail)
    print("\nWrote data-source config to %s" % CONFIG)
    if needs_key and verified:
        print("Set the source. Start a pitch with:")
    elif key == "free":
        print("Set to the keyless path (SEC EDGAR and Treasury). Start a pitch with:")
    else:
        print("Recorded. Start a pitch with:")
    print('  "I want to research <COMPANY> (<TICKER>)" using the '
          "bison-fund-investment-analysis skill, starting at Phase 0.")
    if key == "free":
        print("\nFor the model:  python3 skills/dcf-model/scripts/sec_fundamentals.py <TICKER>")
    elif key == "fmp":
        print("\nFor the model:  python3 skills/dcf-model/scripts/fmp_dcf.py <TICKER>")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main() if "--check" not in sys.argv else check())
