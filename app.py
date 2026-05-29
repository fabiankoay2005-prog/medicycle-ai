import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from festival_manager import *
from inventory_engine import *

# =========================
# 🌍 INTERNATIONAL AI MODULES
# =========================
from weather_api import get_weather, weather_factor
from google_calendar import get_calendar_events, event_risk
from outbreak_data import outbreak_factor
from logistics_engine import transfer_simulation
from doctor_chatbot import doctor_explain
from pdf_report import generate_pdf


# =========================
# 🔐 LOGIN SYSTEM
# =========================
USERS = {
    "admin": "admin123",
    "pharmacist": "pharma123"
}

def login():
    st.sidebar.title("🔐 Login System")

    user = st.sidebar.text_input("Username")
    pw = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if user in USERS and USERS[user] == pw:
            st.session_state["login"] = True
            st.session_state["user"] = user
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

def check_login():
    return st.session_state.get("login", False)


# =========================
# 💊 DRUG DATABASE
# =========================
DRUGS = [
    "flu_meds", "antibiotics", "painkillers", "cough_syrup",
    "antihistamines", "insulin", "antacids", "vitamins",
    "vaccines", "bronchodilators", "oral_rehydration_salts",
    "antihypertensives", "statins", "diuretics",
    "anticoagulants", "antiepileptics", "antidepressants",
    "antifungals", "antivirals", "eye_drops",
    "dermatology_products"
]


# =========================
# 📊 DATA GENERATOR
# =========================
def generate_data(medicine):

    dates = pd.date_range(end=pd.Timestamp.today(), periods=90)

    base = np.random.randint(80, 200)

    data = []

    for i, d in enumerate(dates):

        seasonal = 1 + np.sin(i / 6) * 0.2
        trend = 1 + i / 250
        noise = np.random.normal(0, 5)

        demand = base * seasonal * trend + noise

        data.append([d, medicine, max(5, demand)])

    return pd.DataFrame(data, columns=["date", "medicine", "demand"])


# =========================
# 🧠 AI ENGINE (BASE)
# =========================
def compute_ai(df, medicine):

    base = df["demand"].mean()
    latest = df["date"].max()

    festival, fest_mult = detect_festival(latest, medicine)

    trend = df["demand"].iloc[-5:].mean() / (base + 1e-6)

    final = base * fest_mult * trend

    return final, festival, fest_mult, trend


# =========================
# 🎉 FIXED FESTIVAL ENGINE (CLEAN + WORKING)
# =========================
def detect_festival(date, medicine):

    d = pd.to_datetime(date)

    festival_df = load_festivals()

    if festival_df is None or festival_df.empty:
        return "Normal Day", 1.0

    for _, row in festival_df.iterrows():

        row = row.fillna("")

        start = pd.to_datetime(row["start_date"])
        end = pd.to_datetime(row["end_date"])

        if start <= d <= end:

            festival_name = (
                row.get("festival_name")
                or row.get("Festival Name")
                or row.get("name")
                or row.get("event")
                or "Festival"
            )

            risk_level = row.get("risk_level", "Medium")

            if risk_level == "Low":
                base_mult = 1.1
            elif risk_level == "Medium":
                base_mult = 1.3
            else:
                base_mult = 1.6

            if "flu" in medicine:
                medicine_mult = 1.3
            elif "antibiotic" in medicine:
                medicine_mult = 1.2
            else:
                medicine_mult = 1.0

            return festival_name, base_mult * medicine_mult

    return "Normal Day", 1.0


# =========================
# 🚀 APP START
# =========================
st.set_page_config(
    page_title="MediCycle AI World Champion",
    layout="wide"
)

st.title("🏆 MediCycle AI Global Hospital Intelligence System")

login()

if not check_login():
    st.warning("Please login to continue")
    st.stop()

st.sidebar.success(f"Logged in as: {st.session_state['user']}")


# =========================
# 📅 FESTIVAL MANAGER (YOUR SYSTEM)
# =========================
st.subheader("📅 Festival Calendar Manager")

with st.expander("Add New Festival"):

    festival_name = st.text_input("Festival Name")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    crowd_size = st.number_input("Expected Crowd", min_value=0, value=100000)
    risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])

    if st.button("Save Festival"):
        add_festival(festival_name, start_date, end_date, crowd_size, risk_level)
        st.success("Festival saved successfully")


festival_df = load_festivals()

st.subheader("📋 Festival Database")
st.dataframe(festival_df, use_container_width=True)


# =========================
# 💊 MEDICINE SELECTION
# =========================
medicine = st.selectbox("💊 Select Drug", DRUGS)

df = generate_data(medicine)


# =========================
# 📊 GRAPH
# =========================
st.subheader("📊 Hospital Demand Simulation")
st.line_chart(df.set_index("date")["demand"])


# =========================
# 🧠 AI FORECAST ENGINE
# =========================
final, festival, fest_mult, trend = compute_ai(df, medicine)

st.subheader("🧠 AI Forecast Engine")

col1, col2 = st.columns(2)

with col1:
    st.metric("Base Demand", round(df["demand"].mean(), 2))

with col2:
    st.metric("Forecast Demand", round(final, 2))

st.success(f"Detected Festival: {festival}")


# =========================
# 🌍 GLOBAL AI EXTENSION
# =========================
weather = get_weather()
weather_mult = weather_factor(weather["condition"])

events = get_calendar_events()

calendar_risk = 1.0
for e in events:
    calendar_risk *= event_risk(e)

outbreak_mult = outbreak_factor(medicine)

enhanced = final * weather_mult * calendar_risk * outbreak_mult


st.subheader("🌍 Global Intelligence Layer")

st.metric("Enhanced Forecast", round(enhanced, 2))

st.write("🌦 Weather:", weather["condition"], "|", weather["temp"], "°C")
st.write("📅 Calendar Risk:", calendar_risk)
st.write("🦠 Outbreak:", outbreak_mult)

st.write("📌 Events:")
for e in events:
    st.write(f"- {e['title']}")


# =========================
# 🚚 LOGISTICS
# =========================
st.subheader("🚚 Hospital Drug Transfer Simulation")

a = st.number_input("Hospital A Stock", 0, 10000, 1200)
b = st.number_input("Hospital B Stock", 0, 10000, 2000)

if st.button("Simulate Transfer"):
    result = transfer_simulation(a, b, enhanced)
    st.write(result)


# =========================
# 🧠 DOCTOR AI
# =========================
st.subheader("🧠 Clinical AI Explanation")

st.info(
    doctor_explain(
        medicine,
        enhanced,
        weather["condition"],
        outbreak_mult
    )
)


# =========================
# 🎯 DECISION ENGINE
# =========================
st.subheader("🎯 Hospital Decision System")

if enhanced > 180:
    st.error("🚨 Increase stock immediately")
elif enhanced < 80:
    st.warning("⚠️ Reduce procurement")
else:
    st.success("✅ Stable inventory level")


# =========================
# 📄 PDF EXPORT
# =========================
st.subheader("📄 Generate Report")

if st.button("Export PDF Report"):

    file = generate_pdf({
        "Medicine": medicine,
        "Base Forecast": float(final),
        "Enhanced Forecast": float(enhanced),
        "Festival": festival,
        "Weather": weather["condition"],
        "Outbreak": outbreak_mult,
        "Calendar Risk": calendar_risk
    })

    st.success(f"Report generated: {file}")


# =========================
# 🏆 SUMMARY
# =========================
st.subheader("🏆 Executive Summary")

st.write(f"""
System Type:
Global Hospital AI Intelligence System

Key Features:
- Festival AI (CONNECTED ✔)
- Weather API
- Calendar Events
- Outbreak Prediction
- Logistics Simulation
- Clinical AI

Final Forecast: {round(enhanced,2)}
""")