---
name: bison-fund-investment-analysis
description: Guide equity-pitch research with Socratic gates and sources.
version: 1.0.0
author: Jacob Radke, Hermes Agent
license: MIT
metadata:
 hermes:
  tags: [equity-research, investing, bison-fund, citations, socratic]
  related_skills: [grounded-citations]
---

# Bison Fund Investment Analysis

A research discipline for building an equity pitch, built for the NDSU Bison Fund and
anyone learning to do equity research with an AI assistant. It works the same whether
you run it in Claude Code, Codex, Cowork, Hermes, or a plain chat window.

This skill is deliberately **not** a stock screener, a stock picker, a price-target
generator, or investment advice. It refuses to do the parts that are the analyst's job.
The point is to help you think critically and analyze faster, not to hand you an answer.

## Prime Directive

Two rules govern everything the assistant does inside this skill:

1. **Think first, draft second.** The assistant asks the analyst before it researches,
  and the analyst answers before the assistant drafts. (Socratic gate.)
2. **Every number has a source.** Every figure, claim, and estimate carries a source
  and an as-of date, or it is flagged and cannot enter the pitch. (Evidence gate.)

The analyst owns the judgment calls: the price target, the thesis pillars, the
recommendation, and the confidence behind them. The assistant never writes those.

## When to Use

- An analyst or student is researching a company for an equity pitch.
- A Bison Fund member is building or updating a pitch deck.
- Someone wants to pressure-test an existing thesis with sourced evidence.

Don't use for: quick price quotes, order execution, portfolio management, tax or
personal financial advice, or anything where a citable source cannot exist.

## Prerequisites

- A company name and ticker.
- Web access (the assistant's, or the analyst's own filings, transcripts, and data).
- This skill's reference files, or the analyst's judgment about what a complete pitch needs.
- Data sources the pitch will cite: SEC filings (10-K, 10-Q, 8-K, proxy), earnings calls
  and investor presentations, company IR pages, and reputable market-data providers
  (e.g. Financial Modeling Prep).
- **The fund's valuation method is DCF.** The build guide is `references/dcf-method.md` and the
  working implementation is `scripts/fmp_dcf.py` (FMP inputs, sensitivity grid, math verified offline).
- **Bloomberg Terminal access:** there is no public or free Bloomberg market-data API. BLPAPI, the
  Python `blpapi`/`xbbg` wrappers, and Excel `=BDP()`/`=BDH()` all require a logged-in terminal and
  entitlements on the calling machine. Treat Bloomberg as the terminal-side source for analysts who
  have access, and FMP as the automatable path. Never write a Bloomberg login into a script or deck.

### API keys (FMP and similar)

Market-data keys are **per-analyst** and read from the environment, never hardcode a key
in a skill file, deck, template, or handout, and never paste one into a chat transcript.

- Each analyst stores their own key as an exported `FMP_API_KEY` environment variable, or
 in a local secrets file with `chmod 600`. `scripts/fmp_dcf.py` reads `$FMP_API_KEY` first,
 then `~/.hermes/secrets/fmp_api_key` and `~/.config/fmp/api_key`.
- Code that calls the API reads the key at runtime and prints only success/failure, 
 the key itself never appears in tool output or delivered work.
- A shared fund-wide key will hit FMP's free-tier rate limits (~250 calls/day); plan for
 one key per student.
- If a key has been exposed in a transcript or a shared file, treat it as compromised:
 rotate it in the provider dashboard.

## The Gated Loop

Eight phases plus intake. **Do not skip forward.** Each phase ends with a completion criterion
the analyst can check before the next phase starts. Phases 2, 5, and 6 are owned by the analyst,
not the assistant. The review agent (Phase 7) reruns on every change to the deck, however small.

### Phase 0, Intake

Collect: company name, ticker, exchange, and one sentence on why the analyst is interested.
No thesis yet. The analyst has not researched anything at this point, so an opinion formed now
is a guess. Write the one-liner down and move on; the real thinking happens in Phase 2.
*Done when:* the analyst has stated a company and an interest in their own words.

### Phase 1, Grounding (sub-agent lanes, runs before any thesis exists)

Collect what the business, the street, and the news have independently said. Four lanes:
business reality (transcripts and filings), news flow (trailing 6 to 12 months, dated), peer
intelligence (the two or three closest competitors), and market view (consensus, targets,
valuation commentary). Each lane returns one cited digest; no thesis, no judgment.

Run the lanes as parallel sub-agents when the harness has them; otherwise sequentially.
**Read order for the analyst:** business reality first, then news and peers, then the market
view digest last, so the analyst forms a view from the record before seeing what the street
concluded. The analyst reads and merges: deduplicate, tag the three voices, and turn contested
claims into questions for Phase 2.
Full briefs, contracts, and merge rules: `references/grounding-method.md`.
*Done when:* four digests exist, every line is cited and labeled, and the analyst has read and
merged them.

### Phase 2, Socratic Gate (analyst-led, now informed)

With the grounding digests read, ask the analyst the intake questions from
`references/socratic-question-bank.md` (what does the business do; where does the money come
from; who is the customer; what does the market misunderstand; what would have to be true;
what would make you wrong; where do you land and how confident).

The answers are now hypotheses about a company the analyst has studied, not guesses about a
name they just picked. The assistant does not answer them. The thesis, the kill condition, and
the prior stated here are what the rest of the loop tests. If a digest contradicts an answer,
that contradiction is written down, not smoothed over.
*Done when:* the analyst has written a first-pass belief for each question.

### Phase 3, Gap-Fill

Grounding already produced the evidence base, so this phase is only what the thesis still needs:
the specific figures, comparisons, or statements the Phase 2 hypotheses depend on that the digests
did not cover. Nothing else. Open-ended collection belongs in Phase 1, not here.

Every figure carries its tag in this exact shape, in the working fact sheet:

```
<value>, source: <document/site + link>, as-of: <date>, [fact | estimate | opinion]
```

Anything that cannot be sourced is `[UNVERIFIED]`. `[UNVERIFIED]` items may exist in working notes
but **may never appear in the final pitch.**
*Done when:* every claim the thesis rests on resolves to a source and a date, and nothing was
collected that no hypothesis asked for.

### Phase 4, Section Drafts (deck order)

Draft the five sections in this fixed order: **Business → Competition → Key Deals →
Financials → Valuation.** Follow `references/section-method.md` for what each section
requires and which deck slides it feeds. At the end of each section, list the judgment
calls the analyst still owns (price target, thesis pillars, recommendation strength) and
leave them blank.
*Done when:* all five sections are drafted and every open judgment call is explicitly listed.

### Phase 5, Red-Team (analyst-led)

Before the bull case is final, the assistant must argue the bear side: the strongest
case against the thesis, the assumptions that could break it, and a probability × impact
risk read. The analyst responds and decides which risks are real.
*Done when:* the bear case exists in writing and the analyst has ruled on each risk.

### Phase 6, Verification Pass (analyst-led)

Run the checklist in `references/citation-rules.md`. Reopen every source, confirm every
number against the original, confirm no `[UNVERIFIED]` leaked into the deck, and confirm
every judgment call is the analyst's own. The analyst signs off.
*Done when:* the analyst has personally verified every figure and signed off.

### Phase 7, Review Loop (sub-agent, reruns on every change)

After every change, an independent review agent re-checks the deck: fact audit (every figure
resolves to the fact sheet with a matching source and date), chart audit (SVG values match the
fact sheet), quote audit (attributed text appears near-verbatim in a cited source), rule audit
rule audit (the mechanical writing rules), consistency audit (no slide contradicts another), the
structural browser audit, and the AI-writing audit (no AI-ism tells in slide copy, per
`references/ai-writing-check.md`). It writes findings by slide and region, severity-tagged; the author
fixes blockers, waives minors in writing, and the loop reruns until clean.

The review agent must not have written the deck it reviews, does not rewrite anything, does not
re-litigate the thesis, and does not approve the deck: a clean review is the trigger for the
analyst's own Phase 6 sign-off, not a substitute.
Full brief and contract: `references/review-agent.md`.
*Done when:* zero blockers, every minor fixed or waived, and the browser audit passes.

### Phase 8, Pitch-Ready Map

Map the finished work onto the deck's slide structure so it drops straight into the
pitch template. Flag any slide still missing its evidence.
*Done when:* every slide is either evidence-backed or flagged as open.

## Hard Rules (Non-Negotiable)

1. **Never invent a number.** No plausible-looking figures. If it cannot be sourced, it
  is `[UNVERIFIED]` and stays out of the pitch.
2. **Never generate the price target, the thesis pillars, or the recommendation.** Those
  are the analyst's. The assistant may present the inputs and the range; the analyst picks.
3. **Every figure carries a source and an as-of date.** No exceptions.
4. **Label fact / estimate / opinion** on every claim.
5. **The bear case is mandatory** before the bull thesis is considered finished.
6. **The analyst signs off**, not the assistant. The assistant's draft is a draft.

## Writing Rules (every deck, handout, and export)

Plain copy is the standard. Clever is the failure mode.

1. **Zero em dashes.** Use commas or periods. No exceptions, including quotes and footers.
2. **Zero middle-dot separators.** Use commas, periods, or separate lines.
3. **Plain titles that name the subject:** "Executive Summary", "Key Risk", "Recommendation".
  No "headline, tagline" pairs and no clever framings ("the one-slide case for", "the call").
4. **Only say what needs to be said.** Cut meta-commentary and adjective stacks
  ("in the analyst's words", "argued in good faith"). The evidence speaks; the deck does not narrate itself.
5. **Subtitles state the point in one plain sentence** or are deleted.
6. **The fund or company name appears once per slide**, in the footer. Never repeat it in the
   eyebrow or the title.
7. **The eyebrow never repeats the slide title.** If it would, delete the eyebrow.
8. **No process or method references in deck copy.** No "Phase 1", no naming the skill, no
   narrating the workflow on a slide.
9. **Never quote the analyst.** The thesis, pillars, and risks are stated plainly in the
   presenter's voice: no quotation marks, no attribution lines, no "in the analyst's words".
   The presenter owns them, so saying so is redundant.
10. **Source quality.** Cite primary filings, company IR, or established financial data
    providers (e.g. FMP, exchange data). Aggregator blogs and newsletters (ad-hoc-news.de,
    Substack recaps, aggregator stock pages) are not acceptable. If the only source is one of
    those, mark the figure pending and keep it off the slide.
11. **No method jargon in presented copy.** "derived", "estimate", "company-stated", and
    "[UNVERIFIED]" live in the fact sheet, not on slides.
12. **Brand blocks use the light treatment:** accent-tint fills with dark green text, not
    heavy full-green fills.
13. **The analyst's name does not appear in deck copy.** The recommendation needs no
    attribution; the presenter is the analyst. The only place a name appears is the sign-off
    line on the verification slide.
14. **No housekeeping lines on slides.** No "market data pending", no "FMP refresh", no
    data-source caveats, no "pending key" notes. Provenance lives in the sources slide and
    the fact sheet; if a figure is not confirmed, it is left off the slide.
15. **Subheadlines only when they add information.** If the title already says it, delete the
    subtitle. A bare slide title is fine. Do not write a subtitle to fill space.
16. **Summary boxes use one standard label: "Key takeaway".** No invented labels ("what the
    KPIs say", "why the gap matters"). The box contents are simple and repeatable, so a reader
    learns the pattern once.
17. **No acronyms.** Spell it out: gross bookings, not GB. Year over year, not YoY. Autonomous
    vehicle, not AV. Monthly active consumers, not MAPC. Free cash flow, not FCF. Discount rate,
    not WACC. GAAP and non-GAAP are the exception, as standard accounting terms.
18. **Nothing ambiguous.** State the actual policy or figure. "A $7B repurchase authorization in
    February 2024 and a $1.5B accelerated repurchase in January 2025", never "Ongoing".
19. **Charts must be readable.** Bars need real height and labeled values. A chart nobody can
    read is worse than no chart.
20. **The price target comes from the fund's discounted cash flow model, not from consensus.**
    Consensus is a cross-check and belongs in the takeaway text, never in the price-target box.
21. **Every value on a slide is an actual reported or computed figure.** No process language on
    data cards ("stated before research", "the analyst confirms"). The recommendation slide
    carries the current price, not a confidence score.
22. **Charts are drawn, not decorated.** Use SVG with labeled bars and values; the financial
    analysis section is chart-led: a chart per slide with a Key takeaway, not paragraphs of text.
23. **No confidence scores.** The recommendation is BUY, HOLD, or SELL. Conviction is shown by
    the quality of the argument, not a number next to it.
24. **Fresh prices only.** The current price is the most recent trading figure, not a stale
    snapshot carried across slides. Refresh it the day of the presentation.
25. **Structural consistency.** A new slide never introduces a layout pattern the other slides
    do not share. Same header treatment, same card grid language, same footer, same spacing.
    Section eyebrows follow their section: Overview slides have none, section slides carry the
    section label. Review a new slide against its neighbors before it enters the deck.
26. **Every deck must render correctly in the harness format, first time.** Follow
    `references/deck-build-checklist.md` and run its browser audit before handing the deck over.
    A deck is not delivered until the audit reports no overflow, no note collisions, charts with
    real bar heights, working screen switching, a working Download PDF, one title element on the
    title slide, and footers that match the real slide count.

27. **No AI-writing tells in slide copy.** No significance inflation, superficial -ing tack-ons,
signposting, generic positive conclusions, negative parallelism, forced metaphor, or rule-of-three
padding. This is the build-side rule; the review agent runs the full list as the AI-writing audit in
`references/ai-writing-check.md`. Deck copy states evidence plainly and does not perform a voice.

This rule applies to produced materials (decks, handouts, PDFs, exports). Working notes
and fact sheets may keep their internal tag formats.

## Reference Files

- `references/section-method.md`, required elements per section, deck slide mapping, and
 the judgment calls the analyst owns.
- `references/socratic-question-bank.md`, the Phase 1 and Phase 4 question sets.
- `references/citation-rules.md`, the evidence standard and the Phase 6 verification checklist.
- `references/worked-example-hood.md`, the Robinhood (HOOD) pitch as a described example; no HOOD
 deck file ships with this skill. The accessible reference decks are the Uber pitch (41 slides,
 October 2026) and the Alphabet pitch (23 slides). See `references/deck-standard.md` for the bar.
- `templates/pitch-outline.md`, a blank section skeleton to fill for a new name.
- `references/brand-and-design-tokens.md`, NDSU Bison Fund palette, type, and shadcn token mapping.
- `templates/ndsu-design-tokens.css`, drop-in shadcn/Tailwind v4 token file in NDSU brand colors.
- `references/design-tokens-preview.html` — self-contained visual board of the tokens, both themes.
- `references/dcf-method.md` — how to build the DCF: inputs, WACC, terminal value, bridge, sensitivity.
- `references/deck-build-checklist.md` — the harness render rules, the PDF wiring, chart sizing, and the browser audit.
- `references/fmp-api-docs.md` — the official FMP API documentation, shipped with the skill.
- `references/bloomberg-terminal.md` — Bloomberg path for terminal users, with the API library link.
- `references/review-agent.md` — Phase 7: the review agent brief, its seven checks, and the loop protocol.
- `references/ai-writing-check.md` — the AI-ism tells to flag in deck copy, and how the review agent runs the check.
- `references/grounding-method.md` — Phase 1: the four grounding lanes, sub-agent briefs, and merge rules.
- `references/creative-slides.md`, optional slides (the big vision, bottom-up TAM, the bear debate,
 scenarios, and more) that let a pitch differ creatively while keeping the evidence standard.
- `references/deck-standard.md`, the house bar for a pitch deck: the full slide inventory, the design
 system, the conventions, and the build workflow. Every deck meets this standard.
- `templates/deck-house.css`, the shared deck stylesheet (the fund's design system). Paste it into the
 deck's `<style>`.
- `templates/deck-skeleton.html`, a ready-to-fill deck shipping the full standard slide inventory with
 correct footers. Start here, then wrap it in the commentable harness.
- `scripts/fmp_dcf.py` — DCF from FMP data. `--demo` verifies the math offline; live mode reads the key at runtime.

## Design & Presentation Materials

A pitch gets presented, so the final artifact should look like the fund, not a generic
template. When the analyst is ready to build the deck or handout:

**The deck standard is fixed.** Every Bison Fund deck follows `references/deck-standard.md`: the
five-section arc with dark section dividers, roughly 30 to 41 slides, chart-led analytical slides, a
Recommendation slide, bull and bear cases, a risk matrix, an investment-thesis slide with three
evidence-backed pillars, a verification slide with sign-off blanks, and a sources slide. Start from
`templates/deck-skeleton.html` styled with `templates/deck-house.css`. The reference decks are the
Uber pitch (41 slides) and the Alphabet pitch (23). A deck under 25 slides is under-built.

- Brand palette, typefaces, and the shadcn/ui token mapping: `references/brand-and-design-tokens.md`.
- Drop-in stylesheet: `templates/ndsu-design-tokens.css`, paste into a shadcn/Tailwind v4
 global CSS, then style with `bg-primary`, `text-foreground`, `bg-ndsu-yellow`, etc.
- Visual token board: `references/design-tokens-preview.html`, open in a browser to see the
 palette, both themes, typography, components, and chart colors rendered. Show it to analysts
 before a deck build so they see the target look.
- **Commentable review harness:** `templates/commentable-deck-harness.html`, the
 `design-mockup` review harness rebranded on the Bison Fund tokens. Wrap any deck in it:
 one screen per pitch section, every commentable element gets a `data-region`, then the
 analyst/product owner toggles Comment mode (or presses `c`), drops numbered pins with
 notes, and **Copy feedback** exports everything as markdown grouped by screen. Comments
 persist in localStorage under a per-deck STORE key, change it per deck.

Workflow for a pitch deck review:
1. Build the deck as normal HTML slides using the token file.
2. Wrap it: copy the harness, put the slides into `<section class="mock-screen" data-screen="...">`
  blocks (Overview + one per pitch section), annotate `data-region` on slides and key cards/tables.
3. Hand it to the reviewer; they comment in the browser and paste the exported markdown back.
4. Fix by region name, re-running a review round keeps old comments anchored, because
  comments store the region *name*, not coordinates of the element.

The harness bar includes a **Download PDF** button: it opens the browser print dialog with
`@page` set to 1280×720 (16:9), so every page of the exported PDF is exactly one slide, 
comment pins and harness chrome are hidden in print. No server or converter needed.

Build order, cheapest first:
1. **HTML / shadcn deck**, scaffold shadcn, drop in the token file, build each slide as a
  component. Most control; present live or export to PDF. See `design-mockup` and
  `shadcn-design-system`.
2. **PowerPoint / Google Slides**, set theme colors to `#00583D` (primary), `#FFC425`
  (accent), `#282C2F` (text), `#F2F3F3` (background) and use the font substitutes listed.
3. **Docs / handouts**, same palette and fonts in Word, Docs, or Notion.

Design guardrail: colors mirror the NDSU College of Business / Bison Fund site. The NDSU
name and marks follow university brand rules, use them as the fund's own materials permit,
and never invent or recolor a mark.

## Pitfalls

- **Drafting before the Socratic gate.** The most common failure. If the analyst has not
 answered Phase 1, stop and ask again, do not fill the silence with research.
- **Numbers that "look right."** Market data drifts. A figure without an as-of date is
 worthless in a pitch. Always date it.
- **Sourcing to a blog that sources a filing.** Cite the filing. Go to the primary source.
- **Letting the assistant pick the price target** because the analyst is unsure. That is
 hiding, not analyzing. The analyst picks and owns it.
- **Treating a forecast as a fact.** Revenue projections, TAM, and CAGR callouts are
 estimates. Label them.
- **Bull-case-only decks.** If there is no bear case, the pitch is incomplete regardless
 of how good the story sounds.
- **Keys in artifacts.** An API key pasted into chat, hardcoded in a deck, or committed to a
 template is compromised the moment it is shared. Environment variable or secrets file only.
- **A dead Download PDF button.** The harness needs the button, the print stylesheet, and a click
 handler that calls `window.print()`. Ship all three, then verify by intercepting `window.print`.
- **Stacked screens.** If `.mock-screen` lacks `display:none` and `.cx-active` lacks
 `display:flex`, every screen renders at once and the bar buttons look broken.
- **Charts that overflow.** An SVG with a wide viewBox and no `max-width` scales to the card width
 and runs off the slide. Cap it, and build column charts with a column-sized viewBox.
- **A secrets file that is not the bare key.** The stored key may be a dotfile (`.fmp_api_key`) and
 may hold a `FMP_API_KEY=...` line rather than the value alone. Code that reads the file must try
 both the documented path and the dotfile, and strip a leading `VAR=` prefix, or every call 401s
 with "Invalid API KEY" while the key is in fact fine. Diagnose by testing one `stable/` call before
 blaming the key or rotating it.
- **A fixed-horizon DCF truncates a compounder.** A five-year window with a terminal growth ceiling
 near 2.5% will value a fast grower far below its market price, because the market capitalizes a much
 longer runway than the model's window. That gap is a finding, not a bug: state it plainly, show the
 sensitivity grid, run a reverse DCF for what the price implies, and record every model run
 (inputs, case outputs, grid) in a dated model record beside the fact sheet so each slide figure
 resolves to a source. Justify chart bar heights proportional to value, not roughly ascending.
- **A recommendation label that fights its target.** A HOLD with a price target far below the traded
 price (or a BUY with one far above) reads as the opposite call and a reviewer will flag it. Make the
 label and the target agree, or state in one plain line why the position is held against the target.

## Verification Checklist

Before the pitch is considered done:

- [ ] The analyst answered the Phase 2 Socratic questions in their own words.
- [ ] Grounding digests exist for all four lanes, every line cited and labeled, merged by the analyst.
- [ ] The review agent's last run shows zero blockers, minors fixed or waived in writing, and the deck was re-audited after the final change.
- [ ] The deck passed the AI-writing audit: no significance inflation, signposting, generic positive conclusions, or negative parallelism in slide copy.
- [ ] Every figure has a source and an as-of date.
- [ ] Every claim is labeled fact, estimate, or opinion.
- [ ] No `[UNVERIFIED]` items appear anywhere in the deck.
- [ ] The price target, thesis pillars, and recommendation are the analyst's own.
- [ ] A written bear case exists and the analyst has ruled on each risk.
- [ ] The analyst has personally reopened and confirmed every source.
- [ ] Zero em dashes and zero middle-dot separators anywhere in the deck; every title is plain.
- [ ] The fund or company name appears once per slide; no eyebrow repeats its slide title.
- [ ] No quoted analyst text and no process or method references in the deck copy.
- [ ] Every source is a filing, company IR, or established data provider. No aggregator blogs.
- [ ] The analyst's name appears only in the sign-off line; no housekeeping or pending-refresh notes on any slide.
- [ ] No acronyms anywhere in deck copy; every figure is specific, with no vague descriptors.
- [ ] Summary boxes all read "Key takeaway"; charts render readable bars; the price target is the DCF value.
- [ ] Charts are SVG with labeled bars; the financial slides are chart-led with a takeaway each.
- [ ] No slide introduces a layout pattern its neighbors do not use; eyebrows match section convention.
- [ ] The deck-build browser audit passes: no overflow, no note collisions, bars render, screens switch, PDF prints, one title, correct page count.

## Using This in Your Tool

This skill is plain markdown on purpose so any agent can run it.

- **Claude Code / Codex / Cowork / Hermes:** install this folder into the tool's skills
 directory and invoke it by name (`bison-fund-investment-analysis`). The YAML frontmatter
 at the top is what those loaders read. Per-tool install commands are in the repository's
 README.
- **Plain chat (ChatGPT, Claude web, Gemini):** paste the body of this file, and the
 relevant reference file, as a custom instruction or the first message, then name your
 company and why it interests you.
- **Anywhere:** the reference files work on their own as reading material for a new analyst.
