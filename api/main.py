
from datetime import date
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from utils.pricing_optimizer import optimize_price


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "xgboost_model.pkl"
PRICING_MODEL_PATH = BASE_DIR / "models" / "pricing_demand_model.pkl"
DATA_PATH = BASE_DIR / "data" / "retail_inventory.csv"


# --------------------------------------------------
# INITIALIZE API
# --------------------------------------------------

app = FastAPI(
    title="PRICEPILOT API",
    description=(
        "Retail demand forecasting and scenario-based "
        "dynamic pricing API."
    ),
    version="1.4.0"
)


# --------------------------------------------------
# LOAD DEMAND MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Demand model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# LOAD HISTORICAL DATA
# --------------------------------------------------

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

reference_data = pd.read_csv(DATA_PATH)

reference_data["Date"] = pd.to_datetime(
    reference_data["Date"],
    errors="coerce"
)

if reference_data["Date"].isna().any():
    raise ValueError(
        "Invalid dates found in historical dataset."
    )

if reference_data.duplicated(
    subset=["Store ID", "Product ID", "Date"]
).any():
    raise ValueError(
        "Duplicate store-product-date records found."
    )

reference_data = reference_data.sort_values(
    ["Store ID", "Product ID", "Date"]
).reset_index(drop=True)

VALID_STORES = set(
    reference_data["Store ID"].astype(str).unique()
)

VALID_PRODUCTS = set(
    reference_data["Product ID"].astype(str).unique()
)


# --------------------------------------------------
# REQUEST SCHEMAS
# --------------------------------------------------

class DemandInput(BaseModel):

    store_id: str
    product_id: str
    forecast_date: date

    @field_validator("store_id")
    @classmethod
    def validate_store(cls, value):

        if value not in VALID_STORES:
            raise ValueError("Unknown store ID")

        return value

    @field_validator("product_id")
    @classmethod
    def validate_product(cls, value):

        if value not in VALID_PRODUCTS:
            raise ValueError("Unknown product ID")

        return value


class PricingInput(DemandInput):

    cost_percentage: float = Field(
        default=0.70,
        gt=0,
        lt=1
    )

    minimum_margin: float = Field(
        default=0.10,
        ge=0,
        lt=1
    )

    max_price_change: float = Field(
        default=0.10,
        gt=0,
        le=0.50
    )

    price_elasticity: float = Field(
        default=-1.0,
        lt=0
    )


# --------------------------------------------------
# AUTOMATIC HISTORICAL FEATURE CALCULATION
# --------------------------------------------------

def get_historical_features(
    store_id,
    product_id,
    forecast_date
):

    forecast_timestamp = pd.Timestamp(forecast_date)

    history = reference_data[
        (reference_data["Store ID"].astype(str) == store_id)
        & (reference_data["Product ID"].astype(str) == product_id)
        & (reference_data["Date"] < forecast_timestamp)
    ].copy()

    history = history.sort_values(
        "Date"
    ).reset_index(drop=True)

    if history.empty:
        raise HTTPException(
            status_code=422,
            detail=(
                "No historical records found "
                "for this store and product."
            )
        )

    recent_history = history.tail(90).copy()

    if len(recent_history) < 90:
        raise HTTPException(
            status_code=422,
            detail=(
                "At least 90 days of historical "
                "demand are required."
            )
        )

    expected_dates = pd.date_range(
        end=forecast_timestamp - pd.Timedelta(days=1),
        periods=90,
        freq="D"
    )

    actual_dates = pd.DatetimeIndex(
        recent_history["Date"]
    )

    if not actual_dates.equals(expected_dates):
        raise HTTPException(
            status_code=422,
            detail=(
                "Historical data must contain "
                "90 consecutive days before the forecast date."
            )
        )

    demand_values = recent_history["Demand"].astype(float)

    latest_record = recent_history.iloc[-1]

    return {
        "category": latest_record["Category"],
        "region": latest_record["Region"],
        "demand_lag_1": float(demand_values.iloc[-1]),
        "demand_lag_7": float(demand_values.iloc[-7]),
        "demand_rolling_7": float(
            demand_values.tail(7).mean()
        ),
        "demand_rolling_30": float(
            demand_values.tail(30).mean()
        ),
        "demand_rolling_90": float(
            demand_values.tail(90).mean()
        )
    }


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to PRICEPILOT API",
        "status": "Running",
        "version": "1.4.0",
        "services": [
            "Demand Forecasting",
            "Scenario-Based Dynamic Pricing"
        ]
    }


# --------------------------------------------------
# HEALTH ENDPOINT
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "demand_model_loaded": model is not None,
        "pricing_model_available": PRICING_MODEL_PATH.exists(),
        "dataset_loaded": not reference_data.empty,
        "total_records": len(reference_data)
    }


# --------------------------------------------------
# DEMAND PREDICTION ENDPOINT
# --------------------------------------------------

@app.post("/predict")
def predict_demand(data: DemandInput):

    forecast_timestamp = pd.Timestamp(
        data.forecast_date
    )

    matching_pair = reference_data[
        (reference_data["Store ID"].astype(str) == data.store_id)
        & (reference_data["Product ID"].astype(str) == data.product_id)
    ]

    if matching_pair.empty:
        raise HTTPException(
            status_code=422,
            detail=(
                "This store and product combination "
                "does not exist."
            )
        )

    historical = get_historical_features(
        data.store_id,
        data.product_id,
        data.forecast_date
    )

    year = forecast_timestamp.year
    month = forecast_timestamp.month
    day = forecast_timestamp.day

    day_of_week = forecast_timestamp.dayofweek
    is_weekend = int(day_of_week >= 5)

    month_sin = np.sin(
        2 * np.pi * month / 12
    )

    month_cos = np.cos(
        2 * np.pi * month / 12
    )

    weekday_sin = np.sin(
        2 * np.pi * day_of_week / 7
    )

    weekday_cos = np.cos(
        2 * np.pi * day_of_week / 7
    )

    input_data = pd.DataFrame([{

        "Store ID": data.store_id,
        "Product ID": data.product_id,
        "Category": historical["category"],
        "Region": historical["region"],

        "Year": year,
        "Month": month,
        "Day": day,
        "DayOfWeek": day_of_week,
        "IsWeekend": is_weekend,

        "Month_Sin": month_sin,
        "Month_Cos": month_cos,
        "Weekday_Sin": weekday_sin,
        "Weekday_Cos": weekday_cos,

        "Demand_Lag_1": historical["demand_lag_1"],
        "Demand_Lag_7": historical["demand_lag_7"],
        "Demand_Rolling_7": historical["demand_rolling_7"],
        "Demand_Rolling_30": historical["demand_rolling_30"],
        "Demand_Rolling_90": historical["demand_rolling_90"]

    }])

    try:

        prediction = model.predict(input_data)[0]

        return {
            "product_id": data.product_id,
            "store_id": data.store_id,
            "forecast_date": data.forecast_date.isoformat(),
            "predicted_demand": round(
                max(0, float(prediction)), 2
            ),
            "unit": "units",
            "model": "XGBoost",
            "historical_features": "Automatically calculated"
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail="Demand prediction failed. Check server logs."
        ) from error


# --------------------------------------------------
# DYNAMIC PRICING RECOMMENDATION ENDPOINT
# --------------------------------------------------

@app.post("/pricing/recommend")
def recommend_price(data: PricingInput):

    matching_pair = reference_data[
        (reference_data["Store ID"].astype(str) == data.store_id)
        & (reference_data["Product ID"].astype(str) == data.product_id)
    ]

    if matching_pair.empty:
        raise HTTPException(
            status_code=422,
            detail=(
                "This store and product combination "
                "does not exist."
            )
        )

    try:

        result = optimize_price(
            store_id=data.store_id,
            product_id=data.product_id,
            forecast_date=data.forecast_date,
            cost_percentage=data.cost_percentage,
            minimum_margin=data.minimum_margin,
            max_price_change=data.max_price_change,
            price_elasticity=data.price_elasticity
        )

        return {
            "status": "success",
            "service": "PRICEPILOT Scenario-Based Pricing",
            "recommendation": result
        }

    except (ValueError, FileNotFoundError) as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Pricing recommendation failed. "
                "Check server logs."
            )
        ) from error
