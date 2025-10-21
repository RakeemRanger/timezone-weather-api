"""Combined timezone and weather schemas."""
from pydantic import BaseModel, Field

from app.schemas.timezone import TimezoneResponse
from app.schemas.weather import CurrentWeatherResponse


class TimezoneWeatherResponse(BaseModel):
    """Combined response for timezone and weather data."""

    timezone: TimezoneResponse = Field(..., description="Timezone information")
    weather: CurrentWeatherResponse = Field(..., description="Current weather data")

    class Config:
        json_schema_extra = {
            "example": {
                "timezone": {
                    "timezone": "Asia/Tokyo",
                    "current_time": "2024-01-16T00:30:00+09:00",
                    "utc_offset": "+09:00",
                    "is_dst": False,
                    "abbreviation": "JST",
                },
                "weather": {
                    "location": "Tokyo, JP",
                    "temperature": 8.5,
                    "feels_like": 6.2,
                    "humidity": 62,
                    "description": "few clouds",
                    "condition": "Clouds",
                    "wind_speed": 3.5,
                    "timestamp": "2024-01-15T15:30:00Z",
                    "units": "metric",
                    "witty_message": "Perfect weather for brooding dramatically",
                },
            }
        }