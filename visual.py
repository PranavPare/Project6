import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    .stApp {
        background-color: #90caf9;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("📊 Weather Forecast Visualization")




# Load CSV
csv_file = "weather_forecast.csv"

if not os.path.exists(csv_file):
    st.error("No data available. Please fetch the forecast first from the main page.")
else:
    weather_df = pd.read_csv(csv_file)


    if not weather_df.empty:
        st.subheader("Forecast Data")
        st.dataframe(weather_df)

        # Temperature Trend
        st.subheader("Temperature Trend (°C)")
        st.line_chart(weather_df.set_index("Date")["Temperature"])

        # Humidity Trend
        st.subheader("Humidity Trend (%)")
        st.bar_chart(weather_df.set_index("Date")["Humidity"])

        # Wind Speed Trend
        st.subheader("Wind Speed Trend (m/s)")
        st.line_chart(weather_df.set_index("Date")["Wind Speed"])

        # Scatter Plot
        st.subheader("Scatter Plot: Temperature vs Humidity")
        fig, ax = plt.subplots()
        ax.scatter(weather_df["Temperature"], weather_df["Humidity"], color="blue", alpha=0.7)
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Humidity (%)")
        ax.set_title("Temperature vs Humidity")
        st.pyplot(fig)

    else:
        st.error("The CSV file is empty. Please fetch the forecast from the main page.")
