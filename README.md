# Bison Fund Investment Analysis

A skill for building an equity pitch with an AI assistant. Written for the NDSU Bison Fund
and anyone learning to do equity research with an AI. It installs as a plugin in Claude Code,
Codex, and Hermes, and as a plain skill anywhere that reads `SKILL.md`.

It is built on one idea: the AI should help you **think and analyze faster**, not think for
you. Two rules run through everything:

1. **Think first, draft second.** Before the AI researches anything, it asks you what *you*
   believe about the business. You answer first.
2. **Every number has a source.** Every figure carries a source and an as-of date, or it is
   flagged unverified and cannot go into the pitch.

The AI will never invent a number, and it will never write your price target, your thesis
pillars, or your buy / hold / sell call. Those are yours.

The pitch has five sections, in this order:
Business, Competition, Key Deals, Financials, Valuation.

## Install

One line per tool. Each line runs the two steps behind it in order.

**Claude Code** (adds the marketplace, then installs the plugin):

```bash
claude plugin marketplace add j-raddy/bison-fund-investment-analysis && claude plugin install bison-fund-investment-analysis@bison-fund
```

**Codex** (adds the marketplace, then installs the plugin):

```bash
codex plugin marketplace add j-raddy/bison-fund-investment-analysis && codex plugin add bison-fund-investment-analysis@bison-fund
```

**Hermes** (installs the plugin, then enables it; a portable package installs disabled):

```bash
hermes plugins install j-raddy/bison-fund-investment-analysis && hermes plugins enable bison-fund-investment-analysis
```

**Any other tool that reads skills from a directory** (also the Claude Code and Codex
fallback): clone once and link the skill folder into that tool's skills directory.

```bash
git clone --depth 1 https://github.com/j-raddy/bison-fund-investment-analysis.git ~/bison-fund-investment-analysis && ln -s ~/bison-fund-investment-analysis/plugins/bison-fund-investment-analysis/skills/bison-fund-investment-analysis ~/.claude/skills/bison-fund-investment-analysis
```

Swap the last path for the directory your tool reads: `~/.codex/skills/` or `~/.agents/skills/`
for Codex, `$HERMES_HOME/skills/finance/` (default `~/.hermes/skills/finance/`) for Hermes,
`.claude/skills/` or `.agents/skills/` inside a project to commit the skill with your pitch.

**Plain chat window (ChatGPT, Claude web, Gemini):** open
`plugins/bison-fund-investment-analysis/skills/bison-fund-investment-analysis/SKILL.md`, paste
its body in as a custom instruction or your first message, then start with your company and
why it interests you. Paste `references/section-method.md` when you reach the drafting phase.

Start a new session after installing, then ask for the skill by name:
`bison-fund-investment-analysis`.

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

Eleven skills in one plugin. The hub is the entry point; the specialists load when the loop reaches
them.

```
bison-fund-investment-analysis   the hub: classification, the two non-negotiables, the six hard rules,
                                 the gated loop and its order, routing, the done checklist
pitch-business                   section 01, what the business is and whether its market is growing
pitch-competition                section 02, peers, moat, regulation, M&A, management
pitch-deals                      section 03, the transactions that shape the thesis
pitch-financials                 section 04, revenue, unit economics, returns, margins, cash
pitch-valuation                  section 05, the DCF, scenarios, risk matrix, catalysts, the thesis
grounding-lanes                  phase 1, the four lanes of research run before any thesis exists
dcf-model                        the valuation method, the working script, market data access
deck-build                       the deck standard, the writing rules, tokens, templates, render audit
sourcing-standard                the evidence tag, source quality, the sign-off checklist
pitch-review                     the red team, the verification pass, the independent review loop
```

Each skill holds its own `SKILL.md` and its own `references/` under
`plugins/bison-fund-investment-analysis/skills/`. The design record, including which skill owns which
rule and why, is [docs/design-v2.md](docs/design-v2.md).

The hub keeps the name students already invoke, so nothing about installing changes. The root `skills`
symlink points at the plugin's skill folder so the portable manifest at the repo root resolves for
Hermes.

## The DCF script

`scripts/fmp_dcf.py` under the `dcf-model` skill builds the discounted cash flow from Financial
Modeling Prep data. It needs Python 3 and the standard library only.

```bash
python3 plugins/bison-fund-investment-analysis/skills/dcf-model/scripts/fmp_dcf.py --demo
```

A live run needs your own FMP API key. The script reads `$FMP_API_KEY` first, then
`~/.hermes/secrets/fmp_api_key`, then `~/.config/fmp/api_key`. It never prints the key. Free
tier keys are rate limited to roughly 250 calls a day, so one key per analyst.

## Maintaining this repo

- Bump `version` in `plugin.json` (the portable manifest at the repo root), and in
  `plugins/bison-fund-investment-analysis/.claude-plugin/plugin.json` and
  `plugins/bison-fund-investment-analysis/.codex-plugin/plugin.json`, together when a skill changes.
  The plugin directory's manifests are the ones Claude Code and Codex install, so bumping only the
  root manifest ships nothing. Claude Code keeps users on the version they installed until the
  number moves.
- One rule, one home. Before adding a rule to a skill, check [docs/design-v2.md](docs/design-v2.md)
  for which skill already owns it; if a second file needs the rule, it names the owning skill
  instead of restating it.
- The plugin directory has to hold real files. Codex copies only the plugin directory it
  resolves and skips symlinked skills, which is why the skill lives under `plugins/` and the
  root `skills` is the link, not the other way around.
- No client or household data belongs in this repo. It is public.
- Bloomberg's BLPAPI guides are not redistributed here. `references/bloomberg-terminal.md`
  links to Bloomberg's own download page instead.

## Scope

This is a research discipline, not investment advice, a screener, a stock picker, or a price
target generator. It refuses the parts that are the analyst's job on purpose. Nothing here is
a recommendation to buy or sell any security.

## License

MIT. See [LICENSE](LICENSE).
