
import pandas as pd

from utils.preprocessing import load_data
from utils.features import create_features


def prepare_pricing_data():

    df = load_data()
    df = create_features(df)

    required_columns = [
        "Demand_Lag_1",
        "Demand_Lag_7",
        "Demand_Rolling_7",
        "Demand_Rolling_30",
        "Demand_Rolling_90"
    ]

    df = df.dropna(subset=required_columns).copy()

    feature_columns = [
        "Store ID",
        "Product ID",
        "Category",
        "Region",
        "Year",
        "Month",
        "Day",
        "DayOfWeek",
        "IsWeekend",
        "Month_Sin",
        "Month_Cos",
        "Weekday_Sin",
        "Weekday_Cos",
        "Price",
        "Competitor Pricing",
        "Discount",
        "Promotion",
        "Seasonality",
        "Weather Condition",
        "Inventory Level",
        "Demand_Lag_1",
        "Demand_Lag_7",
        "Demand_Rolling_7",
        "Demand_Rolling_30",
        "Demand_Rolling_90"
    ]

    target_column = "Demand"

    split_date = pd.Timestamp("2023-11-01")

    train_data = df[df["Date"] < split_date].copy()
    test_data = df[df["Date"] >= split_date].copy()

    X_train = train_data[feature_columns]
    y_train = train_data[target_column]

    X_test = test_data[feature_columns]
    y_test = test_data[target_column]

    print("\n========== PRICING MODEL DATA ==========")

    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))

    print("Feature count:", len(feature_columns))

    print("\nTraining period:")
    print(train_data["Date"].min(), "to", train_data["Date"].max())

    print("\nTesting period:")
    print(test_data["Date"].min(), "to", test_data["Date"].max())

    print("\nMissing training values:", X_train.isnull().sum().sum())
    print("Missing testing values:", X_test.isnull().sum().sum())

    print("\nPricing features:")
    print(feature_columns)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    prepare_pricing_data()
