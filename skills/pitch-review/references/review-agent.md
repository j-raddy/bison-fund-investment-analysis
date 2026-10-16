# Review Agent (Phase 7, the loop that never stops)

After every change to the deck, an independent review agent re-checks it against the record. The
analyst verifies meaning (Phase 6); the review agent verifies mechanics and facts. Both run; they
check different things and neither replaces the other.

The review agent is a sub-agent when the harness has one, or the main session wearing a different
hat when it does not. Either way it must not have written the deck it is reviewing: fresh context
is what makes it find what the author stopped seeing.

## What it checks, in order

1. **Fact audit.** Every figure on every slide must appear in the fact sheet or grounding digests
   with a matching source and as-of date. A number on a slide that resolves to nothing is a blocker.
2. **Chart audit.** Every SVG bar label and table value must match the fact sheet. Charts are the
   most common place for a stale number to hide, because the chart was drawn from an earlier draft.
3. **Quote audit.** Anything attributed to the company or the street must appear, near-verbatim, in
   a transcript, filing, or cited source. Paraphrase is fine; invented phrasing is a blocker.
4. **Rule audit.** The mechanical subset of the writing rules, checkable by reading: no em dashes,
   no middle dots, no acronyms, no quotes of the analyst, no process language, one "Key takeaway"
   label per summary box, plain titles, no duplicate title on the title slide, footers state the
   real slide count, eyebrows match section convention.
5. **Consistency audit.** The same fact stated on two slides must not disagree. Consensus targets,
   prices, and dates drift between drafts; the deck must not contradict itself.
6. **Structural audit.** The deck-build browser audit: no overflow, no note collisions, charts with
   real bars, screens switch, PDF prints, one title, page count matches.
7. **AI-writing audit.** Every slide's rendered copy is scanned for AI-writing tells: significance
   inflation, superficial -ing tack-ons, signposting, generic positive conclusions, negative
   parallelism, forced metaphor, rule-of-three padding, and the rest of the list and severity rules
   in `references/ai-writing-check.md` in the `deck-build` skill. The mechanical dash and acronym rules stay in the rule
   audit; this check is about prose that reads machine-written.

## The brief

```
Role: review agent. You did not write this deck. Your job is to find what is wrong with it.
Inputs:
  deck: <path to the deck html>
  fact sheet: <path>
  grounding digests: <paths>
  writing rules: `references/writing-rules.md` in the `deck-build` skill
Checks: fact, chart, quote, rule, consistency, structural (the deck-build browser audit), ai-writing
(the AI-ism tells in `references/ai-writing-check.md` in the `deck-build` skill).
Output: a findings list written to <workspace>/review-findings.md, one line per finding:
  [BLOCKER | MINOR] slide <n>, region <name>: <what is wrong>, <what it should say>, <source>
No fixes. No rewrites. Findings only. If a check passes, one line saying so.
```

## The loop

1. Run the review agent. Read the findings.
2. Fix every BLOCKER. Fix MINOR wording findings unless there is a reason not to, and say why.
3. Re-run the review agent on the changed deck. Repeat until zero BLOCKER findings and every
   MINOR is either fixed or explicitly waived by the analyst in one line.
4. Only then hand the deck to the analyst for Phase 6-style sign-off.

The loop reruns on every change, however small. A one-line edit re-runs the review; the agent is
cheap and the alternative is a stale claim surviving into the room. The comment harness is the
human half of the same loop: human comments come in by region, machine findings come out by
region, and fixes are made against region names so nothing drifts.

## What the review agent must not do

- It does not rewrite the deck. Findings only, fixes by the author or the controller.
- It does not re-litigate the thesis. The analyst owns it. It checks that what is claimed is
  sourced and internally consistent, not whether the call is right.
- It does not approve the deck. A clean review means zero blockers, which is the analyst's signal
  to run their own Phase 6 verification, not a substitute for it.
