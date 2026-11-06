import joblib
import pandas as pd

from sklearn.metrics import mean_absolute_error

from utils.prepare_training import prepare_training_data


# Prepare test data
X_train, X_test, y_train, y_test = prepare_training_data()

# Load the better-performing model
model = joblib.load("models/lightgbm_model.pkl")

# Generate predictions
predictions = model.predict(X_test)

# Create analysis dataframe
results = pd.DataFrame({
    "Store ID": X_test["Store ID"].values,
    "Product ID": X_test["Product ID"].values,
    "Category": X_test["Category"].values,
    "Actual Demand": y_test.values,
    "Predicted Demand": predictions
})

results["Absolute Error"] = (
    results["Actual Demand"] - results["Predicted Demand"]
).abs()

# Error by category
print("\n========== ERROR BY CATEGORY ==========")

category_errors = (
    results.groupby("Category")["Absolute Error"]
    .agg(["mean", "median", "count"])
    .sort_values("mean", ascending=False)
)

print(category_errors.round(2).to_string())

# Error by store
print("\n========== ERROR BY STORE ==========")

store_errors = (
    results.groupby("Store ID")["Absolute Error"]
    .agg(["mean", "median", "count"])
    .sort_values("mean", ascending=False)
)

print(store_errors.round(2).to_string())

# Overall evaluation
print("\n========== OVERALL ERROR ==========")
print(
    "Overall MAE:",
    round(mean_absolute_error(y_test, predictions), 2)
)

print("\nError analysis completed!")