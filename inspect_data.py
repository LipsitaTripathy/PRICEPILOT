import pandas as pd

# Load the dataset
file_path = "data/retail_inventory.csv"
df = pd.read_csv(file_path)

print("\n========== DATASET OVERVIEW ==========")

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nFirst 5 rows:")
print(df.head().to_string())