# Specifications tried

Every specification we have run, including the ones we changed or dropped. The newest run is at the bottom. Settings live in `code/config.py`. Each "run" means `python run_all.py` from scratch.

**Count so far:** 2 runs (v0a, v0b). The exposure measure has 1 version (keyword dictionary v1). There are 3 event windows plus 1 market-adjusted check. None of these choices was made by looking at which one gave a "better" correlation.

---

## v0a: first end-to-end run (Nov 15, 2026)

| Setting | Value |
|---|---|
| Sample | 10 hand-picked firms: AAPL, NKE, BBY, TGT, COST, CAT, TSLA, MSFT, JNJ, XOM |
| 10-K rule | Latest form `10-K` filed strictly before 2025-04-02 |
| Ticker → CIK | SEC's current `company_tickers.json` |
| Exposure score | Keyword dictionary v1 (`code/03_score_text.ipynb`): tariff, import, and China phrase counts per 10,000 words |
| Market model | OLS on SPY, trading days −130 to −11 (≈ 6 months), minimum 100 obs |
| Event windows | [0,+1] Apr 3–4 (main), [−1,+1], [0,+3]; plus market-adjusted [0,+1] |

**What happened**
- **9 of 10 firms made it.** XOM was dropped: "no 10-K filed before 2025-04-02." The cause was look-ahead in the ID mapping. SEC's *current* ticker list maps XOM to CIK 0002115436, a newer registrant with no pre-2025 10-K. ExxonMobil's historical CIK (0000034088) did file a 10-K on 2025-02-19.
- **The betas were unstable:** JNJ −0.14 and TSLA 2.94. On Apr 3–4 SPY fell about 10.5%, so the market-model CAR was driven mostly by beta (beta × −10.5%). Correlation between market-model CAR[0,+1] and market-adjusted CAR[0,+1] across firms: **0.26**.
- Correlation of tariff_score with CAR[0,+1]: −0.54 (n = 9). **Not a result.** It is recorded here only for completeness.
- Both hand checks passed (AAPL CAR, NKE market cap and tariff score).

## v0b: fixes from v0a (Nov 15, 2026)

| Change | Why |
|---|---|
| `CIK_OVERRIDES = {"XOM": "0000034088"}` plus a `cik_source` column | Use the CIK that existed in early 2025, not today's mapping (point-in-time IDs) |
| Estimation window −260 to −11 (≈ 1 year), minimum 200 obs | About 6 months of daily data gave noisy betas. About one year is the standard event-study choice. Decided from the betas' plausibility, **not** from the CAR results |
| `PRICE_START` moved to 2023-10-01 | Enough history for the longer window |

**Results:** *(fill in after the run: number of firms, the range of betas, and the correlation between market-model and market-adjusted CAR)*

---

## Planned, not yet run
- Full sample: S&P 500 members as of March 2025, with CIKs from the same point-in-time source.
- Regression: CAR[0,+1] on tariff_score with Fama-French 12 industry fixed effects, vs. industry fixed effects alone.
- LLM exposure score with a written rubric. Compare it to the keyword score on a hand-labeled sample.
- Second event: the Apr 9, 2025 pause.
