import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Get the API URL from environment variables
API_URL = os.environ.get("WEATHER_API_URL")

def fetch_weather_data(city):
    # Fetch weather data from the FastAPI backend using the URL from .env.
    if not API_URL:
        st.error("WEATHER_API_URL not set in .env file")
        return None
        
    payload = {
        "city": city,
        "output_format": "json"
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None