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
- Any edit to an existing deck. Both audits run again after the change.

## The deck standard

Fixed, not a menu. Every Bison Fund deck follows `references/deck-standard.md`: the five-section arc
with dark section dividers, roughly 30 to 41 slides, chart-led analytical slides, a Recommendation
slide, bull and bear cases, a risk matrix, an investment-thesis slide with three evidence-backed
pillars, a verification slide with sign-off blanks, and a sources slide. A deck under 25 slides is
under-built.

Start from `templates/deck-skeleton.html` styled with `templates/deck-house.css`. The standard is
stated slide by slide, with what each slide has to carry, in `references/deck-standard.md`.

## Prerequisites

- Python 3 with the standard library only, for `scripts/deck_audit.py`. No packages to install.
- A browser, to open a deck in the harness and run the render pass in
  `references/deck-build-checklist.md`.
- The fact sheet for the pitch, because no figure enters a slide without a source and an as-of date.

## Build order, cheapest first

1. **HTML deck.** Drop in the token file, build each slide as a component. Most control; present live
   or export to PDF.
2. **PowerPoint or Google Slides.** Set theme colors to `#00583D` primary, `#FFC425` accent, `#282C2F`
   text, `#F2F3F3` background, and use the font substitutes listed in the brand file.
3. **Docs and handouts.** Same palette and fonts in Word, Docs, or Notion.

## Writing rules, every deck, handout, and export

The 27 rules that keep deck copy plain are in `references/writing-rules.md`. Load that file on any
content edit, which is any edit that changes words a reader will see. The numbering is stable, so
cite a rule by number rather than restating it.

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

- `references/deck-standard.md`, the house bar: the slide inventory with what each slide must carry,
  the design system, the conventions, and the workflow.
- `scripts/deck_audit.py`, the static audit of a deck file: slide structure, footers, one title
  element, charts, harness wiring, and the mechanical copy rules. It exits non-zero on findings and
  takes `--json` so a review agent can cite the same output. Run it before the browser pass.
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

A deck that meets the standard, exits clean on `scripts/deck_audit.py`, renders correctly in the
harness, passes the browser pass, and reads as plain copy with no AI-writing tells.
