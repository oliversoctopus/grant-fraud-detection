import pytest
import pandas as pd
def test_data_pipeline():
    df = pd.read_csv("data/processed_grants.csv")
    assert len(df) >= 26901, "Dataset too small"
    assert not df["Award Amount"].isnull().any(), "Missing Award Amount"