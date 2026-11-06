
import pandas as pd

from utils.preprocessing import load_data
from utils.features import create_features


def prepare_training_data():

    # Load dataset and create features
    df = load_data()
    df = create_features(df)

    # Remove rows without complete historical features
    df = df.dropna(
        subset=[
            "Demand_Lag_1",
            "Demand_Lag_7",
            "Demand_Rolling_7",
            "Demand_Rolling_30",
            "Demand_Rolling_90"
        ]
    ).copy()

    # Updated feature selection
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
        "Demand_Lag_1",
        "Demand_Lag_7",
        "Demand_Rolling_7",
        "Demand_Rolling_30",
        "Demand_Rolling_90"
    ]

    target_column = "Demand"

    # Chronological train-test split
    split_date = pd.Timestamp("2023-11-01")

    train_data = df[
        df["Date"] < split_date
    ].copy()

    test_data = df[
        df["Date"] >= split_date
    ].copy()

    X_train = train_data[feature_columns]
    y_train = train_data[target_column]

    X_test = test_data[feature_columns]
    y_test = test_data[target_column]

    print("\n========== UPDATED TRAINING DATA ==========")

    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))

    print(
        "Training period:",
        train_data["Date"].min(),
        "to",
        train_data["Date"].max()
    )

    print(
        "Testing period:",
        test_data["Date"].min(),
        "to",
        test_data["Date"].max()
    )

    print("\nFeature count:", len(feature_columns))
    print("Target:", target_column)

    print(
        "\nMissing training values:",
        X_train.isnull().sum().sum()
    )

    print(
        "Missing testing values:",
        X_test.isnull().sum().sum()
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    prepare_training_data()
