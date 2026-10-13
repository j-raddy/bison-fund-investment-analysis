# AI-Writing Check (Phase 7, the AI-ism audit)

The mechanical rule audit catches dashes, acronyms, and process words. It does not catch prose that
reads machine-written. This check flags AI-writing tells in the deck and the analyst's written
materials, so a clean deck does not still read like a chatbot wrote it.

Source catalog: Wikipedia "Signs of AI writing" (WikiProject AI Cleanup), the `humanizer` skill's
34-pattern list, and `conorbronsdon/avoid-ai-writing`. The general profile's `humanizer` skill holds
the full catalog; this file is the subset that applies to a compliance-grade equity deck.

## Register note (read this first)

A pitch deck is not a blog post. The humanizer advice to add first person, opinions, humor, and
mixed feelings does **not** apply to deck copy. The writing rules forbid the analyst's name,
quotations, and meta-commentary, and a deck states evidence, it does not perform a voice. Apply
only the removal half here: strip the AI-isms. Voice belongs in the presenter's delivery, not on
the slides.

## The tells to flag in deck copy

1. **Significance inflation:** "stands as", "a testament to", "a pivotal moment", "underscores
the importance", "reflects broader", "setting the stage for", "marks a shift".
2. **Superficial -ing tack-ons:** "highlighting", "underscoring", "reflecting", "showcasing",
"contributing to", "ensuring", "symbolizing".
3. **Promotional language:** "vibrant", "robust" (figurative), "nestled", "in the heart of",
"groundbreaking", "renowned", "seamless", "best-in-class".
4. **Vague attribution:** "experts argue", "industry reports", "observers have noted", "analysts
suggest" when no named source follows.
5. **AI vocabulary:** "delve", "crucial", "landscape" (abstract), "tapestry", "interplay",
"intricate", "pivotal", "underscore", "showcase", "testament", "foster", "garner", "align with".
6. **Copula avoidance:** "serves as", "stands as", "functions as", "boasts", "features" where
"is" or "has" says it plainly.
7. **Negative parallelism:** "not just X, but Y"; "it is not about X, it is about Y"; tailing
negations ("no guessing").
8. **Rule-of-three padding:** forcing ideas into triples to sound comprehensive.
9. **False ranges:** "from X to Y" where X and Y are not on a real scale.
10. **Forced metaphor and figurative overwriting**, especially a metaphor explained right after use.
11. **Signposting:** "let us dive in", "here is what you need to know", "the takeaway here is" when
a Key takeaway box already says it.
12. **Generic positive conclusions:** "the future looks bright", "exciting times ahead", "well
positioned for growth", "a major step in the right direction".
13. **Dramatic fragmentation and punchy kickers:** subjectless fragments for emphasis, a quotable
line ending every section.
14. **Rhetorical questions answered immediately.**
15. **Sentence-opener tics:** "So,", "Look,", habitual "Notably / Importantly / Crucially /
Ultimately".
16. **Reassurance kickers:** "and that is okay", "no shame in".
17. **Marketing cliches:** "at the end of the day", "when it comes to", "in a world where",
"game-changer", "double down", "deep dive", "moving forward", "circle back".
18. **Formulaic challenge/prospect sections:** "faces challenges ... despite these challenges,
continues to thrive".
19. **Formatting artifacts:** emoji, curly quotes, title case in headings, inline-header bolded
lists.

## What does not apply here

- First person, opinions, humor, and "add soul" (delivery, not slides).
- Em dashes, middle dots, and acronyms, which the mechanical rule audit already covers.

## How the review agent runs it

- Read every slide's rendered copy: eyebrow, title, subtitle, cards, Key takeaway text, notes, and
tables.
- Flag each tell by slide and region, with a plain suggested rewrite.
- Severity: **BLOCKER** for significance inflation, signposting, generic positive conclusions, and
negative parallelism in slide copy (these read as machine-written); **MINOR** for single-word
substitutions (a stray "crucial" or "robust").
- A clean pass is one line saying so.

## Automated first pass (optional)

If your tool has the `avoid-ai-writing` skill installed, it ships a read-only detector that
scores text and prints JSON. Reduce the deck to its visible slide text first (strip the HTML
tags), then scan the text file:

```
node <avoid-ai-writing>/bin/avoid-ai-writing.js --context technical /tmp/deck-text.txt
```

Read the `score`, `issues`, and `document_classification` fields. A hit still must be judged in
context: the detector flags "landscape" inside the house slide titles ("Competitive landscape",
"Regulatory landscape"), which the standard fixes, so those are not violations. The list is a net,
not a verdict. A BMNR deck that passed every rule audit still scored 1 of 100 here, which is the
clean baseline to expect.
