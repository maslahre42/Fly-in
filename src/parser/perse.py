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
    # neighbors: list["Node"]



class Perse:
    def optional_part(self, meta_str: str) -> tuple[str, str, str]:
        node_color = "none"
        max_drones = "1"
        zone_type = "normal"
        parts: list[str] = meta_str.split(" ")
        for part in parts:
            if part.startswith("color="):
                temp = part.split("=")
                node_color = temp[1].strip()
            elif part.startswith("max_drones="):
                temp = part.split("=")
                max_drones = temp[1].strip()
            elif part.startswith("zone="):
                temp = part.split("=")
                zone_type = temp[1].strip()
        return node_color, max_drones, zone_type


    def perseing(self, filepath: str) -> tuple[list[Hub], int]:
        list_of_node: list[Hub] = []
        nb_drone = 0
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
                    node_color = "none"
                    max_drones = "1"
                    zone_type = "normal"
                    if "[" in node_name_not_ready and "]" in \
                            node_name_not_ready:
                        base_info, meta_info = node_name_not_ready.split(
                            "[", 1)
                        meta_string = meta_info.replace("]", "").strip()
                        node_color, max_drones, zone_type = self.optional_part(
                            meta_string)
                    else:
                        base_info = node_name_not_ready
                    node_name_parts = base_info.strip().split(" ")
                    nodename = node_name_parts[0].strip()
                    x = int(node_name_parts[1].strip())
                    y = int(node_name_parts[2].strip())
                    node = Hub(
                        name=nodename,
                        x=x,
                        y=y,
                        color=node_color,
                        max_drones=int(max_drones),
                        zone_type=ZoneType(zone_type),
                        is_start=True
                    )
                    list_of_node.append(node)
                elif clean_line.startswith("hub:"):
                    part = clean_line.split(":")
                    node_name_not_ready = part[1].strip()
                    node_color = "none"
                    max_drones = "1"
                    zone_type = "normal"
                    if "[" in node_name_not_ready and "]" in \
                            node_name_not_ready:
                        base_info, meta_info = node_name_not_ready.split(
                            "[", 1)
                        meta_string = meta_info.replace("]", "").strip()
                        node_color, max_drones, zone_type = self.optional_part(
                            meta_string)
                    else:
                        base_info = node_name_not_ready
                    node_name_parts = base_info.strip().split(" ")
                    nodename = node_name_parts[0].strip()
                    x = int(node_name_parts[1].strip())
                    y = int(node_name_parts[2].strip())
                    node = Hub(
                        name=nodename,
                        x=x,
                        y=y,
                        color=node_color,
                        max_drones=int(max_drones),
                        zone_type=ZoneType(zone_type),
                        is_start=False
                    )
                    list_of_node.append(node)
                elif clean_line.startswith("end_hub:"):
                    part = clean_line.split(":")
                    node_name_not_ready = part[1].strip()
                    node_color = "none"
                    max_drones = "1"
                    zone_type = "normal"
                    if "[" in node_name_not_ready and "]" in \
                            node_name_not_ready:
                        base_info, meta_info = node_name_not_ready.split(
                            "[", 1)
                        meta_string = meta_info.replace("]", "").strip()
                        node_color, max_drones, zone_type = self.optional_part(
                            meta_string)
                    else:
                        base_info = node_name_not_ready
                    node_name_parts = base_info.strip().split(" ")
                    nodename = node_name_parts[0].strip()
                    x = int(node_name_parts[1].strip())
                    y = int(node_name_parts[2].strip())
                    node = Hub(
                        name=nodename,
                        x=x,
                        y=y,
                        color=node_color,
                        max_drones=int(max_drones),
                        zone_type=ZoneType(zone_type),
                        is_end=True
                    )
                    list_of_node.append(node)
        return list_of_node, nb_drone
