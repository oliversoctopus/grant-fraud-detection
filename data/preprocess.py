import pandas as pd
df = pd.read_csv("data/grants.csv")
df = df.dropna(subset=["Award Amount", "Recipient Name", "Start Date"])
df["Award Amount"] = df["Award Amount"].astype(float)
df["Start Date"] = pd.to_datetime(df["Start Date"])
df.to_csv("data/processed_grants.csv", index=False)
print("Processed data saved to data/processed_grants.csv")