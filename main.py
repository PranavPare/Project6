import streamlit as st
import pandas as pd
import requests

API_KEY = "68939b3fb09e4bd82110feeebd8d3111"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Function to fetch 5-day weather data
def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        daily_forecast = []

        for i in range(0, len(data["list"]), 8):  # Every 8th entry = 24-hour interval
            day_data = data["list"][i]
            daily_forecast.append({
                "Date": day_data["dt_txt"].split()[0],
                "Temperature": day_data["main"]["temp"],  # No °C
                "Humidity": day_data["main"]["humidity"],  # No %
                "Weather": day_data["weather"][0]["description"].title(),
                "Wind Speed": day_data["wind"]["speed"]  # No m/s
            })

        return pd.DataFrame(daily_forecast)  # Convert to DataFrame
    else:
        return None

# Streamlit UI
st.title("🌦️ Weather Forecaster")
#add background
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

st.image('p1.jpg', caption="***Every cloud has a silver lining.***")
st.write("Enter a city name to get a 5-day weather forecast!")

city = st.text_input("Enter City Name:", "Mumbai")

if st.button("Get Weather"):
    with st.spinner("Fetching weather data... Please wait ⏳"):
        weather_df = get_weather(city)

    if weather_df is not None:
        # Save the CSV file
        csv_file = "weather_forecast.csv"
        weather_df.to_csv(csv_file, index=False)

        # Layout: 5 columns for 5-day forecast
        st.subheader(f"5-Day Forecast for {city}")
        cols = st.columns(5)  # Create 5 columns

        for i in range(len(weather_df)):
            with cols[i]:
                st.markdown(f"<p style='font-size:12px; color:gray;'><b>{weather_df.iloc[i]['Date']}</b></p>", unsafe_allow_html=True)
                st.write(f"🌡️ **{weather_df.iloc[i]['Temperature']}°C**")
                st.write(f"💧 {weather_df.iloc[i]['Humidity']}% Humidity")
                st.write(f"🌤️ {weather_df.iloc[i]['Weather']}")
                st.write(f"💨 {weather_df.iloc[i]['Wind Speed']} m/s")

        # Download CSV Button
        st.download_button(
            label="📥 Download CSV",
            data=weather_df.to_csv(index=False),
            file_name="weather_forecast.csv",
            mime="text/csv"
        )

# Navigation to next page
        st.page_link("pages/visual.py", label="📊 View Forecast Charts")
    else:
        st.error("City not found! Please enter a valid city name.")
