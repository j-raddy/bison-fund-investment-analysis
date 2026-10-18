# first-contact, without-skill

- prompt: hey i need to do my pitch on doordash for thursday, where do i start
- model: deepseek/deepseek-v4.1-flash-1017
- date: 2026-10-18

**Analyst.** hey i need to do my pitch on doordash for thursday, where do i start

**Assistant.** Start with the recommendation and the debate — not the company history.

**1. Pick your stance and write one sentence.**
Most student pitches are long. Example:
> “DoorDash is the scaled leader in U.S. local delivery; density and DashPass create a moat, while ads, grocery/retail, and international expansion lift take rate and cash flow. The market underestimates the margin mix shift. Buy.”

If you’re short:
> “DoorDash’s premium valuation already prices in ads/grocery upside, while competition and courier-regulation risk cap take rate and margins. Sell.”

**2. Pull the latest facts from DoorDash IR / 10-Q / earnings call.**
Get: revenue, Marketplace GOV, total orders, take rate, adjusted EBITDA, free cash flow, guidance, cash/debt, share count, market cap. Use the latest reported quarter — don’t rely on memory.

**3. Build a simple model.**
Orders × average order value = GOV. Revenue = GOV × take rate. Then contribution profit → adjusted EBITDA → FCF. Do three scenarios: base, bull, bear. Keep it simple.

**4. Valuation.**
Use EV/EBITDA, EV/FCF, and EV/GOV vs. Uber, Instacart, and global delivery peers. A DCF is optional; a comps table plus scenario sensitivity is enough.

**5. Deck outline, 8–10 slides.**
1. Recommendation and one-line thesis  
2. Company snapshot: what DoorDash actually is  
3. Three thesis pillars  
4. Market and competitive landscape  
5. Moat: density, DashPass, merchant/courier network  
6. Financials and simple model  
7. Valuation  
8. Catalysts  
9. Risks and mitigants  
10. Conclusion / what would make you wrong

**6. Nail the key debates.**
Is DoorDash a thin-margin utility or a local-commerce platform with ads/retail upside? Can it hold take rate while expanding? Does courier classification regulation raise costs? Is the premium valuation justified by FCF growth? Competition from Uber Eats, Instacart, Amazon, and regional players.

**7. Thursday plan.**
Today: write the one-page outline and thesis. Next: pull data and build the model. Day before: make slides and rehearse a 3-minute and 10-minute version. Prepare five Q&A questions: competition, regulation, take rate, grocery margins, valuation.

Don’t overdo TAM. Show unit economics, the debate, and why the market is wrong.

**Analyst.** DoorDash. It is a delivery network, mostly suburban United States, and I think it makes its money on restaurant commissions and advertising.

**Assistant.** Good — that's the right skeleton. Three corrections/sharpening points before you build slides on it.

**1. "Commissions" is only part of the revenue line.**
DoorDash's revenue has several buckets:
- **Merchant commissions** — the classic 15% / 25% / 30% tiered take on order subtotal (Basic / Plus / Premier).
- **Customer fees** — delivery fee, service fee, small-order fee. This is a big chunk and students usually forget it.
- **DashPass** — subscription revenue, ~$9.99/mo. Its real value isn't the fee, it's that members order far more often and churn less.
- **Advertising** — merchants paying for placement/promoted listings. Very high margin.
- **Other** — Drive (white-label delivery for merchants), Storefront, and international (Wolt).

So when you say "commissions and advertising," you're describing the *merchant-side* economics. The customer-side fees matter just as much for the take rate math.

**2. The suburban point is a real thesis point — use it properly.**
DoorDash's historic strength is suburban and non-dense markets, where Uber Eats was weaker. That matters because:
- Suburban orders tend to have **higher average order value** and restaurant selection is thinner, so merchant bargaining power is lower.
- Courier supply is less contested than in dense cities.
- Density builds over time — each additional order in a zip code shortens delivery times and lowers cost per order.

But don't overstate it. DoorDash is now the leader in most U.S. metros, not just suburbs, and the growth vector is **grocery/retail and international**, not more suburban restaurant penetration. Frame it as "the suburban density advantage is the profit engine; the growth is adjacent categories."

**3. Ads is the margin story — that's your pitch.**
Commissions are a mature, competitive line item. Ads is the thing that moves the model: it's near-100% margin, it's growing much faster than the core, and it lifts blended take rate *without* raising merchant commission rates. That's the cleanest version of the bull case:

> Take rate expands because ad revenue grows as a share of the mix, not because DoorDash squeezes merchants harder.

That distinction is what makes it defensible against the "they're just a thin-margin toll booth" bear case.

**What to pull from the 10-Q / latest earnings call:**
- Revenue disaggregation (Marketplace vs. other)
- Marketplace GOV and total orders, so you can compute take rate yourself
- Any commentary on ad revenue growth — they discuss it on calls but don't break it out as a line, so cite the qualitative language
- DashPass member commentary
- International/Wolt growth rate vs. U.S.

Rough scale to sanity-check against (verify exact figures, don't quote me): full-year revenue in the low-to-mid $10Bs, GOV in the high $70Bs, and the U.S. is still the large majority of revenue.

One framing question to answer on slide 3: **is the ad business a durable structural advantage or a cyclical margin tailwind?** If you can answer that convincingly, you have a pitch.

**Analyst.** The customer is two people at once: the consumer who orders and the restaurant that pays for demand.

**Assistant.** Right, and that framing is the core of the moat — but sharpen it two ways, because the version you just said will get picked apart in Q&A.

**1. It's three-sided, not two.**
Consumer, merchant, and Dasher. The Dasher is the one students forget, and it's the one that breaks naive models. DoorDash doesn't employ couriers — they're independent contractors who choose when to work and can work for Uber Eats in the same hour. So:

- **Consumer** = demand, pays fees + DashPass
- **Merchant** = supplies the food, pays commission + ad spend
- **Dasher** = supplies the labor, gets paid, and can leave any time

The Dasher side is why delivery is hard: you need enough couriers online to keep delivery times short, but not so many that each one earns too little and quits. That balance is the operational core of the business, and it's the thing that regulatory risk (reclassification) directly threatens.

**2. The merchant is a customer *and* a supplier.**
That's the unusual part and worth saying explicitly on a slide. The restaurant is not just buying demand — it's also the product the consumer is buying. So DoorDash is simultaneously:

- selling demand to the merchant (commission, ads)
- selling the merchant's food to the consumer (fees)
- buying labor from the Dasher

Nobody else in the value chain sits in all three seats. That's the structural argument for why the take rate is defensible.

**3. This is *why* ads works — make that link explicit.**
The merchant pays twice: commission on the order, plus ad spend to get placed higher. Ads isn't a separate business bolted on; it's DoorDash monetizing the fact that it *is* the demand channel. The merchant can't generate that demand themselves, so they pay for visibility. That's the cleanest bull argument:

> The merchant is a captive buyer of demand, so ad revenue scales with GOV without raising commission rates.

**4. Where the bargaining power actually sits — this is your Q&A armor.**
- **Consumer side: weak pricing power.** People multi-home — they have both apps installed. DoorDash can't raise consumer fees much without losing orders. This caps the consumer-fee lever.
- **Merchant side: stronger, but contested.** Restaurants are on all platforms too, but they can't skip the market leader — being absent from DoorDash means losing real volume. Small independent restaurants have the least leverage; chains have the most.
- **Dasher side: pure market.** Pay is set by local supply and demand, and it's the line item most exposed to regulation.

So the honest version: **DoorDash's pricing power is strongest on the merchant side, weakest on the consumer side, and most legally exposed on the courier side.** Say that out loud in the pitch and you sound like you've actually thought about it.

**5. The bear case this framing sets up.**
"The merchant is paying a commission *and* an ad tax, and they're starting to notice." That's the real risk — not competition from Uber Eats, but merchant resentment plus regulators noticing the same thing. Restaurant associations have pushed commission caps in several cities. If you can show why that pressure is contained (chains accept it, ads are voluntary and ROI-positive, caps have been narrow) you've pre-empted the strongest objection.

**Slide suggestion:** put the three-sided diagram on the moat slide, with take rate flowing from consumer fees + merchant commission + ads, and cost flowing out to Dashers. Then on the risks slide, show which side of the triangle each risk hits. That one diagram does a lot of work for you.

**Analyst.** I think the market treats it as a low-margin delivery company and misses how much of the profit is advertising.

**Assistant.** The instinct is right. The phrasing will get you killed in Q&A, though — here's why and how to fix it.

**The problem with "the market treats it as a low-margin delivery company."**

It doesn't. DoorDash trades at a premium multiple — high teens to twenties on EBITDA, and a rich EV/sales. A company priced as a low-margin delivery business would trade at 10–15x EBITDA, like a mature logistics name. So if you open with "the market misses the ads," the first question is: *"Then why is it trading at 25x?"* and you're stuck.

The market knows about the ads. Management talks about it every call, sell-side models it, and the stock has re-rated partly *because* of it. Your pitch can't be "nobody noticed." It has to be "the market is pricing it, but getting the **durability** or the **magnitude** wrong." That's a much narrower, more defensible claim.

**Three versions of the thesis that actually survive.**

1. **Durability.** "Consensus treats ad revenue as a cyclical margin tailwind that compresses when delivery competition intensifies. We think it's structural — the merchant is a captive buyer of demand, so ad spend scales with GOV regardless of the delivery cycle."
2. **Flow-through.** "The market models ad revenue growth but under-models the margin flow-through, because ad dollars carry essentially no incremental courier cost. Every point of ad mix shift drops to EBITDA at ~100% margin."
3. **Magnitude.** "The market is sizing the ad business off current disclosure. Benchmarked against Amazon's ad take rate on GMV, the opportunity is materially larger."

Pick one. Don't claim all three — it reads as hand-waving.

**The hard part: DoorDash doesn't disclose ad revenue.**

This is the real obstacle and you should address it head-on rather than glossing over it. It's buried in "other revenue" or discussed qualitatively. So "the market misses it" is hard to prove when nobody — including you — has the exact number.

Two ways to get around it:

- **Triangulate from Amazon.** Amazon *does* disclose ad revenue, and it's roughly a few percent of GMV. Apply a comparable take rate to DoorDash's Marketplace GOV and you get a rough sizing. Then show what that implies for EBITDA margin. This is the single most useful analytical move in your whole pitch — it turns a qualitative claim into a number.
- **Use sell-side estimates.** If analysts publish ad revenue estimates, cite them. Then your argument becomes "even the published estimates under-model X," which is far stronger than "they don't see it."

**The counter-argument you must pre-empt.**

If ads is the profit engine, the bear says: *ads is a tax on merchants, merchants are already paying 30% commission, and Uber Eats and Instacart are building the same ad products — so ad take rate compresses as competition for merchant ad dollars intensifies.* Restaurant associations have already pushed commission caps in some cities; the ad tax is the next thing they'll notice.

Your answer: ads are voluntary and ROI-positive (merchants bid because it works), the market leader captures disproportionate ad spend because it *is* the demand channel, and ad take rates at Amazon-style levels are still well below where merchant marketing budgets sit.

**What goes on the slide.**

- A small table: DoorDash blended take rate, with your estimate of the ad component broken out and the implied EBITDA flow-through.
- A benchmark bar: Amazon ads as % of GMV vs. your DoorDash estimate, with the gap labeled "opportunity."
- One line: "Market prices the ad business; it misprices the durability of it."

**One honest check before Thursday.** Pull the current EV/EBITDA and EV/FCF against Uber, Instacart, and Delivery Hero. If DoorDash is already at a clear premium, say so on the slide and make your case about *why the premium is still too low* — that's a far more credible pitch than pretending the market is asleep. If it's *not* at a premium, then your original framing works and you should lead with it. Let the comps table decide which pitch you give.

**Analyst.** What would have to be true: order frequency keeps rising while the courier cost per order stays flat.

**Assistant.** That's the right *kind* of question — "what would have to be true" is exactly how you should stress a thesis. But as stated it's necessary, not sufficient. You're missing a leg.

**The decomposition.**

Contribution profit per order = revenue per order − courier cost per order − other variable costs (payment processing, support, refunds).

So for the thesis to work you need **three** things, not two:

1. **Orders per customer rise** (frequency)
2. **Courier cost per order stays flat or falls** (your condition)
3. **Revenue per order doesn't fall faster than cost per order**

Leg 3 is the one that kills most operating-leverage pitches. You can absolutely grow frequency by cutting fees, discounting, or pushing DashPass — and end up with more orders and *less* profit per order. Frequency is an input; profit per customer is the output.

**The DashPass tension — this is the sharpest point you can make.**

DashPass is explicitly a trade: members pay ~$10/month and get free or reduced delivery fees. So on a DashPass order, revenue per order is *lower* than a non-member order. Frequency rises, per-order economics fall, and the subscription plus volume has to make up the difference.

Which means **the right unit of analysis is profit per active customer per year, not per order.** If you build your model per-order, DashPass looks margin-dilutive. If you build it per-customer, it looks accretive. Same business, opposite conclusion — and that's a genuinely good slide.

**What "courier cost per order stays flat" actually requires.**

It's not a passive assumption. It requires all of these:

- **Density concentrated in existing markets.** Cost per delivery falls when orders per square mile rise. But DoorDash is expanding into grocery, retail, and international — new categories and new geographies *reset* density. Growth in new markets dilutes the very benefit that makes growth profitable. This is the single biggest hole in the thesis.
- **Batching improves.** Two orders per courier trip cuts cost per order. Batching depends on order density *and* on order timing clustering.
- **Courier pay doesn't step up.** Pay is set by local labor supply. Tight labor markets, minimum-pay-per-offer rules, or reclassification push it up. Note that DoorDash has introduced minimum pay floors in some markets — that's a structural cost increase, not a cyclical one.
- **AOV holds.** A courier trip costs roughly the same whether the bag is $25 or $60. So higher AOV spreads cost. If frequency rises through small convenience orders, AOV falls and cost per order *as a percentage of GOV* rises even if the dollar cost is flat.

**The grocery problem, specifically.**

Grocery has higher AOV but a *much* lower take rate than restaurant — thin margins, and the basket is heavy and perishable, so courier cost per order is higher. So grocery grows GOV and orders while diluting both take rate and cost per order. If your model has grocery as a growth driver and flat cost per order, those two assumptions are in tension. Pick one or explain how batching and multi-order trips bridge it.

**Falsifiable tests — put these in the deck.**

- Orders per active customer, trended over 6–8 quarters
- Marketplace GOV per order (is AOV holding?)
- Revenue as % of GOV (take rate — is it holding or compressing?)
- Any disclosed commentary on cost per order, batching, or delivery times
- DashPass member count and mix, if disclosed

If orders per customer rise, take rate holds, and AOV holds — the thesis is alive. If orders rise but take rate and AOV both fall, you're buying growth, and the operating leverage story is wrong.

**The one-line version for the slide:**

> "The thesis requires frequency to rise *without* buying it — take rate and AOV must hold while density absorbs courier cost. The risk is that grocery and international expansion reset density faster than frequency compounds."

That's a much stronger slide than "frequency up, cost flat," because it names the condition that would break it.

**Analyst.** What would make me wrong: grocery and retail delivery becomes the volume driver and the margin never shows up.

**Assistant.** That's the right failure mode — it's the most likely one, and it's more specific than "competition." But tighten it, because as written it's a vibe, not a falsifiable claim.

**The mechanism isn't failure, it's mix shift.**

Grocery can be a perfectly good business and still dilute the model. Higher AOV, much lower take rate, higher cost per order (heavy, perishable, multi-item, needs shopping time). So grocery grows GOV and orders while pulling blended take rate down and cost per order up. Nothing has to go wrong for the margin to not show up — the mix does it mechanically.

That's the version to put on the slide: **"Grocery grows the volume line and compresses the margin line at the same time, and the market pays for the volume."**

**The sharpest detail — ads don't port to grocery.**

This is the part most people miss, and it's the strongest form of your bear case. Restaurant ads work because food is a *discovery* purchase: highly substitutable, impulse-driven, and the merchant is bidding for a customer who hasn't decided. Grocery is a *replenishment* purchase — people rebuy the same items week over week. Ad value per dollar of GMV is structurally lower.

So the profit engine that justifies the premium (ads) scales with restaurant GOV, not grocery GOV. If the growth mix shifts toward grocery, the highest-margin revenue line grows slower than the business. That's the clean statement of "the margin never shows up."

**Make it falsifiable — put numbers on it.**

Ask: for grocery to be margin-neutral, what take rate and what cost per order does it need? Then compare to what's plausible. If grocery take rate is a fraction of restaurant and cost per order is higher, the math either works through batching or it doesn't. Show the bridge. A slide that says "grocery needs X% take rate to be neutral; we think it lands at Y%" is worth ten slides of prose.

**The bull defense you have to address.**

DoorDash will say grocery isn't a margin play — it's a *frequency and retention* play. Grocery orders are weekly and habitual, which drives DashPass retention, which drives restaurant order frequency. So the value shows up in the halo, not the line item.

That's a legitimate argument and you should engage it rather than ignore it. Your rebuttal: the halo is real but hard to verify, and the market is already paying for it. If the halo is the thesis, the burden is on management to disclose the evidence — and they don't break out grocery cohort behavior.

**The early-warning metric.**

Blended take rate as % of GOV, trended quarterly, alongside grocery/retail as a share of GOV. If grocery share rises and blended take rate holds, the halo is real. If grocery share rises and take rate slides, your bear case is playing out in real time. That single chart is your tripwire.

**One honest note on timing.**

This is a slow-burn failure, not a blowup. If you're wrong this way, the stock doesn't crater — it de-rates over two or three years as growth gets less profitable. Which means you can be right about the business and wrong about the stock for a long time. Say that in the pitch; it shows you understand the difference between being right and making money.

**Analyst.** I land on a positive view and my confidence is medium.

**Assistant.** Good — medium confidence on a long is a legitimate, honest place to land, and it's actually easier to defend than high confidence. Here's how to make it work for you.

**Say it out loud in the pitch. Don't hide it.**

Most students present every idea as a slam dunk. A fund audience trusts the person who says "I like it, I'm not certain, here's what would move me" far more than the person who's certain about everything. Put it on the recommendation slide:

> **Buy. Medium conviction.** The ad mix shift and density economics are real and under-modeled on durability. The open question is whether grocery dilution outruns the margin benefit. Position sizing and the tripwires below reflect that.

That single sentence does more for your credibility than another slide of analysis.

**Medium confidence has to show up in the structure, not just the words.**

If you say medium and then present a base case with 40% upside, you've contradicted yourself. Make the deck internally consistent:

- **Base case is modest.** Mid-teens IRR, not a double. The upside comes from the bull case, not the base.
- **Bear case is genuinely bad, not a token.** If grocery dilution plays out, show the multiple compressing. A bear case that's only −10% means you're actually high confidence.
- **Skew matters more than the point estimate.** Medium confidence on a long usually means "the distribution is favorable but wide." Say that.

**Sizing language — this is what a real fund wants to hear.**

Something like: "This is a starter position, not a full-weight. We'd add on evidence that blended take rate holds as grocery mix rises, and cut on the tripwire." That tells the room you know how to hold a medium-conviction idea in a portfolio. It's the difference between an analyst and a student.

**Name the two things that would move you to high confidence.**

Be specific and observable:

1. **Blended take rate holds while grocery/retail share of GOV rises** — proves the mix shift is margin-neutral or accretive.
2. **Ad revenue growth outpaces GOV growth** — proves the profit engine scales with the business, not just the restaurant segment.

And the two that would flip you to a pass:

1. Take rate slides two or three quarters in a row as grocery mix climbs.
2. Courier cost per order rises structurally — minimum pay floors, reclassification, or batching failing to offset new-market dilution.

**The line that will land in Q&A.**

When someone asks "so what's your conviction?" — don't waffle. Say:

> "Medium. I think the direction is right and the magnitude is uncertain. The thing I'd want before sizing up is evidence that take rate holds through the grocery mix shift, and management doesn't disclose enough to prove it yet. So I'm long the direction, sized for the uncertainty."

That's a complete answer. It states the view, the confidence, the reason for the confidence level, and what would change it. Nobody can poke a hole in it, because you've already named the hole.

**One last check before Thursday.**

Medium confidence plus a premium multiple is a slightly uncomfortable combination — you're paying up for a view you're only moderately sure of. Have a one-line answer ready for "why own it now rather than wait for the evidence?" The good answer: the re-rating happens when the evidence arrives, so waiting means paying a higher price for the same certainty. That's the argument for owning a medium-conviction idea early rather than after the proof.

**Analyst.** you decide for now

**Assistant.** Fine. Here's the call.

## The pitch

**DoorDash — Buy, medium conviction, starter size.**

Thesis in one sentence: *DoorDash is the demand channel for local commerce, not a delivery toll booth. Merchant advertising is a near-100%-margin revenue stream that scales with GOV without raising commission rates, and the market prices the ad business but misprices how durable it is. The risk is that grocery dilution outruns the margin benefit — so size it small and watch blended take rate.*

## Three pillars

1. **Density is the moat.** Suburban and non-dense markets, where DoorDash built its lead, have higher AOV, thinner restaurant selection, and less contested courier supply. Every incremental order per zip code lowers cost per delivery. That's the profit engine.

2. **Ads is the margin story.** The merchant is a captive buyer of demand — it pays commission *and* ad spend because DoorDash is where the order comes from. Ad revenue carries essentially no courier cost, so each point of ad mix drops to EBITDA at ~100%. Take rate expands through mix, not through squeezing merchants harder. That's what makes it defensible.

3. **Frequency compounds through DashPass.** Members order more and churn less. The right unit is profit per active customer per year, not per order — per-order math makes DashPass look dilutive, per-customer math makes it accretive.

## The one chart that carries the deck

Blended take rate as % of Marketplace GOV, trended quarterly, with grocery/retail share of GOV overlaid. If take rate holds while grocery mix rises, the thesis is working. If take rate slides as grocery climbs, you're wrong. That chart is your entire argument in one image — build the rest of the deck around it.

## The bear case, stated properly

Grocery is a mix-shift problem, not a failure. Higher AOV, much lower take rate, higher cost per order. And critically: **ads don't port to grocery.** Restaurant food is a discovery purchase, so merchants bid for placement. Grocery is replenishment — people rebuy the same basket. Ad value per dollar of GMV is structurally lower. So the highest-margin line grows slower than the business.

The bull defense is the halo: grocery drives weekly habit, which drives DashPass retention, which drives restaurant frequency. Legitimate, but unverifiable — management doesn't disclose grocery cohort behavior. Say that.

## Tripwires

**Move to high confidence if:** blended take rate holds while grocery share rises; ad revenue growth outpaces GOV growth.

**Cut if:** take rate slides two or three consecutive quarters as grocery mix climbs; or courier cost per order rises structurally — minimum pay floors, reclassification, batching failing to offset new-market dilution.

## Deck order

1. Recommendation + medium conviction + sizing rationale
2. What DoorDash actually is — three-sided network, revenue buckets
3. Three thesis pillars
4. The take-rate chart
5. Ads: triangulate off Amazon's ad revenue as % of GMV, show the gap
6. Model: orders × AOV × take rate → contribution profit → EBITDA → FCF
7. Comps: EV/EBITDA and EV/FCF vs. Uber, Instacart, Delivery Hero — be honest about the premium
8. Bear case: grocery dilution
9. Tripwires
10. What would make me wrong

## Two things you must do before Thursday

**Verify every number.** I'm giving you the shape of the argument, not the figures. Pull revenue, GOV, orders, take rate, EBITDA, FCF, cash, share count from the latest 10-Q. Compute take rate yourself — don't trust a summary.

**Do the comps table first.** Everything above assumes DoorDash trades at a premium. If it doesn't, your framing changes and the pitch gets easier. Let the numbers decide which version you give.

## The Q&A answer to rehearse

> "Medium conviction. Direction's right, magnitude's uncertain. I'd want evidence that take rate holds through the grocery mix shift before sizing up, and management doesn't disclose enough to prove it yet. So I'm long the direction, sized for the uncertainty."

That's the pitch. Build it.
