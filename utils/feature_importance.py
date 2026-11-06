
import joblib
import pandas as pd

from utils.prepare_training import prepare_training_data


# Prepare data
X_train, X_test, y_train, y_test = prepare_training_data()

# Load tuned XGBoost model
model = joblib.load("models/xgboost_model.pkl")

# Access trained model and preprocessing
preprocessor = model.named_steps["preprocessor"]
xgb_model = model.named_steps["model"]

# Get transformed feature names
feature_names = preprocessor.get_feature_names_out()

# Extract feature importance
importance = xgb_model.feature_importances_

# Create importance dataframe
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

# Sort by importance
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

# Display top 20 features
print("\n========== TOP 20 FEATURE IMPORTANCE ==========")

print(
    importance_df.head(20).to_string(index=False)
)

# Save complete results
importance_df.to_csv(
    "models/feature_importance.csv",
    index=False
)

print("\nFeature importance saved to models/feature_importance.csv")
