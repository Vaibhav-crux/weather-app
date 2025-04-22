import streamlit as st
from datetime import datetime

def get_weather_icon(temp):
    """Pick an icon based on temperature."""
    temp = float(temp.split()[0])
    if temp > 30:
        return "☀️"  # Hot and sunny
    elif 20 <= temp <= 30:
        return "⛅"  # Pleasant, partly cloudy
    elif 10 <= temp < 20:
        return "☁️"  # Cool and cloudy
    else:
        return "❄️"  # Cold, maybe snowy

def display_weather(weather_data):
    """Display weather data in a formatted box."""
    weather_icon = get_weather_icon(weather_data["Weather"])

    st.markdown('<div class="weather-box">', unsafe_allow_html=True)
    
    # Weather and city
    st.markdown(
        f"""
        <h2>{weather_icon} {weather_data['Weather']}</h2>
        <h3>{weather_data['City']}</h3>
        """,
        unsafe_allow_html=True
    )

    # Latitude and Longitude in columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="metric-label">Latitude</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{weather_data["Latitude"]}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="metric-label">Longitude</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{weather_data["Longitude"]}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Timestamp
    st.write(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")