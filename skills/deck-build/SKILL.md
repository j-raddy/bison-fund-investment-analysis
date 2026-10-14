---
name: deck-build
description: "Use when building or changing a Bison Fund pitch deck: the deck standard, the writing rules, the tokens, the templates, and the render audit."
author: Jacob Radke
license: MIT
---

# Deck Build

The house standard for a Bison Fund pitch deck, and the rules that keep deck copy plain. A pitch gets
presented, so the final artifact looks like the fund, not a generic template.

## Triggers

- The hub routes Phase 7 or Phase 8 here, or a request to build, restyle, or fix a deck.
- Any edit to an existing deck. The render audit runs again after the change.

## The deck standard

Fixed, not a menu. Every Bison Fund deck follows `references/deck-standard.md`: the five-section arc
with dark section dividers, roughly 30 to 41 slides, chart-led analytical slides, a Recommendation
slide, bull and bear cases, a risk matrix, an investment-thesis slide with three evidence-backed
pillars, a verification slide with sign-off blanks, and a sources slide. A full-arc deck under 25
slides is under-built; the cited 23-slide Alphabet deck is the accepted short-form variant.

Start from `templates/deck-skeleton.html` styled with `templates/deck-house.css`. The reference decks
are the Uber pitch (41 slides) and the Alphabet pitch (23 slides).

## Build order, cheapest first

1. **HTML deck.** Drop in the token file, build each slide as a component. Most control; present live
   or export to PDF.
2. **PowerPoint or Google Slides.** Set theme colors to `#00583D` primary, `#FFC425` accent, `#282C2F`
   text, `#F2F3F3` background, and use the font substitutes listed in the brand file.
3. **Docs and handouts.** Same palette and fonts in Word, Docs, or Notion.

## Writing rules, every deck, handout, and export

Plain copy is the standard. Clever is the failure mode.

1. **Zero em dashes.** Use commas or periods. No exceptions, including quotes and footers.
2. **Zero middle-dot separators.** Use commas, periods, or separate lines.
3. **Plain titles that name the subject:** "Executive Summary", "Key Risk", "Recommendation". No
   headline and tagline pairs, and no clever framings ("the one-slide case for", "the call").
4. **Only say what needs to be said.** Cut meta-commentary and adjective stacks ("in the analyst's
   words", "argued in good faith"). The evidence speaks; the deck does not narrate itself.
5. **Subtitles state the point in one plain sentence** or are deleted.
6. **The fund or company name appears once per slide**, in the footer. Never repeat it in the eyebrow
   or the title.
7. **The eyebrow never repeats the slide title.** If it would, delete the eyebrow.
8. **No process or method references in deck copy.** No phase numbers, no naming the skill, no
   narrating the workflow on a slide.
9. **Never quote the analyst.** The thesis, pillars, and risks are stated plainly in the presenter's
   voice: no quotation marks, no attribution lines, no "in the analyst's words". The presenter owns
   them, so saying so is redundant.
10. **Source quality.** Cite primary filings, company investor relations, or established financial
    data providers. Aggregator blogs and newsletters are not acceptable. If the only source is one of
    those, mark the figure pending and keep it off the slide.
11. **No method jargon in presented copy.** "Derived", "estimate", "company-stated", and the
    unverified marker live in the fact sheet, not on slides.
12. **Brand blocks use the light treatment:** accent-tint fills with dark green text, not heavy
    full-green fills.
13. **The analyst's name does not appear in deck copy.** The recommendation needs no attribution; the
    presenter is the analyst. The only place a name appears is the sign-off line on the verification
    slide.
14. **No housekeeping lines on slides.** No "market data pending", no refresh notes, no data-source
    caveats. Provenance lives in the sources slide and the fact sheet; if a figure is not confirmed,
    it is left off the slide.
15. **Subheadlines only when they add information.** If the title already says it, delete the
    subtitle. A bare slide title is fine. Do not write a subtitle to fill space.
16. **Summary boxes use one standard label: "Key takeaway".** No invented labels. The box contents are
    simple and repeatable, so a reader learns the pattern once.
17. **No acronyms.** Spell it out: gross bookings, not GB. Year over year, not YoY. Autonomous vehicle,
    not AV. Monthly active consumers, not MAPC. Free cash flow, not FCF. Discount rate, not WACC. GAAP
    and non-GAAP are the exception, as standard accounting terms.
18. **Nothing ambiguous.** State the actual policy or figure. "A $7B repurchase authorization in
    February 2024 and a $1.5B accelerated repurchase in January 2025", never "Ongoing".
19. **Charts must be readable.** Bars need real height and labeled values. A chart nobody can read is
    worse than no chart.
20. **The price target comes from the fund's discounted cash flow model, not from consensus.**
    Consensus is a cross-check and belongs in the takeaway text, never in the price-target box.
21. **Every value on a slide is an actual reported or computed figure.** No process language on data
    cards ("stated before research", "the analyst confirms"). The recommendation slide carries the
    current price, not a confidence score.
22. **Charts are drawn, not decorated.** Use SVG with labeled bars and values; the financial analysis
    section is chart-led: a chart per slide with a Key takeaway, not paragraphs of text.
23. **No confidence scores.** The recommendation is buy, hold, or sell. Conviction is shown by the
    quality of the argument, not a number next to it.
24. **Fresh prices only.** The current price is the most recent trading figure, not a stale snapshot
    carried across slides. Refresh it the day of the presentation.
25. **Structural consistency.** A new slide never introduces a layout pattern the other slides do not
    share. Same header treatment, same card grid language, same footer, same spacing. Section eyebrows
    follow their section: overview slides have none, section slides carry the section label. Review a
    new slide against its neighbors before it enters the deck.
26. **Every deck must render correctly in the harness format, first time.** Follow
    `references/deck-build-checklist.md` and run its browser audit before handing the deck over. A deck
    is not delivered until the audit reports no overflow, no note collisions, charts with real bar
    heights, working screen switching, a working Download PDF, one title element on the title slide,
    and footers that match the real slide count.
27. **No AI-writing tells in slide copy.** No significance inflation, superficial -ing tack-ons,
    signposting, generic positive conclusions, negative parallelism, forced metaphor, or rule-of-three
    padding. This is the build-side rule; the review agent runs the full list as the AI-writing audit
    in `references/ai-writing-check.md`. Deck copy states evidence plainly and does not perform a
    voice.

These rules apply to produced materials (decks, handouts, PDFs, exports). Working notes and fact
sheets may keep their internal tag formats.

## Review harness and PDF

Wrap any deck in `templates/commentable-deck-harness.html`:

1. Build the deck as normal HTML slides using the token file.
2. Wrap it: copy the harness, put the slides into `<section class="mock-screen" data-screen="...">`
   blocks (overview plus one per pitch section), and annotate `data-region` on slides and key cards.
3. Hand it to the reviewer. They comment in the browser and paste the exported markdown back.
4. Fix by region name. Comments store the region name, not coordinates, so a re-review keeps old
   comments anchored.

The harness bar includes a **Download PDF** button: `@page` is set to 1280 by 720, so every page of
the export is exactly one slide, with comment pins and harness chrome hidden. No server or converter.

## Design materials

- `references/deck-standard.md`, the house bar: slide inventory, design system, conventions, workflow.
- `references/deck-build-checklist.md`, the render rules and the browser audit.
- `references/brand-and-design-tokens.md`, the palette, type, and shadcn token mapping.
- `templates/ndsu-design-tokens.css`, the drop-in token file for shadcn and Tailwind v4.
- `references/design-tokens-preview.html`, open in a browser to see the palette rendered; show it to
  analysts before a build so they see the target look.
- `templates/deck-house.css` and `templates/deck-skeleton.html`, the stylesheet and the starter deck.
- `templates/pitch-outline.md`, a blank section skeleton.

Design guardrail: the colors mirror the NDSU College of Business and Bison Fund site. The NDSU name
and marks follow university brand rules, and a mark is never invented or recolored.

## Pitfalls

- **A dead Download PDF button.** The harness needs the button, the print stylesheet, and a click
  handler that calls `window.print()`. Ship all three, then verify by intercepting `window.print`.
- **Stacked screens.** If the screen class lacks `display:none` and the active class lacks
  `display:flex`, every screen renders at once and the bar buttons look broken.
- **Charts that overflow.** An SVG with a wide viewBox and no `max-width` scales to the card width and
  runs off the slide. Cap it, and build column charts with a column-sized viewBox.
- **Bar heights that do not track the values.** Chart bars are proportional to value, not roughly
  ascending.

## Output

A deck that meets the standard, renders correctly in the harness, passes the browser audit, and reads
as plain copy with no AI-writing tells.
