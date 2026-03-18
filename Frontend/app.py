import streamlit as st
import joblib
import json
import numpy as np
import pandas as pd
import os

# ─── Load Model ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../Model")

model = joblib.load(os.path.join(MODEL_DIR, "car_price_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

with open(os.path.join(MODEL_DIR, "model_columns.json"), "r") as f:
    model_columns = json.load(f)


st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #FDFDFD;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

.block-container {
    padding-top: 2rem;
}

label[data-testid="stWidgetLabel"] p {
    color: #1A1A1A !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

[data-testid="stSelectbox"] * {
    cursor: pointer !important;
}

div.stButton > button {
    background-color: #1A1A1A;
    color: #FDFDFD;
    border: none;
    border-radius: 2px;
    padding: 0.65rem 2rem;
    font-size: 0.9rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    width: 100%;
    transition: transform 0.15s ease, background-color 0.15s ease;
}

div.stButton > button:hover {
    background-color: #2D2D2D;
    transform: translateY(-1px);
}

.custom-divider {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 0.5rem 0 1.5rem 0;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #1A1A1A !important;
    margin-bottom: 0;
}

.main-subtitle {
    font-size: 1rem;
    color: #4A5568 !important;
    margin-top: 0.2rem;
}

.result-card {
    border: 1px solid #1A1A1A;
    border-radius: 2px;
    padding: 2rem 2.5rem;
    background-color: #1A1A1A;
    height: 100%;
}

.result-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #A0AEC0;
    margin-bottom: 0.5rem;
}

.result-price {
    font-size: 2.8rem;
    font-weight: 700;
    color: #FDFDFD;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.result-note {
    font-size: 0.8rem;
    color: #A0AEC0;
    margin-top: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────
st.markdown('<p class="main-title">🚗 Car Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Estimate the resale value of a used car using machine learning.</p>', unsafe_allow_html=True)
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ─── Layout ────────────────────────────────────────────────────
left, right = st.columns([1.2, 1])

with left:
    col1, col2 = st.columns(2)

    with col1:
        vehicle_age = st.number_input("Vehicle Age (years)", min_value=0, max_value=30, value=5)
        km_driven   = st.number_input("KM Driven", min_value=0, max_value=1000000, value=45000, step=1000)
        mileage     = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=21.0, step=0.1)
        engine      = st.number_input("Engine Size (cc)", min_value=500, max_value=7000, value=1197, step=100)
        max_power   = st.number_input("Max Power (bhp)", min_value=0.0, max_value=700.0, value=82.0, step=1.0)

    with col2:
        seats             = st.number_input("Seats", min_value=2, max_value=9, value=5)
        brand             = st.selectbox("Brand", [
            "Maruti", "Hyundai", "Ford", "Honda", "Toyota", "BMW",
            "Audi", "Mercedes-Benz", "Volkswagen", "Tata", "Mahindra",
            "Renault", "Kia", "Skoda", "Nissan", "Datsun", "MG",
            "Jeep", "Volvo", "Land Rover", "Jaguar", "Porsche",
            "Mini", "Lexus", "Maserati", "Bentley", "Rolls-Royce",
            "Ferrari", "Mercedes-AMG", "Isuzu", "ISUZU", "Force"
        ])
        fuel_type         = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        transmission_type = st.selectbox("Transmission", ["Manual", "Automatic"])
        seller_type       = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("Predict Price")

# ─── Result ────────────────────────────────────────────────────
with right:
    if predict_btn:
        try:
            # Build input dataframe
            input_df = pd.DataFrame(columns=model_columns)
            input_df.loc[0] = 0

            # Fill numeric values
            input_df["vehicle_age"] = vehicle_age
            input_df["km_driven"]   = km_driven
            input_df["mileage"]     = mileage
            input_df["engine"]      = engine
            input_df["max_power"]   = max_power
            input_df["seats"]       = seats

            # Fill OHE columns
            for col in [
                f"brand_{brand}",
                f"fuel_type_{fuel_type}",
                f"transmission_type_{transmission_type}",
                f"seller_type_{seller_type}"
            ]:
                if col in model_columns:
                    input_df[col] = 1

            # Scale and predict
            input_scaled = scaler.transform(input_df)
            log_price    = model.predict(input_scaled)
            price        = round(float(np.exp(log_price[0])), 2)

            st.markdown(f"""
            <div class="result-card">
                <p class="result-label">Estimated Resale Value</p>
                <p class="result-price">₹{price:,.0f}</p>
                <p class="result-note">{vehicle_age} yr old {brand} · {km_driven:,} km · {fuel_type} · {transmission_type}</p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction failed: {e}")

    else:
        st.markdown("""
        <div class="result-card">
            <p class="result-label">Estimated Resale Value</p>
            <p class="result-price" style="color: #333333;">——</p>
            <p class="result-note">Fill in the details and click Predict Price.</p>
        </div>
        """, unsafe_allow_html=True)