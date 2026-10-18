---
name: dcf-model
description: "Use when valuing a company with the fund's discounted cash flow: building the model, running the script, or pulling market data."
author: Jacob Radke
license: MIT
---

# DCF Model

The fund's valuation method. The analyst owns the discount rate, the terminal growth, and the final
number; this skill produces the inputs, the mechanics, and the sensitivity, and never the price
target.

## Triggers

- The hub routes Phase 4 Valuation here, or a request names the model directly ("run the DCF").
- An analyst needs the implied value, the sensitivity range, or a reverse DCF on a traded price.

## Prerequisites

- Python 3 with the standard library only. Nothing to install.
- Network access for a live run. `--demo` needs none.
- A data source, chosen once with `python3 setup.py`. `scripts/sec_fundamentals.py` needs no key at
  all, so a machine with nothing configured still builds the model; `scripts/fmp_dcf.py` needs an FMP
  key of your own, which setup stores at `~/.config/bison/keys/fmp.key`. Both scripts read the key at
  runtime and never print it.
- The analyst's discount rate and terminal growth, because those are the analyst's calls.

## Inputs

- Ticker and the latest filings.
- Current price, diluted shares, net debt, and free cash flow history.
- Market data access: Financial Modeling Prep for the automatable path, a Bloomberg Terminal for
  analysts who have entitlements.
- The analyst's discount rate and terminal growth assumptions.

## Method

The full build guide is `references/dcf-method.md`: inputs, the discount rate via CAPM, terminal
value, the bridge from enterprise to equity value, the sensitivity grid, and the checks. Follow it
rather than reconstructing the method from memory.

The working implementation is `scripts/fmp_dcf.py`, standard library only:

```bash
python3 scripts/fmp_dcf.py --demo        # canned inputs, no key, verifies the math offline
python3 scripts/fmp_dcf.py UBER          # live, pulls from FMP and builds the model
python3 scripts/fmp_dcf.py UBER --wacc 0.09 --terminal-g 0.025 --years 5
```

Run the demo once on a new machine before trusting a live run.

## Market data

**Financial Modeling Prep.** Keys are per analyst and read at runtime, never hardcoded in a skill
file, deck, template, or handout, and never pasted into a chat transcript. `setup.py` stores the key at
`~/.config/bison/keys/fmp.key`; the script reads `$FMP_API_KEY` first, then that file, then the older
paths (`~/.hermes/secrets/fmp_api_key`, its dotfile variant `~/.hermes/secrets/.fmp_api_key`, and
`~/.config/fmp/api_key`), and it strips a leading `VAR=` wrapper line if the file holds one. It prints
only success or failure. A shared fund-wide key will hit the free-tier rate limit of roughly 250 calls
a day, so plan for one key per student. The endpoint cheatsheet is `references/fmp-api-docs.md`, with a
link to FMP's full current docs for anything beyond the calls this package makes.

**Bloomberg Terminal.** There is no public or free Bloomberg market-data API. The programming
interface, the Python wrappers, and the Excel functions all require a logged-in terminal and
entitlements on the calling machine. `references/bloomberg-terminal.md` covers the three routes in,
the mnemonics to pull for each model input, and the redistribution rule: terminal data is licensed to
the subscriber for internal use, so cite the filing or a public source in anything the fund
distributes. Never store a Bloomberg login or session token anywhere.

## Set up a source, and the keyless path

`python3 setup.py` in the package root runs once in a terminal. It reports what the machine already
has, asks which source to use, takes the key when one is needed, checks it with one live call, and
records the choice in `~/.config/bison/config.json`. The four choices, and where students get each
source on campus or for free, are in `references/data-sources.md`. No key is a valid answer.

With no key, `scripts/sec_fundamentals.py` builds the model from SEC EDGAR and the US Treasury yield
curve, which need nothing:

```bash
python3 scripts/sec_fundamentals.py UBER                 # keyless model inputs
python3 scripts/sec_fundamentals.py UBER --price 62.40   # adds the reverse DCF
```

It maps the ticker to a CIK, pulls the XBRL facts, prints the dated risk-free rate, and renders the
model through the same code as the FMP path, so the two sources cannot drift apart. The XBRL tag names
differ from FMP's field names (`NetCashProvidedByUsedInOperatingActivities` for operating cash flow),
which is why the mapping lives in the script and not in a prompt.

## Rules

- Every model output is an estimate, labeled as one.
- Record every model run, inputs, case outputs, and the sensitivity grid, in a dated model record
  beside the fact sheet, so every slide figure resolves to a source.
- Consensus fills the earnings base; it is the cross-check, never the price target. The rules for
  using it are in `pitch-valuation`.
- The price target is the analyst's. Present the range and stop.

## Pitfalls

- **A fixed-horizon model truncates a compounder.** A five-year window with a terminal growth ceiling
  near 2.5% values a fast grower far below its market price, because the market capitalizes a longer
  runway than the window. That gap is a finding, not a bug: state it plainly, show the sensitivity
  grid, and run a reverse DCF for what the price implies.
- **A terminal value that carries the whole model.** The script prints the terminal value share of
  enterprise value. When it dominates, say so on the slide rather than presenting the output as clean.
- **A discount rate below the risk-free rate.** Check the rate against the dated 10-year Treasury
  before trusting the output.
- **A secrets file that is not the bare key.** The stored key may be a dotfile and may hold a
  `FMP_API_KEY=...` line rather than the value alone. Code that reads it must try the documented
  paths and strip a leading variable prefix, or every call fails with an invalid key error while the
  key is in fact fine. Diagnose with one live call before blaming or rotating the key.

## Output

A model record: inputs with sources, case outputs, the sensitivity grid, the implied per-share value,
and the reverse DCF against the traded price, with the analyst's assumptions marked as the analyst's.
