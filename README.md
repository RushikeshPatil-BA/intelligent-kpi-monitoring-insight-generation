# Intelligent-kpi-monitoring-insight-generation
MSc Business Analytics dissertation project developing a hybrid anomaly detection and insight generation system for SME KPI monitoring using Python, Power BI, Streamlit, and Isolation Forest.
# Intelligent KPI Monitoring and Insight Generation System for SMEs

## MSc Business Analytics Dissertation Project

### Project Overview

Small and Medium Enterprises (SMEs) often rely on dashboards and manual analysis to monitor business performance. However, identifying unusual changes in Key Performance Indicators (KPIs) can be time-consuming and may result in delayed decision-making.

This project develops an Intelligent KPI Monitoring and Insight Generation System that combines statistical anomaly detection techniques and machine learning methods to automatically identify KPI anomalies and generate actionable business insights.

The system is designed as a lightweight decision-support solution for SMEs and demonstrates how hybrid analytics techniques can improve KPI monitoring compared to traditional dashboard-only approaches.

## Research Question

How effective is an Intelligent KPI Monitoring and Insight Generation System in improving SME KPI monitoring and business decision-support compared with traditional dashboard-based analysis?

## Project Objectives

* Develop a KPI monitoring framework for SME operations.
* Implement hybrid anomaly detection using statistical rules and Isolation Forest.
* Generate structured business insights from detected anomalies.
* Build interactive Power BI dashboards and a Streamlit prototype.
* Evaluate system performance using quantitative metrics and scenario-based validation.

## Dataset

The project uses a structured synthetic e-commerce dataset designed to simulate SME business operations.

The dataset contains:

* Customer transactions
* Product information
* Marketing channel data
* Revenue metrics
* Order data
* Return information
* Shipping performance indicators

The dataset structure is inspired by the UCI Online Retail Dataset and has been extended to support KPI modelling and anomaly detection experiments.

## Technology Stack

### Analytics & Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Isolation Forest

### Visualisation

* Power BI
* Streamlit

### Development Tools

* Jupyter Notebook
* GitHub

## Project Architecture

The system follows a layered analytics architecture:

Raw Data → Silver Layer → Gold Layer → KPI Modelling → Hybrid Anomaly Detection → Insight Generation → Power BI & Streamlit

Architecture Diagram:

docs/architecture/system_architecture.png

## Repository Structure

### data/

Contains raw, cleaned (silver), and analytical (gold) datasets.

### notebooks/

Contains notebooks used for data preparation, KPI modelling, anomaly detection, and evaluation.

### dashboard/

Contains the Power BI dashboard file.

### app/

Contains the Streamlit application and supporting Python scripts.

### docs/

Contains architecture diagrams, screenshots, and validation outputs.

### results/

Contains anomaly detection outputs and evaluation results.

## Power BI Dashboards

The project includes the following dashboards:

* Executive Overview
* Marketing Performance
* Category Performance
* Operations & Returns
* Alerts & Anomalies

Screenshots are available in:

- [View Streamlit Documentation](https://github.com/RushikeshPatil-BA/intelligent-kpi-monitoring-insight-generation/tree/main/docs/powerbi)

## Streamlit Prototype

The prototype provides:

* KPI monitoring
* Anomaly alerts
* Insight generation
* Evaluation outputs

Screenshots are available in:

- [View Streamlit Documentation](https://github.com/RushikeshPatil-BA/intelligent-kpi-monitoring-insight-generation/tree/main/docs/streamlit)

## Evaluation Framework

The system is evaluated using:

* Precision
* Recall
* F1 Score
* Scenario-based validation
* Dashboard-only vs proposed system comparison

## Key Deliverables

* KPI Monitoring Framework
* Hybrid Anomaly Detection Engine
* Insight Generation Module
* Power BI Dashboard Suite
* Streamlit Prototype
* Evaluation Framework

## Author

Rushikesh Atul Patil
MSc Business Analytics
University of Greenwich - 2026
