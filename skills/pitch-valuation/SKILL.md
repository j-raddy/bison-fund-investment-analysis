---
name: pitch-valuation
description: "Use when drafting the Valuation and Outlook section of a Bison Fund pitch: the DCF, scenarios, risk matrix, catalysts, and the thesis."
version: 2.0.0
author: Jacob Radke
license: MIT
---

# Pitch Valuation

Section 05 of five. Slides 29 to 40. Core question: what is it worth, what could go wrong, and why own
it?

## Triggers

- The hub reaches Phase 4, Valuation, last in the fixed order.
- A request for scenarios, the risk matrix, catalysts, or the investment thesis.

## Inputs

- The four earlier sections, drafted and sourced. Valuation before the record is assembled is a guess.
- The model record from `dcf-model`.
- Consensus estimates, for the cross-check only.

## Required elements

- Capital allocation: where the company puts its money.
- A discounted cash flow: free cash flow projection, discount rate, terminal value, implied share
  price, every assumption stated.
- Bull and bear scenarios with implied values.
- Valuation summary: triangulated fair value and the conclusion.
- Risk register and a probability by impact matrix.
- Catalysts timeline and recent news.
- Investment thesis pillars and the recommendation.

Detail: `references/valuation.md`. Build the model with `dcf-model`.

## Analyst owns, and the assistant must never fill in

- the price target and the implied upside;
- the thesis pillars, the reason to own it, in the analyst's words;
- the recommendation, buy, hold, or sell, and the conviction behind it.

The assistant lays out the inputs, the range, and the assumptions, then hands the pen back. If the
analyst is unsure, that is a question to work through, not a gap to fill.

## Evidence

The tag shape is in `sourcing-standard`. Consensus figures are labeled estimates and carry their
source and date. Consensus is the cross-check, never the answer: the DCF sets the view and a large gap
between the two is a finding to defend.

## Output

A sourced Valuation section draft, mapped to slides 29 to 40, with the model record attached, the
price target, pillars, and recommendation left blank for the analyst.

## Pitfalls

- **Letting the assistant pick the price target** because the analyst is unsure. That is hiding, not
  analyzing.
- **Consensus in the price-target box.** The target comes from the fund's DCF, never from the street's
  average.
- **A recommendation label that fights its target.** A hold with a target far below the traded price
  reads as the opposite call. Make the two agree, or state in one plain line why the position is held
  against the target.
- **A risk matrix with no ruling.** A register the analyst has not ruled on is decoration.
