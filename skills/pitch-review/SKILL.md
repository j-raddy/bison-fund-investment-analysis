---
name: pitch-review
description: "Use when a draft section or deck needs the red-team pass, the verification pass, or the independent review loop."
author: Jacob Radke
license: MIT
---

# Pitch Review

Everything that attacks a draft. Three passes, in order, and none of them may be run by the author of
the material being checked when an independent agent is available.

## Triggers

- The hub routes Phase 5, Phase 6, or Phase 7 here.
- A request to poke holes in a thesis, review a deck, or stress-test a recommendation.
- Any change to a deck, however small. Phase 7 reruns on every change.

## Phase 5, Red team (analyst-led)

Before the bull case is final, argue the bear side: the strongest case against the thesis, the
assumptions that could break it, and a probability by impact read on each risk. Write it down. The
analyst rules on each risk and decides which are real. A pitch with no bear case is incomplete,
regardless of how good the story sounds.

## Phase 6, Verification pass (analyst-led)

Run the sign-off checklist in `sourcing-standard`: reopen every source, confirm every number against
the original, confirm no unverified item reached the deck, and confirm the price target, pillars, and
recommendation are the analyst's own. The analyst signs off. A clean review agent run is the trigger
for this pass, never a substitute for it.

## Phase 7, Review loop

An independent review agent re-checks the deck on seven audits:

1. **Fact audit.** Every figure resolves to the fact sheet with a matching source and date.
2. **Chart audit.** SVG values match the fact sheet.
3. **Quote audit.** Attributed text appears near-verbatim in a cited source.
4. **Rule audit.** The mechanical writing rules in `deck-build`.
5. **Consistency audit.** No slide contradicts another.
6. **Structural browser audit.** The render checks in `deck-build`.
7. **AI-writing audit.** No AI-ism tells in slide copy, per `references/ai-writing-check.md` in
   `deck-build`.

Findings come back by slide and region, severity-tagged. The author fixes blockers and waives minors
in writing. The loop reruns until clean.

**The contract.** The review agent must not have written the deck it reviews. It does not rewrite
anything, does not re-litigate the thesis, and does not approve the deck. A clean review is the
trigger for the analyst's own Phase 6 sign-off, not a substitute for it.
Full brief: `references/review-agent.md`.

## Output

A written bear case with the analyst's ruling on each risk, a signed-off verification pass, and a
review run with zero blockers, every minor fixed or waived in writing.

## Pitfalls

- **Self-review.** The author reviewing their own deck is not a review. Use a separate agent, or at
  minimum a fresh session with only the deck and the fact sheet.
- **Reading a clean review as approval.** The review is evidence for the analyst's sign-off, nothing
  more.
- **One pass.** A review that ran before the last edit did not review the deck that ships.
- **A reviewer rewriting the deck.** The reviewer reports; the author fixes. A reviewer that edits
  has left the role.
- **A recommendation label that fights its target.** A hold with a price target far below the traded
  price reads as the opposite call. Flag it: the label and the target agree, or one plain line says
  why the position is held against the target.
