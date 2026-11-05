"""Data model representing a bidirectional connection between hubs."""
from pydantic import BaseModel, Field


class Connection(BaseModel):
    """Represents an edge linking two hubs with an associated capacity."""

    from_hub: str
    to_hub: str
    max_link_capacity: int = Field(default=1, gt=0)
