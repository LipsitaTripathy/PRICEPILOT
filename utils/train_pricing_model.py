
import joblib
import pandas as pd

from pathlib import Path
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from utils.prepare_pricing_data import prepare_pricing_data


def train_pricing_models():

    X_train, X_test, y_train, y_test = prepare_pricing_data()

    categorical_features = [
        "Store ID",
        "Product ID",
        "Category",
        "Region",
        "Seasonality",
        "Weather Condition"
    ]

    numeric_features = [
        column for column in X_train.columns
        if column not in categorical_features
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    models = {
        "XGBoost": XGBRegressor(
            n_estimators=400,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1
        ),

        "LightGBM": LGBMRegressor(
            n_estimators=400,
            max_depth=7,
            learning_rate=0.05,
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            verbosity=-1,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []
    trained_models = {}

    for name, model in models.items():

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

        print(f"\nTraining {name} pricing demand model...")

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(
            y_test,
            predictions
        ) ** 0.5
        r2 = r2_score(y_test, predictions)

        results.append({
            "Model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })

        trained_models[name] = pipeline

        print(f"\n{name} Results:")
        print(f"MAE: {mae:.3f}")
        print(f"RMSE: {rmse:.3f}")
        print(f"R2 Score: {r2:.4f}")

    results_df = pd.DataFrame(results).sort_values("MAE")

    best_model_name = results_df.iloc[0]["Model"]
    best_model = trained_models[best_model_name]

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    joblib.dump(
        best_model,
        models_dir / "pricing_demand_model.pkl"
    )

    results_df.to_csv(
        models_dir / "pricing_model_performance.csv",
        index=False
    )

    print("\n========== PRICING MODEL COMPARISON ==========")
    print(results_df.to_string(index=False))

    print("\nBest model:", best_model_name)
    print("Saved: models/pricing_demand_model.pkl")
    print("Saved: models/pricing_model_performance.csv")


if __name__ == "__main__":
    train_pricing_models()
