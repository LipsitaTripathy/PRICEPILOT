
import pandas as pd
from utils.preprocessing import load_data


def analyze_product_elasticity():

    df = load_data()

    print("\n========== PRODUCT PRICE-DEMAND ANALYSIS ==========")

    results = []

    for product_id, group in df.groupby("Product ID"):

        correlation = group["Price"].corr(group["Demand"])

        results.append({
            "Product ID": product_id,
            "Category": group["Category"].iloc[0],
            "Average Price": group["Price"].mean(),
            "Average Demand": group["Demand"].mean(),
            "Price-Demand Correlation": correlation,
            "Unique Prices": group["Price"].nunique()
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "Price-Demand Correlation"
    )

    print("\nProducts with strongest negative price-demand correlation:")

    print(results_df.head(10).round(3).to_string(index=False))

    print("\nProducts with strongest positive price-demand correlation:")

    print(results_df.tail(10).sort_values(
        "Price-Demand Correlation",
        ascending=False
    ).round(3).to_string(index=False))

    print("\nOverall product correlation statistics:")

    print(
        results_df["Price-Demand Correlation"]
        .describe()
        .round(3)
    )

    results_df.to_csv(
        "models/product_price_correlations.csv",
        index=False
    )

    print("\nSaved to models/product_price_correlations.csv")


if __name__ == "__main__":
    analyze_product_elasticity()
