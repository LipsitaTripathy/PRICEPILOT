
import pandas as pd

from utils.preprocessing import load_data


def analyze_pricing_data():

    df = load_data()

    print("\n========== PRICING DATA ANALYSIS ==========")

    # Basic pricing information
    print("\nDataset shape:", df.shape)

    print("\nPrice statistics:")
    print(df["Price"].describe())

    print("\nCompetitor pricing statistics:")
    print(df["Competitor Pricing"].describe())

    # Overall correlations
    print("\nPrice and demand correlations:")

    correlation_columns = [
        "Price",
        "Competitor Pricing",
        "Discount",
        "Demand",
        "Units Sold"
    ]

    print(
        df[correlation_columns]
        .corr()
        .round(3)
    )

    # Check price variation for each product-store combination
    price_variation = (
        df.groupby(["Store ID", "Product ID"])
        .agg(
            Average_Price=("Price", "mean"),
            Minimum_Price=("Price", "min"),
            Maximum_Price=("Price", "max"),
            Unique_Prices=("Price", "nunique"),
            Average_Demand=("Demand", "mean"),
            Records=("Demand", "count")
        )
        .reset_index()
    )

    print("\nProduct-store pricing variation:")

    print(
        price_variation[
            [
                "Unique_Prices",
                "Average_Price",
                "Minimum_Price",
                "Maximum_Price"
            ]
        ].describe().round(2)
    )

    print("\nProducts with the most price variation:")

    print(
        price_variation
        .sort_values("Unique_Prices", ascending=False)
        .head(10)
        .to_string(index=False)
    )

    # Save analysis
    price_variation.to_csv(
        "models/pricing_data_analysis.csv",
        index=False
    )

    print("\nAnalysis saved to models/pricing_data_analysis.csv")


if __name__ == "__main__":
    analyze_pricing_data()
