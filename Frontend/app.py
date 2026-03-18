import streamlit as st
import requests

st.title("🚗 Car Price Predictor")
st.write("Fill in the car details below to get a predicted price.")

# Input fields
vehicle_age       = st.number_input("Vehicle Age (years)", min_value=0, max_value=30, value=5)
km_driven         = st.number_input("KM Driven", min_value=0, max_value=1000000, value=45000)
mileage           = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=21.0)
engine            = st.number_input("Engine Size (cc)", min_value=500, max_value=7000, value=1197)
max_power         = st.number_input("Max Power (bhp)", min_value=0.0, max_value=700.0, value=82.0)
seats             = st.number_input("Seats", min_value=2, max_value=9, value=5)

brand             = st.selectbox("Brand", ["Maruti", "Hyundai", "Ford", "Honda", "Toyota", "BMW", 
                                           "Audi", "Mercedes-Benz", "Volkswagen", "Tata", "Mahindra",
                                           "Renault", "Kia", "Skoda", "Nissan", "Datsun", "MG",
                                           "Jeep", "Volvo", "Land Rover", "Jaguar", "Porsche",
                                           "Mini", "Lexus", "Maserati", "Bentley", "Rolls-Royce",
                                           "Ferrari", "Mercedes-AMG", "Isuzu", "ISUZU", "Force"])

fuel_type         = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission_type = st.selectbox("Transmission", ["Manual", "Automatic"])
seller_type       = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])

# Predict button
if st.button("Predict Price"):
    payload = {
        "vehicle_age":       vehicle_age,
        "km_driven":         km_driven,
        "mileage":           mileage,
        "engine":            engine,
        "max_power":         max_power,
        "seats":             seats,
        "brand":             brand,
        "fuel_type":         fuel_type,
        "transmission_type": transmission_type,
        "seller_type":       seller_type
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=payload)

    if response.status_code == 200:
        price = response.json()["predicted_price"]
        st.success(f"Predicted Price: ₹{price:,.0f}")
    else:
        st.error("Something went wrong. Make sure the API is running!")