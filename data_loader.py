# data_loader.py

import pandas as pd

def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv("sales_data.csv")

    # Convert types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Quantity"] = df["Quantity"].astype(int)
    df["Price Each"] = df["Price Each"].astype(float)

    # Create revenue column
    df["Revenue"] = df["Quantity"] * df["Price Each"]

    # Time features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Year_Month"] = df["Date"].dt.to_period("M")

    return df