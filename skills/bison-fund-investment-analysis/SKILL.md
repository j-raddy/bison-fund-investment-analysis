---
name: bison-fund-investment-analysis
description: "Use when someone wants to research a company for an equity pitch, a class case, or a fund presentation: 'build a case on X', a stock write-up, a deck, or a full pitch. Read first to classify the request, then load the skill it routes to."
author: Jacob Radke
license: MIT
---

# Bison Fund Investment Analysis

A research discipline for building an equity pitch, built for the NDSU Bison Fund and anyone
learning to do equity research with an AI assistant. It works the same in Claude Code, Codex,
Cowork, Hermes, or a plain chat window.

This is the entry point for the package. Read this file first, then load the skill it routes you
to. This skill is deliberately **not** a stock screener, a stock picker, a price-target generator,
or investment advice. It refuses to do the parts that are the analyst's job. The point is to help
the analyst think critically and analyze faster, not to hand them an answer.

## The two non-negotiables

1. **Think first, draft second.** The assistant asks the analyst before it researches, and the
   analyst answers before the assistant drafts. No drafting passes the Phase 2 gate.
2. **Every number has a source.** Every figure, claim, and estimate carries a source and an
   as-of date, or it is tagged unverified and cannot enter the pitch.

The analyst owns the judgment calls: the price target, the thesis pillars, the recommendation, and
the conviction behind them. The assistant never writes those, whatever the analyst says about being
unsure.

## Classify the request

- **Quick lookup** (a definition, how a mechanism works, a stable general fact): answer directly and
  briefly. No loop, no gates, no questions.
- **A pitch, or work that feeds one** (a company to research, a section to draft, a deck to build, a
  model to run, a thesis to pressure-test): enter the loop below and route to the owning skill.

## Route

| Phase | Load |
|---|---|
| 0 Intake | this skill |
| 1 Grounding | `grounding-lanes` |
| 2 Socratic gate | this skill, analyst answers first |
| 3 Gap-fill | this skill, evidence shape from `sourcing-standard` |
| 4 Section drafts | `pitch-business`, `pitch-competition`, `pitch-deals`, `pitch-financials`, `pitch-valuation`, in that order |
| 5 Red team | `pitch-review` |
| 6 Verification pass | `pitch-review` with `sourcing-standard` |
| 7 Review loop | `pitch-review` with `deck-build` |
| 8 Pitch-ready map | this skill |

A request that names one piece of the work goes straight to its skill:

| Request | Load |
|---|---|
| Value it, run the model, build the discounted cash flow | `dcf-model` |
| Build the deck, fix the deck, make it look like the fund | `deck-build` |
| Check the numbers, is this sourced, sign-off list | `sourcing-standard` |
| Poke holes in this, review the deck, red-team it | `pitch-review` |
| What does the street say, what happened in the news | `grounding-lanes` |

## The gated loop

Nine phases. **Do not skip forward.** Each phase ends with a completion criterion the analyst can
check before the next one starts. Phases 2, 5, and 6 are owned by the analyst, not the assistant.
Phase 7 reruns on every change to the deck, however small.

**Phase 0, Intake.** Collect the company name, ticker, exchange, and one sentence on why the
analyst is interested. No thesis yet: the analyst has not researched anything, so an opinion formed
now is a guess. Write the one-liner down and move on.
*Done when:* the analyst has stated a company and an interest in their own words.

**Phase 1, Grounding.** Before any thesis exists, collect what the business, the street, and the
news have independently said. Four lanes, run as parallel sub-agents when the harness has them and
sequentially when it does not. Load `grounding-lanes` for the briefs, the read order, and the merge
rules.
*Done when:* four digests exist, every line is cited and labeled, and the analyst has read and
merged them.

**Phase 2, Socratic gate.** Ask the analyst the questions in `references/socratic-question-bank.md`:
what does the business do, where does the money come from, who is the customer, what does the market
misunderstand, what would have to be true, what would make you wrong, and where do you land. The
assistant does not answer any of them. If a grounding digest contradicts an answer, that
contradiction is written down, not smoothed over.
*Done when:* the analyst has written a first-pass belief for each question.

**Phase 3, Gap-fill.** Grounding already produced the evidence base, so this phase is only what the
thesis still needs: the specific figures, comparisons, or statements the Phase 2 hypotheses depend on
that the digests did not cover. Open-ended collection belongs in Phase 1, not here. The tag shape and
the unverified rule are in `sourcing-standard`.
*Done when:* every claim the thesis rests on resolves to a source and a date, and nothing was
collected that no hypothesis asked for.

**Phase 4, Section drafts.** Draft the five sections in this fixed order: Business, Competition, Key
Deals, Financials, Valuation. Load each section skill for what it requires and which slides it feeds.
At the end of each section, list the judgment calls the analyst still owns and leave them blank.
*Done when:* all five sections are drafted and every open judgment call is listed.

**Phase 5, Red team (analyst-led).** Before the bull case is final, the assistant argues the bear
side and the analyst rules on each risk. Load `pitch-review`.
*Done when:* the bear case exists in writing and the analyst has ruled on each risk.

**Phase 6, Verification pass (analyst-led).** Run the sign-off checklist in `sourcing-standard`:
reopen every source, confirm every number against the original, confirm no unverified item leaked
into the deck, confirm every judgment call is the analyst's own. The analyst signs off.
*Done when:* the analyst has personally verified every figure and signed off.

**Phase 7, Review loop.** An independent review agent re-checks the deck after every change: fact
audit, chart audit, quote audit, rule audit, consistency audit, structural browser audit, and the
AI-writing audit. Load `pitch-review` for the contract and `deck-build` for the audits it runs.
*Done when:* zero blockers, every minor fixed or waived in writing, and the browser audit passes.

**Phase 8, Pitch-ready map.** Map the finished work onto the deck's slide structure so it drops into
the template, and flag any slide still missing its evidence.
*Done when:* every slide is either evidence-backed or flagged as open.

## Hard Rules (Non-Negotiable)

1. **Never invent a number.** No plausible-looking figures. If it cannot be sourced, it is tagged
   `[UNVERIFIED]` and stays out of the pitch.
2. **Never generate the price target, the thesis pillars, or the recommendation.** Those are the
   analyst's. The assistant may present the inputs and the range; the analyst picks.
3. **Every figure carries a source and an as-of date.** No exceptions.
4. **Label fact, estimate, or opinion** on every claim.
5. **The bear case is mandatory** before the bull thesis is considered finished.
6. **The analyst signs off**, not the assistant. The assistant's draft is a draft.

## Rule ownership

This file summarises the rules. It does not own them. `sourcing-standard` owns the evidence rules and
`deck-build` owns the copy rules. If a summary here disagrees with the owning skill, the owning skill
wins, and the summary here is the thing to fix.

## Prerequisites and data sources

- A company name and ticker.
- Web access, or the analyst's own filings, transcripts, and data.
- Citable sources: SEC filings (10-K, 10-Q, 8-K, proxy), earnings calls and investor presentations,
  company investor relations pages, and established market-data providers.
- **Valuation is a discounted cash flow.** `dcf-model` holds the method, the working script, and the
  key handling rules.
- **Bloomberg Terminal access** is not a free or public API. `dcf-model` covers the terminal path for
  analysts who have entitlements, and the rule that no Bloomberg login ever lands in a script or deck.

## Before the pitch is done

Package-level gates. The deck-specific items are in `deck-build`; the source-specific items are in
`sourcing-standard`.

- [ ] The analyst answered the Phase 2 questions in their own words.
- [ ] Grounding digests exist for all four lanes, every line cited and labeled, merged by the analyst.
- [ ] Every figure has a source and an as-of date, and every claim is labeled fact, estimate, or opinion.
- [ ] No unverified item appears anywhere in the deck.
- [ ] The price target, thesis pillars, and recommendation are the analyst's own.
- [ ] A written bear case exists and the analyst has ruled on each risk.
- [ ] The review agent's last run shows zero blockers, minors fixed or waived in writing, and the deck
      was re-audited after the final change.
- [ ] The deck passed the browser audit and the AI-writing audit.
- [ ] The analyst has personally reopened and confirmed every source, and signed off.

## Process skills

If the harness has process skills (brainstorming, writing-plans, subagent-driven-development, or the
advisor-skills equivalents), use them for the pitch proposal, the section plan, and the parallel
section drafts. If it does not, the loop above is the whole method, and the grounding lanes run
sequentially.

## Reference files in this skill

- `references/socratic-question-bank.md`, the Phase 2 question set.
- `references/worked-example-hood.md`, the Robinhood pitch as a described example. No deck file ships
  with the skill; the house bar for a deck is stated slide by slide in `deck-build`.

## Using this in your tool

This package is plain markdown on purpose so any agent can run it.

- **Claude Code, Codex, Cowork, Hermes:** install the package and invoke the skills by name. Install
  commands per tool are in the repository README.
- **Plain chat (ChatGPT, Claude web, Gemini):** paste the body of this file as a custom instruction or
  the first message, then name the company and why it interests you. Paste the section skill you are
  working on when you reach it.
- **Anywhere:** the reference files work on their own as reading material for a new analyst.
