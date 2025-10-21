"""Weather data schemas."""
from typing import List

from pydantic import BaseModel, Field


class CurrentWeatherResponse(BaseModel):
    """Response for current weather data."""

    location: str = Field(..., description="Location name")
    temperature: float = Field(..., description="Current temperature")
    feels_like: float = Field(..., description="Feels like temperature")
    humidity: int = Field(..., description="Humidity percentage")
    description: str = Field(..., description="Weather description")
    condition: str = Field(..., description="Main weather condition")
    wind_speed: float = Field(..., description="Wind speed")
    timestamp: str = Field(..., description="Data timestamp in ISO format")
    units: str = Field(..., description="Temperature units (metric or imperial)")
    witty_message: str = Field(..., description="Humorous weather message")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "London, GB",
                "temperature": 12.5,
                "feels_like": 10.2,
                "humidity": 76,
                "description": "light rain",
                "condition": "Rain",
                "wind_speed": 5.5,
                "timestamp": "2024-01-15T15:30:00Z",
                "units": "metric",
                "witty_message": "You'll regret not wearing a coat!",
            }
        }


class TemperatureRange(BaseModel):
    """Temperature range for a day."""

    min: float = Field(..., description="Minimum temperature")
    max: float = Field(..., description="Maximum temperature")
    avg: float = Field(..., description="Average temperature")


class DailyForecast(BaseModel):
    """Daily forecast data."""

    date: str = Field(..., description="Date in YYYY-MM-DD format")
    temperature: TemperatureRange = Field(..., description="Temperature range")
    description: str = Field(..., description="Weather description")
    condition: str = Field(..., description="Main weather condition")
    humidity: int = Field(..., description="Average humidity percentage")
    wind_speed: float = Field(..., description="Average wind speed")
    witty_message: str = Field(..., description="Humorous weather message")


class ForecastResponse(BaseModel):
    """Response for 5-day weather forecast."""

    location: str = Field(..., description="Location name")
    units: str = Field(..., description="Temperature units")
    forecast: List[DailyForecast] = Field(..., description="5-day forecast")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "New York, US",
                "units": "imperial",
                "forecast": [
                    {
                        "date": "2024-01-15",
                        "temperature": {"min": 32.5, "max": 45.2, "avg": 38.8},
                        "description": "clear sky",
                        "condition": "Clear",
                        "humidity": 65,
                        "wind_speed": 8.5,
                        "witty_message": "Time to blind everyone with your pale legs!",
                    }
                ],
            }
        }