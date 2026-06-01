\
import os
import pandas as pd
import numpy as np
import streamlit as st
from datetime import timedelta
from src.analytics import compare_periods, channel_contribution, confidence_score, find_method_agreement

st.set_page_config(page_title="Insight-to-Action Assistant", layout="wide")

# ---- UPDATED ----
PROJECT_ROOT = r"C:\Users\dell\Desktop\Documents for UK\dissertation_project"
GOLD_DIR = os.path.join(PROJECT_ROOT, "data_gold")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

@st.cache_data
def load_data():
    daily = pd.read_csv(os.path.join(GOLD_DIR, "gold_daily_kpis.csv"))
    daily["date"] = pd.to_datetime(daily["date"], errors="coerce")
    daily = daily.dropna(subset=["date"]).sort_values("date")

    ch = pd.read_csv(os.path.join(GOLD_DIR, "gold_daily_channel_kpis.csv"))
    ch["date"] = pd.to_datetime(ch["date"], errors="coerce")
    ch = ch.dropna(subset=["date"]).sort_values("date")

    alerts = pd.read_csv(os.path.join(GOLD_DIR, "alerts_daily_combined.csv"))
    alerts["date"] = pd.to_datetime(alerts["date"], errors="coerce")
    alerts = alerts.dropna(subset=["date"]).sort_values(["date","severity"], ascending=[False, True])

    actions = pd.read_csv(os.path.join(DOCS_DIR, "action_library.csv"))
    return daily, ch, alerts, actions

daily, ch, alerts, actions = load_data()

# ---- Evaluation Setup ----
from sklearn.metrics import precision_score, recall_score, f1_score

df_eval = alerts.copy()

# Create ground truth
df_eval['actual_anomaly'] = 0
df_eval.loc[df_eval['pct_change'].abs() > 0.3, 'actual_anomaly'] = 1

y_true = df_eval['actual_anomaly']

# Predictions
y_rules = (df_eval['method'] == "RULES").astype(int)
y_iforest = (df_eval['method'] == "IFOREST").astype(int)
y_hybrid = ((y_rules + y_iforest) > 0).astype(int)

def evaluate_df(y_true, y_pred, name):
    return {
        "Method": name,
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred)
    }

results = [
    evaluate_df(y_true, y_rules, "Rule-Based"),
    evaluate_df(y_true, y_iforest, "Isolation Forest"),
    evaluate_df(y_true, y_hybrid, "Hybrid")
]

results_df = pd.DataFrame(results)

METRIC_MAP = {
    "Revenue": "revenue",
    "Orders": "orders",
    "AOV": "aov",
    "Conversion Rate": "conversion_rate_calc",
    "Return Rate": "return_rate",
    "CAC Proxy": "cac_proxy",
    "Avg Shipping Days": "avg_shipping_days",
}

st.title("Insight-to-Action Assistant (Phase 5 Prototype)")
st.caption("Alert-driven assistant: Summary → Evidence → Drivers → Actions → Confidence.")

with st.sidebar:
    st.header("Filters")
    metric_name = st.selectbox("Metric", list(METRIC_MAP.keys()))
    methods = st.multiselect("Method", ["RULES", "IFOREST"], default=["RULES","IFOREST"])
    severities = st.multiselect("Severity", ["HIGH", "MEDIUM", "LOW"], default=["HIGH","MEDIUM"])

    min_d = daily["date"].min().date()
    max_d = daily["date"].max().date()
    dr = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    baseline_days = st.slider("Baseline window (days)", min_value=7, max_value=28, value=7, step=7)
    top_n = st.slider("Top drivers", min_value=3, max_value=10, value=5)

start_date, end_date = pd.to_datetime(dr[0]), pd.to_datetime(dr[1])

metric_label = metric_name
metric_col = METRIC_MAP[metric_name]

alerts_view = alerts[
    (alerts["date"] >= start_date) & (alerts["date"] <= end_date) &
    (alerts["method"].astype(str).str.upper().isin([m.upper() for m in methods])) &
    (alerts["severity"].astype(str).str.upper().isin([s.upper() for s in severities])) &
    (alerts["metric"].isin([metric_label, "MULTI-METRIC"]))
].copy()

left, right = st.columns([1.25, 1])

with left:
    st.subheader("Alerts (filtered)")
    st.dataframe(alerts_view.head(200), use_container_width=True, height=520)
    st.info("Tip: Filter Severity=HIGH and narrow dates for quick review.")

chosen = None
if len(alerts_view) > 0:
    chosen_idx = st.selectbox(
        "Choose an alert to generate an insight:",
        alerts_view.index.tolist(),
        format_func=lambda i: f"{alerts_view.loc[i,'date'].date()} | {alerts_view.loc[i,'metric']} | {alerts_view.loc[i,'severity']} | {alerts_view.loc[i,'method']}"
    )
    chosen = alerts_view.loc[chosen_idx]

with right:
    st.subheader("Generated Insight")
    if chosen is None:
        st.warning("No alerts found for the selected filters.")
    else:
        alert_date = pd.to_datetime(chosen["date"])
        cur_end = alert_date
        cur_start = alert_date - timedelta(days=baseline_days-1)
        base_end = alert_date - timedelta(days=baseline_days)
        base_start = alert_date - timedelta(days=baseline_days*2-1)

        comp = compare_periods(daily, metric_col, cur_start, cur_end, base_start, base_end)

        pct = comp.pct_change
        if not np.isnan(pct):
            direction = "UP" if pct > 0 else "DOWN"
        else:
            direction = "UP" if comp.current_value > comp.baseline_value else "DOWN"

        agreement = find_method_agreement(alerts, alert_date, metric_label)
        conf = confidence_score(
            chosen.get("severity","MEDIUM"),
            agreement,
            chosen.get("z_score", np.nan),
            chosen.get("pct_change", np.nan)
        )

        st.markdown("### What happened")
        st.write(f"**{metric_name}** triggered a **{chosen['severity']}** alert on **{alert_date.date()}** "
                 f"({chosen['method']}). Direction: **{direction}**.")

        st.markdown("### Evidence")
        st.json({
            "Current period": f"{cur_start.date()} → {cur_end.date()}",
            "Baseline period": f"{base_start.date()} → {base_end.date()}",
            "Current value": comp.current_value,
            "Baseline value": comp.baseline_value,
            "% change": comp.pct_change,
            "z_score (if available)": chosen.get("z_score", np.nan),
            "pct_change (day-level, if available)": chosen.get("pct_change", np.nan),
            "Agreement (RULES+IFOREST same day/metric)": agreement,
            "Confidence (0-100)": conf,
        })

        st.markdown("### Likely drivers")
        if metric_name in ["Revenue", "Orders", "CAC Proxy"]:
            target = "revenue" if metric_name == "Revenue" else "orders"
            drivers = channel_contribution(ch, target, cur_start, cur_end, base_start, base_end).head(top_n)
            st.write("Top channel contribution deltas (current period vs baseline):")
            st.dataframe(drivers, use_container_width=True)
        else:
            st.write("Driver breakdown is implemented for channel-based metrics (Revenue/Orders/CAC). "
                     "You can extend to category drivers using gold_weekly_category_kpis in the next iteration.")

        st.markdown("### Recommended actions (Action Library)")
        recs = actions[(actions["metric"]==metric_name) & (actions["direction"]==direction)]
        if len(recs)==0:
            st.info("No matching action rule found. Add it to docs/action_library.csv.")
        else:
            for _, r in recs.iterrows():
                st.markdown(f"**{r['action_title']}**  \n"
                            f"- Impact: **{r['expected_impact']}** | Effort: **{r['effort']}** | Owner: **{r['owner']}**  \n"
                            f"- Steps: {r['action_steps']}  \n"
                            f"- Evidence needed: {r['evidence_needed']}")

        st.markdown("---")
        st.caption("Evidence-based prototype: uses gold tables + alert log and only pre-approved actions.")
        
        st.markdown("## Model Evaluation Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Best Precision", round(results_df["Precision"].max(), 2))
        col2.metric("Best Recall", round(results_df["Recall"].max(), 2))
        col3.metric("Best F1 Score", round(results_df["F1 Score"].max(), 2))
        st.dataframe(results_df)

