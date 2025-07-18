from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pandas as pd
import sys

# Load data
df = pd.read_csv("data/processed_grants.csv")
if len(df) == 0:
	print("Error: processed_grants.csv is empty")
sys.exit(1)

# Prepare features
le = LabelEncoder()
scaler = MinMaxScaler()
df["Recipient Encoded"] = le.fit_transform(df["Recipient Name"])
df["Award Amount Normalized"] = scaler.fit_transform(df[["Award Amount"]])
features = ["Award Amount Normalized", "Recipient Encoded"]

# Detect anomalies
iso_forest = IsolationForest(contamination=0.01, random_state=42)  # Lower contamination to reduce false positives
anomalies = iso_forest.fit_predict(df[features])
df["anomaly"] = anomalies
df.to_csv("data/grants_with_anomalies.csv", index=False)
print("Anomalies saved to data/grants_with_anomalies.csv")