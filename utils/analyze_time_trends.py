import pandas as pd
from utils.preprocessing import load_data


def analyze_time_trends():

    df = load_data()

    df["Date"] = pd.to_datetime(df["Date"])

    print("\n========== TIME TREND ANALYSIS ==========")

    # Monthly averages
    df["YearMonth"] = df["Date"].dt.to_period("M")

    monthly = (
        df.groupby("YearMonth")
        .agg(
            Average_Price=("Price", "mean"),
            Average_Demand=("Demand", "mean"),
            Average_Competitor_Price=("Competitor Pricing", "mean"),
            Average_Discount=("Discount", "mean")
        )
        .reset_index()
    )

    print("\nMonthly trends:")
    print(monthly.round(2).to_string(index=False))

    # Correlation with time for each store-product combination
    results = []

    for (store, product), group in df.groupby(
        ["Store ID", "Product ID"]
    ):

        group = group.sort_values("Date").copy()

        group["Time_Index"] = range(len(group))

        results.append({
            "Store ID": store,
            "Product ID": product,
            "Price_Time_Correlation":
                group["Time_Index"].corr(group["Price"]),
            "Demand_Time_Correlation":
                group["Time_Index"].corr(group["Demand"]),
            "Price_Demand_Correlation":
                group["Price"].corr(group["Demand"])
        })

    trends = pd.DataFrame(results)

    print("\nStore-product time correlation summary:")

    print(
        trends[
            [
                "Price_Time_Correlation",
                "Demand_Time_Correlation",
                "Price_Demand_Correlation"
            ]
        ].describe().round(3)
    )

    # Save results
    monthly.to_csv(
        "models/monthly_pricing_trends.csv",
        index=False
    )

    trends.to_csv(
        "models/store_product_time_trends.csv",
        index=False
    )

    print("\nAnalysis files saved successfully.")


if __name__ == "__main__":
    analyze_time_trends()