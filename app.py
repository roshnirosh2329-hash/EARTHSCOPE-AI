import streamlit as st
import pandas as pd
import plotly.express as px

from modules.analysis import (
    climate_fingerprint,
    detect_climate_anomalies,
    discover_climate_relationships,
    calculate_long_term_trend
)

st.set_page_config(
    page_title="EARTHSCOPE AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 EARTHSCOPE AI")
st.subheader("Intelligent Climate Pattern Discovery System")

st.markdown(
    "Explore climate patterns, detect unusual conditions "
    "and compare environmental behaviour across regions."
)

# Load NASA data
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/multi_location_climate.csv",
        parse_dates=["Date"]
    )

try:
    df = load_data()

    locations = sorted(df["Location"].unique())

    selected_location = st.selectbox(
        "Select a location",
        locations
    )

    city_data = df[
        df["Location"] == selected_location
    ].copy()

    st.header(f"Climate Analysis: {selected_location}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Temperature",
        f"{city_data['Temperature'].mean():.2f} °C"
    )

    col2.metric(
        "Average Rainfall",
        f"{city_data['Rainfall'].mean():.2f} mm"
    )

    col3.metric(
        "Average Humidity",
        f"{city_data['Humidity'].mean():.2f} %"
    )

    col4.metric(
        "Average Wind Speed",
        f"{city_data['Wind Speed'].mean():.2f} m/s"
    )

    st.header("Climate Trends")

    parameter = st.selectbox(
        "Choose climate parameter",
        ["Temperature", "Rainfall", "Humidity", "Wind Speed"]
    )

    fig = px.line(
        city_data,
        x="Date",
        y=parameter,
        title=f"{parameter} Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Climate Fingerprint")

    st.write(climate_fingerprint(city_data))

    st.header("Climate Anomaly Detection")

    st.write(detect_climate_anomalies(city_data))

    st.header("Climate Relationships")

    st.write(discover_climate_relationships(city_data))

    st.header("Long-Term Climate Trend")

    st.write(calculate_long_term_trend(city_data))

    st.header("Regional Comparison")

    comparison = df.groupby("Location")[
        ["Temperature", "Rainfall", "Humidity", "Wind Speed"]
    ].mean()

    st.dataframe(comparison)

except Exception as error:
    st.error(f"Application error: {error}")

    st.info(
        "Check that NASA climate data has been collected "
        "and all analysis modules are available."
    )