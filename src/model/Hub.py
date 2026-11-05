"""Data model representing a zone/hub in the graph network."""
from pydantic import BaseModel, Field, field_validator
from src.model.ZoneType import ZoneType


class Hub(BaseModel):
    """Represents a node/hub in the drone transit graph."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = Field(default=ZoneType.normal)
    max_drones: int = Field(default=1, gt=0)
    color: str = "none"
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)

    @field_validator('name')
    @staticmethod
    def validate_name(value: str) -> str:
        """Validate that hub names contain no dashes or spaces."""
        if "-" in value or " " in value:
            raise ValueError(f"Invalid name '{value}'")
        return value

    @field_validator('zone_type')
    @staticmethod
    def validate_zonetype(value: str) -> str:
        """Validate that the zone type is one of the supported types."""
        if value in ("normal", "restricted", "priority", "blocked"):
            return value
        raise ValueError(f"Invalid name '{value}'")
