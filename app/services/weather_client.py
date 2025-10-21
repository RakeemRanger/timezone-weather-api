"""Weather API client service."""
import hashlib
import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.schemas.weather import (
    CurrentWeatherResponse,
    DailyForecast,
    ForecastResponse,
    TemperatureRange,
)
from app.services.cache import cache_service
from app.services.weather_messages import get_witty_message

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client for interacting with OpenWeatherMap API."""

    def __init__(self):
        self.base_url = settings.WEATHER_API_BASE_URL
        self.api_key = settings.WEATHER_API_KEY
        self.timeout = settings.WEATHER_API_TIMEOUT
        self.max_retries = settings.WEATHER_API_MAX_RETRIES

    def _generate_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache key for request."""
        key_string = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return f"weather:{hashlib.md5(key_string.encode()).hexdigest()}"

    def _build_location_query(self, city: str, country_code: Optional[str] = None) -> str:
        """Build location query string."""
        if country_code:
            return f"{city},{country_code}"
        return city

    async def get_current_weather(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric",
    ) -> CurrentWeatherResponse:
        """Fetch current weather data.

        Args:
            city: City name
            country_code: ISO 3166 country code (optional)
            units: Temperature units (metric or imperial)

        Returns:
            CurrentWeatherResponse with weather data and witty message

        Raises:
            ValueError: If validation fails
            httpx.HTTPError: If API request fails
        """
        if not self.api_key:
            raise ValueError("Weather API key not configured")

        location = self._build_location_query(city, country_code)
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units,
        }

        # Check cache
        cache_key = self._generate_cache_key("current", params)
        cached_data = await cache_service.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for current weather: {location}")
            data = json.loads(cached_data)
            return CurrentWeatherResponse(**data)

        logger.info(f"Fetching current weather for: {location}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.get(
                        f"{self.base_url}/weather",
                        params=params,
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Extract weather data
                    condition = data["weather"][0]["main"]
                    description = data["weather"][0]["description"]
                    temp = data["main"]["temp"]
                    feels_like = data["main"]["feels_like"]
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]
                    timestamp = datetime.utcfromtimestamp(data["dt"]).isoformat() + "Z"

                    location_name = f"{data['name']}, {data['sys']['country']}"

                    # Get witty message
                    witty_message = get_witty_message(
                        condition=condition,
                        temperature=temp,
                        wind_speed=wind_speed,
                        units=units,
                    )

                    result = CurrentWeatherResponse(
                        location=location_name,
                        temperature=temp,
                        feels_like=feels_like,
                        humidity=humidity,
                        description=description,
                        condition=condition,
                        wind_speed=wind_speed,
                        timestamp=timestamp,
                        units=units,
                        witty_message=witty_message,
                    )

                    # Cache result
                    await cache_service.set(
                        cache_key,
                        result.model_dump_json(),
                        ttl=settings.CACHE_TTL,
                    )

                    return result

                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        raise ValueError(f"City not found: {location}")
                    logger.warning(
                        f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}"
                    )
                    if attempt == self.max_retries - 1:
                        raise
                except httpx.HTTPError as e:
                    logger.warning(
                        f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}"
                    )
                    if attempt == self.max_retries - 1:
                        raise
                except Exception as e:
                    logger.error(f"Unexpected error: {e}", exc_info=True)
                    raise

    async def get_forecast(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric",
    ) -> ForecastResponse:
        """Fetch 5-day weather forecast.

        Args:
            city: City name
            country_code: ISO 3166 country code (optional)
            units: Temperature units (metric or imperial)

        Returns:
            ForecastResponse with 5-day forecast and witty messages

        Raises:
            ValueError: If validation fails
            httpx.HTTPError: If API request fails
        """
        if not self.api_key:
            raise ValueError("Weather API key not configured")

        location = self._build_location_query(city, country_code)
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units,
        }

        # Check cache
        cache_key = self._generate_cache_key("forecast", params)
        cached_data = await cache_service.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for forecast: {location}")
            data = json.loads(cached_data)
            return ForecastResponse(**data)

        logger.info(f"Fetching 5-day forecast for: {location}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.get(
                        f"{self.base_url}/forecast",
                        params=params,
                    )
                    response.raise_for_status()
                    data = response.json()

                    location_name = f"{data['city']['name']}, {data['city']['country']}"

                    # Group forecast data by date
                    daily_data: Dict[str, List[Dict]] = defaultdict(list)
                    for item in data["list"]:
                        date = datetime.utcfromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                        daily_data[date].append(item)

                    # Process daily forecasts (take first 5 days)
                    forecasts = []
                    for date in sorted(daily_data.keys())[:5]:
                        day_items = daily_data[date]

                        # Calculate temperature range
                        temps = [item["main"]["temp"] for item in day_items]
                        min_temp = min(temps)
                        max_temp = max(temps)
                        avg_temp = sum(temps) / len(temps)

                        # Get most common weather condition
                        conditions = [item["weather"][0]["main"] for item in day_items]
                        condition = max(set(conditions), key=conditions.count)
                        descriptions = [item["weather"][0]["description"] for item in day_items]
                        description = max(set(descriptions), key=descriptions.count)

                        # Calculate average humidity and wind speed
                        humidity = sum(item["main"]["humidity"] for item in day_items) // len(
                            day_items
                        )
                        wind_speed = sum(item["wind"]["speed"] for item in day_items) / len(
                            day_items
                        )

                        # Get witty message
                        witty_message = get_witty_message(
                            condition=condition,
                            temperature=avg_temp,
                            wind_speed=wind_speed,
                            units=units,
                        )

                        forecasts.append(
                            DailyForecast(
                                date=date,
                                temperature=TemperatureRange(
                                    min=round(min_temp, 1),
                                    max=round(max_temp, 1),
                                    avg=round(avg_temp, 1),
                                ),
                                description=description,
                                condition=condition,
                                humidity=humidity,
                                wind_speed=round(wind_speed, 1),
                                witty_message=witty_message,
                            )
                        )

                    result = ForecastResponse(
                        location=location_name,
                        units=units,
                        forecast=forecasts,
                    )

                    # Cache result
                    await cache_service.set(
                        cache_key,
                        result.model_dump_json(),
                        ttl=settings.CACHE_TTL,
                    )

                    return result

                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        raise ValueError(f"City not found: {location}")
                    logger.warning(
                        f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}"
                    )
                    if attempt == self.max_retries - 1:
                        raise
                except httpx.HTTPError as e:
                    logger.warning(
                        f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}"
                    )
                    if attempt == self.max_retries - 1:
                        raise
                except Exception as e:
                    logger.error(f"Unexpected error: {e}", exc_info=True)
                    raise


weather_client = WeatherClient()