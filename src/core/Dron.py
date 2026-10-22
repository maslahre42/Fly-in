from src.core.graph import Graph
from src.model.ZoneType import ZoneType


class Dron:
    def __init__(
            self, dron_id: int,
            path: list[str],
            start_turn: int,
            graph: Graph) -> None:
        self.id_dron = dron_id
        self.path = path
        self.start_turn = start_turn
        self._helper_for_restricted(graph)

    def _helper_for_restricted(self, graph: Graph):
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

    def location(self, current_turn: int) -> str | None:
        if current_turn < self.start_turn:
            return None
        steps_done = current_turn - self.start_turn + 1
        if steps_done >= len(self.path):
            return None
        return (f"D{self.id_dron}-{self.path[steps_done]}")
