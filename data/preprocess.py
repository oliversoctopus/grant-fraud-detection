import pandas as pd

# Load data
df = pd.read_csv("data/grants.csv")

# Map possible column names
column_map = {
    "Award Amount": ["Award Amount", "total_obligation", "federal_action_obligation"],
    "Recipient Name": ["Recipient Name", "recipient_name"],
    "Start Date": ["Start Date", "period_of_performance_start_date", "date"],
    "CFDA Title": ["cfda_program_title", "CFDA Title"]
}

# Find matching columns
selected_columns = {}
for key, possible_names in column_map.items():
    for name in possible_names:
        if name in df.columns:
            selected_columns[key] = name
            break

# Ensure required columns exist
if not all(key in selected_columns for key in ["Award Amount", "Recipient Name", "Start Date"]):
    print("Error: Missing required columns")
    print(f"Available columns: {list(df.columns)}")
    exit(1)

# Rename columns for consistency
df = df.rename(columns={v: k for k, v in selected_columns.items()})

# Preprocess: Drop rows with missing values, convert types
df = df.dropna(subset=["Award Amount", "Recipient Name", "Start Date"])
df["Award Amount"] = df["Award Amount"].astype(float)
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
df = df.dropna(subset=["Start Date"])  # Drop invalid dates

# Save processed data
df.to_csv("data/processed_grants.csv", index=False)
print(f"Processed {len(df)} rows to data/processed_grants.csv")