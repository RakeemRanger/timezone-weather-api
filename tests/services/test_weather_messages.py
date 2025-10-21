"""Tests for weather message generator."""
import pytest

from app.services.weather_messages import get_witty_message


def test_get_witty_message_rain():
    """Test witty message for rainy weather."""
    message = get_witty_message("Rain", 15.0, 5.0, "metric")
    assert isinstance(message, str)
    assert len(message) > 0


def test_get_witty_message_clear():
    """Test witty message for clear weather."""
    message = get_witty_message("Clear", 20.0, 3.0, "metric")
    assert isinstance(message, str)
    assert len(message) > 0


def test_get_witty_message_snow():
    """Test witty message for snowy weather."""
    message = get_witty_message("Snow", -5.0, 8.0, "metric")
    assert isinstance(message, str)
    assert len(message) > 0


def test_get_witty_message_hot_metric():
    """Test witty message for hot weather (metric)."""
    message = get_witty_message("Clear", 35.0, 2.0, "metric")
    assert isinstance(message, str)
    # Should get a hot weather message


def test_get_witty_message_hot_imperial():
    """Test witty message for hot weather (imperial)."""
    message = get_witty_message("Clear", 95.0, 2.0, "imperial")
    assert isinstance(message, str)


def test_get_witty_message_cold_metric():
    """Test witty message for cold weather (metric)."""
    message = get_witty_message("Clear", 0.0, 3.0, "metric")
    assert isinstance(message, str)


def test_get_witty_message_cold_imperial():
    """Test witty message for cold weather (imperial)."""
    message = get_witty_message("Clear", 32.0, 3.0, "imperial")
    assert isinstance(message, str)


def test_get_witty_message_windy_metric():
    """Test witty message for windy weather (metric)."""
    message = get_witty_message("Clear", 15.0, 15.0, "metric")
    assert isinstance(message, str)


def test_get_witty_message_windy_imperial():
    """Test witty message for windy weather (imperial)."""
    message = get_witty_message("Clear", 60.0, 25.0, "imperial")
    assert isinstance(message, str)


def test_get_witty_message_thunderstorm():
    """Test witty message for thunderstorm."""
    message = get_witty_message("Thunderstorm", 18.0, 6.0, "metric")
    assert isinstance(message, str)


def test_get_witty_message_clouds():
    """Test witty message for cloudy weather."""
    message = get_witty_message("Clouds", 16.0, 4.0, "metric")
    assert isinstance(message, str)