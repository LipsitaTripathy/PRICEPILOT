
import pandas as pd

from utils.preprocessing import load_data


def analyze_pricing_patterns():

    df = load_data()

    print("\n========== PRICING PATTERN ANALYSIS ==========")

    # Correlations across important variables
    columns = [
        "Price",
        "Competitor Pricing",
        "Discount",
        "Promotion",
        "Inventory Level",
        "Demand",
        "Units Sold"
    ]

    print("\nOverall correlations:")
    print(df[columns].corr().round(3))

    # Price-demand correlations within each product-store combination
    grouped = (
        df.groupby(["Store ID", "Product ID"])
        .apply(
            lambda group: pd.Series({
                "Price_Demand_Correlation":
                    group["Price"].corr(group["Demand"]),
                "Price_Competitor_Correlation":
                    group["Price"].corr(group["Competitor Pricing"]),
                "Average_Price": group["Price"].mean(),
                "Average_Demand": group["Demand"].mean()
            }),
            include_groups=False
        )
        .reset_index()
    )

    print("\nStore-product correlation summary:")
    print(
        grouped[
            [
                "Price_Demand_Correlation",
                "Price_Competitor_Correlation"
            ]
        ].describe().round(3)
    )

    # Compare demand by price range within each product
    df["Price_Group"] = pd.qcut(
        df.groupby("Product ID")["Price"].rank(method="first"),
        q=4,
        labels=["Low", "Medium", "High", "Very High"]
    )

    price_analysis = (
        df.groupby(["Product ID", "Price_Group"], observed=True)
        .agg(
            Average_Price=("Price", "mean"),
            Average_Demand=("Demand", "mean"),
            Average_Discount=("Discount", "mean"),
            Average_Competitor_Price=("Competitor Pricing", "mean")
        )
        .reset_index()
    )

    print("\nDemand across price groups (first 20 rows):")
    print(price_analysis.head(20).round(2).to_string(index=False))

    grouped.to_csv(
        "models/store_product_price_patterns.csv",
        index=False
    )

    price_analysis.to_csv(
        "models/price_group_analysis.csv",
        index=False
    )

    print("\nAnalysis files saved successfully.")


if __name__ == "__main__":
    analyze_pricing_patterns()
