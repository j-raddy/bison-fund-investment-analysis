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
import argparse, datetime, getpass, json, os, re, shutil, sys, urllib.request

try:
    import select, termios, tty
except ImportError:          # Windows has no termios, so the prompts fall back to plain input
    termios = None

CONFIG = os.path.expanduser("~/.config/bison/config.json")
KEY_DIR = os.path.expanduser("~/.config/bison/keys")
UA = "bison-fund-setup/1.0 (contact: %s)" % os.environ.get("BISON_CONTACT", "student@example.edu")

SOURCES = [
    ("fmp", "Financial Modeling Prep", "needs an API key; free tier about 250 calls a day"),
    ("free", "SEC EDGAR plus US Treasury", "no key, nothing to install; filings, XBRL facts, risk-free rate"),
    ("other", "Another provider you already have a key for", "school-issued, Finnhub, Alpha Vantage, Polygon, Tiingo, EODHD, Twelve Data"),
    ("bloomberg", "Bloomberg Terminal", "only if you have a logged-in terminal with entitlements"),
]

# The closing line for each source, and the model script to point at (None: none).
CLOSING = {
    "fmp": ("Set the source. Start a pitch with:", "fmp_dcf.py"),
    "free": ("Set to the keyless path (SEC EDGAR and Treasury). Start a pitch with:", "sec_fundamentals.py"),
    "other": ("Recorded. Start a pitch with:", None),
    "bloomberg": ("Recorded. Start a pitch with:", None),
}


def raw_supported():
    """True when the prompts can read keystrokes directly."""
    return termios is not None and sys.stdin.isatty() and sys.stdout.isatty()


class Terminal:
    """Prompt input on a real terminal.

    Keystrokes arrive one at a time with echo off (cbreak mode), held for as long
    as this is open. Nothing typed can appear on screen, because the mode is set
    once up front rather than around each keystroke. Output translation stays on,
    so ordinary print() still works. Without a usable terminal it falls back to
    plain input and getpass, which keeps piped and Windows use working.
    """

    def __init__(self):
        self.capable = raw_supported()
        self.fd = sys.stdin.fileno() if self.capable else None
        self.saved = None

    def __enter__(self):
        if self.capable:
            self.saved = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
            self.write("\033[?2004l")        # bracketed paste off, so a paste arrives bare
        return self

    def __exit__(self, *_exc):
        if self.capable:
            self.write("\033[?2004h")
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.saved)
        return False

    @staticmethod
    def write(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def _byte(self):
        """One byte from the terminal, bypassing Python's buffered stdin."""
        return os.read(self.fd, 1).decode("utf-8", "replace")

    def key(self):
        """One keypress: 'up', 'down', 'enter', 'backspace', or the character.

        Reads the descriptor directly. sys.stdin is buffered, so it can swallow
        the rest of an escape sequence out of the kernel buffer, leaving select()
        with nothing to report and the arrow key silently ignored.
        """
        ch = self._byte()
        if ch == "\x1b":
            ready, _, _ = select.select([self.fd], [], [], 0.05)
            seq = (self._byte() + self._byte()) if ready else ""
            return {"[A": "up", "[B": "down"}.get(seq, "other")
        if ch in ("\r", "\n"):
            return "enter"
        if ch in ("\x7f", "\x08"):
            return "backspace"
        return ch

    def line(self, prompt, secret=False):
        """Read a line, echoing one asterisk per character when it is a secret.

        cbreak mode turns echo off, so this echoes the characters itself and
        handles the backspace key.
        """
        if not self.capable:
            try:
                return (getpass.getpass(prompt) if secret else input(prompt)).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                sys.exit("No input. Nothing changed.")
        self.write(prompt)
        chars = []
        while True:
            key = self.key()
            if key == "enter":
                break
            if key == "backspace":
                if chars:
                    chars.pop()
                    self.write("\b \b")
                continue
            if len(key) == 1 and key.isprintable():
                chars.append(key)
                self.write("*" if secret else key)
        print()
        text = "".join(chars)
        return sanitize_key(text) if secret else text.strip()


def sanitize_key(text):
    """Keep only the key itself.

    A paste can arrive wrapped in bracketed-paste markers (ESC [ 200 ~ ... ESC [ 201 ~).
    The prompt turns that mode off, but terminals differ, so strip the markers too.
    Keys are alphanumeric, so dropping everything unprintable is safe.
    """
    text = re.sub(r"\x1b\[20[01]~", "", text)
    return "".join(c for c in text if c.isprintable() and c != "\x1b").strip()


def read_config():
    if os.path.exists(CONFIG):
        try:
            with open(CONFIG) as f:
                return json.load(f)
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
    os.chmod(path, 0o600)
    return path


def stored_key(name):
    path = os.path.join(KEY_DIR, "%s.key" % name)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return ""


def http(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()


def verify_fmp(key):
    body = http("https://financialmodelingprep.com/stable/quote?symbol=AAPL&apikey=%s" % key)
    data = json.loads(body)
    if isinstance(data, dict) and data.get("error-message"):
        raise RuntimeError(str(data["error-message"])[:120])
    row = data[0] if isinstance(data, list) and data else data
    price = row.get("price") if isinstance(row, dict) else None
    return "AAPL quoted at %s" % price


def verify_free():
    http("https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", timeout=45)
    year = datetime.date.today().year
    http("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
         "daily-treasury-rates.csv/%d/all?type=daily_treasury_yield_curve"
         "&field_tdr_date_value=%d&page&_format=csv" % (year, year), timeout=45)
    return "SEC EDGAR and the Treasury yield curve both answered"


def detect():
    """What this machine already has. Key values are never shown, only presence."""
    found = []
    if os.environ.get("FMP_API_KEY"):
        found.append("$FMP_API_KEY is set")
    cfg = read_config()
    for name in sorted(cfg.get("keys", {})):
        found.append("a key is stored for %s" % name)
    for legacy in ("~/.hermes/secrets/fmp_api_key", "~/.config/fmp/api_key"):
        if os.path.exists(os.path.expanduser(legacy)):
            found.append("a key file exists at %s" % legacy)
    if cfg.get("provider"):
        found.append("a data-source config already exists (using %s)" % cfg["provider"])
    return found


def readiness():
    """Per source: what is already here, and whether it would work right now.

    A key that is present is checked with one live call, so this says whether the
    source works rather than that a key merely exists. None means nothing is known,
    and the menu falls back to its own description of the source.
    """
    state = {"free": "ready, needs nothing"}
    env_key = os.environ.get("FMP_API_KEY")
    fmp_key = env_key or stored_key("fmp")
    if fmp_key:
        where = "$FMP_API_KEY" if env_key else "the stored FMP key"
        try:
            verify_fmp(fmp_key)
            state["fmp"] = "ready, %s works" % where
        except Exception as e:
            state["fmp"] = "%s was refused just now (%s)" % (where, str(e)[:60])
    else:
        state["fmp"] = None
    others = sorted(n for n in read_config().get("keys", {}) if n != "fmp")
    state["other"] = ("keys stored: %s" % ", ".join(others)) if others else None
    state["bloomberg"] = None
    return state


def menu_rows(state):
    """The menu rows: what was detected, or the description when nothing is known."""
    return [(label, state.get(key) or blurb) for key, label, blurb in SOURCES]


def check():
    print("\nBison Fund data source: what this machine has\n")
    found = detect()
    print("\n".join("  - " + f for f in found) if found else "  - nothing yet")
    print("\nRun `python3 setup.py` to configure a source.\n")


def menu_line(i, label, blurb, width, active=False, final=False):
    """One rendered line of the menu.

    Capped to the terminal width, because the redraw works by moving the cursor up
    as many lines as it drew. A row that wraps to a second line breaks that count,
    and the menu then walks down the screen instead of redrawing in place.
    """
    mark = ("\033[7m>\033[0m" if not final else ">") if active else " "
    body = "%d) %-44s %s" % (i, label, blurb)
    # Cap the visible text, not the whole string: the highlight escape occupies no
    # columns, and truncating it mid-sequence would leak its tail onto the screen.
    # One marker, two spaces, one spare column: the row cannot reach the width.
    room = max(1, width - 4)
    return mark + "  " + body[:room]


def choose(title, options, term, default=0):
    """Pick one of the options, returning a 1-based choice.

    Arrow keys when the terminal allows it, otherwise typing a number, so piped
    and Windows use still works.
    """
    if not term.capable:
        print(title)
        for i, (label, blurb) in enumerate(options, 1):
            print("  %d) %-44s %s" % (i, label, blurb))
        try:
            n = int(term.line("Number [%d]: " % (default + 1)) or str(default + 1))
        except ValueError:
            sys.exit("Not a number from the list. Nothing changed.")
        if not 1 <= n <= len(options):
            sys.exit("Pick a number from 1 to %d. Nothing changed." % len(options))
        return n

    idx = default
    drawn = 0

    width = shutil.get_terminal_size((100, 24)).columns

    def draw(final=False):
        nonlocal drawn
        if drawn:
            sys.stdout.write("\033[%dA" % drawn)
        for i, (label, blurb) in enumerate(options, 1):
            line = menu_line(i, label, blurb, width, active=(i - 1 == idx), final=final)
            sys.stdout.write("\033[2K%s\n" % line)
        drawn = len(options)
        sys.stdout.flush()

    print(title)
    draw()
    while True:
        key = term.key()
        if key == "up":
            idx = (idx - 1) % len(options)
            draw()
        elif key == "down":
            idx = (idx + 1) % len(options)
            draw()
        elif key == "enter":
            draw(final=True)
            return idx + 1
        elif key.isdigit() and 1 <= int(key) <= len(options):
            idx = int(key) - 1
            draw(final=True)
            return idx + 1


def interact(term):
    print("\nBison Fund data source setup\n" + "-" * 29)
    for line in detect() or ["nothing found yet"]:
        print("  " + line)
    state = readiness()
    n = choose("\nWhich source do you want to use?   (arrow keys, or type a number)",
               menu_rows(state), term)
    key, label, _blurb = SOURCES[n - 1]

    cfg = read_config()
    cfg.setdefault("keys", {})

    if key == "fmp":
        existing = os.environ.get("FMP_API_KEY") or stored_key("fmp")
        if existing:
            print("  %s. Press Enter to keep it, or paste a new one."
                  % (state.get("fmp") or "An FMP key is already here"))
        value = term.line("Paste your FMP API key (hidden): ", secret=True) or existing
        if not value:
            sys.exit("No key given. Use option 2 for the keyless path. Nothing changed.")
        cfg["keys"]["fmp"] = {"file": store_key("fmp", value), "verified": False}
        print("  checking key against an AAPL quote ...")
        try:
            print("  " + verify_fmp(value))
            cfg["keys"]["fmp"]["verified"] = True
        except Exception as e:
            print("  that key did not work: %s" % str(e)[:120])
            print("  Keeping it, but the keyless path (option 2) works right now if you need it.")

    elif key == "free":
        print("  checking SEC EDGAR and the Treasury ...")
        try:
            print("  " + verify_free())
        except Exception as e:
            print("  could not reach a free source: %s" % str(e)[:120])

    elif key == "other":
        name = term.line("Provider name (for example finnhub, capitaliq, school-issued): ").lower()
        if not name:
            sys.exit("No provider name given. Nothing changed.")
        value = term.line("Paste the %s key (hidden): " % name, secret=True)
        if not value:
            sys.exit("No key given. Nothing changed.")
        cfg["keys"][name] = {"file": store_key(name, value), "verified": False}
        print("  stored, not verified: setup only knows how to test FMP and the free "
              "sources, so a human should confirm this key works")

    else:  # bloomberg
        print("  recorded. The terminal path needs a logged-in machine with entitlements; "
              "see the dcf-model skill. Nothing to store.")

    cfg["provider"] = key
    cfg["configured_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    write_config(cfg)

    opener, model = CLOSING[key]
    print("\nWrote data-source config to %s" % CONFIG)
    print(opener)
    print('  "I want to research <COMPANY> (<TICKER>)" using the '
          "bison-fund-investment-analysis skill, starting at Phase 0.")
    if model:
        print("\nFor the model:  python3 skills/dcf-model/scripts/%s <TICKER>" % model)
    print()
    return 0


def main():
    if not sys.stdin.isatty():
        print("No terminal to prompt in. Run this interactively, or set one of:\n"
              "  $FMP_API_KEY                 (Financial Modeling Prep)\n"
              "  nothing at all                (SEC EDGAR and Treasury need no key)\n"
              "Config is written to %s" % CONFIG)
        return 0
    try:
        with Terminal() as term:
            return interact(term)
    except KeyboardInterrupt:
        print("\nCancelled. Nothing changed.")
        return 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Set up a market-data source for the Bison Fund investment-analysis skill.")
    ap.add_argument("--check", action="store_true",
                    help="report what this machine already has, and change nothing")
    a = ap.parse_args()
    sys.exit(check() if a.check else main())
