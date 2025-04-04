import httpx
from fastapi import HTTPException
from app.config.settings import get_settings
from app.utils.logger_config import setup_logger

# Initialize logger for weather service
logger = setup_logger("weather_service")

async def get_weather_data(city: str) -> dict:
    """Fetch weather data asynchronously from WeatherAPI."""
    # Retrieve configuration settings, including API keys
    settings = get_settings()
    # Define WeatherAPI endpoint
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    
    # Set request headers for authentication
    headers = {
        "X-RapidAPI-Key": settings.api_key,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    
    # Define query parameters with city
    params = {"q": city}
    
    # Log request initiation
    logger.debug(f"Fetching weather data for city: {city}")
    
    # Use async HTTP client for efficient request handling
    async with httpx.AsyncClient() as client:
        try:
            # Send GET request and await response
            response = await client.get(url, headers=headers, params=params)
            # Raise exception for HTTP errors
            response.raise_for_status()
            # Parse JSON response
            data = response.json()
            
            # Extract relevant weather data
            weather_data = {
                "temp": data["current"]["temp_c"],
                "lat": data["location"]["lat"],
                "lon": data["location"]["lon"],
                "city": data["location"]["name"]
            }
            # Log successful data retrieval
            logger.debug(f"Successfully fetched weather data: {weather_data}")
            return weather_data
            
        except httpx.HTTPStatusError as e:
            # Log HTTP-specific errors
            logger.error(f"HTTP error fetching weather data for {city}: {str(e)}")
            # Raise exception for invalid city
            raise HTTPException(status_code=400, detail=f"City not found: {city}")
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error fetching weather data: {str(e)}")
            # Raise exception for service failure
            raise HTTPException(status_code=500, detail="Weather service unavailable")