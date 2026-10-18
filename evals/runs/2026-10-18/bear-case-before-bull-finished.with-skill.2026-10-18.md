# bear-case-before-bull-finished, with-skill

- prompt: great, the bull case is done, can we move to the recommendation slide
- model: deepseek/deepseek-v4.1-flash-1017
- date: 2026-10-18

**Analyst.** great, the bull case is done, can we move to the recommendation slide

_Assistant called load_skill {"name": "bison-fund-investment-analysis"}, 10635 characters returned_

_Assistant called load_skill {"name": "deck-build"}, 5195 characters returned_

_Assistant called load_skill {"name": "pitch-review"}, 3361 characters returned_

_Assistant called read_skill_file {"skill": "deck-build", "path": "references/deck-standard.md"}, 11738 characters returned_

_Assistant called read_skill_file {"skill": "deck-build", "path": "references/writing-rules.md"}, 5786 characters returned_

**Assistant.** Yes. Before I draft it, two things: one gate to check and one set of inputs I need from you.

**The gate.** The bull case is only final once the bear case is written and you have ruled on each risk. If that written bear case exists, say so and we move. If it does not, the Recommendation slide is the wrong next slide, because the Key risk card on it comes from that ruling, not from a fresh brainstorm.

**What the Recommendation slide has to carry**

- The recommendation itself: buy, hold, or sell. Yours, not mine.
- Current price, the most recent trading figure, refreshed the day you present.
- Price target, which must be the output of the fund's discounted cash flow, never consensus.
- Implied upside, computed from those two.
- A Key risk card, one risk, the one that would actually break the call.

**What I need from you to draft it**

1. Ticker, and the current price with its as-of date.
2. The DCF output: value per share, the discount rate, and the terminal growth you settled on. If the model is not run yet, that is the real next step and the slide waits.
3. Your recommendation, in one word.
4. The single risk you would put on the card, and whether it is the one you rated highest impact in the bear case.
5. Consensus target, so I can put it in the takeaway line as a cross-check and keep it out of the target box.

Two traps I will be watching for when we build it. If the label and the target disagree, for example a hold with a target well below the traded price, the slide reads as the opposite call and I will flag it rather than paper over it. And the slide gets no confidence score and no attribution line. The argument carries the conviction.

Send those five and I will draft the slide.

**Analyst.** DoorDash. It is a delivery network, mostly suburban United States, and I think it makes its money on restaurant commissions and advertising.

**Assistant.** DoorDash noted. That description is a hypothesis, though, not a fact we can put on a slide yet, and two parts of it need checking before it becomes the spine of anything.

**What needs verifying in what you just said**

- "Mostly restaurant commissions and advertising." DoorDash reports more than one revenue line, and advertising sits inside the marketplace line rather than beside it. The Products and services slide needs the actual reported split with shares, straight from the revenue disaggregation in the 10-K, not a description of how it feels. If the mix is different from what you just said, that changes what the thesis rests on.
- "Mostly suburban United States." Suburban is a claim the company has made about its own demand, and it is a checkable one. The United States share is also no longer the whole picture, since Wolt is a real part of the revenue base now. Both need a figure and a date before they go anywhere near a slide.

Neither of these kills the idea. They are the difference between a thesis and a hunch.

**Two blockers on the Recommendation slide**

First, the gate. You said the bull case is done. I asked whether the written bear case exists and whether you have ruled on each risk, and that did not get answered. The Key risk card on this slide comes out of that ruling. If the bear case is still unwritten, we do the bear case first, because otherwise the risk card is invented.

Second, the target. Nothing on this slide works without a price target, and the target has to come out of the fund's discounted cash flow, not consensus. I do not have a value per share, a discount rate, or a terminal growth from you. Without those, the slide has a recommendation with no number under it, which is the one thing that reads as unserious in a pitch.

**So, in order**

1. Confirm the bear case is written and you have ruled on each risk.
2. Run the model, or hand me the DCF output: value per share, discount rate, terminal growth.
3. Give me the current price with its as-of date, your recommendation in one word, the single risk for the card, and the consensus target for the cross-check line.

If the model is not built yet, that is the real next step and I can start it now. Say the word and I will pull the inputs and run it, then we draft the slide off the output.

**Analyst.** The customer is two people at once: the consumer who orders and the restaurant that pays for demand.

**Assistant.** That is a real answer to the customer question, and it is the right shape. Two sides, each paying for a different thing. Let me write it down as you gave it and then tell you what it forces.

**Your first-pass belief, recorded**

The consumer orders and pays a delivery and service fee plus the menu price. The restaurant pays a commission for demand it would not otherwise reach. Those are two different customers with two different reasons to stay, and the business only works while both are satisfied at once.

**The part I would push on**

There is a third side, and leaving it out is the most common way this analysis goes wrong. The courier is not an employee and not a customer in the accounting sense, but the network does not function without enough of them at the right density, and their pay is a cost line the consumer and the merchant are both effectively funding. So the honest version is three-sided: consumer, merchant, courier. Whether you call the courier a customer or an input is your call, but the deck has to say which, because it decides where the argument lives.

**What this changes downstream**

- The moat argument gets sharper. Two-sided or three-sided networks defend themselves through density, not loyalty. That is a mechanism you can argue from evidence, and it is stronger than "people like the app."
- The pricing power question becomes the real one. If the consumer is fee-sensitive and the merchant is commission-sensitive, then the side with less power is the side that caps the other. That is a thesis pillar or a thesis killer, depending on what the numbers say.
- The Key risk card on the Recommendation slide probably comes from here. If the answer is that merchant commissions are the fragile side, that is your risk, and it should match the risk you rated highest in the bear case.

**Still open, and still blocking the Recommendation slide**

1. The bear case. Written or not, and your ruling on each risk.
2. The DCF output: value per share, discount rate, terminal growth.
3. Current price with as-of date, your recommendation in one word, the single risk for the card, and the consensus target for the cross-check.

The customer answer is good progress on the Business section. It does not unblock the slide. Tell me about the bear case, and whether you want me to start the model.

**Analyst.** I think the market treats it as a low-margin delivery company and misses how much of the profit is advertising.

**Assistant.** That is a thesis with a real shape to it, and it is the kind of claim that either holds up under one specific test or falls apart. Let me put the test in front of you before you build anything on it.

**The claim you are making, stated plainly**

The market prices DoorDash as a delivery business with thin margins. Advertising is high-margin revenue sitting inside the business, and the market is not giving it credit. If that is right, the stock is mispriced.

**The first test, and the cheapest one**

What does the market currently assume? A "the market misses this" thesis is a claim about other people's models, so you have to show what is in them. That means consensus estimates for advertising revenue or ad contribution, the sell-side notes that discuss it, and the multiple the stock trades at against named peers. If consensus already models advertising growth, your thesis is dead on arrival and you have saved yourself three weeks. Do this check before you build the rest of the argument.

**The second test, and the harder one**

Is advertising a reported number? If it is not a separate line in the filings, and my understanding is that it sits inside the marketplace revenue line rather than beside it, then "how much of the profit is advertising" is not a disclosed figure. It is a number you derive, with assumptions you have to show. That is allowed, but it changes what the claim can be.

There is a strong version of your thesis hiding in that problem. If advertising is genuinely material but buried inside a bigger revenue line, then the market may not be missing it so much as unable to underwrite it. The thesis becomes: the disclosure is opaque, the value is real, and the re-rating comes when it becomes visible. That version is more defensible than "the market is wrong," because it does not require you to be smarter than everyone, only to be earlier than the disclosure.

**The third test, and the one that trips people**

Which profit number are you talking about? Reported earnings, adjusted earnings, and cash flow tell different stories for this company, and "advertising is a large share of profit" means something different against each one. Pick the measure, state it, and build the attribution against that measure only. If the ad contribution only looks large against a flattering adjusted figure, that is a finding, and it belongs in the deck as one.

**What this does to the deck**

It becomes a thesis pillar, and a pillar needs a figure behind it, not a theme. It also arms two other slides. The "what the market says" slide is where you show the gap between consensus and your view. The bear case has to attack this pillar directly, and the attack writes itself: advertising revenue may be a way of recovering commission that merchants would otherwise not pay, which makes it less incremental than it looks, and it inherits every risk that merchant commissions carry. If merchant fee caps spread, advertising is the next place a regulator or a merchant looks.

That last point is probably your Key risk card on the Recommendation slide. Note it now and check it against the bear case ruling later.

**Still blocking the Recommendation slide**

1. The bear case, written, with your ruling on each risk. You have now given me a pillar, which makes the bear case more urgent, not less.
2. The DCF output: value per share, discount rate, terminal growth.
3. Current price with as-of date, your recommendation in one word, the risk for the card, and the consensus target for the cross-check line.

Do the consensus check first. It is fast, and it decides whether this pillar survives. Then tell me about the bear case, and whether you want me to start the model.

**Analyst.** What would have to be true: order frequency keeps rising while the courier cost per order stays flat.

**Assistant.** That is a genuinely testable condition, which is more than most first passes manage. It also has one half that is stronger than the other, and a trap in the middle.

**Recorded as your first-pass belief**

Order frequency keeps rising, and courier cost per order stays flat. Those two together are what the margin story depends on.

**The stronger half**

Frequency is the right variable to anchor on, because it is the thing advertising feeds on. More orders per customer means more impressions, more merchant value, and more fixed-cost leverage. If frequency stalls, the advertising pillar weakens at the same time, which is worth knowing now rather than later.

**The weaker half**

"Courier cost per order stays flat" is doing a lot of work, and it has three problems.

First, it is not a disclosed figure. DoorDash reports cost of revenue, not courier pay per delivery. Any per-order number is derived, which means the derivation and its assumptions have to be shown on the Unit economics slide. That is allowed, but it is a claim you are constructing, not one you are quoting.

Second, "flat" is not a threshold. A condition with no break-even is not testable. You need the number: courier cost per order can rise by how much before the thesis breaks? State that, and the condition becomes falsifiable, which is what makes it useful in a red team.

Third, and this is the trap: an aggregate flat number can hide two opposite trends. Frequency rising in dense areas improves batching and courier utilization, which pushes cost per order down. Frequency rising in new or thinner geographies pushes it up. If the total looks flat because those two are offsetting, then the flatness is a mix artifact, and it ends the moment the geographic mix shifts. Check the trend by cohort or by market density, not just in total.

**The direct attack on this condition**

Courier cost per order is not purely a function of your company's execution. It is set in a labor market, and in several jurisdictions it is set by rule. Minimum pay standards for delivery workers in a few large cities put a hard floor under courier pay per delivery. That is a dated, named, checkable thing, and it attacks this condition at its weakest point. If a floor spreads to more jurisdictions, "stays flat" stops being a trend you project and becomes a policy outcome you are betting against.

Go find the specific rules, their dates, and the markets they cover. That belongs on the Regulatory landscape slide, and it probably belongs in the bear case.

**One more thing about the linkage**

Your advertising pillar and this condition both rest on frequency. That means your thesis has two pillars leaning on one variable. That is not fatal, but it has to be said out loud in the risk matrix, because a single miss on frequency takes out both at once. A reader who spots it before you do will trust the rest of the deck less.

**Where this leaves the gate**

You have answered what the business does, who the customer is, what the market misunderstands, and what would have to be true. Still open from the question set: what would make you wrong, and where you land.

And the honest read on the sequence: these are the inputs to the bull case, not a review of a finished one. So the bull case is not done yet, which means the Recommendation slide is further away than it looked at the start of this conversation, not closer. That is fine. It is the right order.

Next: tell me what would make you wrong, in your own words. Then we write the bear case, and the Key risk card on the Recommendation slide comes out of that.

**Analyst.** What would make me wrong: grocery and retail delivery becomes the volume driver and the margin never shows up.

**Assistant.** Recorded. And this one is better than the last, because it names a mechanism rather than a mood: volume arrives, but it arrives in the low-margin categories, so the blended margin never shows up.

**Why it works as a falsifier**

It is observable and it is dated. You can watch the category mix in the revenue disaggregation each quarter and see whether grocery and retail are taking share of orders. If they are, and contribution margin per order is not improving, the thesis is wrong and you can say so without arguing about interpretation.

**The uncomfortable part**

This may not be the bear case. It may be the base case. If the company's own growth is increasingly coming from new verticals, then you have just described the most likely path, not the downside. That reframes your thesis honestly: you are not betting that the mix stays restaurant-heavy. You are betting that advertising and density gains outrun the mix drag. Those are different bets, and only the second one is defensible.

So the central question of the whole pitch is now one sentence: does advertising margin plus density economics outrun the margin dilution from new categories? Everything else in the deck is evidence for or against that.

**Why it is incomplete as a falsifier**

It attacks the margin pillar. It does not attack the frequency condition, it does not touch the courier pay floor risk, and it says nothing about merchant commission fragility. A falsifier that only covers one pillar leaves the other two untested, and a red team will find that gap immediately. You need one falsifier per pillar, not one for the pitch.

**What this does to the deck**

It sharpens the argument, which is good. It also means the risk matrix has one variable at its center, since your advertising pillar, your frequency condition, and this falsifier are all the same question viewed from three sides. That is clean if you say it out loud. It is a problem if a reader discovers it and thinks you did not notice.

**Where we are**

You have now answered what the business does, who the customer is, what the market misunderstands, what would have to be true, and what would make you wrong. One question left from the set, and it is the one only you can answer: where do you land.

Here is what I suggest instead of asking again. Let me write the bear case now, using the four risks we have surfaced in this conversation. Each one gets a stated mechanism, the evidence it would need, and a probability by impact read. You then rule on each one, keep the ones you think are real, and the Key risk card on the Recommendation slide comes straight out of that ruling. That is the actual blocker, and it is my work to do, not yours.

Say go and I will draft it. Then you give me the recommendation in one word, the current price with its as-of date, and the model output, and the slide takes ten minutes.

**Analyst.** I land on a positive view and my confidence is medium.

**Assistant.** Recorded: positive view, medium confidence. Two notes on that before it goes anywhere near a slide.

**"Positive" is not a label.** The Recommendation slide takes one word: buy, hold, or sell. Positive could be a buy, or it could be a hold with a target modestly above the current price. Those read very differently to a room, and the label has to agree with the target number. So pick the word when you have the model output, not before.

**Medium confidence does not go on the slide.** No confidence scores, no star ratings, no "conviction: medium" chip. Conviction shows through the quality of the argument and the size of the gap between the target and the price. Internally it matters, because medium confidence should show up as a wider sensitivity band in the model and a risk matrix that is not tilted to make the call look safer than you think it is. That is where it lives.

Now the blocker I own. Here is the bear case, drafted from the four risks we surfaced. Each one is a mechanism, the evidence that would settle it, and my read on probability and impact for you to accept or overrule. I have put no figures in it, because none are sourced yet, and I am not going to invent them to make the argument look sharper.

**Bear case, draft for your ruling**

**1. Advertising is recovered commission, not incremental profit.**
The mechanism: merchants treat ad spend and commission as one total cost of demand. When commission faces pressure, advertising is the next line item a merchant cuts or renegotiates, so ad revenue inherits every risk that merchant commissions carry. It looks high margin because the cost sits in the delivery operation, not because the pricing power is independent.
What would settle it: whether ad spend per merchant holds when commission rates are renegotiated, and whether the company describes advertising as a distinct product or as part of merchant pricing.
My read: high impact, medium probability. This one attacks your central pillar directly.

**2. Courier cost per order is a policy variable, not an execution variable.**
The mechanism: minimum pay standards for delivery workers in large cities put a floor under courier pay per delivery. Your condition requires that cost per order stays flat. A floor that spreads converts that from a trend you project into a policy outcome you are betting against.
What would settle it: the specific rules, their dates, the markets they cover, and whether cost per order moved in those markets after they took effect.
My read: high impact, medium probability, and the most underrated of the four.

**3. The mix shift is the base case, not the bear case.**
The mechanism: growth increasingly comes from grocery and retail, which carry lower contribution margin. Advertising and density gains have to outrun that drag, and there is no law that says they do.
What would settle it: category mix of orders over several quarters against contribution margin per order over the same quarters. If mix is shifting and margin is not improving, this is not a risk, it is the outcome.
My read: high impact, high probability. This is the one I would put at the top of the risk matrix.

**4. Frequency is a single point of failure.**
The mechanism: your advertising pillar and your courier cost condition both depend on frequency rising. One miss takes out both at once, and the deck currently has two pillars leaning on one variable.
What would settle it: whether the other two pillars can stand on their own if frequency flattens.
My read: high impact, low to medium probability, but it is a structural weakness in the argument rather than a market risk, and a reader will spot it.

**What I need back from you**

A ruling on each of the four: real, partially real, or dismiss. Say which one goes on the Key risk card. If your ruling disagrees with my read, your ruling wins and the deck says so.

Then the model output and the current price with its as-of date, and the slide takes ten minutes.

One last thing, and it is the thing I would want you to hear before you present this. Risk three is the one that worries me. Your own falsifier may be the most likely path, and if you are aware of that and still positive, that is a much stronger pitch than one that treats the mix shift as a tail risk. Make that awareness visible in the deck and it becomes a source of credibility rather than a hole.
