# section-trigger, with-skill

- prompt: i need to show how they actually make money
- model: deepseek/deepseek-v4.1-flash-1017
- date: 2026-10-18

**Analyst.** i need to show how they actually make money

_Assistant called load_skill {"name": "bison-fund-investment-analysis"}, 10635 characters returned_

_Assistant called load_skill {"name": "pitch-business"}, 2238 characters returned_

_Assistant called read_skill_file {"skill": "pitch-business", "path": "references/business.md"}, 1058 characters returned_

_Assistant called read_skill_file {"skill": "bison-fund-investment-analysis", "path": "references/socratic-question-bank.md"}, 2106 characters returned_

**Assistant.** Good — that's the Business section, and it's the right thing to nail first. Two things before I can build it.

**1. Which company?** You haven't named it. Give me the name and ticker and I'll pull the segment revenue, the KPIs, and the market sizing from the filings and transcripts.

**2. Your first-pass answer, in your own words.** Don't look it up — I want your current belief so the research can test it rather than replace it:

- Where does the money actually come from? Name the main revenue lines and roughly what share each is.
- Who is the customer, and why do they stay?
- What does the market misunderstand about how this company earns?

Short and half-right is fine. I'm not going to answer these for you — the pitch has to be yours.

Once you answer, here's what I'll assemble for that section, and what "actually make money" has to mean on the slide:

- **Revenue by segment**, each with its disclosed contribution, and a flag on anything I had to infer rather than read off a filing.
- **The unit economics** — what one customer, one transaction, or one unit actually throws off, not just the top line. This is usually where the real "how they make money" answer lives.
- **The operating metric the market trades on** (users, net deposits, assets under custody, take rate — depends on the business), because that's what drives the revenue line.
- **Margin structure by segment**, since a revenue mix that looks diversified can still be one profit pool.
- **Market size with a cited source and a growth rate.** Both, or it doesn't go on a slide.

Every figure comes with a source and an as-of date. Anything I can't source gets tagged unverified and stays out of the deck.

One thing worth deciding now: do you want the "how they make money" story told as **revenue lines** (what they sell) or as **the economics underneath** (who pays, how often, and what it costs to serve them)? The first is easier to source. The second is what a fund committee actually argues with you about. I'd do both, revenue lines first, then the economics — but tell me if you'd rather keep it tight to one.

**Analyst.** DoorDash. It is a delivery network, mostly suburban United States, and I think it makes its money on restaurant commissions and advertising.

**Assistant.** Good, that's a real starting point. Two of the seven answered. Before I go pull filings, a few more, and one flag on your money answer.

**The flag.** "Restaurant commissions and advertising" is probably the right shape but it may not cover the whole revenue line. Think about the money that moves when you order: the restaurant pays a commission, but the customer also pays fees, and some customers pay a flat monthly fee. Ask yourself whether those are separate revenue lines or just how the commission gets collected. I'm not going to tell you which — I want your read first, because if you walk into a committee saying "commissions and ads" and the deck shows three or four lines, that's the first thing they'll hit you on.

Same with "mostly suburban United States." That's a claim that needs a source and a date. It might be right, but it's a geography assertion, not a fact yet.

**The rest of the set:**

3. **Who is the customer, and why do they stay?** Be specific about which customer — the person ordering, the restaurant, or the courier. They're three different businesses with three different reasons to stick around, and the pitch usually only survives if you know which one you're really serving.

4. **What do you think the market misunderstands?** Why might the stock be mispriced? If your answer is "it's a good business," that's not a misunderstanding, that's a preference.

5. **What would have to be true for you to be right?** Two or three assumptions the thesis rests on. For a delivery network these are usually about order frequency, courier cost per order, or whether advertising can keep expanding margin.

6. **What would make you wrong?** Name the strongest counter-case now, before you're attached to the bull case. Competition on courier pay, a regulatory reclassification of couriers, or the ad business stalling are the usual candidates — pick the one that actually scares you.

7. **Your prior — buy, hold, or sell — and confidence, 1 to 5.**

Short answers are fine. Once you've got these down I'll run the grounding lanes on DoorDash and come back with segment revenue, the operating metrics the market trades on, unit economics per order, and market sizing with sources and dates. Then we'll see which of your answers the evidence supports and which it doesn't.

**Analyst.** The customer is two people at once: the consumer who orders and the restaurant that pays for demand.

**Assistant.** That's a sharper answer than most people give, and it's the right instinct — DoorDash genuinely runs two demand-side relationships. But it leaves out the third party, and that's the one that decides whether the business works.

**The courier.** Couriers aren't a customer, but they're the supply side that the whole network depends on, and they're paid out of the same dollar the consumer and restaurant are paying in. So the real question isn't just "who pays for demand" — it's **who absorbs the cost of fulfillment**. That's where the margin lives or dies. If you can't say who's really carrying the courier cost, you can't explain how they make money.

Also worth tightening: "the restaurant pays for demand" is doing a lot of work. Is the restaurant buying *demand* (marketing, discovery, incremental orders it wouldn't otherwise get) or buying *delivery logistics* (someone to move the food)? Those are different products with different pricing power and different churn risk. Your answer implies the first. The filings may describe the second. That gap is exactly the kind of thing a committee will find.

So, before I start pulling:

- **Confirm or revise:** is the courier a cost line, a customer, or a partner — and who pays for them?
- **4. What does the market misunderstand?** Why might it be mispriced?
- **5. What would have to be true?** Two or three assumptions.
- **6. What would make you wrong?** The single strongest counter-case.
- **7. Prior and confidence, 1 to 5.**

Give me those and I'll run the grounding lanes — business, street, news — and come back with the segment revenue breakdown, per-order economics, the KPIs the market actually trades on, and sourced market sizing. Then we test your answers against the record instead of guessing at it.

**Analyst.** I think the market treats it as a low-margin delivery company and misses how much of the profit is advertising.

**Assistant.** That's the first real thesis statement you've made, and it's testable — which is what matters. Two things to note about it, though, and then the last three questions.

**It's a claim about profit, not revenue.** Those are different. Advertising could be a small slice of revenue and still a large slice of profit, because ad dollars carry almost no cost of goods. That's the whole reason your thesis has teeth. But it also means you can't prove it with a revenue mix chart — you'd need segment-level margin, or a disclosed contribution figure. If the company only discloses ad revenue and not ad profit, then "how much of the profit" becomes **your estimate**, and it gets labeled as one on the slide. That's allowed. It just can't be presented as fact.

**Check whether it's actually misunderstood.** This is red-team question 3, and you can answer it now: if advertising is a well-known part of the bull case, the market isn't missing it — it's already in the price, and your edge has to be something else. The version of your thesis that survives is narrower and more interesting: not "the market misses the ads," but something like "the market is pricing the ads correctly but underestimating how fast they grow" or "the market assumes ad margin gets competed away and it doesn't." Which of those is yours?

**Still open:**

- **The courier.** You skipped it, and it's not optional — it's the largest cost in the business. Cost line, customer, or partner, and who pays for them?
- **5. What would have to be true?** Give me two or three assumptions your thesis rests on. If advertising drives the profit, at least one of them has to be about ads: what share it needs to reach, or how fast it needs to grow.
- **6. What would make you wrong?** The single strongest counter-case. For your specific thesis, the obvious one is that ad growth slows or gets priced down and profit reverts to delivery economics. Say it in your own words and say whether you believe it.
- **7. Prior and confidence, 1 to 5.**

Answer those five and I'll start grounding — business, street, and news lanes — and come back with the segment revenue, per-order economics, the KPIs the market trades on, and sourced market sizing. Then we find out whether the record supports the ad-profit thesis or contradicts it.

**Analyst.** What would have to be true: order frequency keeps rising while the courier cost per order stays flat.

**Assistant.** That's a clean assumption, and it's the right kind — measurable, and it can be checked against the record. But notice what it doesn't cover.

**Your thesis is about advertising driving profit. Your assumption is about delivery economics.** Those aren't the same claim. "Order frequency rises while courier cost per order stays flat" would make the delivery business better — it says nothing about whether ads grow, whether ad margin holds, or whether ads end up being the profit pool. If that's your only assumption, then the ad thesis isn't actually load-bearing in your own argument.

You need at least one assumption that would have to be true *for the ads specifically*. Candidates, pick or reject:

- Ad revenue grows faster than order volume, so ad revenue per order rises.
- Ad margin stays high as the business scales — no pricing pressure from restaurants or from competitors selling ads.
- Advertisers keep paying because the channel converts, not because it's subsidized.

Also worth flagging on the frequency assumption itself: **rising frequency and flat courier cost per order may be in tension.** More orders per courier hour is how cost per order usually falls — which helps you. But more orders also means more peak-hour congestion and longer distances in suburban markets, which pushes the other way. Suburban density is the interesting part of your geography claim, and it cuts both directions. Worth knowing which force dominates before you defend this.

**Still open, and these are the last ones:**

- **The courier** — cost line, customer, or partner, and who pays for them. You've skipped this twice. It's the biggest cost in the business; I can't build the section without your read on it.
- **6. What would make you wrong?** One counter-case, in your words.
- **7. Prior and confidence, 1 to 5.**

Then I'll ground it — business, street, news — and come back with segment revenue, per-order economics, ad revenue and whatever margin disclosure exists, the KPIs the market trades on, and sourced market sizing. Then we test the ad-profit thesis against the record.

**Analyst.** What would make me wrong: grocery and retail delivery becomes the volume driver and the margin never shows up.

**Assistant.** That's a good counter-case — better than most. It's specific, it's plausible, and it points at a real strategic question: DoorDash has been pushing hard into grocery and retail, and those categories have different economics than restaurants. Lower commission rates, thinner baskets relative to the labor involved, and a customer who orders less often. If that becomes where the volume comes from, you can grow orders and never get the margin.

One thing to sharpen: your counter-case is about **mix**, and your assumption was about **frequency and courier cost**. They connect — grocery orders tend to have a worse cost-to-basket ratio — but they're not the same risk. Worth knowing which one you'd actually be defending against in the room.

**Two things left, and then I'll start.**

**The courier.** You've skipped it three times now. If the honest answer is "I don't know how courier cost is structured," say that — that's a legitimate answer, and it's the one case where we research it together rather than me waiting on you. But I still need your read on the *conceptual* question, which doesn't require data: when a customer pays a delivery fee, does that fee cover the courier, or does the company top it up? Your answer changes what the entire margin story means.

**7. Prior and confidence, 1 to 5.** Buy, hold, or sell, and how sure. This is the one thing I can't help you with and can't research for you. Even a rough call — "lean buy, 2 out of 5" — is enough to start.

On the ad assumption: you still haven't given me one that's specifically about advertising. Your frequency/courier assumption is about delivery. If you believe the ad thesis, there has to be a condition on the ads. Add it when you answer the two above, or tell me you're dropping the ad-profit framing and the thesis is really about delivery unit economics improving. Either is a real thesis. They just aren't the same pitch, and the deck has to commit to one.

**Analyst.** I land on a positive view and my confidence is medium.

_Assistant called load_skill {"name": "grounding-lanes"}, 3147 characters returned_

_Assistant called load_skill {"name": "sourcing-standard"}, 3343 characters returned_

**Assistant.** Good — "positive, medium confidence" is a usable starting point. It's a prior, not a conclusion, and it stays provisional until the record tests it.

Two gaps I have to be straight about before we go further:

**You never answered the courier question.** You've now built a thesis about advertising profit on top of a business whose largest single cost you haven't described. I'm not going to draft around that. Answer this one, conceptually, no data needed: when a customer pays a delivery fee, does that fee cover the courier, or does the company top it up? Your answer decides whether the ad profit is funding a subsidy or adding to a business that already works.

**You never gave an assumption about advertising.** Your only stated assumption was order frequency and flat courier cost — that's delivery economics. So right now your thesis and your assumptions don't match. Pick one:

- **The ad thesis:** add a condition on ads (ad revenue per order rises, or ad margin holds as it scales), and we test that.
- **The delivery thesis:** drop the ad framing and argue unit economics improve with density and frequency.
- **Both:** legitimate, but then you need assumptions for each, and the deck has to say which one is doing the work.

**On the research:** I can't pull live filings or market data in this conversation — I have no web access here. So the grounding lanes have to run against sources you bring me, or against the data files on your machine if the fund's setup is configured. What I can do right now is tell you exactly what to pull, so you're not guessing.

**Pull these, with dates:**

1. **Latest 10-K and most recent 10-Q** — the revenue disaggregation note. That's where the actual revenue lines are, and it's where "commissions and advertising" gets tested. Also the segment note and any marketplace/Logistics split.
2. **Last two earnings call transcripts** — management's own words on ad revenue growth, ad margin, courier cost per order, and order frequency. Quote them directly; paraphrases don't survive a committee.
3. **Investor presentation or shareholder letter** — whatever they disclose on marketplace GOV, orders, and monthly active users.
4. **The 10-K risk factors on courier classification** — this is the regulatory risk that sits under your entire thesis and it's usually longer than people expect.
5. **Peer filings** — Uber Eats and Instacart, on the same metrics. Instacart especially, because it's the cleanest read on what grocery-delivery economics look like, which is your stated counter-case.

**What the record has to show for your thesis to hold:**

- Ad revenue as a share of total revenue **and** as a share of gross profit, with the second one being the number that matters. If they don't disclose ad profit, that becomes your estimate and gets labeled as one.
- Courier cost per order, trended. Flat, falling, or rising.
- Order frequency, trended.
- Contribution margin per order, if disclosed.

Every one of those gets tagged `<value>, source: <document and link>, as-of: <date>, [fact | estimate | opinion]`. Anything I can't source stays out of the deck.

Send me the filings or the numbers you pull and I'll build the fact sheet, then the Business section draft. And answer the courier question — that one's still blocking.

**Analyst.** you decide for now

**Assistant.** Fair. Let me split it, because one of those is a mechanism question and the other isn't.

**The courier question I can answer, because it's mechanical, not a judgment call.**

In a delivery marketplace, the consumer's delivery fee and the courier's payout are two separate things, and the fee is generally smaller than the payout. The gap gets covered by the restaurant commission and by the marketplace's own margin. So the delivery fee is a revenue line, courier pay is a cost line, and neither one is meant to match the other. The business only works if commission plus fees plus ads exceed courier cost plus support and refunds, on a per-order basis.

That's the structure, and it's why your ad thesis has force: ads are the piece that carries almost no cost of goods, so ad dollars land close to the bottom line while every delivery dollar gets eaten into by courier pay.

What I can't give you is the number. Whether DoorDash's delivery fee covers 60% or 90% of courier payout, and whether that ratio is improving or deteriorating, comes out of the 10-K cost-of-revenue note and the call transcripts. I won't estimate it. So the mechanism is settled; the magnitude is still open and it's the single most important number in your pitch.

**The thesis framing I won't decide for you.** Not to be difficult — it's that a committee will ask you why you believe it, and "the analyst tool picked it" is not an answer you can give. It's also the one thing that has to be genuinely yours for the pitch to be worth presenting. You can defer it. You can't outsource it.

**What I'll do instead, right now:**

I'll build the fact sheet skeleton for the Business section with every slot the record has to fill, and leave the judgment calls visibly blank so you can see exactly what's missing. That's the part I can do without inventing anything.

**Fact sheet — Business section, DoorDash**

| Slot | Status |
|---|---|
| Total revenue, latest fiscal year | open — 10-K |
| Revenue by line: commissions, consumer fees, advertising, other | open — 10-K disaggregation note |
| Advertising revenue, absolute and % of total | open — 10-K / calls |
| Advertising gross profit or contribution | open — likely undisclosed; becomes estimate |
| Orders, marketplace GOV, monthly active users | open — shareholder letter |
| Order frequency, trended | open — calls |
| Courier cost per order, trended | open — 10-K cost of revenue |
| Contribution margin per order | open — calls, if disclosed |
| Suburban vs. urban order mix | open — may not be disclosed at all |
| Grocery/retail order mix and margin | open — calls |
| TAM and growth rate, with source | open — needs a cited third-party estimate |
| Courier classification risk | open — 10-K risk factors |

Three of those are load-bearing for your thesis: ad revenue as a share of gross profit, courier cost per order trend, and order frequency trend. If those three come back the wrong way, the thesis doesn't hold.

**Judgment calls I'm leaving blank, for you:**

- Which thesis the pitch commits to — ads, delivery economics, or both.
- The ad-specific assumption.
- Whether "suburban" survives as a claim once you see the disclosure.
- Your durability argument: why this network keeps its position.

Send me the 10-K and the last two transcripts — or just the numbers you pull from them — and I'll fill the sheet with sourced, dated tags and draft the section around it. If you want to move before you have the filings, tell me and I'll draft the section structure with the evidence slots marked, so you can drop numbers in as you find them.
