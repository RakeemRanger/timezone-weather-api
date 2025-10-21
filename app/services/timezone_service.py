"""Timezone service for handling timezone operations."""
import hashlib
import json
import logging
from datetime import datetime

import pytz

from app.core.config import settings
from app.schemas.timezone import TimezoneResponse
from app.services.cache import cache_service

logger = logging.getLogger(__name__)


class TimezoneService:
    """Service for timezone operations."""

    def _generate_cache_key(self, timezone: str) -> str:
        """Generate cache key for timezone."""
        return f"timezone:{hashlib.md5(timezone.encode()).hexdigest()}"

    async def get_timezone_info(self, timezone: str) -> TimezoneResponse:
        """Get timezone information.

        Args:
            timezone: Timezone name (e.g., 'America/New_York')

        Returns:
            TimezoneResponse with timezone information

        Raises:
            ValueError: If timezone is invalid
        """
        # Check cache
        cache_key = self._generate_cache_key(timezone)
        cached_data = await cache_service.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for timezone: {timezone}")
            data = json.loads(cached_data)
            return TimezoneResponse(**data)

        try:
            # Get timezone
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)

            # Get UTC offset
            offset = now.strftime("%z")
            formatted_offset = f"{offset[:3]}:{offset[3:]}"

            # Check if DST is active
            is_dst = bool(now.dst())

            # Get timezone abbreviation
            abbreviation = now.strftime("%Z")

            result = TimezoneResponse(
                timezone=timezone,
                current_time=now.isoformat(),
                utc_offset=formatted_offset,
                is_dst=is_dst,
                abbreviation=abbreviation,
            )

            # Cache result for 5 minutes (timezone info doesn't change often)
            await cache_service.set(
                cache_key,
                result.model_dump_json(),
                ttl=300,
            )

            return result

        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {timezone}")
        except Exception as e:
            logger.error(f"Error getting timezone info: {e}", exc_info=True)
            raise ValueError(f"Invalid timezone: {timezone}")


timezone_service = TimezoneService()