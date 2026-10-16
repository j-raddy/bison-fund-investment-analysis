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

## Repo layout

The plugin is the repository root: manifests at the top, one directory per skill under `skills/`.

```
plugin.json                       portable Agent Plugins v1 manifest (Hermes)
.claude-plugin/marketplace.json   Claude Code marketplace, plugin source "./"
.claude-plugin/plugin.json        the one plugin manifest Claude Code and Codex both read
.agents/plugins/marketplace.json  Codex marketplace
skills/<skill-name>/              SKILL.md plus references/ per skill
```

Four manifest files, each with a consumer that was verified by deleting the file and reinstalling:

- **Codex needs `.agents/plugins/marketplace.json`.** Delete it and Codex finds no plugins at all,
  even though the Claude marketplace is still there. It has no fallback to the other file.
- **Codex needs a plugin manifest, but not a Codex-specific one.** With no manifest it fails with
  "missing plugin.json"; with only `.claude-plugin/plugin.json` it installs the skill set correctly.
  So there is no `.codex-plugin/` directory here.
- **Claude Code accepts the marketplace root as the plugin**, so its entry stays the relative `"./"`.
  **Codex does not**: it fails with "missing plugin.json" for a relative source, and its entry
  therefore points at the repository URL instead.
- **Hermes installs from the repository root only** (`hermes plugins install <owner>/<repo>`), and a
  local path is parsed as `owner/repo`, so the portable `plugin.json` stays at the top level.

No file carries a `version`. Both harnesses install without one; a version would have to be bumped
in every manifest to reach anyone who already installed, a chore that silently ships nothing when one
file is missed. Unversioned plugins track the newest commit, which is what a public teaching package
wants. The only cost is a semver advisory from `claude plugin validate`.

## Proof and maintenance

The package carries no version fields, so every commit reaches everyone who installed it. That
decision is only safe with checks that run on every commit, which is what these are:

| Path | What it proves |
|---|---|
| `scripts/validate.py` | The package is internally consistent: frontmatter parses and matches the directory name, every `references/` `templates/` `scripts/` path resolves inside the skill that cites it, every skill named in the hub's route tables exists, no skill is orphaned from the hub, and the deck templates carry none of the banned characters |
| `.github/workflows/validate.yml` | Both of the mechanical checks run on every push and pull request |
| `tests/` | The validator catches each failure class it claims to catch, the deck audit passes on the shipped templates, and the DCF math and key lookup order are pinned |
| `skills/deck-build/scripts/deck_audit.py` | A deck file meets the mechanical part of the standard, so the review loop's zero blockers claim rests on output rather than an assertion |
| `evals/` | The instructions change agent behaviour, measured against a run without the skill |

Two limits are stated rather than papered over. The evals are human in the loop, because the analyst
answers the Socratic questions, so they are run by hand after a rule change and never in CI. And the
deck audit reads the file, so overflow and note collisions stay with the browser pass in
`references/deck-build-checklist.md`.

## Rule ownership and precedence

One rule, one home, and one tiebreak. The hub summarises the hard rules and owns none of them:
`sourcing-standard` owns the evidence rules, `deck-build` owns the copy rules. When a summary and its
owning skill disagree, the owning skill wins and the summary is the thing to fix. Restating a rule at
the point of use is allowed, and it is why several rules appear in more than one file; a restatement is
never allowed to become the authority.

## Naming

- The hub keeps the name students already invoke, so installed copies and the README install
  lines do not change.
- Section skills carry the `pitch-` prefix so a flat install cannot collide with anything else
  in a skills directory.
- Inside Claude Code, skills are namespaced: `/bison-fund-investment-analysis:pitch-valuation`.

## Versioning

There is none, on purpose. Manifests carry no `version`, so both harnesses track the newest commit
and a change reaches everyone on their next update. Add a version to the one manifest a harness reads
only if pinned releases ever become necessary; a version that has to be bumped in four files is a
maintenance trap that fails silently.
