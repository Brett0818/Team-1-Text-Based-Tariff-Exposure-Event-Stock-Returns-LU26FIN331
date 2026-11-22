# Instructor audit: Team 1 (Text-Based Tariff Exposure), Checkpoint 3

**Repo:** Brett0818/Team-1-Text-Based-Tariff-Exposure-Event-Stock-Returns-LU26FIN331 · **Audited commit:** `a60315f` (2026-11-17, `main`, merge of PR #3) · **Seed:** 5, tariff exposure: who lost on Liberation Day? · **CP2 audit:** `audits/02_instructor_audit.md` (commit `412af70`)

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

## Summary

There is no v1 yet. The six commits since Checkpoint 2 change only documentation files, and no code, data or output changed. Two of those changes made things worse:
- `requirements.txt` now begins with the line `pip freeze > requirements.txt`, so `pip install -r requirements.txt` fails (B2).
- `README.md` was deleted. Its replacement describes the older five-ticker notebook (B3).

The v0 pipeline itself still works. With that one line removed, notebooks 02, 04 and 05 rerun and match the committed outputs, and the dashboard launches. All five CP2 findings are still open. The most useful steps before Dec 1: fix the install line, then run the full S&P 500 sample (CP2 A5) with the outcome choice from CP2 A2.

## Follow-up on your Checkpoint 2 audit

Response file: not found. The statuses below come from the repo itself.

| CP2 finding | Status | Evidence |
|---|---|---|
| A1 · Required files missing; README describes three ideas | claimed, not fixed | Commit `aa4528e` ("Status.md (a1)") added a file named `Status`, with no `.md`. Its text is the Checkpoint 1 memo ("the code doesn't run yet due to several bugs …"). `README.md` was deleted (`92c5089`), and `project_readme.md` has no threats-to-validity section. There is still no `PROPOSAL.md` (only PDFs) and no `audits/01_self_audit.md` (`audits/` holds only `02_instructor_audit.md`) |
| A2 · Market-model CAR is mostly a beta estimate | unaddressed | `code/04_event_car.ipynb` and `specs_tried.md` are unchanged since `412af70` (`git diff --stat 412af70 a60315f` lists neither) |
| A3 · Check that the keyword score measures import exposure; test vs industry | unaddressed | `code/03_score_text.ipynb` is unchanged. No hand-label table or industry comparison in `outputs/` |
| A4 · Reproducibility and data details | claimed, not fixed | Commit `b875a7e` ("Add pip freeze command to requirements.txt") added the shell command as line 1 instead of running it. `pip install -r requirements.txt` in a fresh venv exits 1: `ERROR: Invalid requirement: 'pip freeze > requirements.txt'`. The other lines are still unpinned (`pandas>=2.0`, `numpy`, …) |
| A5 · v0 sample picked on expected exposure | unaddressed | `outputs/sample_log.csv` still lists the same 10 firms, and `code/config.py` is unchanged |

**0 of 5 fixed, 5 still open.**

## Checkpoint 3 checks

| Check | Result |
|---|---|
| Reruns from scratch (full sample) | ❌ no full sample. The documented install fails (B2). With line 1 removed, notebooks 02, 04 and 05 rerun (exit 0), and the outputs match to 3.5e-6 (live yfinance drift in `beta`) |
| Inputs have provenance | ✅ unchanged from CP2 (`tenk_manifest.csv`, `prices_download_log.csv`) |
| Keys unique, merges validated | ✅ unchanged from CP2 |
| No look-ahead / survivorship | ⚠️ 10 hand-picked firms (A5) |
| LLM leakage handled | n/a (keyword score). The masked-name plan is in `project_readme.md` |
| `specs_tried.md` complete | ⚠️ unchanged since CP2 (A2) |
| Magnitudes discussed | ❌ |
| Hand checks | ✅ the AAPL CAR (`04`) and NKE (`05`) checks passed in the rerun |
| Threats to validity | ❌ no README threats section (A1, B3) |
| Every number traces to `outputs/` | ✅ the dashboard reads `outputs/` and `data/processed/` |
| Dashboard matches `outputs/` | ✅ for v0: "Firms in sample 10", "Average CAR, Apr 3–4 −1.9%" |

Steps not rerun by design: `code/01_download_edgar.ipynb` (SEC EDGAR; the audit makes no SEC requests). `03_score_text.ipynb` needs the git-ignored 10-K HTML from step 01. These are not counted against you.

## Getting ready for Dec 1

Presentations run only from URLs, with a hard cutoff at 9 minutes (10:45 section) or 10 minutes (12:10 section). Put your URL(s) in column G of the Team Projects sheet.

| Check | Result |
|---|---|
| Dashboard launches from a clean clone | ⚠️ not with the documented install (B2). With `requirements.txt` line 1 removed: `streamlit run app.py --server.headless true --server.port 8609` on a clean export of `a60315f` returned `ok` on `/_stcore/health` after 3 s, and a headless browser clicked all 4 tabs with no exceptions. Streamlit Cloud installs from `requirements.txt`, so a deployed app would fail the same way |
| Dashboard shows the v1 numbers from `outputs/` | ❌ it shows "v0 pilot: 10 hand-picked firms … The full S&P 500 sample comes in v1." |
| README links the live URL(s) | ❌ no README, and no URL in `project_readme.md` |

**Core story for 9–10 minutes:** the S&P 500 exposure score vs the Apr 3–4 CAR, with and without industry controls (CP2 A3), and the market-adjusted vs market-model choice (CP2 A2). Everything else is backup.

## What holds up

- The v0 pipeline still reruns. Notebooks 02, 04 and 05 regenerate `final_dataset.csv`, `summary_stats.csv`, `event_car.csv` and `daily_abnormal_returns.csv` (max relative difference 3.5e-6, which is today's yfinance data vs your pull), and both built-in hand checks pass.
- The dashboard's labeling is honest: "The charts are not evidence for or against the hypothesis."
- `project_readme.md` states the right design: 10-Ks filed before April 2025, masked names for the LLM step, and industry fixed effects.

## New findings

### B1 · Blocking · No v1: no code, data or output changes since Checkpoint 2

**Evidence:** `git diff --stat 412af70 a60315f` touches only `Pip check`, `README.md` (deleted), `Status`, `audits/02_instructor_audit.md`, `project_readme.md` and `requirements.txt`. `outputs/final_dataset.csv` still has 10 firms.

**Why it matters:** Checkpoint 3 was v1 on the full sample. There's no result to present.

**Fix:** Build the S&P 500 sample as of March 2025 (CP2 A5), run steps 01–05 on it, fix the primary outcome in `specs_tried.md` first (CP2 A2), and add the industry comparison (CP2 A3).

**How to show it's fixed:** `outputs/final_dataset.csv` has the full sample, and `outputs/sample_log.csv` gives a reason for every missing member.

### B2 · Blocking · `pip install -r requirements.txt` fails

**Evidence:** `requirements.txt:1` is `pip freeze > requirements.txt`. In a fresh venv, `pip install -r requirements.txt` exits 1 in 0.4 s: `ERROR: Invalid requirement: 'pip freeze > requirements.txt'`. `Pip check` has the venv instructions that lead to this error.

**Why it matters:** Nobody can install the project as documented, and Streamlit Cloud can't build the dashboard from this file.

**Fix:** Run `pip freeze > requirements.txt` in a terminal from your working environment, so the file holds exact versions. Delete the command line, and move the venv steps into the README.

**How to show it's fixed:** `pip install -r requirements.txt` succeeds in a fresh venv, and the notebooks run.

### B3 · Major · The README was deleted, and its replacement describes the old v0

**Evidence:** Commit `92c5089` ("Delete README.md"). `project_readme.md` says the repo "currently contains a v0 proof-of-concept notebook (`VO_end_to_end.ipynb`) built on a 5-ticker test sample" and lists `STATUS.md` and `README.md`, neither of which exists. The pipeline in `code/01`–`05` and `app.py` isn't mentioned. There are no run steps, no threats section and no dashboard URL.

**Fix:** Restore `README.md`: question, run steps for `code/01`–`05` and `app.py`, data sources, threats to validity, and the live URL. Rename `Status` to `STATUS.md` with a current section.

**How to show it's fixed:** `README.md` exists, and its run steps work on a fresh clone.

## How to respond

This audit is `audits/04_instructor_audit.md` in your repo. Fix what you can, then add `audits/05_audit_response.md`, replying to each **B** finding and to each CP2 finding still open (A1–A5): fixed (the commit), disputed (why), or disclosed as a limitation (where).

There's no separate deadline for this response. Keep working through these until your final deliverables are due: the final repo is audited again then.
