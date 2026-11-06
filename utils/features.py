
import pandas as pd
import numpy as np

from utils.preprocessing import load_data


def create_features(df):
    """Create calendar, seasonal and historical demand features."""

    df = df.copy()

    # Calendar features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.day_of_week

    df["IsWeekend"] = (
        df["DayOfWeek"] >= 5
    ).astype(int)

    # Cyclical month features
    df["Month_Sin"] = np.sin(
        2 * np.pi * df["Month"] / 12
    )

    df["Month_Cos"] = np.cos(
        2 * np.pi * df["Month"] / 12
    )

    # Cyclical weekday features
    df["Weekday_Sin"] = np.sin(
        2 * np.pi * df["DayOfWeek"] / 7
    )

    df["Weekday_Cos"] = np.cos(
        2 * np.pi * df["DayOfWeek"] / 7
    )

    # Sort chronologically within each store-product pair
    df = df.sort_values(
        ["Store ID", "Product ID", "Date"]
    ).reset_index(drop=True)

    # Historical demand features
    group = df.groupby(
        ["Store ID", "Product ID"]
    )["Demand"]

    df["Demand_Lag_1"] = group.shift(1)
    df["Demand_Lag_7"] = group.shift(7)

    shifted_demand = group.shift(1)

    # Rolling averages calculated separately per group
    df["Demand_Rolling_7"] = (
        shifted_demand.groupby(
            [df["Store ID"], df["Product ID"]]
        )
        .rolling(7, min_periods=7)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )

    df["Demand_Rolling_30"] = (
        shifted_demand.groupby(
            [df["Store ID"], df["Product ID"]]
        )
        .rolling(30, min_periods=30)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )

    df["Demand_Rolling_90"] = (
        shifted_demand.groupby(
            [df["Store ID"], df["Product ID"]]
        )
        .rolling(90, min_periods=90)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )

    return df


if __name__ == "__main__":

    data = load_data()
    featured_data = create_features(data)

    print("\nFEATURE ENGINEERING SUCCESSFUL")

    print("\nNew columns:")
    print(featured_data.columns.tolist())

    print("\nTotal records:", len(featured_data))

    print(
        "\nMissing 90-day rolling values:",
        featured_data["Demand_Rolling_90"].isna().sum()
    )
