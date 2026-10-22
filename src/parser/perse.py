from typing import Any
from src.model.ZoneType import ZoneType
from src.model.Connection import Connection
from src.model.Hub import Hub


class Parser:
    def __init__(self):
        pass

    def _parse_optional_part(self, optional_info: str) -> dict:
        """Parses the metadata brackets and returns a dict of kwargs."""
        kwargs: dict[str, Any] = {}
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
                else:
                    raise ValueError(
                        f"unknowen metadata '{key}'"
                    )
            else:
                raise ValueError(
                    f"in no '=' in '{part}'"
                )
        return kwargs

    def _parse_hub_line(
            self, line_data: str, line_number: int, **flags) -> Hub:
        """Shared logic to create a Hub from a data string."""
        kwargs: dict[str, Any] = {}
        if "[" in line_data and "]" in line_data:
            base_info, meta_info = line_data.split("[", 1)
            meta_string = meta_info.replace("]", "").strip()
            kwargs = self._parse_optional_part(meta_string)
        else:
            base_info = line_data
        parts = base_info.strip().split()
        if len(parts) != 3:
            raise ValueError(
                f"Parse Error on '{base_info}': Expected exactly 3 parts "
                f"(name, x, y). Ensure coordinates are present and the name"
                f" contains NO spaces."
            )
        name = parts[0].strip()
        if "-" in name:
            raise ValueError(f"Parse Error: Hub name "
                             f"'{name}' contains a dash.")
        try:
            return Hub(
                name=name,
                x=int(parts[1]),
                y=int(parts[2]),
                **kwargs,
                **flags
            )
        except Exception as ex:
            raise ValueError(f"line: {line_number}  hub_name:{name}\n {ex}")

    def _conection_lines_sep(self, line: str) -> Connection:
        capacity_str = "1"
        if "[" in line and "]" in line:
            base_info, meta_info = line.split("[", 1)
            meta_string = meta_info.replace("]", "").strip()
            if "max_link_capacity=" in meta_string:
                capacity_str = meta_string.split("=")[1].strip()
            elif meta_string:
                raise ValueError(f"unknown {meta_string}!")
        else:
            base_info = line
        from_hub, to_hub = base_info.strip().split("-")
        if from_hub == to_hub:
            raise ValueError("error self connection!")
        try:
            return Connection(
                from_hub=from_hub.strip(),
                to_hub=to_hub.strip(),
                max_link_capacity=int(capacity_str)
            )
        except Exception as ex:
            raise ValueError(
                f"error in connection, {ex}"
            )

    def parse(self, filepath: str) -> tuple[list[Hub], list[Connection], int]:
        list_of_nodes: list[Hub] = []
        list_of_conection: list[Connection] = []
        nb_drones = 0
        nb_drones_bool = 0
        seen_hubs = set()
        seen_connections = set()
        stup_check_start = False
        stup_check_end = False
        line_number = 0
        j = 0
        try:
            with open(filepath, "r") as file:
                for line in file:
                    clean_line = line.split("#")[0].strip()
                    line_number += 1
                    if not clean_line:
                        continue
                    j += 1
                    if j == 1:
                        if clean_line.startswith("nb_drones:"):
                            nb_drones_bool += 1
                            try:
                                nb_drones = int(
                                    clean_line.split(":", 1)[1].strip())
                            except Exception as ex:
                                raise ValueError(
                                    f"in {line_number} ,{ex}"
                                )
                            if nb_drones < 1:
                                raise ValueError(
                                    "the number of drons should be "
                                    f">= 1not{nb_drones}in line {line_number}")
                        else:
                            raise ValueError(
                                f"number of drons is not in the first line"
                                f" in {line_number}")
                    elif j != 1 and clean_line.startswith("nb_drones:"):
                        raise ValueError(
                                f"number of drons is repeted in {line_number}")
                    elif clean_line.startswith("start_hub:"):
                        if stup_check_start:
                            raise ValueError(
                                f"error, we already had start hub! line"
                                f" {line_number}")
                        stup_check_start = True
                        hub_data = clean_line.split(":", 1)[1].strip()
                        new_hub = self._parse_hub_line(
                            hub_data, line_number=line_number, is_start=True)
                        if new_hub.name in seen_hubs:
                            raise ValueError(
                                f"Parse Error: Duplicate hub name "
                                f"'{new_hub.name}' detected. "
                                f"in line {line_number}")
                        seen_hubs.add(new_hub.name)
                        list_of_nodes.append(new_hub)
                    elif clean_line.startswith("hub"):
                        if ":" not in clean_line:
                            raise ValueError(
                                f"missing : in hub decleration in line:"
                                f" {line_number} it should be 'hub:name, x, y'"
                            )
                        hub_data = clean_line.split(":", 1)[1].strip()
                        new_hub = self._parse_hub_line(
                            hub_data, line_number=line_number)
                        if new_hub.name in seen_hubs:
                            raise ValueError(
                                f"Parse Error: Duplicate hub name "
                                f"'{new_hub.name}' detected in line:"
                                f" {line_number} ")
                        seen_hubs.add(new_hub.name)
                        list_of_nodes.append(new_hub)
                    elif clean_line.startswith("end_hub:"):
                        if stup_check_end:
                            raise ValueError(
                                f"error, we already had end hub! in line"
                                f" {line_number}")
                        stup_check_end = True
                        hub_data = clean_line.split(":", 1)[1].strip()
                        new_hub = self._parse_hub_line(
                            hub_data, line_number, is_end=True)
                        if new_hub.name in seen_hubs:
                            raise ValueError(
                                f"Parse Error: Duplicate hub name "
                                f"'{new_hub.name}' detected in line"
                                f" {line_number} ")
                        seen_hubs.add(new_hub.name)
                        list_of_nodes.append(new_hub)
                    elif clean_line.startswith("connection"):
                        connection_data = clean_line.split(":", 1)[1].strip()
                        new_connection = self._conection_lines_sep(
                            connection_data
                        )
                        connection_pair = tuple(
                            sorted([
                                new_connection.from_hub,
                                new_connection.to_hub
                            ]))
                        if (new_connection.from_hub not in seen_hubs):
                            raise ValueError(
                                f"Parse Error: {new_connection.from_hub} is "
                                f"not define! in line {line_number} "
                            )
                        if (new_connection.to_hub not in seen_hubs):
                            raise ValueError(
                                f"Parse Error: {new_connection.to_hub} is "
                                f"not define! in line {line_number} "
                            )
                        if connection_pair in seen_connections:
                            raise ValueError(
                                f"Parse Error: Duplicate connection between "
                                f"{connection_pair[0]} and "
                                f"{connection_pair[1]} in line {line_number}")
                        seen_connections.add(connection_pair)
                        list_of_conection.append(new_connection)
                    else:
                        raise ValueError(
                            f"Unknown key in{clean_line}in line {line_number} "
                        )
            if nb_drones_bool != 1:
                raise ValueError(
                    f"number of the drons are missing or "
                    f"it is written mor than one time{nb_drones_bool}")
        except Exception as ex:
            str_number = str(line_number)
            errormessage = str(ex)
            if str_number in errormessage:
                raise ValueError(f"parsing error {ex}")
            else:
                raise ValueError(f"parsing error {ex} in line {line_number}")
        return list_of_nodes, list_of_conection, nb_drones
