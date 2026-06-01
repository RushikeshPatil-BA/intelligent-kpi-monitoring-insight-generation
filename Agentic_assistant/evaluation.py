import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# Load your alerts dataset
df = pd.read_csv("data_gold/alerts_daily_combined.csv")

# ---- STEP 1: Create ground truth ----
df['actual_anomaly'] = 0

# Example thresholds (adjust if needed)
df.loc[df['pct_change'] < -0.3, 'actual_anomaly'] = 1
df.loc[df['pct_change'] > 0.3, 'actual_anomaly'] = 1

# ---- STEP 2: Predictions ----
y_true = df['actual_anomaly']

y_rules = (df['method'] == "RULES").astype(int)
y_iforest = (df['method'] == "IFOREST").astype(int)

# Hybrid = either method detects
y_hybrid = ((y_rules + y_iforest) > 0).astype(int)

# ---- STEP 3: Evaluation function ----
def evaluate(name, y_true, y_pred):
    print(f"\n{name} Results:")
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall:", recall_score(y_true, y_pred))
    print("F1 Score:", f1_score(y_true, y_pred))

# ---- STEP 4: Run evaluation ----
evaluate("Rule-Based", y_true, y_rules)
evaluate("Isolation Forest", y_true, y_iforest)
evaluate("Hybrid Model", y_true, y_hybrid)
