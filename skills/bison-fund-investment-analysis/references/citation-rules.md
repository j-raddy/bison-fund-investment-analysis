# Citation Rules, The Evidence Standard

The whole point of the skill is that nothing enters a pitch unsourced. This file is the
standard, and the checklist at the bottom is the Phase 5 sign-off.

## The tag

```
<value>, source: <document/site + link>, as-of: <date>, [fact | estimate | opinion]
```

Example:

```
Funded customers 28.4M, source: Q2 2026 earnings presentation, investor.xyz, as-of: 2026-07-30, [fact]
```

## Labeling

- **fact**, reported by the company or a primary source. Verifiable as stated.
- **estimate**, a forecast, projection, TAM sizing, CAGR, or anything computed. Always
 show the assumption behind it.
- **opinion**, a judgment or take. Belongs in the analyst's reasoning, flagged as such.

Mislabeling an estimate as a fact is the most damaging error in an equity pitch.

## Source hierarchy (prefer the top)

1. **Primary filings**, 10-K, 10-Q, 8-K, proxy statement (SEC EDGAR).
2. **Company-disclosed**, earnings calls, investor presentations, IR pages.
3. **Reputable market data**, established data providers, exchange data.
4. **Reputable press**, named outlet, dated, quoting a source.
5. **Anything else**, treat as `[UNVERIFIED]` until confirmed against a primary source.

If a blog cites a filing, cite the filing. Go one level up to the primary source.

## As-of dates are mandatory

Prices, share counts, ratios, and market caps drift daily. A number without an as-of date
is unusable in a pitch. Date every figure, even ones that feel stable.

## `[UNVERIFIED]` handling

- `[UNVERIFIED]` items may live in the working fact sheet as open questions.
- They may **never** appear in the finished pitch, the deck, or the thesis.
- Each one is either upgraded with a real source or deleted before sign-off.

## Phase 6, Verification checklist (analyst signs off)

- [ ] Every figure in the deck traces to a source and an as-of date.
- [ ] Every claim is labeled fact, estimate, or opinion.
- [ ] Every estimate shows its underlying assumption.
- [ ] No `[UNVERIFIED]` item survives anywhere in the deck.
- [ ] Every source was reopened and the number confirmed against the original.
- [ ] Peer comparison metrics are on consistent definitions (account types, margin bases).
- [ ] The price target, thesis pillars, and recommendation are the analyst's own.
- [ ] The bear case is written and each risk has been ruled on.
- [ ] A final proofread pass has caught typos and numbering errors.
