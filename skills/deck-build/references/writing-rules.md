# Writing Rules

Every deck, handout, and export. Plain copy is the standard. Clever is the failure mode.

These live here so they load on a content edit rather than on every structural poke at a deck. The
numbering is stable: cite a rule by number, and never restate one anywhere else.

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
26. **Every deck must render correctly in the harness format, first time.** Run
    `scripts/deck_audit.py` on the deck, then run the browser pass in
    `references/deck-build-checklist.md`. A deck is not delivered until the audit exits 0 and the
    browser pass reports no overflow and no note collisions. The script reads the file, so it covers
    the slide structure, the footers, the charts, the harness wiring, and the mechanical copy rules;
    overflow and note collisions depend on layout and stay with the browser pass.
27. **No AI-writing tells in slide copy.** No significance inflation, superficial -ing tack-ons,
    signposting, generic positive conclusions, negative parallelism, forced metaphor, or rule-of-three
    padding. This is the build-side rule; the review agent runs the full list as the AI-writing audit
    in `references/ai-writing-check.md`. Deck copy states evidence plainly and does not perform a
    voice.

These rules apply to produced materials (decks, handouts, PDFs, exports). Working notes and fact
sheets may keep their internal tag formats.
