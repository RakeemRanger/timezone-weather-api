"""Timezone API endpoints."""
import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
import pytz

from app.models.timezone import TimezoneInfo, TimezoneResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Major world timezones
MAJOR_TIMEZONES = [
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/Mexico_City",
    "America/Sao_Paulo",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "Europe/Moscow",
    "Africa/Cairo",
    "Africa/Johannesburg",
    "Asia/Dubai",
    "Asia/Kolkata",
    "Asia/Shanghai",
    "Asia/Tokyo",
    "Asia/Seoul",
    "Asia/Singapore",
    "Australia/Sydney",
    "Australia/Melbourne",
    "Pacific/Auckland",
    "UTC",
]


@router.get("/timezones", response_model=TimezoneResponse)
async def get_all_timezones():
    """Get current time for all major world timezones.

    Returns:
        TimezoneResponse with list of timezone information

    Raises:
        HTTPException: If unable to fetch timezone data
    """
    logger.info("Fetching timezone information for all major timezones")

    try:
        timezone_data: List[TimezoneInfo] = []
        utc_now = datetime.now(pytz.UTC)

        for tz_name in MAJOR_TIMEZONES:
            try:
                tz = pytz.timezone(tz_name)
                local_time = utc_now.astimezone(tz)
                
                timezone_info = TimezoneInfo(
                    timezone=tz_name,
                    current_time=local_time.isoformat(),
                    utc_offset=local_time.strftime("%z"),
                    timezone_abbreviation=local_time.strftime("%Z"),
                )
                timezone_data.append(timezone_info)
            except Exception as e:
                logger.warning(f"Error processing timezone {tz_name}: {e}")
                continue

        if not timezone_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve timezone information"
            )

        return TimezoneResponse(timezones=timezone_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching timezones: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch timezone data"
        )


@router.get("/timezones/{timezone_name}", response_model=TimezoneInfo)
async def get_timezone(timezone_name: str):
    """Get current time for a specific timezone.

    Args:
        timezone_name: Timezone identifier (e.g., 'America/New_York')

    Returns:
        TimezoneInfo for the specified timezone

    Raises:
        HTTPException: If timezone not found or invalid
    """
    logger.info(f"Fetching timezone information for {timezone_name}")

    try:
        tz = pytz.timezone(timezone_name)
        local_time = datetime.now(pytz.UTC).astimezone(tz)

        return TimezoneInfo(
            timezone=timezone_name,
            current_time=local_time.isoformat(),
            utc_offset=local_time.strftime("%z"),
            timezone_abbreviation=local_time.strftime("%Z"),
        )

    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=404,
            detail=f"Timezone '{timezone_name}' not found"
        )
    except Exception as e:
        logger.error(f"Error fetching timezone {timezone_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch timezone data"
        )