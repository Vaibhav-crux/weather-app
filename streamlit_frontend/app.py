import streamlit as st
from components.weather_display import display_weather
from utils.api_client import fetch_weather_data
import os

# Set page config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="⛅",
    layout="centered"
)

# Load external CSS using the correct path
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    """Main function to run the Weather Dashboard."""
    st.markdown('<div class="title">Weather Dashboard</div>', unsafe_allow_html=True)
    st.write("Enter a city name and click 'Get Weather' to see the current weather!")

    # City input and button
    city = st.text_input("City Name", placeholder="e.g., Bangalore")
    fetch_button = st.button("Get Weather")

    # Create a placeholder for weather data
    weather_placeholder = st.empty()

    if fetch_button and city:
        with st.spinner(f"Fetching weather for {city}..."):
            weather_data = fetch_weather_data(city)
            if weather_data:
                # Display weather data in the placeholder
                with weather_placeholder.container():
                    display_weather(weather_data)
            else:
                # Display error in the placeholder
                with weather_placeholder.container():
                    st.markdown(
                        '<p class="error">Could not get the weather data. Check the city name or try again later!</p>',
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()