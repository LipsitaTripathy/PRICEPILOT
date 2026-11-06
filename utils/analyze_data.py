import pandas as pd

# Load dataset
df = pd.read_csv("data/retail_inventory.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("\n========== DATASET STRUCTURE ==========")

print("Total records:", len(df))
print("Unique dates:", df["Date"].nunique())
print("Unique store-product combinations:",
      df.groupby(["Store ID", "Product ID"]).ngroups)

print("\n========== DEMAND VS SALES ==========")

print("Demand greater than Units Sold:",
      (df["Demand"] > df["Units Sold"]).sum())

print("Demand equal to Units Sold:",
      (df["Demand"] == df["Units Sold"]).sum())

print("Demand lower than Units Sold:",
      (df["Demand"] < df["Units Sold"]).sum())

print("\n========== CORRELATION WITH DEMAND ==========")

numeric_columns = [
    "Units Sold",
    "Units Ordered",
    "Inventory Level",
    "Price",
    "Discount",
    "Promotion",
    "Competitor Pricing",
    "Epidemic",
    "Demand"
]

print(
    df[numeric_columns]
    .corr()["Demand"]
    .sort_values(ascending=False)
    .round(3)
)

print("\n========== DAILY DEMAND TREND ==========")

daily_demand = df.groupby("Date")["Demand"].sum()

print("Average daily demand:", round(daily_demand.mean(), 2))
print("Minimum daily demand:", daily_demand.min())
print("Maximum daily demand:", daily_demand.max())

print("\n========== SAMPLE PRODUCT HISTORY ==========")

sample = df[
    (df["Store ID"] == "S001") &
    (df["Product ID"] == "P0001")
].sort_values("Date")

print(
    sample[[
        "Date",
        "Inventory Level",
        "Units Sold",
        "Units Ordered",
        "Price",
        "Discount",
        "Demand"
    ]].head(10).to_string(index=False)
)