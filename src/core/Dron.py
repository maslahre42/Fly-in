"""Drone simulation entity managing path execution and transit state."""
from src.core.graph import Graph
from src.model.ZoneType import ZoneType


class Dron:
    """Represents an autonomous drone with an assigned route and start turn."""

    def __init__(
            self, dron_id: int,
            path: list[str],
            start_turn: int,
            graph: Graph) -> None:
        """Initialize drone with identifier, route path, turn, and graph."""
        self.id_dron = dron_id
        self.path = path
        self.start_turn = start_turn
        self.graph = graph
        self._helper_for_restricted(graph)

    def _helper_for_restricted(self, graph: Graph) -> None:
        """Insert intermediate connection hops for restricted zone transit."""
        new_path = []
        new_path.append(self.path[0])
        for i in range(len(self.path) - 1):
            hub = self.path[i]
            next_hub = self.path[i+1]
            hub_type = graph.get_hub_type(next_hub)
            if hub_type == ZoneType.restricted:
                new_path.append(f"{hub}-{next_hub}")
            new_path.append(next_hub)
        self.path = new_path

    def location(self, current_turn: int) -> str:
        """Return formatted location string for the current simulation turn."""
        if current_turn < self.start_turn:
            return self.graph.start_hub
        steps_done = current_turn - self.start_turn + 1
        if steps_done >= len(self.path):
            return self.graph.end_hub
        return (f"D{self.id_dron}-{self.path[steps_done]}")
