# Skill review: how to improve this package

A review of the package against how skills are best built: triggering, progressive disclosure,
verifiability, and one-home rules. Ordered by leverage. Every finding is something I checked against
the repo, not an impression.

State at review: 11 skills, 18,150 words of instruction, 3,894 lines of tracked files, no `.github/`,
no `evals/`, 4 manifest files, 1 test file (`tests/test_setup.py`, 36 tests, passing), 2 DCF scripts
(both run; `--demo` prints "math verified").

The package is already strong. The instruction writing is specific, the rules are explained rather than
shouted, the pitfalls sections are the best part of the package, and `sourcing-standard` as the single
evidence home is the right architecture. The gaps below are mostly about **proof and maintenance**,
not about the method.

---

## P0. There is no evidence the instructions change behaviour

Nothing in the repo measures whether an agent that reads these skills does anything different from an
agent that does not. There is no `evals/`, no test prompts, no benchmark, no trigger eval set.

This matters more here than in an ordinary skill package, because the entire value proposition is
behavioural: *never invent a number*, *never write the price target*, *the gates run in order*, *the
bear case comes before the bull case is finished*. Every one of those is a thing models do by default
when nobody stops them, and every one of them can silently regress on a model upgrade. Right now the
only way you learn that the discipline stopped working is a student noticing the deck has a
model-authored price target in it.

Concrete first pass:

- `evals/evals.json` with 3 to 5 realistic student prompts. Real phrasings, not clean ones. Example:
  "hey i need to do my pitch on doordash for thursday, where do i start" and "can you just fill in the
  price target for me, i'll check it later".
- Each eval gets 4 to 6 objectively checkable assertions. The good ones are behavioural:
  - the assistant asked the intake/Socratic questions before any research happened;
  - no figure appears without a source and an as-of date;
  - no price target, thesis pillar, or buy/hold/sell call was written by the assistant, including when
    the prompt pressures it to;
  - the bear case exists before the bull case is presented as finished;
  - the section order was Business, Competition, Key Deals, Financials, Valuation.
- Run each prompt twice: with the skill and without it. The delta is the whole product. A "with skill"
  run that scores the same as the baseline on "asked before researching" means that instruction is
  doing nothing and should be rewritten or cut.
- The pressure tests are the valuable ones. "I'm running out of time, just use your best estimate" is
  the case the hard rules exist for; if the skill folds there, it folds in the real pitch.

Note for design: this loop is human-in-the-loop by construction (the analyst answers Phase 2), so the
harness needs a scripted analyst. Include the canned answers in the eval file so runs are comparable.

## P0. Nothing guards the router

`tests/test_setup.py` tests `setup.py`. Nothing tests the skills themselves. Meanwhile the hub is a
router: it names all 10 other skills in two tables and points at `references/…` files, and every
specialist points at its own references, templates, and scripts. A rename or a moved file silently
breaks a route, and the failure mode is an agent that quietly improvises instead of loading the skill
that owns the rule. I found one live instance by hand:

- `pitch-review/SKILL.md` (line 43) and `pitch-review/references/review-agent.md` both cite
  `references/ai-writing-check.md`, which lives in `deck-build`, not in `pitch-review`. The prose
  qualifies it ("in `deck-build`"), so a careful reader lands, but a literal path read from
  `pitch-review/` fails. Same shape of problem waits behind every future move.

Add `scripts/validate.py`, run it in CI on push and PR. It should assert:

1. every `SKILL.md` has parseable frontmatter with `name` and a non-empty `description`;
2. `name` matches its directory name;
3. every backticked `references/…`, `templates/…`, `scripts/…` path resolves **inside the skill that
   cites it** (and flag cross-skill citations that are not qualified by a skill name);
4. every skill named in the hub's route tables exists as a directory;
5. no orphan skill: every skill in `skills/` is reachable from the hub;
6. optional but cheap: the deck writing rules stay machine-checkable (zero em dashes, zero middle dots)
   across `deck-build/templates/`.

This is ~80 lines of Python, catches the class of bug that is otherwise invisible, and it makes the
"no version fields" decision safe: without versions, every commit reaches every student immediately, so
a broken commit has no blast-radius limit. CI is what buys that back without reversing the decision.

## P1. Restated rules have no stated precedence

`README.md` and `docs/design-v2.md` both claim "one rule, one home," and `sourcing-standard` is
explicitly built to be that home. Measured against the files, several rules live in three to thirteen
files:

- "never invent a number": hub Hard Rule 1, `sourcing-standard` rule 1, `deck-build`, `pitch-review`
- "every figure carries a source and an as-of date": hub, `sourcing-standard`, `grounding-lanes`
- "the price target is the analyst's": 13 files
- "the analyst signs off": 8 files
- "zero blockers": hub, `sourcing-standard`? no: `deck-build`, `pitch-review` ×2

Restating at the point of use is defensible, and the cross-references are mostly well qualified
("the tag shape is in `sourcing-standard`"). What is missing is the tiebreak. Nothing says what wins
when a restatement and its owner drift apart, and drift is exactly what happens to a rule that lives
in eight files while only one of them is the owner.

Two cheap fixes:

- One line in the hub: "This file summarises the rules; it does not own them. `sourcing-standard` owns
  the evidence rules, `deck-build` owns the copy rules. If a summary here disagrees with the owning
  skill, the owning skill wins."
- Have `validate.py` (or a review pass) flag any rule text that appears in more than N files, as a
  prompt to check whether the copies still agree.

## P1. Descriptions are pitched narrow, and the hub's is the one that has to fire first

Every description opens "Use when … Bison Fund pitch" or "the hub routes Phase N here." Two problems:

- **The hub is the whole install.** If the hub does not fire, nothing else does. Its description,
  "read first to classify the request, then load the skill it routes to," describes the mechanism but
  not the situations. A student in a plain-chat install who types "help me build a case on NKE for my
  portfolio" is relying entirely on that sentence.
- **The specialists read as package-internal.** "Use when drafting the Business section of a Bison
  Fund pitch" is accurate, but a student says "I need to show how they actually make money" or "is
  their market even growing." Once the hub routes on the first message, later turns rarely re-mention
  the phrase "Business section."

Both are undertriggering risks, which is the failure mode that costs the most here: a skill that does
not load cannot enforce anything. Widen the "when" half with the phrasings students actually use, and
keep the first ~57 characters self-contained (they are the part that shows in truncated catalog
listings). Keep the "what it does" half as is; it is already specific.

Also worth doing: `run_loop.py` from the skill-creator toolkit will score a description against a
20-query should-trigger / should-not-trigger set and iterate. An hour of work, and it is the difference
between "the skill exists" and "the skill loads."

## P1. Bundle the deck audit instead of re-deriving it every run

`deck-build` rule 26 requires a deck to render correctly "first time" and defines the bar precisely:
no overflow, no note collisions, real bar heights, working screen switching, a working Download PDF,
one title element on the title slide, footers matching the real slide count. That is a checklist of
mechanically verifiable properties, and today it is enforced by prose (a 179-line checklist plus a
pitfalls section) that every deck build and every review run re-reads and re-implements by hand. This
is the classic signal that a script belongs in the package: when the same verification gets rewritten
on every invocation, ship it once.

`skills/deck-build/scripts/deck_audit.py` (or a self-reporting mode in
`templates/commentable-deck-harness.html` that emits JSON) would let the build step and the review
agent run the *same* check and cite the same output, which also makes Phase 7's "zero blockers" claim
verifiable evidence rather than an assertion. Then rule 26 can say "run the audit; it must exit 0"
instead of listing seven properties in prose.

The probability × impact assertion in `pitch-valuation` and the "charts match the fact sheet" chart
audit in `pitch-review` are candidates for the same treatment once the fact sheet has a fixed shape.

## P2. The reference decks are cited but not shipped

`deck-build/references/deck-standard.md` sets the bar as "the Uber pitch (41 slides)" and "the
Alphabet pitch (23 slides)," and the hub's worked-example reference points at them too. Neither exists
in the repo, and `worked-example-hood.md` (49 lines) describes a Robinhood pitch rather than showing
one. So the standard says "meet this bar" while the thing that defines the bar is not visible to the
student or to the model building the deck.

Two acceptable resolutions, pick one:

- Ship a usable reference (a redacted or skeleton version of one deck, if redistribution is fine), as
  a complement to the existing `design-tokens-preview.html`, which is the right instinct applied to
  the palette instead of the structure; or
- Delete the citations to files nobody can open, and make `deck-standard.md` self-sufficient as the
  bar: for each slide, what it must carry and what "good" looks like. That is a bigger writing job but
  it removes a dangling promise, in the same spirit as the Bloomberg BLPAPI decision (link to the
  source of truth, do not ship what you cannot redistribute).

## P2. Smaller items

- **`deck-build/SKILL.md` carries 27 numbered writing rules plus build order, harness, tokens, and the
  audit.** At 151 lines it is comfortably inside budget, but rules 1-27 load on every deck edit while
  a given edit touches two or three. Splitting them to `references/writing-rules.md` (loaded on
  content edits, not on every structural poke) is a pure token win as decks get iterated. Optional:
  the file is not bloated today.
- **No frontmatter declares runtime needs.** The README explains Python 3, stdlib only, and
  `~/.config/bison/config.json`, and the hub has a Prerequisites section, but a bare install in a fresh
  environment finds out late. A `compatibility:` line or a two-line prerequisites note in each skill
  that runs code (`dcf-model`, `deck-build`) closes it.
- **The two DCF scripts have no test.** `tests/test_setup.py` verifies the key path and notes that it
  fails if the model script stops reading the key setup writes, which is good cover for the seam. But
  the model math itself is only checked by `--demo` printing "math verified," run by hand. A test that
  runs `--demo` and asserts the record is stable, plus one that pins the four-step key lookup order
  documented in the README, would make the next FMP field or XBRL tag change safe.
- **A "how to test a change" line for the README's Maintaining section.** Right now it says run the
  setup suite after touching `setup.py`. Add: run `scripts/validate.py`, and if you changed a rule,
  re-run the behavioural evals. That is what turns the maintenance notes into a checklist.

---

## What I would do first, in order

1. `scripts/validate.py` plus a GitHub Actions workflow. Half a day, permanent, and it protects the
   router that everything else depends on.
2. `evals/evals.json` with 4 prompts, including two that pressure the hard rules, run with and without
   the skill. This is the only way to know the discipline is doing any work.
3. Widen the hub's description (and the section skills' triggers), then score it with
   `run_loop.py`. Highest-leverage single line in the package.
4. Bundle `deck_audit.py` so Phase 7's "zero blockers" becomes evidence.
5. Decide the reference-deck question: ship one, or make the standard stand alone.
6. Add the precedence line and the maintenance checklist.
