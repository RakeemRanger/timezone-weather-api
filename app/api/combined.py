"""Combined API endpoints."""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.api.timezones import get_all_timezones
from app.api.weather import get_weather
from app.models.combined import CombinedResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/combined", response_model=CombinedResponse)
async def get_combined_data(
    city: str = Query(..., description="City name for weather data"),
    units: str = Query("metric", description="Units: metric, imperial, or standard"),
):
    """Get both timezone and weather information.

    Args:
        city: Name of the city for weather data
        units: Unit system for weather (metric, imperial, standard)

    Returns:
        CombinedResponse with both timezone and weather data

    Raises:
        HTTPException: If any service fails
    """
    logger.info(f"Fetching combined data for {city}")

    try:
        # Fetch timezone data
        timezone_data = await get_all_timezones()

        # Fetch weather data
        weather_data = await get_weather(city=city, units=units)

        return CombinedResponse(
            timezones=timezone_data.timezones,
            weather=weather_data,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching combined data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch combined data"
        )