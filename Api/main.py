from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import numpy as np
import pandas as pd

# Load model, scaler, and columns
model   = joblib.load("../model/car_price_model.pkl")
scaler  = joblib.load("../model/scaler.pkl")

with open("../model/model_columns.json", "r") as f:
    model_columns = json.load(f)

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class CarFeatures(BaseModel):
    vehicle_age: int
    km_driven: int
    mileage: float
    engine: int
    max_power: float
    seats: int
    brand: str
    fuel_type: str
    transmission_type: str
    seller_type: str

@app.get("/")
def home():
    return {"message": "Car Price Prediction API is running!"}

@app.post("/predict")
def predict(car: CarFeatures):

    # Create empty dataframe with all model columns
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0

    # Fill numeric values
    input_df["vehicle_age"] = car.vehicle_age
    input_df["km_driven"]   = car.km_driven
    input_df["mileage"]     = car.mileage
    input_df["engine"]      = car.engine
    input_df["max_power"]   = car.max_power
    input_df["seats"]       = car.seats

    # Fill categorical columns (OHE)
    brand_col        = f"brand_{car.brand}"
    fuel_col         = f"fuel_type_{car.fuel_type}"
    transmission_col = f"transmission_type_{car.transmission_type}"
    seller_col       = f"seller_type_{car.seller_type}"

    if brand_col in model_columns:
        input_df[brand_col] = 1

    if fuel_col in model_columns:
        input_df[fuel_col] = 1

    if transmission_col in model_columns:
        input_df[transmission_col] = 1

    if seller_col in model_columns:
        input_df[seller_col] = 1

    # Scale and predict
    input_scaled = scaler.transform(input_df)
    log_price    = model.predict(input_scaled)
    actual_price = np.exp(log_price[0])

    return {"predicted_price": round(actual_price, 2)}