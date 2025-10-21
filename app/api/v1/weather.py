"""Weather API endpoints."""
import logging

from fastapi import APIRouter, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.schemas.weather import CurrentWeatherResponse, ForecastResponse
from app.services.weather_client import weather_client

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/weather/current", response_model=CurrentWeatherResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_current_weather(
    request: Request,
    city: str = Query(..., description="City name"),
    country_code: str = Query(None, description="ISO 3166 country code (e.g., US, GB)"),
    units: str = Query("metric", regex="^(metric|imperial)$", description="Temperature units"),
) -> CurrentWeatherResponse:
    """Get current weather data with a witty message.

    Args:
        request: FastAPI request object
        city: City name
        country_code: ISO 3166 country code (optional)
        units: Temperature units (metric or imperial)

    Returns:
        CurrentWeatherResponse with weather data and witty message

    Raises:
        HTTPException: If city not found or API error occurs
    """
    logger.info(f"Fetching current weather for: {city}, {country_code}")

    try:
        result = await weather_client.get_current_weather(city, country_code, units)
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching weather: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")


@router.get("/weather/forecast", response_model=ForecastResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_weather_forecast(
    request: Request,
    city: str = Query(..., description="City name"),
    country_code: str = Query(None, description="ISO 3166 country code (e.g., US, GB)"),
    units: str = Query("metric", regex="^(metric|imperial)$", description="Temperature units"),
) -> ForecastResponse:
    """Get 5-day weather forecast with witty messages.

    Args:
        request: FastAPI request object
        city: City name
        country_code: ISO 3166 country code (optional)
        units: Temperature units (metric or imperial)

    Returns:
        ForecastResponse with 5-day forecast and witty messages

    Raises:
        HTTPException: If city not found or API error occurs
    """
    logger.info(f"Fetching 5-day forecast for: {city}, {country_code}")

    try:
        result = await weather_client.get_forecast(city, country_code, units)
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching forecast: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data")