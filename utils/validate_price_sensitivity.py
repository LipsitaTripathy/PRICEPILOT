
import pandas as pd

from utils.pricing_optimizer import (
    load_pricing_model,
    get_product_history,
    create_candidate_features
)


def validate_price_sensitivity():

    model = load_pricing_model()

    store_id = "S001"
    forecast_date = "2024-01-31"

    df = pd.read_csv("data/retail_inventory.csv")

    product_ids = sorted(df["Product ID"].unique())

    results = []

    for product_id in product_ids:

        history = get_product_history(store_id, product_id)

        previous = history[
            history["Date"] < pd.Timestamp(forecast_date)
        ]

        current_price = float(previous.iloc[-1]["Price"])

        predictions = {}

        for label, factor in [
            ("Low Price", 0.90),
            ("Current Price", 1.00),
            ("High Price", 1.10)
        ]:

            candidate_price = round(current_price * factor, 2)

            features = create_candidate_features(
                history,
                candidate_price,
                forecast_date
            )

            predicted_demand = float(model.predict(features)[0])

            predictions[label] = predicted_demand

        results.append({
            "Product ID": product_id,
            "Current Price": current_price,
            "Demand at -10%": predictions["Low Price"],
            "Demand at Current": predictions["Current Price"],
            "Demand at +10%": predictions["High Price"],
            "Demand Change (+10%)": (
                predictions["High Price"]
                - predictions["Current Price"]
            )
        })

    results_df = pd.DataFrame(results)

    print("\n========== PRICE SENSITIVITY VALIDATION ==========")

    print(results_df.round(2).to_string(index=False))

    increasing = (
        results_df["Demand Change (+10%)"] > 0
    ).sum()

    decreasing = (
        results_df["Demand Change (+10%)"] < 0
    ).sum()

    unchanged = (
        results_df["Demand Change (+10%)"] == 0
    ).sum()

    print("\n========== SUMMARY ==========")

    print("Products tested:", len(results_df))
    print("Demand increases at higher price:", increasing)
    print("Demand decreases at higher price:", decreasing)
    print("Demand unchanged:", unchanged)

    results_df.to_csv(
        "models/price_sensitivity_validation.csv",
        index=False
    )

    print("\nSaved to models/price_sensitivity_validation.csv")


if __name__ == "__main__":
    validate_price_sensitivity()
