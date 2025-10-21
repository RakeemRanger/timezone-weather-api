"""Weather data models."""
from typing import Optional
from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    """Current weather information."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code")
    temperature: float = Field(..., description="Current temperature")
    feels_like: float = Field(..., description="Feels like temperature")
    temp_min: float = Field(..., description="Minimum temperature")
    temp_max: float = Field(..., description="Maximum temperature")
    humidity: int = Field(..., description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    description: str = Field(..., description="Weather description")
    weather_main: str = Field(..., description="Main weather condition")
    wind_speed: float = Field(..., description="Wind speed")
    wind_deg: Optional[int] = Field(None, description="Wind direction in degrees")
    clouds: int = Field(..., description="Cloudiness percentage")
    units: str = Field(..., description="Unit system used")