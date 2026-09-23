from pydantic import BaseModel, Field
from enum import Enum


class ZoneType(str, Enum):
    normal = 'normal'
    restricted = 'restricted'
    priority = 'priority'
    blocked = 'blocked'


class Hub(BaseModel):
    name: str
    x: int
    y: int
    zone_type: ZoneType = Field(default=ZoneType.normal)
    max_drones: int = Field(default=1, gt=0)
    color: str = "none"
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    max_link_capacity: int = Field(default=1, gt=0)


class Parser:
    def _parse_optional_part(self, optional_info: str) -> dict:
        """Parses the metadata brackets and returns a dict of kwargs."""
        kwargs = {}
        for part in optional_info.split():
            if "=" in part:
                key, value = part.split("=", 1)
                key, value = key.strip(), value.strip()
                if key == "color":
                    kwargs["color"] = value
                elif key == "max_drones":
                    kwargs["max_drones"] = int(value)
                elif key == "zone":
                    kwargs["zone_type"] = ZoneType(value)
        return kwargs

    def _parse_hub_line(self, line_data: str, **flags) -> Hub:
        """Shared logic to create a Hub from a data string."""
        kwargs = {}
        if "[" in line_data and "]" in line_data:
            base_info, meta_info = line_data.split("[", 1)
            meta_string = meta_info.replace("]", "").strip()
            kwargs = self._parse_optional_part(meta_string)
        else:
            base_info = line_data
        parts = base_info.strip().split()
        return Hub(
            name=parts[0].strip(),
            x=int(parts[1].strip()),
            y=int(parts[2].strip()),
            **kwargs,
            **flags
        )

    def parse(self, filepath: str) -> tuple[list[Hub], int]:
        list_of_nodes: list[Hub] = []
        nb_drones = 0
        with open(filepath, "r") as file:
            for line in file:
                clean_line = line.split("#")[0].strip()
                if not clean_line:
                    continue
                if clean_line.startswith("nb_drones:"):
                    nb_drones = int(clean_line.split(":", 1)[1].strip())
                elif clean_line.startswith("start_hub:"):
                    hub_data = clean_line.split(":", 1)[1].strip()
                    list_of_nodes.append(self._parse_hub_line(
                        hub_data, is_start=True))
                elif clean_line.startswith("hub:"):
                    hub_data = clean_line.split(":", 1)[1].strip()
                    list_of_nodes.append(self._parse_hub_line(hub_data))
                elif clean_line.startswith("end_hub:"):
                    hub_data = clean_line.split(":", 1)[1].strip()
                    list_of_nodes.append(self._parse_hub_line(
                        hub_data, is_end=True))
        return list_of_nodes, nb_drones