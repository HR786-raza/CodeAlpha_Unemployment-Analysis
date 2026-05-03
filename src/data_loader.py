from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/unemployment.csv")

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    df = df.drop_duplicates()
    df = df.dropna()

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
    )

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    df = df.sort_values(
        by=["Region", "Date"]
    )

    return df