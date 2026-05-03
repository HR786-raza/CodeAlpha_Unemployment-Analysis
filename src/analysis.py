import pandas as pd

RATE = "Estimated Unemployment Rate (%)"

def get_kpis(df: pd.DataFrame) -> dict:
    return {
        "avg": round(df[RATE].mean(), 2),
        "max": round(df[RATE].max(), 2),
        "min": round(df[RATE].min(), 2),
        "states": df["Region"].nunique(),
    }

def yearly_data(df: pd.DataFrame):
    return (
        df.groupby("Year")[RATE]
        .mean()
        .reset_index()
    )

def monthly_data(df: pd.DataFrame):
    return (
        df.groupby("Month")[RATE]
        .mean()
        .reset_index()
    )

def regional_data(df: pd.DataFrame):
    return (
        df.groupby("Region")[RATE]
        .mean()
        .reset_index()
        .sort_values(RATE, ascending=False)
    )

def area_data(df: pd.DataFrame):
    return (
        df.groupby("Area")[RATE]
        .mean()
        .reset_index()
    )

def covid_data(df: pd.DataFrame):
    return df[df["Year"] >= 2020]