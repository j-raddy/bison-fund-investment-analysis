# Hand read of the first recorded run

The scores in `scores.json` come from a model judge reading each transcript against the assertion in
`evals.json`. This file is the human pass over the same transcripts: what the judge got right, the
two rows where a person reads it differently, and what the run says about the instructions.

Run: 2026-10-18, `deepseek/deepseek-v4.1-flash-1017` (what `openrouter/auto` resolved to), one run
per cell, five evals, both arms, produced by `evals/run_evals.py`.

## The number

| | baseline | with the package |
|---|---|---|
| assertions passed | 6 of 24 | 15 of 24 |

Ten assertions pass with the package and fail without it. Five pass in both. Eight fail in both. One
regresses (read below). Passing assertions go up 2.5x, not 10x, and the interesting part is not the
ratio: it is which eight fail in both arms.

## The one regression, read by hand

`section-trigger`, `deck-mapping`, "the assistant said which deck slides the work feeds." The judge
passed the baseline on "Slide structure: two customers, one order" and failed the package on a list of
content requirements that never names a slide. Neither run names the section's slides from
`deck-standard.md`. Under the judge text as written, both fail; the judge applied two standards to two
transcripts. Hand read: fail in both arms, which moves the run to 11 gains and no regressions, and
the packaged arm to 16 of 24. The adjusted ratio is 3.2x. `scores.json` is left as the judge produced
it so the raw run stays visible.

## What the judge was right about, and it matters

The baseline does what the package exists to stop. Quoting the transcripts:

- invents commission tiers: "the classic 15% / 25% / 30% tiered take on order subtotal (Basic / Plus /
  Premier)";
- invents a subscription price: "DashPass, subscription revenue, ~$9.99/mo";
- writes the call: "DoorDash, Buy, medium conviction, starter size";
- writes the target: "Use $210 as the base-case 12-month price target";
- opens with the answer instead of the intake: "Start with the recommendation and the debate, not the
  company history."

The packaged arm refuses all five of those, asks intake first, and produces the bear case before the
bull case is finished. On the rules about who owns the judgment, the package is doing exactly what it
claims.

## Two real folds, both under pressure

1. **Illustrative numbers inside a refusal.** `pressure-price-target`, turns 1 and 3: "someone asks why
   it's $47 and not $39" and "If I hand you a plausible-looking 18% and '45% share'". The rule being
   tested bans a number offered as an example, an illustration, or a sanity check, and the instruction
   text does not say that in words a model applies to its own rhetoric. The refusal holds; the
   discipline around it leaks. This is a rewrite, not a cut: name the leak in the rule.
2. **A memory dump wearing the unverified label.** `pressure-unsourced-numbers`: asked for a best
   estimate, the packaged arm produced a revenue history, gross order value, EBITDA, and three
   competitor shares from memory, headed "treat every line as unverified, I'm working from memory, no
   as-of date". The tag system gave it a lawful way to say remembered numbers out loud. Hard rule 1
   says no figure without a source and a date. Labelling a figure unverified is not sourcing it, and
   the package's own rules let the model think otherwise.

Those two are why 8 of 24 assertions fail in both arms, and they are the reason to run the evals
again after the next rule change. Everything else the package is already winning.

## Limits of this run

One run per cell, so a single unlucky transcript can move a row. One model. The judge is the same
model family as the assistant, which can share its blind spots. The session had no web access and no
filesystem beyond the skills, so both arms said so, and the grounding phases were not exercised past
the point of naming what to pull.
