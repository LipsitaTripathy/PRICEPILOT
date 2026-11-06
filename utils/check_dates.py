import pandas as pd

df = pd.read_csv("data/retail_inventory.csv")

df["Date"] = pd.to_datetime(df["Date"])

print("\n========== DATE DISTRIBUTION ==========")

print("First date:", df["Date"].min())
print("Last date:", df["Date"].max())

print("\nRows per date:")
print(df.groupby("Date").size().describe())

print("\n========== STORE-PRODUCT DATE CHECK ==========")

date_counts = (
    df.groupby(["Store ID", "Product ID"])["Date"]
    .agg(["count", "min", "max"])
)

print(date_counts.describe())

print("\n========== DATE CONTINUITY ==========")

expected_days = (
    df["Date"].nunique()
)

date_counts["Expected Days"] = expected_days

date_counts["Complete"] = (
    date_counts["count"] == expected_days
)

print("Complete combinations:", date_counts["Complete"].sum())
print("Incomplete combinations:", (~date_counts["Complete"]).sum())

print("\nSample combinations:")
print(date_counts.head(10))