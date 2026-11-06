
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

from utils.preprocessing import load_data


def analyze_adjusted_price_effect():

    df = load_data()

    df["Date"] = pd.to_datetime(df["Date"])

    df["Time_Index"] = (
        df["Date"] - df["Date"].min()
    ).dt.days

    print("\n========== ADJUSTED PRICE EFFECT ANALYSIS ==========")

    categorical_features = [
        "Store ID",
        "Product ID",
        "Seasonality",
        "Weather Condition"
    ]

    numerical_features = [
        "Competitor Pricing",
        "Discount",
        "Promotion",
        "Inventory Level",
        "Time_Index"
    ]

    features_without_price = (
        categorical_features + numerical_features
    )

    features_with_price = (
        features_without_price + ["Price"]
    )

    def create_model(numerical_columns):

        preprocessor = ColumnTransformer([
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_columns
            )
        ])

        return Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression())
        ])

    # Model A: Without price
    model_without_price = create_model(
        numerical_features
    )

    model_without_price.fit(
        df[features_without_price],
        df["Demand"]
    )

    predictions_without_price = model_without_price.predict(
        df[features_without_price]
    )

    # Model B: With price
    model_with_price = create_model(
        numerical_features + ["Price"]
    )

    model_with_price.fit(
        df[features_with_price],
        df["Demand"]
    )

    predictions_with_price = model_with_price.predict(
        df[features_with_price]
    )

    print("\nModel comparison:")

    print(
        "Without Price MAE:",
        round(mean_absolute_error(
            df["Demand"],
            predictions_without_price
        ), 3)
    )

    print(
        "With Price MAE:",
        round(mean_absolute_error(
            df["Demand"],
            predictions_with_price
        ), 3)
    )

    print(
        "Without Price R2:",
        round(r2_score(
            df["Demand"],
            predictions_without_price
        ), 4)
    )

    print(
        "With Price R2:",
        round(r2_score(
            df["Demand"],
            predictions_with_price
        ), 4)
    )

    # Extract price coefficient
    regressor = model_with_price.named_steps["regressor"]

    feature_names = (
        model_with_price
        .named_steps["preprocessor"]
        .get_feature_names_out()
    )

    coefficient_table = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": regressor.coef_
    })

    print("\nPrice coefficient:")

    price_coefficients = coefficient_table[
        coefficient_table["Feature"].str.endswith("Price")
    ]

    print(price_coefficients.round(4).to_string(index=False))

    coefficient_table.to_csv(
        "models/adjusted_price_coefficients.csv",
        index=False
    )

    print("\nAnalysis saved successfully.")


if __name__ == "__main__":
    analyze_adjusted_price_effect()
