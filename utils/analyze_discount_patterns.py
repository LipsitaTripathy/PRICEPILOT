
import pandas as pd
from utils.preprocessing import load_data


def analyze_discount_patterns():

    df = load_data()

    print("\n========== DISCOUNT AND PROMOTION ANALYSIS ==========")

    print("\nDiscount statistics:")
    print(df["Discount"].describe().round(2))

    print("\nDemand by promotion status:")

    promotion_analysis = (
        df.groupby("Promotion")
        .agg(
            Average_Demand=("Demand", "mean"),
            Average_Price=("Price", "mean"),
            Average_Discount=("Discount", "mean"),
            Record_Count=("Demand", "count")
        )
        .reset_index()
    )

    print(promotion_analysis.round(2).to_string(index=False))

    print("\nDemand by discount range:")

    df["Discount_Group"] = pd.cut(
        df["Discount"],
        bins=[-1, 0, 5, 10, 15, 20, 100],
        labels=[
            "No Discount",
            "0-5%",
            "5-10%",
            "10-15%",
            "15-20%",
            "Above 20%"
        ]
    )

    discount_analysis = (
        df.groupby("Discount_Group", observed=True)
        .agg(
            Average_Demand=("Demand", "mean"),
            Average_Price=("Price", "mean"),
            Record_Count=("Demand", "count")
        )
        .reset_index()
    )

    print(discount_analysis.round(2).to_string(index=False))

    print("\nAnalysis completed.")


if __name__ == "__main__":
    analyze_discount_patterns()
