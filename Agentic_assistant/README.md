# Phase 5 — Insight-to-Action Assistant (Prototype)

This folder contains a Streamlit prototype for the dissertation **Product Development Project**:
**Agentic Insight-to-Action analytics assistant for SMEs**.

## What it does
- Loads KPI tables (**gold_daily_kpis.csv**, **gold_daily_channel_kpis.csv**) and anomaly log (**alerts_daily_combined.csv**)
- Filters alerts by **date range, severity, method, metric**
- For a selected alert, generates:
  1) **What happened** (metric, date, severity, method, direction)
  2) **Evidence** (current vs baseline period, % change, z-score if available)
  3) **Likely drivers** (channel contribution deltas for Revenue/Orders/CAC)
  4) **Recommended actions** from a controlled **Action Library**
  5) **Confidence score** (severity + method agreement + evidence strength)

## Files
- `app.py` — Streamlit app
- `src/analytics.py` — analytics helper functions
- `docs/action_library.csv` — action library (guardrail)
- `requirements.txt` — dependencies

## How to run
1. Copy `docs/action_library.csv` into your dissertation project folder:  
   `C:\Users\dell\Desktop\Documents for UK\dissertation_project\docs\action_library.csv`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the path in `app.py` if needed:
   ```python
   PROJECT_ROOT = r"C:\Users\dell\Desktop\Documents for UK\dissertation_project"
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```

## Required data files (already built in Phases 2 & 4)
- `data_gold/gold_daily_kpis.csv`
- `data_gold/gold_daily_channel_kpis.csv`
- `data_gold/alerts_daily_combined.csv`
