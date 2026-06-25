#============================================================
# 1. IMPORT LIBRARIES
#============================================================
import os
import pandas as pd
import numpy as np
import streamlit as st
from datetime import timedelta
from src.analytics import compare_periods, channel_contribution, confidence_score, find_method_agreement

# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI-Powered KPI Intelligence Assistant",
    layout="wide"
)
st.markdown("""
<style>

/* ===============================
   AI Card Styling
================================ */

.ai-card{
#    border-left:9px solid #2E86DE;
    border-radius:14px;
    padding:20px;
    background:transparent;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    margin-top:15px;
    margin-bottom:20px;
}

/* Section Title */
.ai-title{
    font-size:22px;
    font-weight:700;
    margin-bottom:10px;
}

/* Subtitle */
.ai-subtitle{
    font-size:15px;
    color:#666666;
    margin-bottom:15px;
}

/* Divider */
.ai-divider{
    border-top:1px solid #EAEAEA;
    margin-top:12px;
    margin-bottom:12px;
}

/* ===============================
   Reduce Heading Spacing
================================ */

h1{
    margin-top:0px !important;
    margin-bottom:8px !important;
}

h2{
    margin-top:8px !important;
    margin-bottom:8px !important;
}

h3{
    margin-top:6px !important;
    margin-bottom:6px !important;
}

h4{
    margin-top:4px !important;
    margin-bottom:4px !important;
}

hr{
    margin-top:8px !important;
    margin-bottom:12px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='margin-bottom:5px;'>
AI-Powered KPI Intelligence Assistant
</h1>
""", unsafe_allow_html=True)

st.caption("AI-driven anomaly detection, business insight generation and decision support for SMEs.")

st.markdown(""" 
### Welcome to the AI-Powered KPI Intelligence Assistant
This intelligent decision-support system helps SMEs automatically:
- Monitor KPIs in real time
- Detect business anomalies using Hybrid AI
- Explain why anomalies occurred
- Identify business drivers
- Recommend evidence-based actions

Built using: 
- Rule-Based Analytics
- Isolation Forest Machine Learning
- Hybrid AI Decision Engine
- Explainable AI (XAI)
""")

# ============================================================
# 3. PROJECT PATHS
# ============================================================
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
GOLD_DIR = os.path.join(PROJECT_ROOT, "data_gold")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# ============================================================
# 4. LOAD DATA
# ============================================================
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

# ============================================================
# 5. MODEL PERFORMANCE EVALUATION
# ============================================================
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

# ============================================================
# 6. KPI CONFIGURATION
# ============================================================
METRIC_MAP = {
    "Revenue": "revenue",
    "Orders": "orders",
    "AOV": "aov",
    "Conversion Rate": "conversion_rate_calc",
    "Return Rate": "return_rate",
    "CAC Proxy": "cac_proxy",
    "Avg Shipping Days": "avg_shipping_days",
}

# ============================================================
# 7. USER FILTERS
# ============================================================
with st.sidebar:
    st.header("Filters")
    metric_name = st.selectbox("Metric", list(METRIC_MAP.keys()))
    methods = st.multiselect("Method", ["RULES", "IFOREST"], default=["RULES","IFOREST"])
    severities = st.multiselect("Severity", ["HIGH", "MEDIUM", "LOW"], default=["HIGH","MEDIUM","LOW"])

    min_d = daily["date"].min().date()
    max_d = daily["date"].max().date()
    dr = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    baseline_days = st.slider("Baseline window (days)", min_value=7, max_value=28, value=7, step=7)
    top_n = st.slider("Top drivers", min_value=3, max_value=10, value=5)

# ============================================================
# 8. FILTER ALERT DATA
# ============================================================
start_date, end_date = pd.to_datetime(dr[0]), pd.to_datetime(dr[1])

metric_label = metric_name
metric_col = METRIC_MAP[metric_name]

alerts_view = alerts[
    (alerts["date"] >= start_date) & (alerts["date"] <= end_date) &
    (alerts["method"].astype(str).str.upper().isin([m.upper() for m in methods])) &
    (alerts["severity"].astype(str).str.upper().isin([s.upper() for s in severities])) &
    (alerts["metric"].isin([metric_label, "MULTI-METRIC"]))
].copy()

# ============================================================
# 9. DASHBOARD LAYOUT
# ============================================================
left, right = st.columns([2.25, 2])

# ============================================================
# 10. AI MONITORING DASHBOARD
# ============================================================
with left:
    st.markdown("""AI Monitoring Dashboard)
<h2 style="margin-bottom:4px;">
AI Monitoring Dashboard
</h2>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "High Alerts",
        len(alerts_view[alerts_view["severity"]=="HIGH"])
    )

    c2.metric(
        "Medium Alerts",
        len(alerts_view[alerts_view["severity"]=="MEDIUM"])
    )

    c3.metric(
        "Low Alerts",
        len(alerts_view[alerts_view["severity"]=="LOW"])
    )

    c4.metric(
        "Total Alerts",
        len(alerts_view)
    )

    st.markdown("### Alert Distribution")
    st.bar_chart(alerts_view["severity"].value_counts())

    st.markdown("### Recent Alerts")

    st.dataframe(
        alerts_view[
            ["date","metric","severity","method"]
        ].head(10),
        use_container_width=True
    )

    st.info("Select an alert below to generate insights and recommendations.")

# ============================================================
# 11. ALERT SELECTION
# ============================================================
chosen = None

if len(alerts_view) > 0:
    chosen_idx = st.selectbox(
        "Choose an alert to generate an insight:",
        alerts_view.index.tolist(),
        format_func=lambda i:
            f"{alerts_view.loc[i,'date'].date()} | "
            f"{alerts_view.loc[i,'metric']} | "
            f"{alerts_view.loc[i,'severity']} | "
            f"{alerts_view.loc[i,'method']}"
    )

    chosen = alerts_view.loc[chosen_idx]

# ============================================================
# 12. AI BUSINESS INSIGHT ENGINE
# ============================================================
with right:
    st.markdown("## AI Generated Business Insight")
    st.divider()
    
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
        st.markdown("### AI KPI Trend Analysis")
        trend_df = daily[
        (daily["date"] >= base_start)
        & (daily["date"] <= cur_end)
        ][["date", metric_col]]
        st.line_chart(
            trend_df.set_index("date")
        )
        
        st.markdown("## AI Executive Brief")
        st.divider()
        severity_icon = {
            "HIGH":"🔴",
            "MEDIUM":"🟡",
            "LOW":"🟢"
        }.get(chosen["severity"],"🔵")
        
        st.markdown(f"""
<div class="ai-card">

<div class="ai-title">
AI Executive Summary
</div>

<div class="ai-subtitle">
Hybrid AI analysis completed successfully
</div>

<b>KPI Analysed</b><br>
{metric_name}

<div class="ai-divider"></div>

<b>Alert Severity</b><br>
{chosen['severity']} {severity_icon}

<div class="ai-divider"></div>

<b>Performance Trend</b><br>
{direction}

<div class="ai-divider"></div>

<b>Detection Model</b><br>
{chosen['method']}

<div class="ai-divider"></div>

<b>AI Confidence</b><br>
{conf}%

<div class="ai-divider"></div>

<b>Business Recommendation</b><br>
Review the KPI trend, analyse contributing drivers and implement the AI-generated recommendations below.

</div>
""", unsafe_allow_html=True)
        
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

        st.markdown("### AI Drivers Analysis")
        if metric_name in ["Revenue", "Orders", "CAC Proxy"]:
            target = "revenue" if metric_name == "Revenue" else "orders"
            drivers = channel_contribution(ch, target, cur_start, cur_end, base_start, base_end).head(top_n)
            st.write("Top channel contribution deltas (current period vs baseline):")
            st.dataframe(drivers, use_container_width=True)
        else:
            st.write("Driver breakdown is implemented for channel-based metrics (Revenue/Orders/CAC). "
                     "You can extend to category drivers using gold_weekly_category_kpis in the next iteration.")

        st.markdown("### Why did the AI flag this?")
        st.write(
            """
            The anomaly was detected using a hybrid framework combining
            statistical thresholds and Isolation Forest machine learning.
            The KPI behaviour deviated significantly from its historical baseline.
            """
        )
        
        st.markdown("### Recommended actions by AI")
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
        
        st.markdown("## AI Performace Evaluation")
        col1, col2, col3 = st.columns(3)
        col1.metric("Best Precision", round(results_df["Precision"].max(), 2))
        col2.metric("Best Recall", round(results_df["Recall"].max(), 2))
        col3.metric("Best F1 Score", round(results_df["F1 Score"].max(), 2))
        st.dataframe(results_df)
