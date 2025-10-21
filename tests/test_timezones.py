"""Tests for timezone endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_timezones():
    """Test getting all timezones."""
    response = client.get("/api/timezones")
    assert response.status_code == 200
    data = response.json()
    assert "timezones" in data
    assert len(data["timezones"]) > 0
    assert "timezone" in data["timezones"][0]
    assert "current_time" in data["timezones"][0]


def test_get_specific_timezone():
    """Test getting a specific timezone."""
    response = client.get("/api/timezones/America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"
    assert "current_time" in data


def test_get_invalid_timezone():
    """Test getting an invalid timezone."""
    response = client.get("/api/timezones/Invalid/Timezone")
    assert response.status_code == 404