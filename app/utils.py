import pandas as pd
import numpy as np

def load_data():
    """
    Load and preprocess climate datasets for all countries.
    Returns a unified DataFrame.
    """
    countries = {
        "Ethiopia": "../Data/ethiopia.csv",
        "Kenya": "../Data/kenya.csv",
        "Nigeria": "../Data/nigeria.csv",
        "Sudan": "../Data/sudan.csv",
        "Tanzania": "../Data/tanzania.csv"
    }

    dfs = []

    for country, path in countries.items():
        df = pd.read_csv(path)
        df["Country"] = country

        df = df.replace(-999, np.nan)

        df["Date"] = pd.to_datetime(
            df["YEAR"] * 1000 + df["DOY"],
            format="%Y%j"
        )

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def filter_data(df, countries, year_range):
    """
    Filter dataset by country and year range.
    """
    return df[
        (df["Country"].isin(countries)) &
        (df["Date"].dt.year >= year_range[0]) &
        (df["Date"].dt.year <= year_range[1])
    ]


def compute_summary(df, variable):
    """
    Compute summary statistics for selected variable.
    """
    return df.groupby("Country")[variable].agg(
        Mean="mean",
        Std="std",
        Min="min",
        Max="max"
    )