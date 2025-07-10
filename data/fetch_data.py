import requests
import pandas as pd
import sys

url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
payload = {
    "filters": {
        "award_type_codes": ["07", "08"],  # Grant types
        "time_period": [{"start_date": "2020-10-01", "end_date": "2025-09-30"}]
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency", "Start Date"],
    "limit": 100,
    "page": 1
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    if "results" in data:
        df = pd.DataFrame(data["results"])
        df.to_csv("data/grants.csv", index=False)
        print("Data saved to data/grants.csv")
    else:
        print("No results found in response:", data)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print("Response:", response.text)
    sys.exit(1)
except requests.exceptions.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    print("Response:", response.text)
    sys.exit(1)
except Exception as e:
    print(f"Unexpected Error: {e}")
    sys.exit(1)