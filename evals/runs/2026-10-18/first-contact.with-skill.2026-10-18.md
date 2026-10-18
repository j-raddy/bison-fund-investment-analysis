# first-contact, with-skill

- prompt: hey i need to do my pitch on doordash for thursday, where do i start
- model: deepseek/deepseek-v4.1-flash-1017
- date: 2026-10-18

**Analyst.** hey i need to do my pitch on doordash for thursday, where do i start

_Assistant called load_skill {"name": "bison-fund-investment-analysis"}, 10635 characters returned_

_Assistant called load_skill {"name": "grounding-lanes"}, 3147 characters returned_

**Assistant.** Start at Phase 0: intake. Before any research, I need three things from you, in your own words.

1. **Company and ticker** — DoorDash, NASDAQ: DASH. Confirm that's the one you mean.
2. **One sentence on why you're interested.** Not a thesis — just what put DoorDash on your list. "It's the biggest delivery platform and I think the market is wrong about X" is a thesis; "I use it four times a week and I want to know if the economics work" is an intake note. Either is fine, but keep it to one sentence.
3. **How much time you actually have.** Thursday is the deadline, so tell me whether you're presenting a full pitch (all five sections plus a valuation and a deck) or a shorter version. That changes what we cut.

Once you answer those, here's the order we work in, and it's not negotiable on sequence:

- **Grounding (four lanes).** Business reality from filings and earnings calls, news flow over the last 6–12 months, peer intelligence from Uber/Delivery Hero/Grubhub's own filings, and the market view (consensus, price targets). Each lane cited and dated. You read business reality first, the street's view last — so you form your own read before you see what analysts concluded.
- **Socratic gate.** I ask you seven questions: what the business does, where the money comes from, who the customer is, what the market misunderstands, what would have to be true, what would make you wrong, where you land. I don't answer any of them. You write a first pass on each.
- **Gap-fill.** Only the specific numbers your hypotheses depend on.
- **Sections in fixed order.** Business, Competition, Key Deals, Financials, Valuation. Then the DCF.
- **Red team, verification, review, deck map.**

Two things to know now so they don't bite you Thursday:

- **Every number needs a source and an as-of date.** Anything I can't source gets tagged unverified and stays out of the deck. DoorDash is a company where the interesting numbers (order frequency, contribution margin per order, DashPass penetration) are spread across 10-K, 10-Q, and shareholder letters — so we'll be in the filings, not in blog posts.
- **The price target, thesis pillars, and recommendation are yours.** I'll build you the inputs, the DCF, and the range. I won't pick the number for you, and I won't write your thesis for you. That's the part you're being graded on.

One practical check: run `python3 setup.py` once in the package root if you haven't, so the machine knows which market data source to use. If it's not set up, we fall back to SEC filings, which is fine but slower.

Give me those three answers and I'll kick off the grounding lanes.

**Analyst.** DoorDash. It is a delivery network, mostly suburban United States, and I think it makes its money on restaurant commissions and advertising.

_Assistant called read_skill_file {"skill": "grounding-lanes", "path": "references/grounding-method.md"}, 5114 characters returned_

_Assistant called load_skill {"name": "sourcing-standard"}, 3343 characters returned_

**Assistant.** Good — that's enough to start, with two flags.

**Flag one: what you gave me is a set of claims, not a reason for interest.** "Mostly suburban US" and "makes its money on restaurant commissions and advertising" are testable statements about the business. I'm writing them down as hypotheses, not facts, and the grounding lanes will check them. That matters because if either is wrong, your thesis changes shape. Two things I'd want you to be ready for: DoorDash reports revenue in segments and geographies, so "mostly suburban US" needs a definition before it can be checked, and the company has been pushing beyond restaurants (grocery, retail, convenience) plus a logistics/white-label business. Whether those are material yet is exactly what the filings answer. Don't defend the claim yet — let the record come in first.

**Flag two: you didn't answer the scope question.** Thursday is the deadline and I don't know if you're doing a full pitch or a short one. That's the one thing blocking me, because it decides whether we run all four grounding lanes or cut to two.

Here are the four lane briefs. These are fixed regardless of scope, so you can start pulling sources now.

**Lane 1 — Business reality.** What management has said, guided, and shipped. Sources: latest 10-K, the last two or three 10-Qs, the shareholder letter and earnings call transcript for the last two quarters, the investor presentation. Pulls: revenue by segment and geography, orders, marketplace GOV, contribution profit, adjusted EBITDA, take rate, advertising revenue if disclosed, and what management guided for next quarter. Every line tagged with source and as-of date.

**Lane 2 — Market view.** Consensus revenue and EBITDA estimates, price target range and dispersion, ratings, and the two or three dominant street narratives. Read this one **last**, after the other three. That ordering is deliberate: I want you to have your own read before you see what analysts concluded, so your pitch is a position and not an echo.

**Lane 3 — News flow.** Trailing 6–12 months, every item dated. Deals, regulatory moves (this is a company with real classification and labor questions in multiple jurisdictions), executive changes, litigation, product launches. Dated items only — an undated news list is unusable in a pitch.

**Lane 4 — Peer intelligence.** Uber (delivery segment), plus one or two of Grubhub/Just Eat Takeaway and Delivery Hero. One page each, from each peer's own filings, on the metrics that matter: order growth, take rate, delivery margins. Not coverage volume — the numbers.

One practical constraint you need to know now: I can't pull filings or market data myself in this session — I don't have web or data access here. So either you run these lanes in a tool that does, or you bring me the documents (10-K, 10-Qs, transcripts, investor deck) and I'll build the cited digests with you. The second path is slower but it puts you in the filings, which is where the gradeable insight usually is.

Tell me the scope, and how you want to handle sourcing, and we'll go.

**Analyst.** The customer is two people at once: the consumer who orders and the restaurant that pays for demand.

**Assistant.** That's a better answer than the last one, and it's the right shape of answer — a two-sided market is the correct frame for a marketplace, and "the restaurant pays for demand" is a testable claim about who bears the cost of the network. Keep it.

Three things before you go further.

**One: it's probably three people, not two.** You've named the consumer and the restaurant. The courier is the third side, and it's the one that decides whether the network works — supply density sets delivery times, delivery times set consumer willingness to pay, and courier pay is the largest variable cost in the model. So the question isn't "who is the customer," it's "who has pricing power, and who absorbs the cost when the network needs to grow." That's a much harder question and it's the one your pitch will live or die on. Don't answer it now — but put it on the list. Check the filings for how the company discloses its courier base and courier pay, because that's where the answer sits.

**Two: "the restaurant pays for demand" is contested, not settled.** Restaurants pay commission; consumers pay delivery and service fees; the split between them, and whether advertising is now a bigger lever than commission, is empirical. It also differs by market and by merchant size. This is exactly the kind of claim that should go into grounding as a question rather than into a slide as a fact. If the record shows advertising is carrying more of the economics than commission, your customer definition needs revising — and that revision is the interesting part of the pitch.

**Three: you're answering the wrong phase.** I asked the customer question in the Socratic gate, which comes *after* grounding, for a reason. Right now you're reasoning from what you already believe, and what you already believe is a set of untested claims. That's how a pitch becomes a defense of a hunch instead of a read of the record. I'm not going to stop you from thinking — but I'm going to hold your answer as a draft and re-ask it once the digests are in. If the record contradicts it, we write the contradiction down rather than smoothing it over.

**Still blocking, and now it's blocking twice:** you haven't told me the scope, and you haven't told me how we're sourcing. I have no web or data access in this session. So I need one of two things from you:

- **Scope:** full pitch (five sections, DCF, deck) or a shorter version? Thursday is close and this changes what we cut.
- **Sourcing:** either you run the four lanes in a tool that can reach filings, or you drop the 10-K, the last two 10-Qs, the two most recent earnings transcripts, and the investor deck into this conversation and I'll build the cited digests with you line by line.

Give me those two and I'll start on Lane 1. Until then I'm collecting your hypotheses in a working file, tagged as unverified, and nothing from them goes near a slide.

**Analyst.** I think the market treats it as a low-margin delivery company and misses how much of the profit is advertising.

**Assistant.** Now you've stated a thesis. That's the first real thing you've given me, and it's a genuine one — "the market is mispricing the mix" is a legitimate pitch shape. But it's also the most common version of this argument, so before you build on it, four things.

**It's testable, which is good.** Advertising revenue is disclosed, commission/take rate is disclosed, and adjusted EBITDA is disclosed. So "how much of the profit is advertising" is answerable from filings, not a matter of opinion. That's what makes it a pitch rather than a hunch.

**But "the market misses it" is the claim most likely to be wrong.** Sell-side analysts covering this name model advertising explicitly, and it's been a talking point on calls for several quarters. So the honest version of your thesis probably isn't "nobody sees the ad business" — it's "the street sees it and still applies a multiple to the whole thing that implies it doesn't believe the ad margin is durable." Those are different theses with different evidence requirements. The second is stronger and much harder to knock down. You need to find out which one is true before Thursday, and that's Lane 2 — which is why you read it last.

**Three things would falsify your thesis, and you should write them down now.** One: advertising is large in absolute dollars but small relative to total profit, so the mix argument doesn't move the valuation. Two: ad revenue is concentrated in a way that makes it less durable than it looks — tied to a subset of merchants or markets. Three: the ad business is growing because the core marketplace is subsidizing it, so the margin is real but not separable. If any of those hold, the pitch has to change. Naming them now is what stops you from arguing backwards from a conclusion on Wednesday night.

**And the question you still haven't answered:** why does the market get this wrong? Not "the market is lazy" — that's not an argument. If the ad mix is disclosed and analysts model it, there's a reason the multiple is where it is. Either the market is applying a discount for a risk you think is overstated, or it's applying a discount for a reason you haven't found yet. Your pitch is the answer to that question, and it's yours to write, not mine.

**Now the blockers, third time.** I have no web or data access in this session, and I still don't know your scope. Concretely:

- **Full pitch or short version?** Full means Business, Competition, Key Deals, Financials, Valuation, a DCF, and a deck. Short means Business, Financials, Valuation and a handful of slides. Thursday is close. Pick one.
- **Who's pulling the documents?** Either you run the four lanes somewhere with filing access, or you paste in the 10-K, the last two 10-Qs, the two most recent call transcripts, and the investor deck. I'll build the cited digests with you from those.

I'm keeping a working file of your claims — suburban US, restaurant commissions and advertising, two-sided customer, ad-mix mispricing — all tagged unverified. Nothing in it is a fact yet, and nothing from it goes on a slide until it resolves to a source and a date.

Answer the two blockers and I'll start on Lane 1 with you.

**Analyst.** What would have to be true: order frequency keeps rising while the courier cost per order stays flat.

**Assistant.** That's the best answer you've given me, and it's the load-bearing one. But it's two assumptions chained together, and the chain has a missing link. Let's make it explicit, because you'll need to say it out loud on Thursday.

**The chain as you've stated it:** order frequency rises → order volume grows → ad revenue grows faster than commission revenue because ad revenue is nearly all incremental margin → advertising becomes a larger share of profit → the market re-rates the multiple.

**The missing link is ad penetration, not order volume.** Ad revenue depends on how many merchants buy ads and how much they pay, not just on how many orders flow through. Orders can grow 20% and ad revenue grow 5% if merchant attach is saturating. So the assumption you actually need is *frequency up AND ad attach rate up AND ad pricing holding*. Three moving parts, not one. Write it that way and your pitch gets harder to attack, because you'll have shown you know where the risk sits.

**Now the pressure on "courier cost per order stays flat."** Two problems. First, in a density business cost per order should *fall* as volume grows — that's the entire scale argument for a delivery network. So "flat" is a conservative assumption, which is good for you, but you should say so, because a reviewer will ask why you're assuming away the upside. Second, flat is not free. Courier pay floors, reclassification risk in various jurisdictions, and competition for courier supply all push the other way. And be precise: flat in nominal terms while inflation runs is a real decline. Say which one you mean.

**The trap you haven't seen yet.** Frequency can rise for bad reasons. If the growth is coming from grocery and retail rather than restaurants, you get more orders at lower contribution margin per order and different courier economics — baskets are heavier, delivery is less efficient, and the mix dilutes rather than compounds. That's low-quality growth, and it would break your thesis while looking like it confirms it. So the test isn't "frequency up." It's "frequency up in restaurants, or up in new categories without contribution margin per order falling." Those come apart, and the filings will tell you which is happening.

**Turn it into a test table.** Do this before Thursday, with blanks where the numbers go:

1. Order frequency, trailing four quarters — rising? Threshold: must rise every quarter, not just year-over-year.
2. Contribution margin per order — flat or rising? Threshold: must not fall while frequency rises.
3. Ad revenue as a share of total revenue and of contribution profit — rising? Threshold: must rise for four consecutive quarters.
4. Merchant ad attach or ad revenue per active merchant — rising? This is the missing link; if you can't source it, your thesis has a hole.
5. Courier cost per order, nominal and as a share of GOV — flat or falling?

Each row needs a source and an as-of date, and each needs a number you're willing to defend. If row 4 comes back unavailable, say so in the deck rather than skipping it.

**On the blockers — I'll stop asking and set a default.** If you don't tell me otherwise, I'll assume a short pitch: Business, Financials, Valuation, and a deck of the slides that carry those. And I can't reach filings from here, so the fastest path is you pasting, in this order: the latest 10-K, the most recent 10-Q, and the last two earnings call transcripts. Start with the 10-K — it has the segment and geography disclosure that tests your "suburban US" and "restaurant commissions" claims in one place.

Paste the 10-K and I'll start building Lane 1 with you, line by line, tagged.

**Analyst.** What would make me wrong: grocery and retail delivery becomes the volume driver and the margin never shows up.

_Assistant called read_skill_file {"skill": "bison-fund-investment-analysis", "path": "references/socratic-question-bank.md"}, 2106 characters returned_

**Assistant.** That's a real counter-case, and it's the same risk you identified as your missing link — which is a good sign, because it means you're converging on the actual fault line rather than collecting unrelated worries. Write it down as your primary bear case. You'll need it in the red-team section.

But sharpen it, because as stated it's a business risk, not a stock risk. There are two distinct ways you lose money here:

**Business risk:** grocery and retail become the volume driver and margin never shows up. Your thesis dies on the numbers.

**Valuation risk:** you're right about the business and the stock still doesn't work, because the multiple already discounts the ad mix. You'd be correct and broke. This one is more common than the first, and it's the one students skip. The test is simple: if you build your DCF and your target lands at or below the current price, you don't have a buy — you have a well-researched hold. Be prepared for that outcome and don't force the conclusion.

There's also a third, subtler version: margin shows up in grocery but it's a *different* margin — lower contribution per order, different courier economics — so blended margins look fine while the restaurant business quietly deteriorates. A blend can hide a decay. That's worth one line in your risk matrix.

**One question left in the gate, and then it's done.** Question seven: **what's your current prior — buy, hold, or sell — and how confident are you, 1 to 5?**

Be honest and be low. A 2 is a respectable answer at this stage. What I'm looking for is whether your conviction moves after you read the filings, because a prior that never moves means the research didn't do anything.

**Then the gate closes and the real work starts, which I have to be straight with you about.** You've now answered six of seven questions in your own words, which is more thinking than most people do before a pitch. But you have zero evidence. Every claim in your working file — suburban US, restaurant commissions, ad mix, frequency up, courier cost flat — is tagged unverified. I can't source any of it from here.

So here's the plan for the time you have left:

**What I can build now, with no documents:** the test table skeleton with your five rows and blank cells, the deck outline with the slides your short pitch needs, and the DCF structure with the line items laid out and empty. That's real progress and it means the moment the numbers land, they have somewhere to go.

**What I can't do:** fill a single cell. Not one number.

**What you need to get:** the latest 10-K first — it settles your segment, geography, and revenue-mix claims in one document. Then the most recent 10-Q, then the last two call transcripts. Paste the 10-K text into this conversation and we'll build Lane 1 together, line by line, tagged with source and date.

Give me your prior and confidence, and tell me to start on the skeleton — or paste the 10-K if you have it in front of you.

**Analyst.** I land on a positive view and my confidence is medium.

_Assistant called load_skill {"name": "deck-build"}, 5195 characters returned_

_Assistant called load_skill {"name": "dcf-model"}, 6359 characters returned_

**Assistant.** Gate closed. Your prior is recorded: **positive, confidence 3 of 5 — before reading any evidence.** I'm writing that down with the date, because it's the benchmark your research has to move. If you finish Thursday with the same confidence and the same view, the work didn't do anything. If it moves up, you earned it. If it moves down, you learned something worth presenting — a well-argued hold or a pass is a legitimate pitch outcome and better than a forced buy.

Now the honest status. You've done the thinking. You have no evidence. Every claim is still tagged unverified, and I can't reach a filing from here. So here's what I'm handing you, and what you have to bring back.

**What you need to fetch — in this order, and stop after each one to read it:**

1. **Latest 10-K.** Settles segment revenue, geography, revenue mix (commission vs. advertising vs. other), order and GOV disclosure, and courier cost. That's four of your five test rows in one document.
2. **Most recent 10-Q.** Gives you the trend — is frequency actually rising, is margin per order holding.
3. **Last two earnings call transcripts.** Management's own words on ad attach, new categories, and courier economics. This is where you find out whether your "market misunderstands" claim survives contact with what's been said publicly.

**Your test table — fill every cell or mark it open:**

| # | Test | Threshold | Value | Source | As-of |
|---|---|---|---|---|---|
| 1 | Order frequency, trailing 4 quarters | Rises every quarter, not just YoY | | | |
| 2 | Contribution margin per order | Does not fall while frequency rises | | | |
| 3 | Ad revenue as % of revenue and of contribution profit | Rises 4 consecutive quarters | | | |
| 4 | Ad revenue per active merchant, or merchant attach | Rising — **this is your missing link** | | | |
| 5 | Courier cost per order, nominal and % of GOV | Flat or falling | | | |

Row 4 is the one that decides whether your thesis is a thesis or a hope. If it's not disclosed, you say so in the deck and your confidence should come down, not stay at 3.

**Your short-pitch deck outline — the slides that carry your argument:**

1. Title
2. What the business does, in your words
3. How it makes money — the revenue mix chart, sourced
4. **What the market says** — consensus, target dispersion, the street's narrative. Sourced, dated.
5. The thesis in one sentence, with three evidence-backed pillars
6. The ad-mix evidence — the chart that proves your claim
7. Unit economics — contribution per order, courier cost per order
8. Competition — Uber delivery, one or two others, on order growth and take rate
9. Valuation — DCF range plus the reverse DCF: what the current price implies
10. Bull case
11. **Bear case** — grocery/retail volume with no margin. Your own words.
12. Risk matrix
13. Catalysts
14. Recommendation — yours
15. Sources

That's a defensible short form. It's under the house standard of 30–41 slides, which is fine for a class pitch but you should know it's the abbreviated variant.

**What I can't do, said plainly one more time:** I can't fill a single cell above. Not the frequency number, not the ad percentage, not the price. If I gave you plausible-looking figures you'd walk into Thursday with numbers you can't defend when someone asks where they came from — and that's the fastest way to lose the room.

Paste the 10-K text and we build Lane 1 line by line. If you can't get it in front of me, tell me now and we'll plan the pitch around what you can verify yourself, which will be a smaller and more honest pitch.
