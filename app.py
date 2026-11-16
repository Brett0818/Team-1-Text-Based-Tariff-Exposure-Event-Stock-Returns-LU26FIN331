"""
Dashboard: Text-Based Tariff Exposure & Liberation Day Stock Returns (FIN 331, Team 1)

Run locally:   streamlit run app.py
Reads ONLY files the pipeline writes (run_all.py), so every number shown traces to outputs/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
FINAL_CSV = ROOT / "outputs" / "final_dataset.csv"
AR_CSV = ROOT / "data" / "processed" / "daily_abnormal_returns.csv"
LOG_CSV = ROOT / "outputs" / "sample_log.csv"

# Colors (validated categorical slots 1-2; neutral gray for reference lines)
BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#8a8984"

SCORES = {
    "Tariff exposure score": "tariff_score",
    "Import dependency score": "import_score",
    "China mention score": "china_score",
}
WINDOWS = {
    "CAR [0,+1]: Apr 3–4 (main)": "car_0_1",
    "CAR [−1,+1]: Apr 2–4": "car_m1_1",
    "CAR [0,+3]: Apr 3–8 (before the pause)": "car_0_3",
    "Market-adjusted [0,+1]: Apr 3–4": "mktadj_0_1",
}
FF12_NAMES = {
    "NoDur": "Consumer nondurables", "Durbl": "Consumer durables", "Manuf": "Manufacturing",
    "Enrgy": "Energy", "Chems": "Chemicals", "BusEq": "Business equipment & tech",
    "Telcm": "Telecom", "Utils": "Utilities", "Shops": "Retail & wholesale",
    "Hlth": "Healthcare", "Money": "Finance", "Other": "Other",
}

st.set_page_config(page_title="Tariff Exposure & Liberation Day", layout="wide")


@st.cache_data
def load():
    df = pd.read_csv(FINAL_CSV)
    df["industry"] = df["ff12_industry"].map(FF12_NAMES).fillna(df["ff12_industry"])
    df["size_tier"] = pd.qcut(df["market_cap_musd"].rank(method="first"), 3,
                              labels=["Small", "Mid", "Large"]).astype(str)
    ar = pd.read_csv(AR_CSV) if AR_CSV.exists() else None
    log = pd.read_csv(LOG_CSV) if LOG_CSV.exists() else None
    return df, ar, log


if not FINAL_CSV.exists():
    st.error("No data yet. Run `python run_all.py` first: it creates outputs/final_dataset.csv.")
    st.stop()

df, ar, log = load()

# ---------------------------------------------------------------- header
st.title("Who lost on Liberation Day?")
st.markdown("##### Firm-level tariff exposure measured from 10-K text, and the stock market's reaction to the April 2, 2025 tariff announcement")
st.warning(f"**v0 pilot: {len(df)} hand-picked firms.** This version shows that the pipeline works end to end. "
           "The charts are not evidence for or against the hypothesis. The full S&P 500 sample comes in v1.")

tab_intro, tab_method, tab_results, tab_explore = st.tabs(["Overview", "Method", "Results", "Explore the data"])

# ---------------------------------------------------------------- overview
with tab_intro:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Firms in sample", len(df))
    c2.metric("Event day 0", "Apr 3, 2025")
    c3.metric("Average CAR, Apr 3–4", f"{df['car_0_1'].mean() * 100:.1f}%")
    c4.metric("10-Ks filed before", "Apr 2, 2025")

    st.subheader("The question")
    st.markdown(
        "On **April 2, 2025, after the market closed**, the US announced sweeping tariffs on almost all imports. "
        "Did firms that described more tariff and import exposure in their **own pre-announcement 10-K filings** "
        "lose more value over the next two trading days, **beyond what their industry alone would predict**?"
    )
    st.subheader("Who would pay for the answer")
    st.markdown(
        "- **Macro strategists and portfolio managers:** a screen, built from public filings, that flags which "
        "holdings are exposed before the next trade-policy shock.\n"
        "- **Corporate risk officers and CFOs:** a benchmark of their own firm's disclosed exposure against peers.\n"
    )
    st.subheader("Why it's hard")
    st.markdown(
        "Industry is the obvious answer: retailers and manufacturers import more than software firms. The test "
        "is whether the **text-based** score adds information *within* industries."
    )

# ---------------------------------------------------------------- method
with tab_method:
    st.subheader("Pipeline (each step is a notebook in `code/`; `run_all.py` reruns them all)")
    st.markdown("""
| Step | Notebook | What it does |
|---|---|---|
| 1 | `01_download_edgar` | For each firm, the latest **10-K filed strictly before Apr 2, 2025** (SEC EDGAR), plus SIC code and shares outstanding from that same filing |
| 2 | `02_download_prices` | Daily prices for each firm and SPY, Jan 2024 – Apr 2025 (yfinance) |
| 3 | `03_score_text` | Counts tariff and import phrases in each 10-K, per 10,000 words |
| 4 | `04_event_car` | Market-model abnormal returns, then cumulative abnormal returns (CAR) |
| 5 | `05_build_dataset` | One row per firm: scores, CARs, industry, market cap → `outputs/final_dataset.csv` |
""")
    st.subheader("Exposure score")
    st.latex(r"\text{Tariff score}_i = \frac{\#\,\text{tariff phrases in 10-K}_i}{\#\,\text{words in 10-K}_i}\times 10{,}000")
    st.markdown("Phrases include *tariff(s)*, *trade war / trade policy*, *import / customs / anti-dumping duties*, "
                "*Section 301 / 232*. The plain word *duty* is excluded, so *fiduciary duty* doesn't count.")
    st.subheader("Event study")
    st.latex(r"R_{i,t}=\alpha_i+\beta_i R_{SPY,t}+\varepsilon_{i,t}\quad\text{(estimated on trading days }-130\text{ to }-11)")
    st.latex(r"CAR_i[0,+1]=\sum_{t=0}^{1}\big(R_{i,t}-\hat\alpha_i-\hat\beta_i R_{SPY,t}\big)")
    st.markdown(
        "**Timing:** the announcement came after the close on Apr 2, so **day 0 = Apr 3**. The 90-day pause "
        "came midday on Apr 9 (day +4), so no window goes past Apr 8.\n\n"
        "**Industry:** Fama-French 12 industries from SEC SIC codes. GICS is proprietary, and Yahoo's sector "
        "labels are current, not as of 2025."
    )
    st.subheader("Planned for v1")
    st.markdown("- S&P 500 members **as of March 2025** (avoids survivorship bias)\n"
                "- Regression: CAR on exposure score **with industry fixed effects**\n"
                "- An LLM-based exposure score with a written rubric, checked by hand against the keyword score\n"
                "- Second event: the Apr 9 pause. Do the same firms bounce back?")

# ---------------------------------------------------------------- results
with tab_results:
    f1, f2, f3, f4 = st.columns([1.3, 1.3, 1.6, 1.2])
    score_label = f1.selectbox("Exposure measure", list(SCORES))
    window_label = f2.selectbox("Return window", list(WINDOWS))
    industries = sorted(df["industry"].unique())
    pick_ind = f3.multiselect("Industry", industries, default=industries)
    pick_size = f4.multiselect("Size (within sample)", ["Small", "Mid", "Large"], default=["Small", "Mid", "Large"])

    xcol, ycol = SCORES[score_label], WINDOWS[window_label]
    d = df[df["industry"].isin(pick_ind) & df["size_tier"].isin(pick_size)].copy()

    if len(d) < 2:
        st.info("Select at least two firms to plot.")
    else:
        d["y_pct"] = d[ycol] * 100
        fig = go.Figure()
        fig.add_hline(y=0, line_color=GRAY, line_width=1)
        if d[xcol].nunique() > 1:
            slope, intercept = np.polyfit(d[xcol], d["y_pct"], 1)
            xs = np.linspace(d[xcol].min(), d[xcol].max(), 50)
            fig.add_trace(go.Scatter(x=xs, y=intercept + slope * xs, mode="lines", name="Best-fit line",
                                     line=dict(color=GRAY, width=2, dash="dash"), hoverinfo="skip"))
        fig.add_trace(go.Scatter(
            x=d[xcol], y=d["y_pct"], mode="markers+text", text=d["ticker"], textposition="top center",
            marker=dict(size=12, color=BLUE, line=dict(color="white", width=2)), name="Firm",
            customdata=np.stack([d["company"], d["industry"], d["market_cap_musd"] / 1000], axis=-1),
            hovertemplate="<b>%{text}</b> · %{customdata[0]}<br>%{customdata[1]}<br>"
                          f"{score_label}: " + "%{x:.2f}<br>" + f"{window_label.split(':')[0]}: " + "%{y:.2f}%<br>"
                          "Market cap: $%{customdata[2]:,.0f}B<extra></extra>",
        ))
        fig.update_layout(height=520, showlegend=False, margin=dict(t=30, l=10, r=10, b=10),
                          xaxis_title=f"{score_label} (matches per 10,000 words)",
                          yaxis_title=f"{window_label.split(':')[0]} (%)")
        st.plotly_chart(fig, width="stretch")
        corr = d[xcol].corr(d[ycol])
        corr_txt = "n/a" if pd.isna(corr) else f"{corr:.2f}"
        st.caption(f"n = {len(d)} firms · correlation = {corr_txt}. With this few firms, a correlation means "
                   "little. Treat it as a pipeline check, not a finding.")

    if ar is not None:
        st.subheader("Average cumulative abnormal return around the announcement")
        st.caption("Firms split at the sample median of the selected exposure measure. Day 0 = Apr 3, 2025.")
        med = d[xcol].median() if len(d) else np.nan
        grp = d.assign(group=np.where(d[xcol] > med, "Above-median exposure", "Below-median exposure"))[["ticker", "group"]]
        a = ar.merge(grp, on="ticker", how="inner")
        if a["group"].nunique() == 2:
            path = a.groupby(["group", "event_day"])["car_cum"].mean().reset_index()
            fig2 = go.Figure()
            fig2.add_hline(y=0, line_color=GRAY, line_width=1)
            fig2.add_vline(x=-0.5, line_color=GRAY, line_width=1, line_dash="dot",
                           annotation_text="Announcement (after close Apr 2)", annotation_position="top left")
            for name, color in [("Above-median exposure", ORANGE), ("Below-median exposure", BLUE)]:
                p = path[path["group"] == name]
                fig2.add_trace(go.Scatter(x=p["event_day"], y=p["car_cum"] * 100, mode="lines+markers", name=name,
                                          line=dict(color=color, width=2), marker=dict(size=8),
                                          hovertemplate=name + "<br>Day %{x}: %{y:.2f}%<extra></extra>"))
            fig2.update_layout(height=380, margin=dict(t=30, l=10, r=10, b=10), hovermode="x unified",
                               xaxis_title="Trading days relative to Apr 3, 2025",
                               yaxis_title="Average cumulative abnormal return (%)",
                               legend=dict(orientation="h", y=1.12, x=0))
            st.plotly_chart(fig2, width="stretch")
        else:
            st.info("Need firms on both sides of the median to draw this chart.")

# ---------------------------------------------------------------- explore
with tab_explore:
    st.subheader("One row per firm (from `outputs/final_dataset.csv`)")
    show = df[["ticker", "company", "industry", "filing_date", "market_cap_musd", "word_count",
               "tariff_score", "import_score", "china_score", "car_0_1", "car_m1_1", "car_0_3", "beta"]].copy()
    for c in ["car_0_1", "car_m1_1", "car_0_3"]:
        show[c] = show[c] * 100
    st.dataframe(show, width="stretch", hide_index=True, column_config={
        "market_cap_musd": st.column_config.NumberColumn("Market cap ($M)", format="%,.0f"),
        "word_count": st.column_config.NumberColumn("10-K words", format="%,d"),
        "tariff_score": st.column_config.NumberColumn("Tariff score", format="%.2f"),
        "import_score": st.column_config.NumberColumn("Import score", format="%.2f"),
        "china_score": st.column_config.NumberColumn("China score", format="%.2f"),
        "car_0_1": st.column_config.NumberColumn("CAR Apr 3–4 (%)", format="%.2f"),
        "car_m1_1": st.column_config.NumberColumn("CAR Apr 2–4 (%)", format="%.2f"),
        "car_0_3": st.column_config.NumberColumn("CAR Apr 3–8 (%)", format="%.2f"),
        "beta": st.column_config.NumberColumn("Beta", format="%.2f"),
        "filing_date": "10-K filed",
    })
    st.download_button("Download the dataset (CSV)", df.to_csv(index=False), "final_dataset.csv", "text/csv")

    if log is not None and (~log["in_final"]).any():
        st.subheader("Firms dropped from the sample, and why")
        st.dataframe(log[~log["in_final"]], hide_index=True, width="stretch")

st.divider()
st.caption("FIN 331 · Lehigh University · Team 1. Data: SEC EDGAR, Yahoo Finance (yfinance), Ken French Data Library. "
           "Code: [GitHub repo](https://github.com/Brett0818/Team-1-Text-Based-Tariff-Exposure-Event-Stock-Returns-LU26FIN331)")
