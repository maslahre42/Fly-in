from pydantic import BaseModel, Field
from enum import Enum


class ZoneType(str, Enum):
    normal = 'normal'
    restricted = 'restricted'
    priority = 'priority'
    blocked = 'blocked'


class Node(BaseModel):
    name: str
    y: int = Field(ge=0)
    x: int = Field(ge=0)
    zone_type: ZoneType = Field(default=ZoneType.normal)
    max_drones: int = Field(default=1)
    color: str = "none"
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)
    # neighbors: list["Node"]



class Perse:
    def optional_part(self, str: str) -> tuple[str, str, str]:
        parts: list[str] = str.split(" ")
        for part in parts:
            if part.startswith("color="):
                temp = part.split("=")
                node_color = temp[1].strip()
            elif part.startswith("max_drones="):
                temp = part.split("=")
                max_drones = temp[1].strip()
            elif part.startswith("zone"):
                temp = part.split("=")
                zone_type = temp[1].strip()
        return node_color, max_drones, zone_type


    def perseing(self, filepath: str) -> None:
        list_of_node: list[Node] = []
        with open(filepath, "r") as file:
            for line in file:
                clean_line = line.split("#")[0].strip()
                if not clean_line:
                    continue
                if clean_line.startswith("nb_drones:"):
                    part = clean_line.split(":")
                    nb_drone_str = part[1].strip()
                    nb_drone = int(nb_drone_str)
                elif clean_line.startswith("start_hub:"):
                    part = clean_line.split(":")
                    node_name_not_ready = part[1].strip()
                    node_name_parts = node_name_not_ready.split(" ")
                    if node_name_parts[3].startswith("[") \
                            and node_name_parts[3].endswith("]"):
                        node_color, max_drones, zone_type = \
                                self.optional_part(node_name_parts[3][1:-1])
                    nodename = node_name_parts[0].strip()
                    x = int(node_name_parts[1].strip())
                    y = int(node_name_parts[2].strip())
                    node = Node(
                        name=nodename,
                        x=x,
                        y=y,
                        color=node_color,
                        max_drones=int(max_drones),
                        zone_type=zone_type,
                        is_start=True
                        )




