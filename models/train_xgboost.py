from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import sys
import numpy as np

# Load data
df = pd.read_csv("data/processed_grants.csv")
if len(df) == 0:
    print("Error: processed_grants.csv is empty")
    sys.exit(1)

# Prepare features
le = LabelEncoder()
X = pd.DataFrame({
    "Award Amount": df["Award Amount"],
    "Recipient Encoded": le.fit_transform(df["Recipient Name"]),
    "CFDA Encoded": le.fit_transform(df["CFDA Title"])
})

# Use anomaly scores from Isolation Forest
df_anomaly = pd.read_csv("data/grants_with_anomalies.csv")
y = (df_anomaly["anomaly"] == -1).astype(int)  # Use anomalies as fraud labels

# Split data
try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
except ValueError as e:
    print(f"Error splitting data: {e}")
    sys.exit(1)

# Train model
model = XGBClassifier(max_depth=6, n_estimators=100, base_score=0.5, objective="binary:logistic")
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
model.save_model("models/xgboost_fraud.json")

from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='precision')
print(f"Cross-Validation Precision: {scores.mean():.2f}")
from sklearn.metrics import f1_score
print(f"F1: {f1_score(y_test, y_pred):.2f}")