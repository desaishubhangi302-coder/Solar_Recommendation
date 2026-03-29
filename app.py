import streamlit as st
import pickle
import pandas as pd

# Load model & columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("⚡ Electricity Savings Predictor")

st.write("Enter details to predict savings")

# Inputs (default values)
tariff = st.number_input("Tariff Rate (₹/unit)", value=4.3)
load = st.number_input("Load (kW)", value=0.26)
monthly = st.number_input("Monthly Units", value=47)

# Button
if st.button("Predict"):

    # ❗ Validation
    if tariff == 0 or load == 0 or monthly == 0:
        st.warning("⚠️ Please enter valid values (0 is not allowed)")

    else:
        #  Step 1: Input dictionary
        input_dict = {
            "Tariff_Rate": tariff,
            "Load_kW": load,
            "Monthly_kWh": monthly
        }

        #  Step 2: Convert to DataFrame
        input_data = pd.DataFrame([input_dict])

        #  Step 3: Match training columns
        input_data = input_data.reindex(columns=columns, fill_value=0)

        #  Step 4: Prediction
        prediction = model.predict(input_data)

        #  Output (FIXED ✅)
        if prediction[0] < 0:
            st.error("⚠️ No Savings Possible for given data")
            st.write(" Try higher units or tariff")
        else:
            st.success(f"💰 Estimated Monthly Savings: ₹{prediction[0]:.2f}")

        #  Solar calculation
        solar_kw = monthly / 120

        st.subheader("🌞 Solar Recommendation")

        st.info(f"🔋 Required Solar: {solar_kw:.2f} kW")
        st.info(f"⚡ Panel Size: {solar_kw*1000:.0f} Watts")

        # 👉 Extra info (improved)
        if solar_kw < 1:
            st.info("🏠 Suitable for small home usage")
        elif solar_kw < 3:
            st.info("🏡 Suitable for medium household")
        else:
            st.info("🏢 High usage – large solar system needed")

        # 👉 Cost estimation (bonus)
        cost = solar_kw * 50000
        st.info(f"💸 Estimated Solar Cost: ₹{cost:.0f}")