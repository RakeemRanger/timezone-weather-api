"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_weather_response():
    """Mock OpenWeatherMap current weather response."""
    return {
        "coord": {"lon": -0.1257, "lat": 51.5085},
        "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
        "main": {
            "temp": 12.5,
            "feels_like": 10.2,
            "temp_min": 11.0,
            "temp_max": 14.0,
            "pressure": 1013,
            "humidity": 76,
        },
        "wind": {"speed": 5.5, "deg": 230},
        "dt": 1642262400,
        "sys": {"country": "GB"},
        "name": "London",
    }


@pytest.fixture
def mock_forecast_response():
    """Mock OpenWeatherMap forecast response."""
    return {
        "city": {"name": "London", "country": "GB"},
        "list": [
            {
                "dt": 1642262400,
                "main": {
                    "temp": 12.5,
                    "feels_like": 10.2,
                    "humidity": 76,
                },
                "weather": [{"main": "Rain", "description": "light rain"}],
                "wind": {"speed": 5.5},
            },
            {
                "dt": 1642348800,
                "main": {
                    "temp": 15.0,
                    "feels_like": 13.5,
                    "humidity": 70,
                },
                "weather": [{"main": "Clear", "description": "clear sky"}],
                "wind": {"speed": 3.2},
            },
        ],
    }