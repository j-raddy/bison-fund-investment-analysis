# Bison Fund Investment Analysis

A skill for building an equity pitch with an AI assistant. Written for the NDSU Bison Fund
and anyone learning to do equity research with an AI, and usable in Claude Code, Codex,
Hermes, Cowork, Cursor, or a plain ChatGPT / Claude / Gemini chat window.

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

## What's in here

```
SKILL.md                                  the workflow, the hard rules, and how to run it in your tool
references/section-method.md              what each of the 5 pitch sections requires, plus the slide map
references/socratic-question-bank.md      the questions the AI asks you first
references/citation-rules.md              the evidence standard and the sign-off checklist
references/grounding-method.md            Phase 1: the four grounding lanes and their merge rules
references/worked-example-hood.md         the Robinhood (HOOD) pitch as a described example, no deck file
references/deck-standard.md               the house deck bar: slide inventory, design system, workflow
references/deck-build-checklist.md        the render rules and the browser audit before a deck ships
references/review-agent.md                the independent review agent brief for Phase 7
references/dcf-method.md                  how to build the discounted cash flow
references/fmp-api-docs.md                the Financial Modeling Prep API documentation
references/bloomberg-terminal.md          the terminal path for analysts with access
references/creative-slides.md             optional slides beyond the core five sections
references/ai-writing-check.md            the AI-ism tells to flag in deck copy
references/brand-and-design-tokens.md     NDSU Bison Fund palette, type, and shadcn token map
references/design-tokens-preview.html     open in a browser to see the tokens rendered
scripts/fmp_dcf.py                        the discounted cash flow script (Python 3, stdlib only)
templates/deck-house.css                  the shared deck stylesheet, the fund's design system
templates/deck-skeleton.html              a ready-to-fill deck with the full standard slide inventory
templates/commentable-deck-harness.html   the commentable review wrapper and the PDF export
templates/ndsu-design-tokens.css          drop-in shadcn / Tailwind token file in the fund's colors
templates/pitch-outline.md                a blank text skeleton to fill for your own company
```

## Install

Every harness loads the same thing: a folder that contains `SKILL.md`. So installation is a
`git clone` into that harness's skills directory, which also makes `git pull` your update
path. Nothing here needs a build step, a package manager, or network access at install time.

The skill folder name has to stay `bison-fund-investment-analysis`, because that is the name
you invoke it by.

### Claude Code

User level, available in every project:

```bash
git clone https://github.com/j-raddy/bison-fund-investment-analysis.git \
  ~/.claude/skills/bison-fund-investment-analysis
```

Project level, committed with the repo you are pitching in:

```bash
git clone https://github.com/j-raddy/bison-fund-investment-analysis.git \
  .claude/skills/bison-fund-investment-analysis
```

Start a new session, run `/skills` to confirm it loaded, then ask for it by name.

Update: `git -C ~/.claude/skills/bison-fund-investment-analysis pull`

### Codex

Codex discovers skills in `$CODEX_HOME/skills` (default `~/.codex/skills`) and in
`.agents/skills/` inside a project.

```bash
git clone https://github.com/j-raddy/bison-fund-investment-analysis.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/bison-fund-investment-analysis"
```

Project level: clone into `.agents/skills/bison-fund-investment-analysis` instead. Legacy
`.codex/skills/` in a project also works.

Update: `git -C "${CODEX_HOME:-$HOME/.codex}/skills/bison-fund-investment-analysis" pull`

### Hermes

Hermes reads `$HERMES_HOME/skills` (default `~/.hermes/skills`), with an optional category
folder such as `finance/`.

```bash
git clone https://github.com/j-raddy/bison-fund-investment-analysis.git \
  "${HERMES_HOME:-$HOME/.hermes}/skills/finance/bison-fund-investment-analysis"
```

Then confirm it loaded:

```bash
hermes skills list | grep bison
```

Update: `git -C "${HERMES_HOME:-$HOME/.hermes}/skills/finance/bison-fund-investment-analysis" pull`

### One clone for every tool

If you use more than one harness, keep a single clone and symlink it into each skills
directory, so one `git pull` updates all of them:

```bash
git clone https://github.com/j-raddy/bison-fund-investment-analysis.git ~/bison-fund-investment-analysis

ln -s ~/bison-fund-investment-analysis ~/.claude/skills/bison-fund-investment-analysis
ln -s ~/bison-fund-investment-analysis "${CODEX_HOME:-$HOME/.codex}/skills/bison-fund-investment-analysis"
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/skills/finance"
ln -s ~/bison-fund-investment-analysis "${HERMES_HOME:-$HOME/.hermes}/skills/finance/bison-fund-investment-analysis"
```

Symlinks are read the same as real directories. Restart the session afterward and check the
skill appears before you rely on it.

### Plain chat window, or no agent at all

Open `SKILL.md`, paste its body in as a custom instruction or your first message, then start
with your company and why it interests you. Paste `references/section-method.md` when you
reach the drafting phase. The reference files also work as a checklist for a new analyst even
if you never touch an AI at all.

## A first message you can paste

```
I want to research <COMPANY> (<TICKER>) for an equity pitch. It interests me because
<your reason, in your own words>. Use the Bison Fund Investment Analysis skill and
start with Phase 0.
```

From there the skill walks you through intake, the questions, evidence-gathering, section
drafts, a bear case, a verification pass, and a pitch-ready map, in that order.

## The DCF script

`scripts/fmp_dcf.py` builds the discounted cash flow from Financial Modeling Prep data. It
needs Python 3 and the standard library only.

```bash
python3 scripts/fmp_dcf.py --demo        # runs the math on canned inputs, no key needed
python3 scripts/fmp_dcf.py UBER          # live: pulls from FMP and builds the model
```

A live run needs your own FMP API key. The script reads `$FMP_API_KEY` first, then
`~/.hermes/secrets/fmp_api_key`, then `~/.config/fmp/api_key`. It never prints the key. Free
tier keys are rate limited to roughly 250 calls a day, so one key per analyst.

## Scope

This is a research discipline, not investment advice, a screener, a stock picker, or a price
target generator. It refuses the parts that are the analyst's job on purpose. Nothing here is
a recommendation to buy or sell any security.

## License

MIT. See [LICENSE](LICENSE).

Bloomberg's BLPAPI guides are not redistributed here. `references/bloomberg-terminal.md`
links to Bloomberg's own download page instead.
