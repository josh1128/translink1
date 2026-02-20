import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="TransLink Energy Management Console",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0055A4;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: #2c3e50;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stPlotlyChart {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.markdown("## ⚡ Controls")

# Date selection
selected_date = st.sidebar.date_input(
    "Select Date",
    datetime.now().date()
)

# Temperature slider (impacts range as per Athens study)
temperature = st.sidebar.slider(
    "Ambient Temperature (°C)",
    min_value=-10,
    max_value=40,
    value=15,
    help="Energy consumption varies significantly with temperature (Athens case study)"
)

# Passenger load factor
load_factor = st.sidebar.slider(
    "Passenger Load Factor (%)",
    min_value=0,
    max_value=100,
    value=60,
    help="Higher passenger load increases energy consumption"
)

# Time-of-Use rate selection
tou_period = st.sidebar.selectbox(
    "Time-of-Use Period",
    ["Off-Peak (0.08 $/kWh)", "Mid-Peak (0.12 $/kWh)", "On-Peak (0.18 $/kWh)"],
    help="Electricity rates vary by time of day"
)

# Main header
st.markdown('<p class="main-header">🔋 TransLink Energy Management Console</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time monitoring and optimization for battery-electric bus fleet</p>', unsafe_allow_html=True)

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: white; margin: 0;">Fleet SOC</h3>
        <h1 style="color: white; margin: 0;">87%</h1>
        <p style="color: rgba(255,255,255,0.8); margin: 0;">↑ 12% from yesterday</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="warning-card">
        <h3 style="color: white; margin: 0;">Peak Demand</h3>
        <h1 style="color: white; margin: 0;">2.4 MW</h1>
        <p style="color: rgba(255,255,255,0.8); margin: 0;">Near capacity (2.8 MW)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="success-card">
        <h3 style="color: #2c3e50; margin: 0;">Chargers Active</h3>
        <h1 style="color: #2c3e50; margin: 0;">18/24</h1>
        <p style="color: #2c3e50; margin: 0;">6 available</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Calculate range factor based on temperature (from Athens study)
    if temperature < 10 or temperature > 30:
        range_factor = "↓ Limited"
        range_color = "#f093fb"
    else:
        range_factor = "✅ Optimal"
        range_color = "#84fab0"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 1rem; color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="color: white; margin: 0;">Range Status</h3>
        <h1 style="color: white; margin: 0;">{range_factor}</h1>
        <p style="color: rgba(255,255,255,0.8); margin: 0;">{temperature}°C affects consumption</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Two main columns for charts
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📊 Charging Window Optimization")
    
    # Generate charging schedule data
    hours = list(range(0, 24))
    charging_power = []
    soc_levels = []
    
    for hour in hours:
        # Simulate charging pattern with overnight preference
        if 1 <= hour <= 5:
            power = random.uniform(300, 500)  # Overnight charging
            soc = min(100, 70 + hour * 6)
        elif 10 <= hour <= 14 or 17 <= hour <= 20:
            power = random.uniform(100, 200)  # Peak hour limited charging
            soc = max(30, 90 - hour * 2)
        else:
            power = random.uniform(50, 150)  # Trickle charging
            soc = random.uniform(60, 85)
        charging_power.append(power)
        soc_levels.append(soc)
    
    # Create dual-axis chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hours,
        y=charging_power,
        name="Charging Power (kW)",
        marker_color='#0055A4',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=soc_levels,
        name="Average SOC (%)",
        marker_color='#FF6B6B',
        yaxis='y2',
        line=dict(width=3)
    ))
    
    fig.update_layout(
        xaxis=dict(title="Hour of Day", tickmode='linear', tick0=0, dtick=2),
        yaxis=dict(title="Charging Power (kW)", side='left', range=[0, 600]),
        yaxis2=dict(title="State of Charge (%)", side='right', overlaying='y', range=[0, 100]),
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add vertical line for current hour
    current_hour = datetime.now().hour
    fig.add_vline(x=current_hour, line_dash="dash", line_color="red", opacity=0.5)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("🕒 Red dashed line indicates current hour. Overnight charging (1-5 AM) optimizes off-peak rates.")

with right_col:
    st.markdown("### 🔋 Battery Health & Range Prediction")
    
    # Generate battery health data
    bus_ids = [f"BUS {i}" for i in range(1, 13)]
    soc = [random.randint(65, 98) for _ in range(12)]
    health = [random.randint(92, 100) for _ in range(12)]
    range_km = []
    
    for i in range(12):
        # Range calculation based on SOC, temperature, and load (from research)
        base_range = 250 * (soc[i] / 100)
        temp_factor = 1.0 if 15 <= temperature <= 25 else 0.7 if temperature > 30 else 0.8
        load_factor_adj = 1.0 - (load_factor / 100) * 0.3
        range_km.append(base_range * temp_factor * load_factor_adj)
    
    df_buses = pd.DataFrame({
        'Bus': bus_ids,
        'SOC (%)': soc,
        'Battery Health (%)': health,
        'Est. Range (km)': [round(r, 1) for r in range_km]
    })
    
    # Color coded dataframe
    def color_soc(val):
        if val > 80:
            return 'background-color: #84fab0'
        elif val > 50:
            return 'background-color: #ffe083'
        else:
            return 'background-color: #f093fb'
    
    styled_df = df_buses.style.applymap(color_soc, subset=['SOC (%)'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400,
        column_config={
            "Bus": "Bus ID",
            "SOC (%)": st.column_config.NumberColumn("SOC (%)", format="%d%%"),
            "Battery Health (%)": st.column_config.NumberColumn("Health", format="%d%%"),
            "Est. Range (km)": st.column_config.NumberColumn("Range (km)", format="%.1f km")
        }
    )
    
    st.caption(f"📍 Range estimates adjusted for {temperature}°C and {load_factor}% passenger load (Athens study methodology)")

# Third row - Energy Storage System and Grid Impact
st.markdown("### ⚡ Energy Storage System Performance")
col5, col6 = st.columns(2)

with col5:
    # ESS charge/discharge cycle
    hours_ess = list(range(0, 24))
    ess_charge = []
    grid_draw = []
    
    for hour in hours_ess:
        if 1 <= hour <= 5:
            ess_charge.append(random.uniform(200, 400))  # ESS charging overnight
            grid_draw.append(random.uniform(100, 200))
        elif 17 <= hour <= 21:
            ess_charge.append(random.uniform(-400, -200))  # ESS discharging during peak
            grid_draw.append(random.uniform(300, 500))  # Still some grid draw
        else:
            ess_charge.append(random.uniform(-100, 100))
            grid_draw.append(random.uniform(150, 300))
    
    fig_ess = go.Figure()
    fig_ess.add_trace(go.Scatter(
        x=hours_ess, y=ess_charge,
        fill='tozeroy', name='ESS Charge/Discharge',
        line=dict(color='#2E86AB')
    ))
    fig_ess.add_trace(go.Scatter(
        x=hours_ess, y=grid_draw,
        name='Grid Draw',
        line=dict(color='#A23B72', dash='dot')
    ))
    fig_ess.update_layout(
        title="ESS vs Grid Demand",
        xaxis_title="Hour",
        yaxis_title="Power (kW)",
        height=300,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_ess, use_container_width=True)

with col6:
    st.markdown("### 💰 Cost & Emissions Summary")
    
    # Calculate savings based on research [citation:6]
    base_cost = 12500
    ess_savings = base_cost * 0.27  # 27% cost reduction from OCC/ESS
    emission_reduction = 13  # 13% reduction
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 1rem;">
        <h4>Today's Projected Savings</h4>
        <h2 style="color: #2E86AB;">${int(ess_savings):,}</h2>
        <p>↓ 27% vs baseline (with ESS integration)</p>
        
        <h4 style="margin-top: 1.5rem;">CO₂ Emissions</h4>
        <h2 style="color: #2E86AB;">4.2 tCO₂e</h2>
        <p>↓ {emission_reduction}% vs diesel equivalent</p>
        
        <h4 style="margin-top: 1.5rem;">Peak Demand Reduction</h4>
        <div style="background: #e9ecef; height: 20px; border-radius: 10px;">
            <div style="background: #0055A4; width: 56%; height: 20px; border-radius: 10px;"></div>
        </div>
        <p>56% reduction during on-peak hours [citation:6]</p>
    </div>
    """, unsafe_allow_html=True)

# Footer with recommendations summary
st.markdown("---")
st.markdown("""
<div style="background: #e3f2fd; padding: 1rem; border-radius: 0.5rem;">
    <h4>📋 Key Recommendations Applied</h4>
    <ul>
        <li><strong>Energy Storage System (ESS)</strong> - Shifts charging to off-peak, reducing costs by 27% [citation:6]</li>
        <li><strong>Predictive Range Management</strong> - Accounts for temperature and passenger load (Athens methodology) [citation:3]</li>
        <li><strong>Optimized Charging Windows</strong> - 56% reduction in on-peak grid demand [citation:6]</li>
        <li><strong>Multi-Objective Optimization</strong> - Balances infrastructure cost, electricity cost, and emissions [citation:1]</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Auto-refresh note
st.caption("🔄 Dashboard updates every 5 minutes | Based on research from McMaster University, Aristotle University, and Utah Transit Authority case studies")
