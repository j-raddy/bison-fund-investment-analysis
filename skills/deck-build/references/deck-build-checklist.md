# Deck Build Checklist (commentable harness format)

Two passes, in this order. First `python3 scripts/deck_audit.py DECK.html`, which reads the file and
covers the slide structure, the footers, the title count, the charts, the harness wiring, and the
mechanical copy rules. It must exit 0. Then the browser pass below, which covers what a static read
cannot: overflow and note collisions.

The format is: one HTML file, slides in the Bison Fund design system, wrapped in the review harness
(`templates/commentable-deck-harness.html`). Every deck must render correctly in that format the
first time. This checklist is the difference between a deck that works and the bugs we hit:
stacked screens that never switch, a dead Download PDF button, double titles, wrong page counts,
and charts that blow the slide layout.

## The four canvas rules (the harness dies without these)

1. `#cx-stage { flex:1; min-height:0; display:flex; }` is required. Without it the stage does not
   become the scroll container and all screens stack into one long page.
2. `.mock-screen { display:none; flex:1; min-width:0; flex-direction:column; align-items:center; gap:26px; padding:26px; background:#DDE1E1; overflow-y:auto; }`
3. `.mock-screen.cx-active { display:flex; }` switches the visible screen. If both this and rule 2
   are missing, every screen renders at once and the bar buttons look broken.
4. Body stays `display:flex; flex-direction:column; overflow:hidden;` so the bar pins to the top and
   each screen scrolls independently.

## Download PDF needs three parts, not one

The button, the print stylesheet, and a click handler are separate. Shipping two of three produces a
button that does nothing, which is exactly what happened.

1. Button: `<button type="button" class="cx-btn" id="cx-pdf">Download PDF</button>` in the bar.
2. Print CSS:
   ```css
   @media print {
     @page { size: 1280px 720px; margin: 0; }
     html, body { height:auto !important; overflow:visible !important; display:block !important;
                  background:#fff !important; margin:0 !important; padding:0 !important; }
     #cx-bar, #cx-panel, #cx-pop, #cx-toast { display:none !important; }
     #cx-stage { display:block !important; overflow:visible !important; }
     .mock-screen { display:block !important; overflow:visible !important; background:#fff !important; padding:0 !important; gap:0 !important; }
     .slide { page-break-after:always; break-after:page; box-shadow:none; margin:0; }
     /* Print-safe: dark slides flip to light so nothing depends on Chrome's "Background graphics" */
     .slide.dark { background:#fff !important; }
     .slide.dark * { color:#003524 !important; }
     thead th { background:transparent !important; color:#003524 !important; border-bottom:2px solid #003524 !important; }
     .badge-buy { background:transparent !important; color:#003524 !important; }
     .cx-pin { display:none !important; }
   }
   ```
   **`margin:0 !important; padding:0 !important;` on html and body is load-bearing.** Without it
   Chrome applies its default 8px body margin inside the page box, which shifts every slide, clips
   the right edge, and pushes the remainder onto the next page so the PDF looks like alternating
   clipped halves and blank pages. This was the exact bug behind an "it downloaded and it's wrong"
   report. Do not drop it, and do not try to fix the symptom with `zoom` on `.slide`.

   **Dark slides print via one SVG rectangle each.** Chrome's print dialog leaves "Background
   graphics" off by default, and `print-color-adjust: exact` does not override it (verified). Flipping
   dark slides to light in print also fails the real requirement, which is that the PDF looks like the
   deck. So: inject one background layer per dark slide and let SVG carry the color, since SVG fills
   print in every mode.
   ```html
   <section class="slide dark">
    <svg class="print-bg" viewBox="0 0 1280 720" preserveAspectRatio="none"><rect width="1280" height="720" fill="#003524"/></svg>
   ```
   ```css
   .print-bg { display:none; }
   @media print {
     .print-bg { display:block !important; position:absolute; left:0; top:0; width:100%; height:100%; z-index:0; }
     .slide > *:not(.print-bg) { position:relative; z-index:1; }
   }
   ```
   Two gotchas, both hit in practice: the print rule needs `!important` (the screen rule for
   `.print-bg` sits later in the stylesheet and wins on equal specificity), and the cover slide's own
   text colors must stay white, which they do as long as the dark background layer is present.

   Ceiling: tinted card fills and table header fills still depend on the checkbox. Cards keep their
   colored borders in print, which reads as intentional, and chart bars are SVG so they always print.
   For full fidelity including tints, either tick "Background graphics" in the dialog or extend the
   same SVG layer trick to each tinted card.
3. Verify the real print output, not just print-media emulation in a viewport. Generate a PDF with
   Chrome's own pipeline and inspect it:
   ```python
   res = cdp('Page.printToPDF', printBackground=True, preferCSSPageSize=True,
             marginTop=0, marginBottom=0, marginLeft=0, marginRight=0)
   ```
   Expect: one page per slide, `/MediaBox [0 0 960 540]` (1280x720 CSS px), and no page whose
   content is a slice of a slide. Rasterize a couple of pages to be sure:
   `pdftoppm -png -r 96 -f 2 -l 2 deck.pdf /tmp/check` then look at the PNG. Viewer thumbnails can
   render blank even when the pages are fine, so rasterize before believing a thumbnail.
3. Handler, bound outside the harness IIFE:
   ```js
   var b = document.getElementById('cx-pdf');
   if (b) b.addEventListener('click', function () { setTimeout(function(){ window.print(); }, 250); });
   ```

Verify it by intercepting rather than opening a dialog in a test:
`window.print = function(){ called = true; }`, click `#cx-pdf`, assert `called`.

## Slide structure rules the renderer assumes

- One `<section class="slide">` per slide, in document order, each ending with a `.foot` carrying
  the page number. Divider and title slides use `<section class="slide dark">`.
- **Title slide carries exactly one title element.** A `slide()` helper that injects an `h2` plus a
  hand-written `h1` produces the double title. Check by counting the company name on slide 1.
- **Footers must state the real total.** After inserting a slide, renumber every footer from document
  order, never by hand. A deck showing "01 / 24" with 22 slides is a fail.
- Eyebrows: none on Overview slides, the section label on section slides, and never the slide title.

## Charts

- Charts are inline SVG, drawn by a helper, with labeled bars and real heights.
- **Cap the SVG**: `style="width:100%;max-width:560px;height:auto;display:block;margin:0 auto"`.
  Without a max-width a wide-viewBox chart scales to the card width and overflows the slide, which is
  the bug that produced charts "that look like absolutely nothing" and content running off the page.
- A chart in a narrow column needs a narrow viewBox built for that column, not a wide one shrunk.
- Bar geometry: keep the bars between an explicit top and bottom inside the viewBox, and place value
  labels above the bars with ~10px of clearance, or the numbers vanish.

## Verify with a browser pass (non-negotiable)

Open the file and run this, then fix everything it reports:

```js
(() => {
  const bad = [];
  const btns = [...document.querySelectorAll('#cx-screens button')];
  for (const b of btns) {
    b.click();                                  // measure each screen while it is ACTIVE
    [...document.querySelectorAll('.mock-screen.cx-active .slide')].forEach(s => {
      const c = s.querySelector('.content'); if (!c) return;
      const of = c.scrollHeight - c.clientHeight;
      const cc = c.getBoundingClientRect(), n = s.querySelector('.note');
      const nc = n ? n.getBoundingClientRect() : null;
      const bars = [...s.querySelectorAll('.bar .col')].map(x => Math.round(x.getBoundingClientRect().height));
      if (of > 2 || (nc && nc.height > 0 && nc.top < cc.bottom) || (bars.length && bars.some(h => h < 20)))
        bad.push({ screen: b.dataset.goto, page: s.querySelector('.pageno')?.textContent.trim() });
    });
  }
  btns[0].click();
  return { slides: document.querySelectorAll('.slide').length,
           screens: btns.map(b => b.textContent), problems: bad };
})()
```

Then confirm by hand: the bar renders, screens switch one at a time, Comment mode drops a pin and
persists across reload, `#cx-pdf` triggers print, and print media shows one slide per page with the
chrome hidden.

## Region annotation (what makes comments anchor)

- Every slide gets `data-region="sNN.slug"` on its `<section>`, with the slug derived from the slide
  title so it stays stable across rebuilds.
- Cards, tables, and panels inside `.content` get `data-region="sNN.rN"`.
- Comments store the region name, so a rebuild that keeps the region names keeps the feedback
  anchored.

## Lessons from build (hard-won)

- **Copy every slide figure from the model record, never retype or recompute it by hand.** A
  hand-typed DCF present-value row shipped a wrong number ($104M for a true $96M) and only the
  independent reviewer caught it. Generate slide numbers from the same script that prints the
  model record, so the deck and the record cannot drift.
- **One title element per slide, dividers included.** A slide helper that injects an `h2` when
  passed a title, plus a hand-written body `h2`, double-titles the section dividers. Never pass a
  title to the helper for a divider; keep only the single body `h2` next to the big section number.
- **A helper call inside a plain (non-f) string renders as literal source on the slide.** If a
  slide body calls `{card(...)}` or `{bar(...)}`, the string must be an f-string, or the braces
  print as text. Scan the built HTML for `{card(`, `{bar(`, `%s` before shipping.
- **The note-collision check must measure the last card, not the content box.** `.content` is
  `flex:1` and always reaches the note area, so `content.getBoundingClientRect().bottom` overlaps
  the note by design and the audit reports a permanent false positive. Compare the bottom of the
  last `.card` inside `.content` to the note top.
- **The harness brand label must be short and non-wrapping.** A long brand string wraps in the
  44px bar and collides with the screen buttons. Set it to a short deck code and add
  `white-space:nowrap`.
- **Spell out every market acronym, `mNAV` included.** Use "net asset value multiple". Region
  slugs, CSS comments, and the HTML `<title>` are not deck copy and may keep shorthand; rendered
  slide copy and notes may not. The rule audit greps the whole file, so a shorthand slug is a
  tolerated hit, not a deck-copy violation.
