
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

from utils.prepare_training import prepare_training_data


# --------------------------------------------------
# 1. PREPARE DATA
# --------------------------------------------------

X_train, X_test, y_train, y_test = prepare_training_data()


# --------------------------------------------------
# 2. CHRONOLOGICAL VALIDATION SPLIT
# --------------------------------------------------

# Split each store-product series separately.
# The final 15% of each series becomes validation data.

group_positions = (
    X_train.groupby(
        ["Store ID", "Product ID"],
        sort=False
    )
    .cumcount()
)

group_sizes = (
    X_train.groupby(
        ["Store ID", "Product ID"],
        sort=False
    )["Product ID"]
    .transform("size")
)

validation_mask = (
    group_positions >= (group_sizes * 0.85)
)

X_fit = X_train.loc[~validation_mask]
y_fit = y_train.loc[~validation_mask]

X_validation = X_train.loc[validation_mask]
y_validation = y_train.loc[validation_mask]

print("\n========== VALIDATION SPLIT ==========")
print("Model fitting rows:", len(X_fit))
print("Validation rows:", len(X_validation))


# --------------------------------------------------
# 3. PREPROCESSING
# --------------------------------------------------

categorical_features = [
    "Store ID",
    "Product ID",
    "Category",
    "Region"
]

numerical_features = [
    col for col in X_train.columns
    if col not in categorical_features
]


def create_pipeline(model):

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )


# --------------------------------------------------
# 4. HYPERPARAMETER CONFIGURATIONS
# --------------------------------------------------

model_configs = {

    "XGBoost": [
        {
            "n_estimators": 400,
            "max_depth": 4,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8
        },
        {
            "n_estimators": 600,
            "max_depth": 5,
            "learning_rate": 0.03,
            "subsample": 0.8,
            "colsample_bytree": 0.8
        },
        {
            "n_estimators": 500,
            "max_depth": 6,
            "learning_rate": 0.04,
            "subsample": 0.9,
            "colsample_bytree": 0.9
        }
    ],

    "LightGBM": [
        {
            "n_estimators": 400,
            "max_depth": 6,
            "learning_rate": 0.05,
            "num_leaves": 20,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "subsample_freq": 1
        },
        {
            "n_estimators": 600,
            "max_depth": 7,
            "learning_rate": 0.03,
            "num_leaves": 31,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "subsample_freq": 1
        },
        {
            "n_estimators": 500,
            "max_depth": 8,
            "learning_rate": 0.04,
            "num_leaves": 40,
            "subsample": 0.9,
            "colsample_bytree": 0.9,
            "subsample_freq": 1
        }
    ]
}


# --------------------------------------------------
# 5. HYPERPARAMETER TUNING
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

best_models = {}
tuning_results = []

for model_name, configurations in model_configs.items():

    print(f"\n========== TUNING {model_name} ==========")

    best_mae = float("inf")
    best_pipeline = None
    best_config = None

    for index, config in enumerate(configurations, start=1):

        print(f"\nTesting configuration {index}/3")

        if model_name == "XGBoost":

            model = XGBRegressor(
                **config,
                objective="reg:squarederror",
                random_state=42,
                n_jobs=-1,
                verbosity=0
            )

        else:

            model = LGBMRegressor(
                **config,
                random_state=42,
                verbosity=-1,
                n_jobs=-1
            )

        pipeline = create_pipeline(model)

        pipeline.fit(X_fit, y_fit)

        validation_predictions = pipeline.predict(
            X_validation
        )

        validation_mae = mean_absolute_error(
            y_validation,
            validation_predictions
        )

        validation_rmse = np.sqrt(
            mean_squared_error(
                y_validation,
                validation_predictions
            )
        )

        validation_r2 = r2_score(
            y_validation,
            validation_predictions
        )

        print("Validation MAE:", round(validation_mae, 3))
        print("Validation RMSE:", round(validation_rmse, 3))
        print("Validation R2:", round(validation_r2, 4))

        tuning_results.append({
            "Model": model_name,
            "Configuration": index,
            "MAE": round(validation_mae, 3),
            "RMSE": round(validation_rmse, 3),
            "R2 Score": round(validation_r2, 4)
        })

        if validation_mae < best_mae:

            best_mae = validation_mae
            best_pipeline = pipeline
            best_config = config

    best_models[model_name] = {
        "config": best_config,
        "validation_mae": best_mae
    }

    print(f"\nBest {model_name} validation MAE:", round(best_mae, 3))
    print("Best configuration:", best_config)


# --------------------------------------------------
# 6. DISPLAY VALIDATION RESULTS
# --------------------------------------------------

print("\n========== ALL CONFIGURATION RESULTS ==========")

results_df = pd.DataFrame(tuning_results)

print(
    results_df.sort_values("MAE").to_string(index=False)
)


# --------------------------------------------------
# 7. RETRAIN BEST CONFIGURATIONS ON FULL TRAINING DATA
# --------------------------------------------------

print("\n========== FINAL MODEL TRAINING ==========")

final_results = []

for model_name, selected in best_models.items():

    config = selected["config"]

    if model_name == "XGBoost":

        final_model = XGBRegressor(
            **config,
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1,
            verbosity=0
        )

    else:

        final_model = LGBMRegressor(
            **config,
            random_state=42,
            verbosity=-1,
            n_jobs=-1
        )

    final_pipeline = create_pipeline(final_model)

    print(f"\nTraining final {model_name} model...")

    final_pipeline.fit(X_train, y_train)

    # Evaluate on untouched test data
    test_predictions = final_pipeline.predict(X_test)

    test_mae = mean_absolute_error(
        y_test,
        test_predictions
    )

    test_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            test_predictions
        )
    )

    test_r2 = r2_score(
        y_test,
        test_predictions
    )

    final_results.append({
        "Model": model_name,
        "MAE": round(test_mae, 3),
        "RMSE": round(test_rmse, 3),
        "R2 Score": round(test_r2, 4)
    })

    model_path = (
        f"models/{model_name.lower()}_model.pkl"
    )

    joblib.dump(final_pipeline, model_path)

    print(f"{model_name} saved successfully.")
    print("Test MAE:", round(test_mae, 3))


# --------------------------------------------------
# 8. BASELINE COMPARISON
# --------------------------------------------------

baseline_predictions = X_test["Demand_Lag_1"]

baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

print("\n========== BASELINE ==========")
print("Previous-day MAE:", round(baseline_mae, 3))


# --------------------------------------------------
# 9. FINAL MODEL COMPARISON
# --------------------------------------------------

print("\n========== FINAL TEST PERFORMANCE ==========")

final_results_df = pd.DataFrame(final_results)

print(final_results_df.to_string(index=False))

print("\nHyperparameter tuning and training completed!")
