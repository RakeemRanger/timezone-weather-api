"""Combined timezone and weather endpoints."""
import logging

from fastapi import APIRouter, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.schemas.combined import TimezoneWeatherResponse
from app.services.timezone_service import timezone_service
from app.services.weather_client import weather_client

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/timezone-weather", response_model=TimezoneWeatherResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_timezone_and_weather(
    request: Request,
    city: str = Query(..., description="City name"),
    timezone: str = Query(..., description="Timezone name (e.g., 'America/New_York')"),
    country_code: str = Query(None, description="ISO 3166 country code"),
    units: str = Query("metric", regex="^(metric|imperial)$", description="Temperature units"),
) -> TimezoneWeatherResponse:
    """Get both timezone information and current weather for a location.

    Args:
        request: FastAPI request object
        city: City name
        timezone: Timezone name
        country_code: ISO 3166 country code (optional)
        units: Temperature units (metric or imperial)

    Returns:
        TimezoneWeatherResponse with timezone and weather data

    Raises:
        HTTPException: If data cannot be fetched
    """
    logger.info(f"Fetching combined data for: {city} ({timezone})")

    try:
        # Fetch timezone and weather data concurrently
        timezone_info = await timezone_service.get_timezone_info(timezone)
        weather_info = await weather_client.get_current_weather(city, country_code, units)

        return TimezoneWeatherResponse(
            timezone=timezone_info,
            weather=weather_info,
        )
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching combined data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch timezone and weather data")