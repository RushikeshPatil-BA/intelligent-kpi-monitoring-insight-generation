from __future__ import annotations
import pandas as pd
import numpy as np
from dataclasses import dataclass

RATE_LIKE = {"conversion_rate_calc","return_rate","cac_proxy","avg_shipping_days","aov"}

@dataclass
class PeriodCompare:
    current_value: float
    baseline_value: float
    pct_change: float | float("nan")

def _agg(series: pd.Series, metric_col: str) -> float:
    # For rate/avg style metrics use mean, otherwise sum.
    if metric_col in RATE_LIKE:
        return float(series.mean())
    return float(series.sum())

def compare_periods(daily: pd.DataFrame, metric_col: str,
                    cur_start: pd.Timestamp, cur_end: pd.Timestamp,
                    base_start: pd.Timestamp, base_end: pd.Timestamp) -> PeriodCompare:
    cur = daily[(daily["date"]>=cur_start) & (daily["date"]<=cur_end)][metric_col]
    base = daily[(daily["date"]>=base_start) & (daily["date"]<=base_end)][metric_col]
    cur_val = _agg(cur, metric_col)
    base_val = _agg(base, metric_col)
    pct = np.nan
    if base_val not in (0.0, None) and not np.isnan(base_val):
        pct = (cur_val - base_val) / base_val
    return PeriodCompare(cur_val, base_val, float(pct) if pct==pct else np.nan)

def channel_contribution(ch: pd.DataFrame, target_col: str,
                         cur_start: pd.Timestamp, cur_end: pd.Timestamp,
                         base_start: pd.Timestamp, base_end: pd.Timestamp) -> pd.DataFrame:
    cur = ch[(ch["date"]>=cur_start) & (ch["date"]<=cur_end)].groupby("channel")[target_col].sum()
    base = ch[(ch["date"]>=base_start) & (ch["date"]<=base_end)].groupby("channel")[target_col].sum()
    delta = (cur - base).sort_values()
    return delta.reset_index().rename(columns={target_col:"delta"})

def confidence_score(severity: str, has_agreement: bool, z_score: float | None, pct_change: float | None) -> int:
    score = {"HIGH": 40, "MEDIUM": 25, "LOW": 10}.get(str(severity).upper(), 10)
    if has_agreement:
        score += 15
    if z_score is not None and not np.isnan(z_score):
        score += min(25, max(0, abs(z_score) * 6))
    if pct_change is not None and not np.isnan(pct_change):
        score += min(20, max(0, abs(pct_change) * 50))
    return int(min(100, score))

def find_method_agreement(alerts: pd.DataFrame, alert_date: pd.Timestamp, metric_label: str) -> bool:
    same = alerts[(alerts["date"]==alert_date) & (alerts["metric"]==metric_label)]
    methods = set(same["method"].astype(str).str.upper().unique())
    return methods.issuperset({"RULES","IFOREST"})
