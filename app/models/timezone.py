"""Timezone data models."""
from typing import List
from pydantic import BaseModel, Field


class TimezoneInfo(BaseModel):
    """Information for a single timezone."""

    timezone: str = Field(..., description="Timezone identifier")
    current_time: str = Field(..., description="Current time in ISO format")
    utc_offset: str = Field(..., description="UTC offset (e.g., '+0100')")
    timezone_abbreviation: str = Field(..., description="Timezone abbreviation (e.g., 'EST')")


class TimezoneResponse(BaseModel):
    """Response containing multiple timezones."""

    timezones: List[TimezoneInfo] = Field(..., description="List of timezone information")