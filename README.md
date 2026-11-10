# Team-1-Text-Based-Tariff-Exposure-Event-Stock-Returns-LU26FIN331

Candidate Idea 1: Post-Earnings Announcement Drift (PEAD) & Tradability in 2026

Core Question & Targeted Audience: Do stock prices continue to drift in the weeks following major earnings surprises in the 2020–2026 period, and does the anomaly yield positive risk-adjusted returns after accounting for transaction costs? Targeted at quantitative portfolio managers and buy-side analysts.

One Row of the Final Dataset
ObservationUnit:firm_tickerearnings_announcement_date
Columns: ticker, announcement_date, earnings_surprise_pct, SUE_score, market_cap, analyst_coverage, CAR_minus1_plus1, CAR_plus2_plus60, factor_adjusted_alpha, estimated_trading_cost_bps.
Raw Inputs & Storage Plan: Daily price and volume data via yfinance, quarterly earnings surprise dates via yfinance.Ticker.earnings_dates, and Fama-French 3/5 factor returns from Ken French's data library. Stored under data/raw/yfinance/ and data/raw/ken_french/.
Dashboard Mockup & UI Features: Interactive drift curves showing Cumulative Abnormal Returns (CAR) over event days [-5,+60] segmented by surprise quintiles. Includes dynamic sliders for holding period length (5 to 60 days) and transaction cost thresholds (0 to 50 bps).
Auditor Attack Points & Mitigations:
Survivorship Bias: Using current index membership for historical dates. Mitigation: Pull historical index constituent changes to retain delisted or acquired firms.
Look-Ahead Bias: Earnings announced after market close assigned to day 0. Mitigation: Enforce an explicit timestamp rule assigning post-close announcements to trading day +1.
P-Hacking: Selective reporting of holding windows. Mitigation: Record every parameter variation in specs_tried.md.

Candidate Idea 2: Customer Supply Chain Contagion (Economic Links)

Core Question & Targeted Audience: When a major customer firm announces a significant earnings surprise, do its primary suppliers' stock prices react with a predictable delay? Targeted at supply-chain risk managers, equity analysts, and corporate CFOs.

One Row of the Final Dataset:
ObservationUnit:customer_announcementsupplier_tickerevent_day
Columns: customer_ticker, supplier_ticker, announcement_date, customer_surprise_pct, revenue_share_pct, supplier_CAR_minus1_plus1, supplier_CAR_plus2_plus10, supplier_beta.
Raw Inputs & Storage Plan: SEC EDGAR 10-K filings (Item 1 / Notes disclosing $\ge 10\%$ revenue customers), extracted via LLM parser, matched with daily price series from yfinance. Saved in data/raw/edgar_10k/ and data/raw/prices/.
Dashboard Mockup & UI Features: Network graph displaying customer-supplier connections, customer concentration percentages, and heat-mapped supplier CAR responses upon selecting a customer ticker.
Auditor Attack Points & Mitigations:
LLM Extraction Errors: False customer-supplier entity linking. Mitigation: Hand-audit a randomized sample of 50 pairs to report explicit precision metrics.
Look-Ahead Timing: Supplier links derived from 10-K filings published after the earnings event. Mitigation: Match customer links strictly to 10-K filing dates preceding the event date.

Candidate Idea 3: Text-Based Tariff Exposure & Event Stock Returns

Core Question & Targeted Audience: Did firm-level import and supply-chain tariff exposures disclosed in 10-Ks predict equity losses following trade policy announcements? Targeted at macro strategists, asset allocators, and corporate risk officers.

One Row of the Final Dataset:
ObservationUnit:firm_ticker
Columns: ticker, gics_sector, market_cap, tariff_exposure_score, import_dependency_score, event_CAR_apr3_apr4, pre_event_volatility.
Raw Inputs & Storage Plan: SEC EDGAR 10-K filings prior to April 2025, yfinance daily equity returns, and Ken French industry classifications. Stored under data/raw/edgar_tariffs/ and data/raw/market_data/.
Dashboard Mockup & UI Features: Interactive scatter plot mapping text-based Exposure Scores against Event CAR, filterable by GICS industry sector and market capitalization tiers.
Auditor Attack Points & Mitigations:
LLM Data Leakage: LLM scoring incorporating post-event news knowledge. Mitigation: Apply strict zero-shot prompting constrained exclusively to pre-event 10-K text blocks.
Confounding Industry Shocks: Broad sector downturns driving results instead of firm-specific exposure. Mitigation: Include multi-digit GICS industry fixed effects in all cross-sectional regressions.
