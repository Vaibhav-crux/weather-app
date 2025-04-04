from pydantic import BaseModel, Field
from typing import Literal

class WeatherRequest(BaseModel):
    """Schema defining the weather request payload."""
    city: str = Field(
        ...,
        description="Name of the city for weather data retrieval",
        min_length=1,
        pattern=r"^[a-zA-Z\s,-]+$"  # Restricts to letters, spaces, commas, and hyphens
    )
    output_format: Literal["json", "xml"] = Field(
        ...,
        description="Response format, either 'json' or 'xml'"  # Fixed: removed extra quote
    )

class WeatherResponse(BaseModel):
    """Schema defining the weather response data structure."""
    weather: str = Field(
        ...,
        alias="Weather",
        description="Current temperature in Celsius"
    )
    latitude: str = Field(
        ...,
        alias="Latitude",
        description="City latitude coordinate"
    )
    longitude: str = Field(
        ...,
        alias="Longitude",
        description="City longitude coordinate"
    )
    city: str = Field(
        ...,
        alias="City",
        description="City name including country"
    )

    class Config:
        """Pydantic configuration for the response model."""
        populate_by_name = True  # Allows population by field name
        populate_by_alias = True  # Enables serialization by alias