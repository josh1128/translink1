import streamlit as st
import pandas as pd
import numpy as np

st.title("⚡ Electric Bus Depot Orchestration Demo")
st.subheader("Simple Charging & Readiness Optimization")

# -----------------------------
# PARAMETERS
# -----------------------------
num_buses = st.slider("Number of Buses in Depot", 10, 100, 30)
num_chargers = st.slider("Number of Chargers Available", 5, 50, 15)
min_dispatch_soc = st.slider("Minimum SoC Required for Dispatch (%)", 40, 80, 60)

# -----------------------------
# SIMULATE TELEMETRY DATA
# -----------------------------
np.random.seed(42)

data = pd.DataFrame({
    "Bus_ID": [f"Bus_{i+1}" for i in range(num_buses)],
    "State_of_Charge (%)": np.random.randint(20, 100, num_buses),
    "Requires_Maintenance": np.random.choice([True, False], num_buses, p=[0.2, 0.8])
})

# -----------------------------
# PRIORITIZATION LOGIC
# -----------------------------
# Sort by lowest battery first
data = data.sort_values("State_of_Charge (%)")

# Assign chargers to lowest SoC buses
data["Assigned_to_Charge"] = False
data.loc[data.index[:num_chargers], "Assigned_to_Charge"] = True

# Dispatch Risk Flag
data["Dispatch_Risk"] = data["State_of_Charge (%)"] < min_dispatch_soc

# -----------------------------
# METRICS
# -----------------------------
avg_soc = data["State_of_Charge (%)"].mean()
risk_count = data["Dispatch_Risk"].sum()
charger_utilization = min(num_chargers, num_buses) / num_chargers * 100

st.metric("Average State of Charge (%)", round(avg_soc, 1))
st.metric("Buses at Dispatch Risk", int(risk_count))
st.metric("Charger Utilization (%)", round(charger_utilization, 1))

st.divider()

st.subheader("Depot Operational Overview")
st.dataframe(data)

# -----------------------------
# SIMPLE INSIGHTS
# -----------------------------
st.divider()
st.subheader("System Insight")

if risk_count > 0:
    st.warning("⚠ Charging capacity may be insufficient. Some buses risk missing pull-out.")
else:
    st.success("✅ All buses meet dispatch energy threshold.")

if charger_utilization > 95:
    st.info("🔋 Chargers operating near full capacity. Consider load balancing.")