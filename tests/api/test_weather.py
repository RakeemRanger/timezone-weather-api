"""Tests for weather endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@patch("app.services.weather_client.weather_client.get_current_weather")
def test_get_current_weather_success(mock_get_weather, client: TestClient, mock_weather_response):
    """Test successful current weather retrieval."""
    from app.schemas.weather import CurrentWeatherResponse
    
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
    
    response = client.get("/api/v1/weather/current?city=London&country_code=GB")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "London, GB"
    assert "temperature" in data
    assert "witty_message" in data


def test_get_current_weather_missing_city(client: TestClient):
    """Test current weather with missing city parameter."""
    response = client.get("/api/v1/weather/current")
    assert response.status_code == 422  # Validation error


def test_get_current_weather_invalid_units(client: TestClient):
    """Test current weather with invalid units parameter."""
    response = client.get("/api/v1/weather/current?city=London&units=invalid")
    assert response.status_code == 422


@patch("app.services.weather_client.weather_client.get_forecast")
def test_get_forecast_success(mock_get_forecast, client: TestClient):
    """Test successful forecast retrieval."""
    from app.schemas.weather import ForecastResponse, DailyForecast, TemperatureRange
    
    mock_get_forecast.return_value = ForecastResponse(
        location="London, GB",
        units="metric",
        forecast=[
            DailyForecast(
                date="2024-01-15",
                temperature=TemperatureRange(min=10.0, max=15.0, avg=12.5),
                description="light rain",
                condition="Rain",
                humidity=76,
                wind_speed=5.5,
                witty_message="Pack an umbrella unless you enjoy looking like a drowned rat",
            )
        ],
    )
    
    response = client.get("/api/v1/weather/forecast?city=London&country_code=GB")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "London, GB"
    assert "forecast" in data
    assert len(data["forecast"]) > 0
    assert "witty_message" in data["forecast"][0]