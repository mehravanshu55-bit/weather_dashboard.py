import streamlit as st
import requests

st.title("Live Weather")

CITIES = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88)
}


@st.cache_data(ttl=600)
def get_weather(lat, lon):

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return {}


city = st.selectbox(
    "Choose a city",
    list(CITIES.keys())
)

lat, lon = CITIES[city]

data = get_weather(lat, lon)


if data:
    current = data["current"]

    temp = current["temperature_2m"]
    wind = current["wind_speed_10m"]
    humidity = current["relative_humidity_2m"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperature", f"{temp} °C")

    with col2:
        st.metric("Wind Speed", f"{wind} km/h")

    with col3:
        st.metric("Humidity", f"{humidity}%")
