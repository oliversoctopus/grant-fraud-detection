from sklearn.ensemble import IsolationForest
import pandas as pd
import sys

# Load data
df = pd.read_csv("data/processed_grants.csv")
if len(df) == 0:
    print("Error: processed_grants.csv is empty")
    sys.exit(1)

# Detect anomalies
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomalies = iso_forest.fit_predict(df[["Award Amount"]])
df["anomaly"] = anomalies
df.to_csv("grants_with_anomalies.csv", index=False)
print("Anomalies saved to data/grants_with_anomalies.csv")