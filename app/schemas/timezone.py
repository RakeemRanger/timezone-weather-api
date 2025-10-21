"""Timezone data schemas."""
from pydantic import BaseModel, Field


class TimezoneResponse(BaseModel):
    """Response for timezone information."""

    timezone: str = Field(..., description="Timezone name")
    current_time: str = Field(..., description="Current time in ISO format")
    utc_offset: str = Field(..., description="UTC offset (e.g., '+05:30', '-08:00')")
    is_dst: bool = Field(..., description="Whether daylight saving time is active")
    abbreviation: str = Field(..., description="Timezone abbreviation (e.g., 'EST', 'PST')")

    class Config:
        json_schema_extra = {
            "example": {
                "timezone": "America/New_York",
                "current_time": "2024-01-15T10:30:00-05:00",
                "utc_offset": "-05:00",
                "is_dst": False,
                "abbreviation": "EST",
            }
        }