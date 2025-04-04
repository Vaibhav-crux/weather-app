from fastapi import APIRouter, HTTPException
from app.schemas.weather import WeatherRequest, WeatherResponse
from app.services.v1.weather_service import get_weather_data
from fastapi.responses import JSONResponse, Response
from app.utils.logger_config import setup_logger
import xml.etree.ElementTree as ET

# Initialize router and logger
router = APIRouter()
logger = setup_logger("weather_router")

@router.post("/getCurrentWeather",
             response_model=None,  # Flexible response model for format toggling
             summary="Get current weather data",
             description="Fetches current weather data for a city in JSON or XML format")
async def get_current_weather(request: WeatherRequest):
    """Retrieve current weather data for a city asynchronously."""
    # Log request details
    logger.info(f"Processing weather request for city: {request.city}, format: {request.output_format}")
    
    try:
        # Fetch weather data from service
        weather_data = await get_weather_data(request.city)
        
        # Handle JSON response format
        if request.output_format == "json":
            # Format data into WeatherResponse model
            response_data = WeatherResponse(
                weather=f"{weather_data['temp']} C",
                latitude=str(weather_data['lat']),
                longitude=str(weather_data['lon']),
                city=weather_data['city']
            )
            # Log response data
            logger.debug(f"Returning JSON response: {response_data.dict(by_alias=True)}")
            # Return JSON response using aliases (uppercase keys)
            return JSONResponse(content=response_data.dict(by_alias=True))
        
        # Handle XML response format
        elif request.output_format == "xml":
            # Create XML structure
            root = ET.Element("root")
            ET.SubElement(root, "Temperature").text = f"{weather_data['temp']}"
            ET.SubElement(root, "City").text = weather_data['city']
            ET.SubElement(root, "Latitude").text = str(weather_data['lat'])
            ET.SubElement(root, "Longitude").text = str(weather_data['lon'])
            
            # Convert XML to string
            xml_str = ET.tostring(root, encoding='utf-8', method='xml')
            # Log XML response
            logger.debug(f"Returning XML response: {xml_str.decode('utf-8')}")
            # Return XML response with appropriate media type
            return Response(content=xml_str, media_type="application/xml")
            
    except Exception as e:
        # Log error details
        logger.error(f"Error processing weather request: {str(e)}")
        # Raise HTTP exception with error message
        raise HTTPException(status_code=400, detail=str(e))