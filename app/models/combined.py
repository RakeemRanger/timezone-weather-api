"""Combined data models."""
from typing import List
from pydantic import BaseModel, Field

from app.models.timezone import TimezoneInfo
from app.models.weather import WeatherResponse


class CombinedResponse(BaseModel):
    """Combined timezone and weather information."""

    timezones: List[TimezoneInfo] = Field(..., description="List of timezone information")
    weather: WeatherResponse = Field(..., description="Weather information")