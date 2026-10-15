# Bison Fund Investment Analysis

A skill for building an equity pitch with an AI assistant. Written for the NDSU Bison Fund
and anyone learning to do equity research with an AI. It installs as a plugin in Claude Code,
Codex, and Hermes, and as a plain skill anywhere that reads `SKILL.md`.

It is built on one idea: the AI should help you think and analyze faster, not think for
you. Two rules run through everything:

1. Think first, draft second. Before the AI researches anything, it asks you what you
   believe about the business. You answer first.
2. Every number has a source. Every figure carries a source and an as-of date, or it is
   flagged unverified and cannot go into the pitch.

The AI will never invent a number, and it will never write your price target, your thesis
pillars, or your buy / hold / sell call. Those are yours.

The pitch has five sections, in this order:
Business, Competition, Key Deals, Financials, Valuation.

## Install

One line per tool. Each line runs the two steps behind it in order.

Claude Code, which adds the marketplace and then installs the plugin:

```bash
claude plugin marketplace add j-raddy/bison-fund-investment-analysis && claude plugin install bison-fund-investment-analysis@bison-fund
```

Codex, the same two steps:

```bash
codex plugin marketplace add j-raddy/bison-fund-investment-analysis && codex plugin add bison-fund-investment-analysis@bison-fund
```

Hermes. A portable package installs disabled, so the second command activates it:

```bash
hermes plugins install j-raddy/bison-fund-investment-analysis && hermes plugins enable bison-fund-investment-analysis
```

Any other tool that reads skills from a directory, and the Claude Code and Codex fallback:
clone once and link the skill folder into that tool's skills directory.

```bash
git clone --depth 1 https://github.com/j-raddy/bison-fund-investment-analysis.git ~/bison-fund-investment-analysis && ln -s ~/bison-fund-investment-analysis/skills/bison-fund-investment-analysis ~/.claude/skills/bison-fund-investment-analysis
```

Swap the last path for the directory your tool reads: `~/.codex/skills/` or `~/.agents/skills/`
for Codex, `$HERMES_HOME/skills/finance/` (default `~/.hermes/skills/finance/`) for Hermes,
`.claude/skills/` or `.agents/skills/` inside a project to commit the skill with your pitch.

Plain chat windows (ChatGPT, Claude web, Gemini): open
`skills/bison-fund-investment-analysis/SKILL.md`, paste its body in as a custom instruction or
your first message, then start with your company and why it interests you. Paste the section
skill you are working on when you reach it.

Start a new session after installing, then ask for the skill by name:
`bison-fund-investment-analysis`.

### Set up a data source

Run setup once in a terminal, from wherever the package landed (the clone path above, or
`~/.hermes/plugins/bison-fund-investment-analysis/` for a Hermes plugin install):

```bash
python3 setup.py
```

It reports what the machine already has, asks which market-data source to use, takes your own key if
the source needs one, checks it with one live call, and records the choice. No key is a valid answer:
the SEC EDGAR and Treasury option needs nothing and still builds the model. The sources, and where
students get each one, are in
[skills/dcf-model/references/data-sources.md](skills/dcf-model/references/data-sources.md).

### Updating

```bash
claude plugin marketplace update bison-fund && claude plugin update bison-fund-investment-analysis
codex plugin marketplace upgrade bison-fund
hermes plugins update bison-fund-investment-analysis
```

## A first message you can paste

```
I want to research <COMPANY> (<TICKER>) for an equity pitch. It interests me because
<your reason, in your own words>. Use the Bison Fund Investment Analysis skill and
start with Phase 0.
```

From there the skill walks you through intake, the questions, evidence-gathering, section
drafts, a bear case, a verification pass, and a pitch-ready map, in that order.

## What's in here

Eleven skills. The hub is the entry point; the specialists load when the loop reaches them.

```
bison-fund-investment-analysis   the hub: classification, the two non-negotiables, the six hard rules,
                                 the gated loop and its order, routing, the done checklist
pitch-business                   section 01, what the business is and whether its market is growing
pitch-competition                section 02, peers, moat, regulation, M&A, management
pitch-deals                      section 03, the transactions that shape the thesis
pitch-financials                 section 04, revenue, unit economics, returns, margins, cash
pitch-valuation                  section 05, the DCF, scenarios, risk matrix, catalysts, the thesis
grounding-lanes                  phase 1, the four lanes of research run before any thesis exists
dcf-model                        the valuation method, the working scripts (FMP and keyless SEC),
                                 market data access
sourcing-standard                the evidence tag, source quality, the sign-off checklist
pitch-review                     the red team, the verification pass, the independent review loop
```

Each skill holds its own `SKILL.md` and its own `references/` under `skills/`. The design
record, including which skill owns which rule and why, is [docs/design-v2.md](docs/design-v2.md).

The hub keeps the name students already invoke, so nothing about installing changes.

## Repository layout

Same shape as other published skill packages: the plugin lives at the repository root, so one
directory holds the manifests and the skills.

```
setup.py                         the one-time data-source setup, run once after install
plugin.json                      portable plugin manifest (Agent Plugins v1), read by Hermes
.claude-plugin/plugin.json       the one plugin manifest Claude Code and Codex both read
.claude-plugin/marketplace.json  the marketplace Claude Code reads
.agents/plugins/marketplace.json the marketplace Codex reads
skills/<skill-name>/             one directory per skill, each with SKILL.md and references/
docs/design-v2.md                the design record
```

Four manifest files, kept to the ones a harness actually reads. Each cut was tested by removing the
file and reinstalling, not by reading documentation:

- There is no `.codex-plugin/plugin.json`. Codex installs this plugin with only the Claude manifest
  present, so a second manifest would be a second copy of the same facts.
- There are no `version` fields. Claude Code and Codex both install without one, and a version has to
  be bumped in every manifest for a change to reach anyone who already installed, which is a chore
  that silently ships nothing when one is missed. Without a version, users track the newest commit,
  which is the intent for a public teaching package. The one cost is an advisory warning from
  `claude plugin validate` suggesting semver.

Two structural notes. The Codex marketplace entry points at the repository URL rather than a relative
path, because Codex will not install a plugin whose marketplace source is the marketplace root. And
the skill files have to be real files: Codex copies only the directory it resolves and skips symlinked
skills, which is why every skill lives in its own directory under `skills/` with no links.

## The DCF scripts

Two scripts under the `dcf-model` skill build the same model from different sources. Both need
Python 3 and the standard library only, and both render the model record through the same code, so
the numbers are comparable.

`scripts/fmp_dcf.py` reads Financial Modeling Prep. A live run needs your own key, which
`setup.py` stores at `~/.config/bison/keys/fmp.key`; the script reads `$FMP_API_KEY` first, then that
file, then `~/.hermes/secrets/fmp_api_key` and `~/.config/fmp/api_key`. It never prints the key. Free
tier keys are rate limited to roughly 250 calls a day, so one key per analyst.

`scripts/sec_fundamentals.py` needs no key at all. It builds the inputs from SEC EDGAR XBRL facts and
the US Treasury daily yield curve, which is what a machine with no key uses.

```bash
python3 skills/dcf-model/scripts/fmp_dcf.py --demo        # offline math check, no key
python3 skills/dcf-model/scripts/fmp_dcf.py UBER          # live, needs an FMP key
python3 skills/dcf-model/scripts/sec_fundamentals.py UBER  # live, no key
```

## Maintaining this repo

- There are no `version` fields to keep in sync. A change reaches anyone who installed it as soon as
  they update, because a plugin without a version tracks the newest commit. Setting a version is the
  option to reach for if this ever needs pinned releases.
- One rule, one home. Before adding a rule to a skill, check [docs/design-v2.md](docs/design-v2.md)
  for which skill already owns it; if a second file needs the rule, it names the owning skill
  instead of restating it.
- Run the setup suite after touching `setup.py` or the key paths: `python3 tests/test_setup.py`.
  It runs offline, and it fails if the model script stops reading the key setup writes.
- No client or household data belongs in this repo. It is public.
- Bloomberg's BLPAPI guides are not redistributed here.
  `skills/dcf-model/references/bloomberg-terminal.md` links to Bloomberg's own download page instead.

## Scope

This is a research discipline, not investment advice, a screener, a stock picker, or a price
target generator. It refuses the parts that are the analyst's job on purpose. Nothing here is
a recommendation to buy or sell any security.

## License

MIT. See [LICENSE](LICENSE).
