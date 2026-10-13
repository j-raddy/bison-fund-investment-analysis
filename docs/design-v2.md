# Package design, version 2

Why this package is eleven skills instead of one, and what each one owns. Read this before
adding a twelfth or moving a rule.

## The shape

A hub plus ten specialists. The hub is the entry point a student's agent reads first; the
specialists are loaded only when the loop reaches them. The design is taken from the same
pattern as `superpowers` (hub, process skills, specialist skills) and the advisor-skills
package (`using-advisor-skills` routing into brainstorming, writing-plans, executing-plans).

| Skill | Owns |
|---|---|
| `bison-fund-investment-analysis` | Identity, the two non-negotiables, the six hard rules, the gated loop and its order, routing, the done checklist, the HOOD worked example, the Socratic question bank |
| `pitch-business` | Section 01 content and slide map |
| `pitch-competition` | Section 02 content and slide map |
| `pitch-deals` | Section 03 content and slide map |
| `pitch-financials` | Section 04 content and slide map |
| `pitch-valuation` | Section 05 content and slide map, consensus-as-cross-check rules |
| `grounding-lanes` | Phase 1: the four lanes, their briefs, read order, merge rules |
| `dcf-model` | The DCF method, the working script, market data access (FMP, Bloomberg) |
| `deck-build` | The deck standard, the 27 writing rules, tokens, templates, the commentable harness, the browser audit |
| `sourcing-standard` | The evidence tag, source quality, labeling, the sign-off checklist |
| `pitch-review` | Phase 5 red team, Phase 6 verification pass, Phase 7 review loop and its contract |

## Ownership boundaries

One rule, one home. If a second file needs the rule, it names the owning skill instead of
restating it.

- The evidence standard lives in `sourcing-standard`. Nothing else restates the tag shape.
- Deck presentation rules live in `deck-build`. Nothing else restates the writing rules.
- The order of the loop lives in the hub. Split across five documents, "do not skip forward"
  stops being enforced by anything.
- The six hard rules live in the hub, because they are the package's constitution and every
  specialist points back at them.

## Routing

The hub routes by phase:

| Phase | Owned by |
|---|---|
| 0 Intake | hub |
| 1 Grounding | `grounding-lanes` |
| 2 Socratic gate | hub, analyst answers first, nothing drafts before it |
| 3 Gap-fill | hub, evidence shape from `sourcing-standard` |
| 4 Section drafts | the five `pitch-*` section skills, in fixed order |
| 5 Red team | `pitch-review`, analyst-led |
| 6 Verification | `pitch-review` with `sourcing-standard` |
| 7 Review loop | `pitch-review`, reruns on every change |
| 8 Pitch-ready map | hub |

Direct routes, for a request that names one piece of the work:

| Request | Skill |
|---|---|
| "Just value it" / "run the DCF" | `dcf-model` |
| "Build the deck" / "fix the deck" | `deck-build` |
| "Is this sourced" / "check the numbers" | `sourcing-standard` |
| "Poke holes in this" / "review it" | `pitch-review` |
| "Find out what the street says" | `grounding-lanes` |

## Process skills

The package does not fork brainstorming, writing-plans, or subagent-driven-development. When
the harness has them, the hub points at them for the pitch proposal, the section plan, and the
parallel section drafts. When it does not, the loop in the hub is the whole method.

## Naming

- The hub keeps the name students already invoke, so installed copies and the README install
  lines do not change.
- Section skills carry the `pitch-` prefix so a flat install cannot collide with anything else
  in a skills directory.
- Inside Claude Code, skills are namespaced: `/bison-fund-investment-analysis:pitch-valuation`.

## Versioning

`version` moves in `plugin.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json`
together. Claude Code holds users on the version they installed until the number moves, so a
restructure without a bump never reaches them. Version 2.0.0 is this restructure.
