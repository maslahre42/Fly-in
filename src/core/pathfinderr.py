from src.core.graph import Graph
from collections import deque
from model.ZoneType import ZoneType


class pathfinderr:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.remaining_node_caps: dict[str, int] = {}
        for name, hub in graph.hubs.items():
            if name == graph.start_hub or name == graph.end_hub:
                self.remaining_node_caps[name] = 2000000
            else:
                self.remaining_node_caps[name] = hub.max_drones
        self.remaining_link_caps: dict[
            tuple[str, str], int] = dict(graph.connections_capacities)

    def _solve_bfs(self) -> list[tuple[str, int]]:
        start_hub = self.graph.start_hub
        end_hub = self.graph.end_hub
        if start_hub == end_hub:
            return [(start_hub, self.graph.get_node_capacity(start_hub))]
        path: list[tuple[str, int]] = []
        queue_priority: deque[tuple[str, list[tuple[str, int]]]] = deque(
            [(start_hub, [
                (start_hub, self.graph.get_node_capacity(start_hub))])])
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
                link_cap = self.remaining_link_caps.get((hub, neighbor), 0)
                node_cap = self.remaining_node_caps.get(neighbor, 0)
                if neighbor not in visited and link_cap > 0 and node_cap > 0:
                    new_path = path + [(neighbor, node_cap)]
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

    def calculate_the_capacity(
            self, path: list[tuple[str, int]]) -> tuple[int, int]:
        count_of_restricted_hubs = 0
        minimum = 2000000
        for i in range(len(path) - 1):
            hub, cap = path[i]
            next_hub, next_cap = path[i+1]
            connection_cap = self.remaining_link_caps.get((hub, next_hub), 0)
            minimum = min(minimum, cap, next_cap, connection_cap)
            hubtypee = self.graph.get_hub_type(hub)
            if hubtypee == ZoneType.restricted:
                count_of_restricted_hubs += 1
        result_turns = (len(path) - 1) + count_of_restricted_hubs
        return result_turns, int(minimum)

    def graph_updeter(
            self, path: list[tuple[str, int]], bottleneck: int) -> None:
        for i in range(len(path) - 1):
            u = path[i][0]
            v = path[i+1][0]
            self.remaining_link_caps[(u, v)] -= bottleneck
            self.remaining_link_caps[(v, u)] -= bottleneck
        for hub, _ in path:
            if hub != self.graph.start_hub and hub != self.graph.end_hub:
                self.remaining_node_caps[hub] -= bottleneck

    def get_all_paths(self) -> list[dict]:
        all_found_paths = []
        while True:
            path_tuples = self._solve_bfs()
            if not path_tuples:
                break
            turns, bottleneck = self.calculate_the_capacity(path_tuples)
            if bottleneck == 0:
                break
            clean_path = [hub for hub, _ in path_tuples]
            all_found_paths.append({
                "path": clean_path,
                "turns": turns,
                "throughput": bottleneck
            })
            self.graph_updeter(path_tuples, bottleneck)
        return all_found_paths
