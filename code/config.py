"""
Shared settings for the whole pipeline.

Every notebook in code/ imports this file, so a change here (e.g., adding
tickers or changing the event window) flows through the entire project.
"""
import os
from pathlib import Path

# ----------------------------------------------------------------------------
# Paths (all relative to the repo root, so the code runs on any computer)
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

EDGAR_DIR = ROOT / "data" / "raw" / "edgar_tariffs"      # raw 10-K HTML (git-ignored)
MARKET_DIR = ROOT / "data" / "raw" / "market_data"       # raw prices (git-ignored)
PROCESSED_DIR = ROOT / "data" / "processed"              # small intermediate CSVs
OUTPUT_DIR = ROOT / "outputs"                            # final tables and figures

MANIFEST_CSV = PROCESSED_DIR / "tenk_manifest.csv"
DOWNLOAD_PROBLEMS_CSV = PROCESSED_DIR / "download_problems.csv"
PRICES_CSV = MARKET_DIR / "daily_prices.csv"
SCORES_CSV = PROCESSED_DIR / "filing_scores.csv"
CAR_CSV = PROCESSED_DIR / "event_car.csv"
DAILY_AR_CSV = PROCESSED_DIR / "daily_abnormal_returns.csv"
FINAL_CSV = OUTPUT_DIR / "final_dataset.csv"

# ----------------------------------------------------------------------------
# SEC requires a real contact email in every request, or it blocks you.
# Do NOT type your email here (this repo is public). Set it in Colab with:
#     %env SEC_EMAIL=yourname@lehigh.edu
# ----------------------------------------------------------------------------
SEC_EMAIL = os.environ.get("SEC_EMAIL", "")
SEC_HEADERS = {"User-Agent": f"Lehigh FIN331 Team1 research {SEC_EMAIL}"}

# ----------------------------------------------------------------------------
# v0 sample: 10 firms chosen to span high and low expected tariff exposure.
#   Expected high: consumer goods imported from Asia (AAPL, NKE, BBY, TGT, COST)
#   Expected mixed: manufacturers (CAT, TSLA)
#   Expected low: software, pharma, energy (MSFT, JNJ, XOM)
# The full sample (Checkpoint 3) will be S&P 500 members AS OF MARCH 2025.
# ----------------------------------------------------------------------------
TICKERS = ["AAPL", "NKE", "BBY", "TGT", "COST", "CAT", "TSLA", "MSFT", "JNJ", "XOM"]
MARKET = "SPY"  # benchmark for the market model

# Point-in-time CIK fixes. SEC's ticker->CIK list is CURRENT, so a ticker can now point to a
# different (newer) registrant than the one that existed in early 2025. Pin the historical CIK here.
#   XOM: SEC's current list maps XOM to CIK 0002115436 (a new registrant with no pre-2025 10-K).
#        ExxonMobil's historical CIK, which filed the 10-K on 2025-02-19, is 0000034088.
CIK_OVERRIDES = {"XOM": "0000034088"}

# ----------------------------------------------------------------------------
# Event timing
#   "Liberation Day" tariffs were announced Wed Apr 2, 2025 AFTER the close.
#   So the first trading day that could react is Thu Apr 3, 2025 = day 0.
#   The 90-day pause was announced midday Wed Apr 9, 2025 = day +4,
#   so windows ending at day +3 (Tue Apr 8) are not contaminated by the pause.
# ----------------------------------------------------------------------------
ANNOUNCEMENT_DATE = "2025-04-02"
EVENT_DAY0 = "2025-04-03"
TENK_CUTOFF = "2025-04-02"   # a 10-K counts only if filed STRICTLY before this date

PRICE_START = "2023-10-01"   # leaves room for the ~1-year estimation window
PRICE_END = "2025-04-30"     # yfinance end date is exclusive

# Market model estimation window, in trading days relative to day 0.
# v0a used -130..-11 (about 6 months): betas were unstable (JNJ -0.14, TSLA 2.94). See specs_tried.md.
# v0b uses about one year, the standard choice in event studies.
EST_START, EST_END = -260, -11
MIN_EST_OBS = 200
VOL_WINDOW = 60              # pre-event volatility: daily returns over days -60..-1

# Event windows (inclusive, trading days). car_0_1 = Apr 3-4 is the main test.
CAR_WINDOWS = {
    "car_0_1": (0, 1),       # main: Apr 3 - Apr 4
    "car_m1_1": (-1, 1),     # robustness: Apr 2 - Apr 4
    "car_0_3": (0, 3),       # robustness: Apr 3 - Apr 8 (ends before the pause)
}

# Pre-event window for daily abnormal-return paths (used by the dashboard)
AR_PATH_WINDOW = (-10, 3)
