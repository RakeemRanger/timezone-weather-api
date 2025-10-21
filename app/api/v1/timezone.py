"""Timezone API endpoints."""
import logging

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.schemas.timezone import TimezoneResponse
from app.services.timezone_service import timezone_service

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/timezone/{timezone}", response_model=TimezoneResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_timezone_info(
    request: Request,
    timezone: str,
) -> TimezoneResponse:
    """Get timezone information for a specific timezone.

    Args:
        request: FastAPI request object
        timezone: Timezone name (e.g., 'America/New_York', 'Europe/London')

    Returns:
        TimezoneResponse with timezone information

    Raises:
        HTTPException: If timezone is invalid or not found
    """
    logger.info(f"Fetching timezone info for: {timezone}")

    try:
        result = await timezone_service.get_timezone_info(timezone)
        return result
    except ValueError as e:
        logger.error(f"Invalid timezone: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching timezone info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch timezone information")