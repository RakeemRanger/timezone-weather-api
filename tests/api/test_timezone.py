"""Tests for timezone endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_get_timezone_info_success(client: TestClient):
    """Test successful timezone info retrieval."""
    response = client.get("/api/v1/timezone/America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"
    assert "current_time" in data
    assert "utc_offset" in data
    assert "is_dst" in data
    assert "abbreviation" in data


def test_get_timezone_info_invalid_timezone(client: TestClient):
    """Test timezone info with invalid timezone."""
    response = client.get("/api/v1/timezone/Invalid/Timezone")
    assert response.status_code == 400
    assert "detail" in response.json()


def test_get_timezone_info_europe(client: TestClient):
    """Test timezone info for European timezone."""
    response = client.get("/api/v1/timezone/Europe/London")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "Europe/London"


def test_get_timezone_info_asia(client: TestClient):
    """Test timezone info for Asian timezone."""
    response = client.get("/api/v1/timezone/Asia/Tokyo")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "Asia/Tokyo"