# Instructor audit: Team 1 (Text-Based Tariff Exposure), Checkpoint 2

**Repo:** Brett0818/Team-1-Text-Based-Tariff-Exposure-Event-Stock-Returns-LU26FIN331 · **Audited commit:** `412af70` (2026-11-16, `main`, merge of PR #2) · **Seed:** 5, tariff exposure: who lost on Liberation Day?

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

**Late submission.** At the deadline (Nov 14, 11:59 pm), `main` held only the README, a notebook with syntax errors, and two PDFs. The pipeline audited here arrived on Nov 15–16 (PR #1 and PR #2). Your instructor asked for it to be audited so you get feedback. How the late timing affects your grade is your instructor's decision, not this audit's.

## Summary

You went from nothing runnable to a clean v0 in a day. Five notebooks run in order from `run_all.py`:
1. pick each firm's last 10-K filed before April 2, 2025;
2. pull prices;
3. score tariff, import and China keywords per 10,000 words;
4. estimate market-model CARs for April 3–4;
5. build one row per firm, plus a dashboard that reads only `outputs/`.

**What I checked:**
- **Rerun.** The steps that don't need SEC reproduce your committed outputs on a clean install. The largest relative difference is 4e-5, which is yfinance drift.
- **Independent check.** My own code reproduces all 10 market-model CARs and all 10 market-adjusted returns exactly.
- **Industry map.** Your FF12 mapping matches Ken French's `Siccodes12.txt`.

**What to fix:**
1. Several required files are still missing (A1).
2. On a day the market fell 10.8%, the market-model CAR is largely a bet on each firm's estimated beta. It flips sign for TSLA and JNJ, and it moves your headline correlation from −0.17 to −0.38 (A2).
3. The keyword score picks up things that aren't import exposure, and 10-Ks filed after the November 2024 election mention tariffs more for reasons unrelated to exposure. Plan the seed's industry-dummy test before scaling up (A3).

| Check | Result |
|---|---|
| Reruns from scratch | ⚠️ `python run_all.py` stops at step 01 as designed, because `SEC_EMAIL` isn't set (the audit environment doesn't contact SEC). Steps 02, 04 and 05 rerun on the committed manifest and scores: exit 0 each (5.2 s, 2.4 s, 7.0 s), and the outputs match. Step 03 needs the git-ignored 10-K HTML, so it wasn't rerun |
| Inputs have provenance | ✅ accession numbers, URLs, filing dates and download times in `tenk_manifest.csv`; a yfinance version and pull time in `prices_download_log.csv`; a problems log |
| Keys unique, merges validated | ✅ `is_unique` asserts and `validate="1:1"` on every merge (`05_build_dataset`, cell 4) |
| No look-ahead / survivorship | ✅ 10-Ks filed strictly before 2025-04-02 (asserted), and a point-in-time CIK fix for XOM. ⚠️ 10 hand-picked firms (v0, disclosed). ⚠️ the 10-K vintage varies (A3) |
| LLM leakage handled | n/a so far (keyword dictionary). The proposal plans EDSL/LLM scoring (A3) |
| `specs_tried.md` complete | ⚠️ v0a logged well. v0b's results are still a placeholder (A2) |
| Magnitudes discussed | ❌ not yet |
| Hand checks | ✅ AAPL CAR (`04`, cell 8) and NKE market cap and tariff score (`05`, cell 10) recompute and assert. Regex unit tests (`03`, cell 4) |
| Threats to validity | ❌ not in the README (only in the proposal PDF) (A1) |
| Every number traces to `outputs/` | ✅ the dashboard reads only `outputs/` and `data/processed/` |

## What holds up

- **Day-0 timing (a seed item).** The announcement came after the close on Wed Apr 2, so day 0 is Thu Apr 3. I confirmed on the NYSE calendar that Apr 2 is the session before. `car_0_3` ends Tue Apr 8, before the midday Apr 9 pause. Both are documented in `code/config.py`.
- **Point-in-time IDs.** You caught that SEC's current ticker list maps XOM to a new registrant, and pinned ExxonMobil's historical CIK (`CIK_OVERRIDES`, with a `cik_source` column). That's exactly the kind of look-ahead this course asks you to find yourselves, and you logged it in `specs_tried.md`.
- **Event study.** My recomputation (adjusted closes, OLS on SPY over trading days −260 to −11, 250 observations) matches `event_car.csv` to the printed precision for all 10 firms. Example: AAPL beta 0.9666, CAR[0,+1] −0.06213.
- **Industry map.** All 10 SICs map to the same FF12 industry as Ken French's file, and your range table has the same number of ranges per industry.
- **Engineering.** One config file, relative paths, regex tests with deliberate near-misses ("fiduciary duty", "important"), a sample log that explains every firm in or out, and a snippets file for checking matches by hand.

## Findings

### A1 · Major · Required files are still missing, and the README describes three ideas

**Evidence:** at `412af70` there is:
- no `PROPOSAL.md` (only `FIN Project proposal .pdf`, uploaded Nov 16);
- no `STATUS.md` and no `audits/01_self_audit.md`;
- a `README.md` that still presents "Candidate Idea 1/2/3", with no threats-to-validity section, no run steps, and no dashboard link (`app.py` exists, but nothing says how to launch it or where it's deployed).

**Why it matters:** these are required Checkpoint 2 items. The README is the first thing a reader or auditor sees, and right now it doesn't describe your project.

**Fix:**
- Rewrite the README for the tariff project: question, data, `export SEC_EMAIL=… && python run_all.py`, `streamlit run app.py` (or the deployed link), and a threats section (A2 and A3 belong there).
- Add `PROPOSAL.md` (the PDF's text is fine), `STATUS.md`, and `audits/01_self_audit.md`.

**How to show it's fixed:** the files exist, and the README's run steps work on a fresh clone.

### A2 · Major · The market-model CAR is mostly a beta estimate, and the choice changes your answer

**Evidence:** recomputed independently and identical to `data/processed/event_car.csv`.

- SPY returned −10.78% over Apr 3–4. The market-model CAR subtracts β̂ × (−10.78%), so a beta error of 0.1 moves a firm's CAR by about 1.1 pp. Your betas' standard errors are 0.07–0.26, which means 0.8–2.8 pp of noise per firm from the beta alone.
- The two measures disagree in sign for two firms:

  | Firm | β̂ | Market-model CAR[0,+1] | Market-adjusted |
  |---|---|---|---|
  | TSLA | 2.73 | +13.3% | −5.1% |
  | JNJ | −0.14 | −2.9% | +9.5% |

- Across the 10 firms, the two CARs correlate 0.31.
- The headline correlation with `tariff_score` is −0.38 on the market-model CAR and −0.17 on the market-adjusted one.
- In `specs_tried.md`, v0b lengthened the estimation window because the v0a betas (JNJ −0.14, TSLA 2.94) looked unstable. The v0b run still gives JNJ −0.144 and TSLA 2.73. Its "Results" line is still "*(fill in after the run…)*".

**Why it matters:** the question is which firms lost because of tariffs. With n = 10 and a −11% market day, the beta choice moves the ranking more than the exposure score does. On the full S&P 500 it will still move individual firms by several points.

**Fix:**
- Before the full run, pick the primary outcome and log the reason in `specs_tried.md`. Two good options:
  - industry-adjusted returns (firm minus its FF12 or FF49 industry portfolio), which also helps A3;
  - a market model with the beta shrunk toward 1 (Vasicek/Blume).
- Report the other measures as robustness.
- Fill in v0b's results line: number of firms, beta range, and the correlation of the two CARs.

**How to show it's fixed:** `specs_tried.md` names the primary outcome before the full-sample results exist, and the final table reports both measures.

### A3 · Major · Make sure the keyword score measures import exposure, then test it against industry

**Evidence:**
- **`china_score` counts every mention of China.** That includes revenue segments: AAPL's "greater china … iphone revenue", TSLA's "china 20,944 21,745" sales table. It also includes factory and store lists (CAT "shanghai, china; tianjin, china", COST "seven in china") and regulation (MSFT, JNJ). See `outputs/keyword_snippets_sample.csv`, `china` rows. AAPL has the second-highest `china_score` (6.72) mostly through sales exposure, which is a different channel from import costs.
- **`import_words` matches patent boilerplate.** AAPL: "develop, manufacture, use, import or offer for sale" (`keyword_snippets_sample.csv`). It's 1 of 20 sampled snippets, but this phrase appears in many tech and pharma 10-Ks.
- **The 10-K vintage changes the text.** Filing dates run from Jul 2024 (NKE, MSFT) to Mar 2025 (BBY, TGT). BBY's March 2025 10-K already estimates "approximately 55% and 20%" of its merchandise from China and Mexico. Filings written after the November 2024 election discuss tariffs more whatever the firm's exposure, so the vintage can be confused with exposure.
- **The seed's checks aren't planned in the code yet:**
  - does the score beat simple industry dummies?
  - leakage, once you add the LLM scoring the proposal describes (EDSL).

**Why it matters:** if the score partly measures "sells in China" or "filed recently", a correlation with CARs can't be read as import or tariff exposure.

**Fix:**
- Count only in Item 1A (Risk Factors) and Item 7, or require a supply-side context for China matches ("manufactur", "supplier", "sourc", "import").
- Drop the "make, use, import or sell" patent phrase.
- Add filing month (or "filed after 2024-11-05") as a control or a split.
- Hand-label 20 firms high, medium or low from the snippets *before* the full run, and report the score's agreement with your labels.
- Pre-register `CAR ~ exposure + C(ff12)` against `CAR ~ C(ff12)` (the seed's test).
- When you add the LLM score, run it on name-masked text, and check it on a few firms whose April 2025 outcome the model shouldn't know.

**How to show it's fixed:** a hand-label table in `outputs/`, the dated specs entries, and the industry-only comparison in the results.

### A4 · Minor · Reproducibility and data details

**Evidence:**
- **Unpinned requirements.** `requirements.txt` is unpinned (`pandas>=2.0`, `numpy`, `yfinance>=0.2.40`). It installed pandas 3.1.1 and yfinance 1.8.0 here and ran, but your run used yfinance 0.2.66.
- **Step 03 depends on SEC.** The 10-K HTML is git-ignored, so step 03 can only be rerun after an SEC download. That's fine, but the accession list in `tenk_manifest.csv` is then the only record of the text you scored; a SHA-256 of each file would make it checkable.
- **Market cap mixes dates.** NKE uses FY2024 weighted-average shares (`shares_source = weighted_avg_basic`, fiscal year ending May 2024) against an Apr 2, 2025 price. The others use cover-page counts from different dates.

**Fix:**
- Pin the versions you ran (`pip freeze`).
- Add a hash column to the manifest.
- Note the share-count date. Market cap isn't in a regression yet, so it's low priority.

**How to show it's fixed:** a clean install of the pinned file reproduces `outputs/`.

### A5 · Minor · The v0 sample was picked on expected exposure

**Evidence:** `code/config.py` chooses the 10 firms as "expected high", "mixed" and "low". You disclose this, and it's fine for v0. Your plan for Checkpoint 3 is "S&P 500 members AS OF MARCH 2025". Today's ticker list still supplies the CIKs for 9 of the 10 firms (`cik_source = SEC current ticker list`).

**Fix:** take the March 2025 constituents from a dated source (for example, a pinned Wikipedia revision of the S&P 500 list), and map tickers to CIKs as of that date. Your XOM override shows why. Log firms that have since been delisted or renamed rather than dropping them.

**How to show it's fixed:** `outputs/sample_log.csv` lists every March 2025 member, and the reason for each one that's missing.

## How to respond

This audit is `audits/02_instructor_audit.md` in your repo. Fix what you can, then add `audits/03_audit_response.md`, replying to each finding ID: fixed (the commit), disputed (why), or disclosed as a limitation (where).

**Deadline: Saturday, November 21, 2026.**
