"""ZoneType enumeration representing the different types of zones in Fly-in."""
from enum import Enum


class ZoneType(str, Enum):
    """Enumeration of valid zone types for graph hubs."""

    normal = 'normal'
    restricted = 'restricted'
    priority = 'priority'
    blocked = 'blocked'
