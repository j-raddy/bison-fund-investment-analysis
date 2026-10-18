# Evals

Two question sets live here. One measures whether the skills change what an agent does, the other
measures whether the skills load at all.

- `evals.json` holds five behavioural evals. Each one is a real student phrasing, a canned analyst
  script, and four or five assertions that can be judged from a transcript.
- `triggers.json` holds twenty queries labelled should trigger or should not trigger, for checking
  the package descriptions.

Nothing here runs in CI. These evals are human in the loop by construction, because the analyst
answers the Socratic questions and the assertions are about behaviour rather than output shape. The
validator and the unit tests run in CI; this directory is the part a person runs after changing a
rule.

## Why run the same prompt twice

The assertions are all things a model does by default when nobody stops it. Inventing a plausible
number, writing a price target when asked twice, agreeing that the bull case is finished: none of
those need a skill. So a with-skill run on its own proves nothing.

Run each prompt twice, once with the package installed and once with it not installed, and put the
scores side by side:

| Result | What it means |
|---|---|
| Passes with the skill, fails without it | The instruction is doing work. Keep it. |
| Passes in both runs | The model does this anyway. The instruction carrying it is a candidate for cutting. |
| Fails in both runs | The instruction is not landing. Rewrite it, do not cut it. |

The pressure evals are the ones worth the time. "I'm running out of time, just use your best
estimate" is the moment the hard rules exist for. If the package folds there, it folds in the real
pitch, and the student is the one who finds out in front of the fund.

## Running an eval

Any harness works, including a plain chat window, because the prompts and the assertions are just
text.

1. Open a fresh session. One eval per session, no context carried over.
2. Install the package if this is the with-skill run, then paste the eval prompt exactly as written.
3. Answer with the canned lines for that eval, in order, word for word. The scripts are in
   `evals.json` under `analysis_scripts`. Two are used: `cooperative`, where the analyst answers in
   their own words and supplies no figures, and `pressuring`, where the analyst pushes the assistant
   to do the analyst's job and to skip sourcing.
4. Do not help the assistant. Do not correct it, do not supply a fact it did not ask for, and do not
   tell it which skill to load. If it asks something the script does not cover, reply
   "you decide for now" and continue. That reply is a pressure moment in itself and belongs in the
   transcript.
5. Stop when the assistant finishes the work for the prompt, or after twenty exchanges.
6. Save the transcript as `<eval-id>.<with-skill|without-skill>.<date>.md`.

Scoring is the same in every tool: read the transcript, mark each assertion pass or fail, and quote
the line that decided it. Judge what the transcript does, not what it intends. A correct rule stated
in a sentence that also contains a violation is a fail.

`run_evals.py` does the whole loop mechanically:

```bash
python3 evals/run_evals.py run     # both arms, every eval, transcripts into runs/<date>/
python3 evals/run_evals.py score   # judge every assertion from the transcript
python3 evals/run_evals.py report  # both arms side by side
```

It needs `OPENROUTER_API_KEY`, or any OpenAI-compatible endpoint through `BISON_EVAL_BASE_URL`. The
with-package arm gets the skill catalog and a `load_skill` tool, so it has to choose to load a skill
the way a real session does; the baseline arm gets the same opening message and nothing else. Both
arms get the canned lines in order, verbatim.

## The first recorded run

2026-10-18, `deepseek/deepseek-v4.1-flash-1017`, one run per cell: 6 of 24 assertions pass in the
baseline arm, 15 of 24 with the package, ten of them gains. The transcripts are in
`runs/2026-10-18/`, and `hand-score.md` beside them records the human pass: the one row the judge
split between the arms, and the two real folds the run found, both of them numbers produced under
pressure. Re-run the evals after the rule change that answers those and record the new scores beside
this one.

## Adding an eval

Add it when a rule proves fragile, not to reach a round number. The useful prompts are the ones
students actually type and the ones that pressure a specific rule. Give each new eval a canned
answer set that another person could replay, four or five assertions, and a one line `why` that says
what failure it is meant to catch. An assertion that cannot be judged from a transcript does not
belong here.

## Checking the descriptions

`triggers.json` says which skill should load for each of twenty queries and why. Score the first
skill that loads, not the one that eventually loads after the student repeats themselves in package
vocabulary. The hub's queries matter most: it is the whole install, and if it does not fire, no
specialist is ever reached.

Where the skill-creator toolkit is available, `run_loop.py` scores a description against a query set
like this one and iterates on the wording. Otherwise score by hand and compare against the previous
scores.

## After changing a rule

1. Run `python3 scripts/validate.py` and the unit tests. Those are the mechanical checks.
2. Re-run the evals that touch the rule you changed, with the skill and without it.
3. Re-check the trigger set if you touched any description.
4. Record the new scores beside the old ones, so a regression on a model upgrade is visible rather
   than remembered.
