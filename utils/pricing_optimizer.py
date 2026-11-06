
import joblib
import math
import pandas as pd

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "pricing_demand_model.pkl"
DATA_PATH = BASE_DIR / "data" / "retail_inventory.csv"


def load_pricing_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Pricing model not found. Train it first."
        )

    return joblib.load(MODEL_PATH)


def get_product_history(store_id, product_id):

    if not DATA_PATH.exists():
        raise FileNotFoundError("Retail dataset not found.")

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    history = df[
        (df["Store ID"] == store_id)
        & (df["Product ID"] == product_id)
    ].sort_values("Date")

    if len(history) < 90:
        raise ValueError(
            "At least 90 historical records are required."
        )

    return history


def create_candidate_features(history, candidate_price, forecast_date):

    forecast_date = pd.Timestamp(forecast_date)

    previous = history[
        history["Date"] < forecast_date
    ].sort_values("Date")

    if len(previous) < 90:
        raise ValueError("Insufficient historical records.")

    latest_90_dates = previous["Date"].tail(90)

    if not latest_90_dates.diff().dropna().eq(
        pd.Timedelta(days=1)
    ).all():
        raise ValueError(
            "Latest 90 historical dates must be consecutive."
        )

    latest = previous.iloc[-1]
    demand_history = previous["Demand"]

    month = forecast_date.month
    weekday = forecast_date.day_of_week

    features = {
        "Store ID": latest["Store ID"],
        "Product ID": latest["Product ID"],
        "Category": latest["Category"],
        "Region": latest["Region"],
        "Year": forecast_date.year,
        "Month": month,
        "Day": forecast_date.day,
        "DayOfWeek": weekday,
        "IsWeekend": int(weekday >= 5),
        "Month_Sin": math.sin(2 * math.pi * month / 12),
        "Month_Cos": math.cos(2 * math.pi * month / 12),
        "Weekday_Sin": math.sin(2 * math.pi * weekday / 7),
        "Weekday_Cos": math.cos(2 * math.pi * weekday / 7),
        "Price": candidate_price,
        "Competitor Pricing": float(latest["Competitor Pricing"]),
        "Discount": float(latest["Discount"]),
        "Promotion": latest["Promotion"],
        "Seasonality": latest["Seasonality"],
        "Weather Condition": latest["Weather Condition"],
        "Inventory Level": float(latest["Inventory Level"]),
        "Demand_Lag_1": float(demand_history.iloc[-1]),
        "Demand_Lag_7": float(demand_history.iloc[-7]),
        "Demand_Rolling_7": float(demand_history.tail(7).mean()),
        "Demand_Rolling_30": float(demand_history.tail(30).mean()),
        "Demand_Rolling_90": float(demand_history.tail(90).mean())
    }

    return pd.DataFrame([features])


def optimize_price(
    store_id,
    product_id,
    forecast_date,
    cost_percentage=0.70,
    minimum_margin=0.10,
    max_price_change=0.10,
    price_elasticity=-1.0
):

    if not 0 < cost_percentage < 1:
        raise ValueError(
            "Cost percentage must be between 0 and 1."
        )

    if not 0 <= minimum_margin < 1:
        raise ValueError(
            "Minimum margin must be between 0 and 1."
        )

    if not 0 < max_price_change <= 0.50:
        raise ValueError(
            "Maximum price change must be above 0 and at most 50%."
        )

    if price_elasticity >= 0:
        raise ValueError(
            "Price elasticity must be negative."
        )

    forecast_date = pd.Timestamp(forecast_date)

    model = load_pricing_model()
    history = get_product_history(store_id, product_id)

    previous = history[
        history["Date"] < forecast_date
    ].sort_values("Date")

    if previous.empty:
        raise ValueError(
            "No historical data before forecast date."
        )

    current_price = float(previous.iloc[-1]["Price"])

    if current_price <= 0:
        raise ValueError("Current price must be greater than zero.")

    estimated_unit_cost = current_price * cost_percentage

    baseline_features = create_candidate_features(
        history,
        current_price,
        forecast_date
    )

    baseline_demand = max(
        0.0,
        float(model.predict(baseline_features)[0])
    )

    factors = [
        1 - max_price_change,
        1 - max_price_change * 0.75,
        1 - max_price_change * 0.50,
        1 - max_price_change * 0.25,
        1.0,
        1 + max_price_change * 0.25,
        1 + max_price_change * 0.50,
        1 + max_price_change * 0.75,
        1 + max_price_change
    ]

    candidate_prices = sorted({
        round(current_price * factor, 2)
        for factor in factors
    })

    minimum_price = (
        estimated_unit_cost / (1 - minimum_margin)
    )

    results = []

    for price in candidate_prices:

        if price < minimum_price:
            continue

        demand_multiplier = (
            price / current_price
        ) ** price_elasticity

        predicted_demand = (
            baseline_demand * demand_multiplier
        )

        revenue = price * predicted_demand

        profit = (
            price - estimated_unit_cost
        ) * predicted_demand

        margin = (
            (price - estimated_unit_cost) / price
        ) * 100

        results.append({
            "Candidate Price": float(round(price, 2)),
            "Demand Change (%)": float(round(
                (demand_multiplier - 1) * 100, 2
            )),
            "Predicted Demand": float(round(predicted_demand, 2)),
            "Estimated Revenue": float(round(revenue, 2)),
            "Estimated Profit": float(round(profit, 2)),
            "Estimated Margin": float(round(margin, 2))
        })

    if not results:
        raise ValueError(
            "No candidate price satisfies the margin constraint."
        )

    results_df = pd.DataFrame(results)

    best = results_df.loc[
        results_df["Estimated Profit"].idxmax()
    ]

    recommended_price = float(best["Candidate Price"])

    boundary_selected = bool(
        recommended_price == results_df["Candidate Price"].min()
        or recommended_price == results_df["Candidate Price"].max()
    )

    return {
        "store_id": str(store_id),
        "product_id": str(product_id),
        "forecast_date": str(forecast_date.date()),
        "current_price": float(round(current_price, 2)),
        "baseline_demand": float(round(baseline_demand, 2)),
        "recommended_price": recommended_price,
        "predicted_demand": float(best["Predicted Demand"]),
        "estimated_unit_cost": float(round(estimated_unit_cost, 2)),
        "estimated_revenue": float(best["Estimated Revenue"]),
        "estimated_profit": float(best["Estimated Profit"]),
        "estimated_margin": float(best["Estimated Margin"]),
        "cost_assumption": (
            f"{cost_percentage * 100:.0f}% of current price"
        ),
        "minimum_margin": float(minimum_margin * 100),
        "maximum_price_change": float(max_price_change * 100),
        "price_elasticity_assumption": float(price_elasticity),
        "boundary_selected": boundary_selected,
        "recommendation_status": (
            "BOUNDARY RESULT - review the permitted price range"
            if boundary_selected
            else "Scenario recommendation - validate before use"
        ),
        "model_note": (
            "Baseline demand is model-predicted. "
            "Price response is simulated using an assumed elasticity."
        ),
        "candidate_results": results_df.to_dict(orient="records")
    }


if __name__ == "__main__":

    result = optimize_price(
        store_id="S001",
        product_id="P0001",
        forecast_date="2024-01-31"
    )

    print("\n========== PRICEPILOT RECOMMENDATION ==========")

    for key, value in result.items():

        if key != "candidate_results":
            print(f"{key}: {value}")

    print("\nCandidate price comparison:")

    print(
        pd.DataFrame(result["candidate_results"])
        .to_string(index=False)
    )
