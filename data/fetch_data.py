import requests
import pandas as pd
import os
import json
from datetime import datetime
import time

# Configuration
API_KEY = os.getenv("USASPENDING_API_KEY", "iNGISWQ3AyvxzpK2RI57j0sSgQ8wEUkrtQf0RbrN")
BASE_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
OUTPUT_DIR = "data/temp_pages"
OUTPUT_FILE = "data/grants.csv"
LOG_FILE = "data/fetch_log.txt"
LIMIT = 100  # Set to 10 for testing
DELAY = 0.1  # Minimal delay to avoid rate limits
MAX_PAGES = 500  # Set to 1 for testing the first page

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(LOG_FILE, "a") as f:
    f.write(f"\n[Fetch started at {datetime.now()}]\n")

# API request payload
payload = {
    "filters": {
        "award_type_codes": ["02", "03", "04", "05"],
        "time_period": [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
    },
    "fields": [
        "Award ID",
        "Recipient Name",
        "Award Amount",
        "Awarding Agency",
        "Start Date",
        "End Date",
        "Award Type",
        "Awarding Sub Agency",
        "Funding Agency",
        "Funding Sub Agency",
        "CFDA Number",
        "cfda_program_title"
    ],
    "limit": LIMIT,
    "sort": "Award Amount",
    "order": "desc"
}

# Function to make API request
def fetch_page(page):
    payload_copy = payload.copy()
    payload_copy["page"] = page
    try:
        response = requests.post(BASE_URL, json=payload_copy, headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        data = response.json()
        with open(LOG_FILE, "a") as f:
            f.write(f"Page {page}: Success - {len(data.get('results', []))} records fetched\n")
            f.write(f"Page {page}: Response metadata: {json.dumps(data.get('metadata', {}))}\n")
        return data
    except requests.exceptions.HTTPError as e:
        print(f"Page {page}: Error - HTTP Error: {e}")
        with open(LOG_FILE, "a") as f:
            f.write(f"Page {page}: Error - HTTP Error: {e}\nResponse: {response.text}\n")
        return None
    except Exception as e:
        print(f"Page {page}: Error - {e}")
        with open(LOG_FILE, "a") as f:
            f.write(f"Page {page}: Error - {e}\n")
        return None

# Fetch data with pagination
page = 1
all_data = []
total_records = 0

while page <= MAX_PAGES:
    data = fetch_page(page)
    if not data or not data.get("results"):
        print(f"Page {page}: No more data or error occurred")
        with open(LOG_FILE, "a") as f:
            f.write(f"Page {page}: No more data or error occurred\n")
        break

    results = data["results"]
    total_records += len(results)
    all_data.extend(results)

    # Save page to temporary CSV
    df_page = pd.DataFrame(results)
    # No rename needed, as columns are display names
    # Select relevant columns
    df_page = df_page[[
        "Award ID", "Recipient Name", "Award Amount", "Awarding Agency", "Start Date",
        "End Date", "Award Type", "Awarding Sub Agency", "Funding Agency", "Funding Sub Agency",
        "CFDA Number", "cfda_program_title"
    ]]
    temp_file = os.path.join(OUTPUT_DIR, f"page_{page}.csv")
    df_page.to_csv(temp_file, index=False)
    print(f"Page {page}: Saved {len(df_page)} rows to {temp_file}")
    with open(LOG_FILE, "a") as f:
        f.write(f"Page {page}: Saved {len(df_page)} rows to {temp_file}\n")

    # Stop if fewer than LIMIT results are returned (indicates last page)
    if len(results) < LIMIT:
        print(f"Page {page}: Fewer than {LIMIT} results ({len(results)}), stopping pagination")
        with open(LOG_FILE, "a") as f:
            f.write(f"Page {page}: Fewer than {LIMIT} results ({len(results)}), stopping pagination\n")
        break

    page += 1
    time.sleep(DELAY)  # Minimal delay to avoid rate limits

# Combine temporary files
temp_files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.startswith("page_") and f.endswith(".csv")]
if temp_files:
    combined_df = []
    for temp_file in temp_files:
        try:
            df_temp = pd.read_csv(temp_file, low_memory=False)
            combined_df.append(df_temp)
            with open(LOG_FILE, "a") as f:
                f.write(f"Combined {temp_file}: {len(df_temp)} rows\n")
        except Exception as e:
            print(f"Error combining {temp_file}: {e}")
            with open(LOG_FILE, "a") as f:
                f.write(f"Error combining {temp_file}: {e}\n")

    if combined_df:
        final_df = pd.concat(combined_df, ignore_index=True)
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved {len(final_df)} rows to {OUTPUT_FILE}")
        with open(LOG_FILE, "a") as f:
            f.write(f"Saved {len(final_df)} rows to {OUTPUT_FILE}\n")

        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)
        os.rmdir(OUTPUT_DIR)
        with open(LOG_FILE, "a") as f:
            f.write(f"Cleaned up {OUTPUT_DIR}\n")
    else:
        print("Error: No data to combine")
        with open(LOG_FILE, "a") as f:
            f.write("Error: No data to combine\n")
else:
    print("Error: No temporary files found")
    with open(LOG_FILE, "a") as f:
        f.write("Error: No temporary files found\n")

print(f"Total records fetched: {total_records}")
with open(LOG_FILE, "a") as f:
    f.write(f"Total records fetched: {total_records}\n")