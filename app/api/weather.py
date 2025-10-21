"""Weather API endpoints."""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
import requests

from app.core.config import settings
from app.models.weather import WeatherResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    city: str = Query(..., description="City name"),
    units: str = Query("metric", description="Units: metric, imperial, or standard"),
):
    """Get current weather information for a city.

    Args:
        city: Name of the city
        units: Unit system (metric, imperial, standard)

    Returns:
        WeatherResponse with current weather data

    Raises:
        HTTPException: If city not found or API error occurs
    """
    logger.info(f"Fetching weather for {city} with units={units}")

    if not settings.OPENWEATHER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Weather service not configured. Please set OPENWEATHER_API_KEY."
        )

    # Validate units
    valid_units = ["metric", "imperial", "standard"]
    if units not in valid_units:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid units. Must be one of: {', '.join(valid_units)}"
        )

    try:
        # Make request to OpenWeatherMap API
        url = f"{settings.OPENWEATHER_BASE_URL}/weather"
        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": units,
        }

        response = requests.get(
            url,
            params=params,
            timeout=settings.API_TIMEOUT
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city}' not found"
            )

        response.raise_for_status()
        data = response.json()

        # Extract weather information
        weather_response = WeatherResponse(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            description=data["weather"][0]["description"],
            weather_main=data["weather"][0]["main"],
            wind_speed=data["wind"]["speed"],
            wind_deg=data["wind"].get("deg"),
            clouds=data["clouds"]["all"],
            units=units,
        )

        return weather_response

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching weather for {city}")
        raise HTTPException(
            status_code=504,
            detail="Weather service request timed out"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather: {e}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching weather: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch weather data"
        )