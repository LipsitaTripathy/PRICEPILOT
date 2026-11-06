import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from utils.prepare_training import prepare_training_data


# Load test dataset
X_train, X_test, y_train, y_test = prepare_training_data()

# Load trained models
models = {
    "XGBoost": joblib.load("models/xgboost_model.pkl"),
    "LightGBM": joblib.load("models/lightgbm_model.pkl")
}

print("\n========== DETAILED MODEL EVALUATION ==========")

for name, model in models.items():

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"\n{name}")
    print("MAE:", round(mae, 3))
    print("RMSE:", round(rmse, 3))
    print("R2 Score:", round(r2, 4))


# Examine LightGBM predictions
model = models["LightGBM"]
predictions = model.predict(X_test)

comparison = pd.DataFrame({
    "Actual Demand": y_test.values,
    "Predicted Demand": predictions
})

comparison["Absolute Error"] = abs(
    comparison["Actual Demand"] -
    comparison["Predicted Demand"]
)

comparison["Predicted Demand"] = (
    comparison["Predicted Demand"].round(2)
)

print("\n========== SAMPLE PREDICTIONS ==========")
print(comparison.head(15).to_string(index=False))

print("\n========== ERROR DISTRIBUTION ==========")
print(comparison["Absolute Error"].describe().round(2))

print("\nEvaluation completed!")