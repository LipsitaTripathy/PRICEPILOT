import pandas as pd


def load_data(file_path="data/retail_inventory.csv"):
    """Load and validate the retail dataset."""

    df = pd.read_csv(file_path)

    required_columns = [
        "Date",
        "Store ID",
        "Product ID",
        "Category",
        "Region",
        "Inventory Level",
        "Units Sold",
        "Units Ordered",
        "Price",
        "Discount",
        "Weather Condition",
        "Promotion",
        "Competitor Pricing",
        "Seasonality",
        "Epidemic",
        "Demand"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    if df["Date"].isna().any():
        raise ValueError("Invalid dates found in dataset.")

    if df.duplicated().any():
        raise ValueError("Duplicate records found in dataset.")

    if (df["Demand"] < 0).any():
        raise ValueError("Negative demand values found.")

    df = df.sort_values(
        ["Store ID", "Product ID", "Date"]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":
    data = load_data()

    print("Dataset loaded successfully!")
    print("Rows:", len(data))
    print("Columns:", len(data.columns))
    print("Date range:", data["Date"].min(), "to", data["Date"].max())
    print("\nMissing values:")
    print(data.isnull().sum())