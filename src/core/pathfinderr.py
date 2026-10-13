from src.core.graph import Graph
from collections import deque


def solve_bfs(graph: Graph) -> list:
    start_hub = graph.start_hub
    end_hub = graph.end_hub
    if start_hub == end_hub:
        return [start_hub]
    path: list[str] = []
    queue: deque[tuple[str, list[str]]] = deque([(start_hub, [start_hub])])
    visited: set[str] = {start_hub}
    graph.get_neighbors(start_hub)
    while queue:
        hub, path = queue.popleft()
        for neighbor in graph.get_neighbors(hub):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end_hub:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return []
