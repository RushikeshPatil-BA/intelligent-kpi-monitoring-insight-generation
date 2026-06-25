# AI-Powered KPI Intelligence & Insight Generation System for SMEs

> **An Intelligent Decision Support System that transforms business KPIs into AI-generated insights and actionable recommendations.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Isolation%20Forest-green)
![Status](https://img.shields.io/badge/Project-Completed-success)

---

# Project Overview

This project was developed as part of my **MSc Business Analytics Dissertation (Product Development Project)**.

The objective was to design and develop an **AI-powered KPI Monitoring and Insight Generation System** specifically for **Small and Medium-sized Enterprises (SMEs).**

Unlike traditional dashboards that only display business metrics, this system continuously analyses KPIs, detects anomalies using Artificial Intelligence, explains why an anomaly occurred, and recommends business actions to decision makers.

The project combines:

-  Business Intelligence
-  Machine Learning
-  Statistical Analytics
-  Explainable AI
-  Decision Support Systems

into a single intelligent platform.

---

# Business Problem

Many SMEs rely on dashboards to monitor KPIs.

Traditional dashboards require managers to:

- Monitor hundreds of KPIs
- Detect anomalies manually
- Investigate root causes
- Decide corrective actions

This process is:

❌ Time consuming

❌ Reactive

❌ Dependent on human interpretation

The proposed system automates the entire workflow.

---

# AI Solution

The developed platform automatically performs:

✅ KPI Monitoring

✅ Hybrid Anomaly Detection

✅ AI Insight Generation

✅ Driver Analysis

✅ Confidence Scoring

✅ AI-Powered Recommendations

Instead of showing raw numbers, the system explains:

> **What happened?**

> **Why did it happen?**

> **How confident is the AI?**

> **What should the business do next?**

---

# ⚙️ AI Architecture

```
Business Data
       │
       ▼
Data Cleaning
       │
       ▼
KPI Engine
       │
       ▼
Hybrid AI Detection
(Rules + Isolation Forest)
       │
       ▼
Business Insight Generator
       │
       ▼
AI Recommendation Engine
       │
       ▼
Executive Dashboard
(Streamlit + Power BI)
```

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Analytics Engine |
| Pandas | Data Processing |
| NumPy | Numerical Analysis |
| Scikit-learn | Isolation Forest ML Model |
| Streamlit | AI Web Application |
| Power BI | Business Dashboard |
| GitHub | Version Control |

---

# 🤖 AI Features

## 1. Intelligent KPI Monitoring

Automatically monitors:

- Revenue
- Orders
- Average Order Value (AOV)
- Conversion Rate
- Return Rate
- Customer Acquisition Cost (CAC)
- Average Shipping Days

---

## 2. Hybrid AI Anomaly Detection

The system combines:

### Statistical Detection

- Rolling Average
- Percentage Change
- Z-Score

with

### Machine Learning

Isolation Forest

This hybrid approach improves interpretability while maintaining strong anomaly detection performance.

---

## 3. AI Executive Brief

For every detected anomaly the assistant generates:

- KPI Analysed
- Alert Severity
- Performance Trend
- Detection Method
- AI Confidence Score
- Executive Recommendation

---

## 4. AI Driver Analysis

The assistant identifies:

- Revenue Drivers
- Order Drivers
- Channel Contribution
- CAC Drivers

allowing decision makers to understand the root cause behind KPI changes.

---

## 5. AI Recommendation Engine

Instead of generic suggestions, recommendations are generated from a controlled business Action Library.

Example:

Revenue ↓

↓

Review Marketing Campaigns

↓

Check Traffic Sources

↓

Investigate Channel Performance

↓

Launch Recovery Strategy

---

## 6. Model Performance Evaluation

The platform continuously reports:

- Precision
- Recall
- F1 Score

allowing users to evaluate AI detection performance.

---

# Screens Included

The project contains:

- AI Monitoring Dashboard
- KPI Trend Analysis
- AI Executive Brief
- Driver Analysis
- AI Recommendation Engine
- Model Evaluation Dashboard
- Power BI Executive Dashboard

---

# Project Structure

```
intelligent-kpi-monitoring-insight-generation/

│
├── Agentic_assistant/
│   ├── app.py
│   └── src/
│       └── analytics.py
│
├── dashboards/
│
├── data_gold/
│
├── data_raw/
│
├── data_silver/
│
├── docs/
│   └── action_library.csv
│
├── notebooks/
│
├── requirements.txt
│
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/RushikeshPatil-BA/intelligent-kpi-monitoring-insight-generation.git
```

Move into the project

```bash
cd intelligent-kpi-monitoring-insight-generation
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run Agentic_assistant/app.py
```

---

# Required Data

The application requires:

```
data_gold/

gold_daily_kpis.csv

gold_daily_channel_kpis.csv

alerts_daily_combined.csv
```

The Action Recommendation Engine requires:

```
docs/

action_library.csv
```

---

# Business Benefits

The proposed system enables SMEs to:

- Detect KPI anomalies automatically
- Reduce manual dashboard monitoring
- Improve decision-making speed
- Generate explainable business insights
- Increase confidence in analytical outputs
- Support data-driven management

---

# Research Contribution

This dissertation contributes by developing a lightweight AI-powered Decision Support System that combines:

- Business Analytics
- Explainable AI
- Hybrid Anomaly Detection
- Automated Insight Generation

into an integrated solution designed specifically for SMEs.

---

# Future Enhancements

Future versions may include:

- Real-time streaming analytics
- Predictive KPI forecasting
- Large Language Model (LLM) integration
- Natural Language Querying
- Autonomous AI Agents
- Microsoft Fabric integration
- Azure Machine Learning deployment

---

# Author

**Rushikesh Atul Patil**

MSc Business Analytics

University of Greenwich

---

# License

This repository was developed for academic research and educational purposes.

---

⭐ If you found this project interesting, please consider starring the repository.
