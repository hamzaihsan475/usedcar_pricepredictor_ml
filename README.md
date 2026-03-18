# 🚗 Used Car Price Predictor

A machine learning web app that predicts the resale value of used cars using Linear Regression, built with Streamlit.
# 🚗 Used Car Price Predictor

🌐 **Live Demo:** [https://usedcarpricepredictorr.streamlit.app/](https://usedcarpricepredictorr.streamlit.app/)
---

## 📁 Project Structure
```
usedcar_pricepredictor_ml/
├── Data/
│   └── cardekho_dataset.csv
├── Model/
│   ├── Train_model.ipynb
│   ├── car_price_model.pkl
│   ├── scaler.pkl
│   └── model_columns.json
├── Frontend/
│   └── app.py
├── requirements.txt
└── README.md
```

---

## 🤖 Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Linear Regression |
| R² Score | 0.89 |
| MAE | ₹1,36,469 |
| Overfitting | None |

---

## 🛠️ Tech Stack

- **Language:** Python
- **ML:** Scikit-learn, Pandas, NumPy
- **Frontend:** Streamlit
- **Dataset:** Cardekho Used Cars Dataset

---

## 🚀 How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/hamzaihsan475/usedcar_pricepredictor_ml.git
cd usedcar_pricepredictor_ml
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run Frontend/app.py
```

App will open at `http://localhost:8501`

---

## 🔍 Features

- Predicts resale price based on:
  - Vehicle age, KM driven, Mileage, Engine size, Max power
  - Brand, Fuel type, Transmission, Seller type
- Clean and minimal UI
- Instant predictions with no backend server needed