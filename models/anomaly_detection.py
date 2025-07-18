import pandas as pd
import sys
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Load data
df = pd.read_csv("data/processed_grants.csv")
if len(df) == 0:
    print("Error: processed_grants.csv is empty")
    sys.exit(1)

# Select and prepare features
le = LabelEncoder()
features = [
    "Award Amount"  # Numerical
]
# Add encoded categorical columns if present
if "Recipient Name" in df.columns:
    df["Recipient Encoded"] = le.fit_transform(df["Recipient Name"].astype(str))
    features.append("Recipient Encoded")
if "Awarding Agency" in df.columns:
    df["Agency Encoded"] = le.fit_transform(df["Awarding Agency"].astype(str))
    features.append("Agency Encoded")
if "cfda_program_title" in df.columns:
    df["CFDA Encoded"] = le.fit_transform(df["cfda_program_title"].astype(str))
    features.append("CFDA Encoded")
# Add datetime feature if present
if "Start Date" in df.columns:
    df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df["Start Date Ordinal"] = df["Start Date"].apply(lambda x: x.toordinal() if pd.notnull(x) else datetime.now().toordinal())
    features.append("Start Date Ordinal")

# Detect anomalies
iso_forest = IsolationForest(contamination=0.01, random_state=42)  # Lower contamination for realistic fraud rate
anomalies = iso_forest.fit_predict(df[features])
df["anomaly"] = anomalies
df.to_csv("data/grants_with_anomalies.csv", index=False)
print("Anomalies saved to data/grants_with_anomalies.csv")