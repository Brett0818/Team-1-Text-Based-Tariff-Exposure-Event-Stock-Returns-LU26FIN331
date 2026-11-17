# April 2025 Tariff Shock & Firm Exposure

An empirical event study and cross-sectional analysis measuring whether S&P 500 firms with greater import and China exposure—scored directly from their pre-April 2025 10-K filings—experienced larger stock drops following the April 2, 2025 US tariff announcement.

## Overview & Value Proposition

On April 2, 2025 (after market close), the US announced sweeping tariffs. This project evaluates how effectively a firm's own SEC disclosures predict its market sensitivity to trade shocks. 

* **Target Audience:** Corporate strategists and CFOs looking to benchmark their firm's supply-chain and tariff exposure against industry peers.
* **MVP Scope:** S&P 500 firms, a single LLM-generated exposure score per firm, and the April 3–4, 2025 event window.
* **Stretch Goal:** Extending the analysis to the April 9, 2025 tariff pause to test whether the most exposed firms experienced a symmetric rebound.

## Data & Methodology

1. **Text Data (SEC EDGAR):** Annual 10-K filings submitted strictly prior to April 1, 2025 (`filingDate < "2025-04-01"`) to prevent look-ahead bias.
2. **Market Data (`yfinance`):** Daily adjusted close prices for S&P 500 constituents and `SPY` (market benchmark) covering a 1-year estimation window prior to the shock through the April 2025 event window.
3. **Exposure Scoring:** 
   * *Baseline:* Keyword frequency counts for tariff and import terminology.
   * *Core Model:* Structured LLM rubric scoring import/China reliance from 10-K text (validated against a hand-checked sample, with company identifiers masked to prevent data leakage).
4. **Econometrics:** Cumulative Abnormal Returns (CAR) over April 3–4, 2025, regressed cross-sectionally on firm exposure scores with industry fixed effects and firm size controls.
5. **Dashboard:** Interactive scatter plot comparing firm exposure scores against CAR, filterable by industry.

## Project Structure

```text
├── data/
│   ├── raw/
│   │   ├── edgar_tariffs/      # Pre-April 2025 10-K HTML filings
│   │   └── market_data/        # Daily price series (CSV)
│   └── processed/
│       └── scoring/            # Keyword baselines and LLM exposure scores
├── notebooks/
│   └── VO_end_to_end.ipynb     # v0 proof-of-concept ingestion & scoring pipeline
├── STATUS.md                   # Current development status and open audit questions
└── README.md                   # Project documentation
```

## Current Status & Setup

The repository currently contains a v0 proof-of-concept notebook (`VO_end_to_end.ipynb`) built on a 5-ticker test sample (`AAPL`, `TSLA`, `CAT`, `COST`, `NKE`). See `STATUS.md` for current pipeline blockers and methodological considerations.

### Prerequisites
* Python 3.9+
* Key libraries: `requests`, `yfinance`, `pandas`, `beautifulsoup4`, `python-dotenv`
* Note: SEC EDGAR requires a custom `User-Agent` header (`Name Email`) in all API requests.