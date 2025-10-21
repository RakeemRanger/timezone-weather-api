"""Tests for combined endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@patch("app.services.weather_client.weather_client.get_current_weather")
@patch("app.services.timezone_service.timezone_service.get_timezone_info")
def test_get_timezone_and_weather_success(
    mock_get_timezone, mock_get_weather, client: TestClient
):
    """Test successful combined timezone and weather retrieval."""
    from app.schemas.timezone import TimezoneResponse
    from app.schemas.weather import CurrentWeatherResponse
    
    mock_get_timezone.return_value = TimezoneResponse(
        timezone="Europe/London",
        current_time="2024-01-15T15:30:00+00:00",
        utc_offset="+00:00",
        is_dst=False,
        abbreviation="GMT",
    )
    
    mock_get_weather.return_value = CurrentWeatherResponse(
        location="London, GB",
        temperature=12.5,
        feels_like=10.2,
        humidity=76,
        description="light rain",
        condition="Rain",
        wind_speed=5.5,
        timestamp="2024-01-15T15:30:00Z",
        units="metric",
        witty_message="You'll regret not wearing a coat!",
    )
    
    response = client.get(
        "/api/v1/timezone-weather?city=London&timezone=Europe/London&country_code=GB"
    )
    assert response.status_code == 200
    data = response.json()
    assert "timezone" in data
    assert "weather" in data
    assert data["timezone"]["timezone"] == "Europe/London"
    assert data["weather"]["location"] == "London, GB"
    assert "witty_message" in data["weather"]


def test_get_timezone_and_weather_missing_params(client: TestClient):
    """Test combined endpoint with missing parameters."""
    response = client.get("/api/v1/timezone-weather?city=London")
    assert response.status_code == 422  # Validation error