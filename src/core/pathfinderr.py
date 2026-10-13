from src.core.graph import Graph
from collections import deque
from model.ZoneType import ZoneType


class pathfinderr:
    def __init__(self, graph: Graph):
        self.graph = graph

    def _solve_bfs(self) -> list[tuple[str, int]]:
        start_hub = self.graph.start_hub
        end_hub = self.graph.end_hub
        if start_hub == end_hub:
            return [(start_hub, self.graph.get_node_capacity(start_hub))]
        path: list[tuple[str, int]] = []
        queue_priority: deque[tuple[str, list[tuple[str, int]]]] = deque(
            [(start_hub, [(start_hub, self.graph.get_node_capacity(start_hub))])])
        queue_normal: deque[tuple[str, list[tuple[str, int]]]] = deque()
        queue_restricted: deque[tuple[str, list[tuple[str, int]]]] = deque()
        visited: set[str] = {start_hub}
        while queue_priority or queue_normal or queue_restricted:
            if queue_priority:
                hub, path = queue_priority.popleft()
            elif queue_normal:
                hub, path = queue_normal.popleft()
            else:
                hub, path = queue_restricted.popleft()
            for neighbor in self.graph.get_neighbors(hub):
                if neighbor not in visited:
                    new_path = path + [(neighbor, self.graph.get_node_capacity(neighbor))]
                    if neighbor == end_hub:
                        return new_path
                    visited.add(neighbor)
                    zone_type = self.graph.get_hub_type(neighbor)
                    if zone_type == ZoneType.priority:
                        queue_priority.append((neighbor, new_path))
                    elif zone_type == ZoneType.normal:
                        queue_normal.append((neighbor, new_path))
                    elif zone_type == ZoneType.restricted:
                        queue_restricted.append((neighbor, new_path))
        return []
