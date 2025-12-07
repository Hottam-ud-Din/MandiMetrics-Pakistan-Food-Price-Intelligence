import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MandiMetrics | Hottam Ud Din",
    page_icon="🌾",
    layout="wide"
)

# --- HEADER & BRANDING ---
st.title("🌾 MandiMetrics: Pakistan Food Price Intelligence")
st.markdown("""
**Developed by:** Hottam Ud Din  
**Dataset Source:** [WFP Food Prices for Pakistan](https://data.humdata.org/dataset/wfp-food-prices-for-pakistan) (Humanitarian Data Exchange)

### 📌 Project Overview
This dashboard utilizes **Machine Learning (Facebook Prophet)** and **Time-Series Analysis** to track food inflation in Pakistan. 
It analyzes data from **2004 to 2025** to detect seasonal trends, currency impact, and regional price disparities.
""")
st.markdown("---")

# --- 1. DATA LOADING (Cached) ---
@st.cache_data
def load_data():
    df = pd.read_csv("wfp_food_prices_pak.csv", header=0)
    df = df.drop(0) # Remove meta-row
    
    # Fix Types
    df['date'] = pd.to_datetime(df['date'])
    cols = ['price', 'usdprice', 'latitude', 'longitude']
    for c in cols:
        df[c] = pd.to_numeric(df[c])
    
    # Filter for Retail only
    df = df[df['pricetype'] == 'Retail']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'wfp_food_prices_pak.csv' not found. Please ensure the file is in the same directory.")
    st.stop()

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("🔍 Configuration")

# Commodity Filter
commodities = df['commodity'].unique()
selected_commodity = st.sidebar.selectbox("Select Commodity", commodities, index=0)

# Province Filter (ADDED BACK)
provinces = df['admin1'].unique()
selected_provinces = st.sidebar.multiselect("Select Province", provinces, default=provinces)

# Date Filter
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# Filter Data based on ALL inputs
filtered_df = df[
    (df['commodity'] == selected_commodity) & 
    (df['admin1'].isin(selected_provinces)) & # Filter by selected provinces
    (df['date'] >= pd.to_datetime(date_range[0])) & 
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# --- 3. KEY PERFORMANCE INDICATORS (KPIs) ---
st.subheader(f"📊 Market Snapshot: {selected_commodity}")
col1, col2, col3, col4 = st.columns(4)

latest_date = filtered_df['date'].max()
latest_avg = filtered_df[filtered_df['date'] == latest_date]['price'].mean()

# Compare to 1 year ago
one_year_ago = latest_date - pd.DateOffset(years=1)
old_data = df[(df['commodity'] == selected_commodity) & 
              (df['date'].dt.year == one_year_ago.year) & 
              (df['date'].dt.month == one_year_ago.month)]
old_price = old_data['price'].mean()

if pd.notna(old_price):
    delta = ((latest_avg - old_price) / old_price) * 100
    delta_str = f"{delta:.1f}% vs Last Year"
else:
    delta_str = "Data N/A"

with col1:
    st.metric("Current Avg Price", f"PKR {latest_avg:.2f}", delta_str)
with col2:
    st.metric("Highest Recorded Price", f"PKR {filtered_df['price'].max():.2f}")
with col3:
    st.metric("Lowest Recorded Price", f"PKR {filtered_df['price'].min():.2f}")
with col4:
    st.metric("Data Points Analyzed", f"{len(filtered_df)}")

# --- 4. VISUALIZATION SECTION ---

# A. Trend Analysis
st.markdown("### 📈 Price Trend & Inflation Analysis")
st.caption("This chart visualizes how the price has evolved over time. Peaks usually indicate economic instability or supply shortages.")
fig_trend = px.line(filtered_df.groupby('date')['price'].mean().reset_index(), 
                    x='date', y='price', title=f"Average Retail Price: {selected_commodity}")
st.plotly_chart(fig_trend, use_container_width=True)

# B. Regional Analysis
col_map, col_box = st.columns([2, 1])

with col_map:
    st.markdown("### 🗺️ Geospatial Price Heatmap")
    st.caption("Which cities are most expensive? Red bubbles indicate higher prices.")
    # Get latest available data for map
    latest_map_data = filtered_df[filtered_df['date'] == filtered_df['date'].max()]
    fig_map = px.scatter_mapbox(latest_map_data, lat="latitude", lon="longitude", 
                                size="price", color="price", hover_name="market",
                                zoom=4, mapbox_style="open-street-map",
                                color_continuous_scale="RdYlGn_r",
                                title="Latest Price Intensity by City")
    st.plotly_chart(fig_map, use_container_width=True)

with col_box:
    st.markdown("### 📊 Provincial Disparity")
    st.caption("Comparison of price ranges across provinces.")
    fig_box = px.box(filtered_df, x='admin1', y='price', color='admin1', 
                     title="Price Distribution by Province")
    st.plotly_chart(fig_box, use_container_width=True)

# --- 5. ADVANCED FORECASTING SECTION ---
st.markdown("---")
st.subheader("🤖 AI Price Forecast: Provincial Comparison")
st.markdown("""
**How this works:** We train separate Machine Learning models (Prophet) for each selected province to predict future prices.
This helps in identifying which regions might face severe inflation in the coming months.
""")

# Get available provinces dynamically from data
available_provinces = df['admin1'].unique().tolist()
forecast_provinces = st.multiselect("Select Provinces to Compare", available_provinces, default=available_provinces[:2])
months = st.slider("Prediction Horizon (Months)", 1, 24, 12)

if st.button("Generate Multi-Province Forecast"):
    if not forecast_provinces:
        st.warning("Please select at least one province.")
    else:
        with st.spinner(f"Training AI models for {len(forecast_provinces)} provinces..."):
            fig_forecast = go.Figure()
            
            for province in forecast_provinces:
                # Filter specifically for the province loop
                prov_df = df[(df['commodity'] == selected_commodity) & (df['admin1'] == province)]
                
                if len(prov_df) < 20:
                    st.warning(f"⚠️ Not enough data for {province}. Skipping.")
                    continue
                
                # Prepare Data for Prophet
                p_data = prov_df.groupby('date')['price'].mean().reset_index()
                p_data.columns = ['ds', 'y']
                
                # Train & Predict
                m = Prophet(yearly_seasonality=True)
                m.fit(p_data)
                future = m.make_future_dataframe(periods=months * 30)
                forecast = m.predict(future)
                
                # Plot
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat'], 
                    name=f"{province} (Predicted)", mode='lines'
                ))
            
            fig_forecast.update_layout(title=f"Future Price Projection: {selected_commodity}",
                                       xaxis_title="Date", yaxis_title="Price (PKR)")
            st.plotly_chart(fig_forecast, use_container_width=True)
            st.success("✅ Prediction Complete. Analyze the trend lines above.")