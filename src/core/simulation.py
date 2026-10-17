from src.core.pathfinderr import pathfinderr
from src.core.graph import Graph


class Simulation:
    def __init__(self, graph: Graph, all_pathes: list[dict]) -> None:
        self.graph = graph
        self.all_paths = all_pathes

    def _assign_drones_to_paths(self, number_of_drons: int) -> list[dict]:
        list_of_batches: list[dict] = []
        path_trackers = [
            {
                "path_id": idx,
                "path": p["path"],
                "start_turn": 1,
                "throughput": p["throughput"],
                "current_arrival_turn": p["turns"]
            }
            for idx, p in enumerate(self.all_paths)
        ]
        while number_of_drons > 0:
            path_trackers.sort(key=lambda x: x["current_arrival_turn"])
            best_path = path_trackers[0]
            drones_to_send = min(best_path["throughput"], number_of_drons)
            list_of_batches.append({
                "path_id": best_path["path_id"],
                "start_turn": best_path["sart_turn"],
                "path": best_path["path"],
                "drones_in_this_batch": drones_to_send,
                "arrival_turn": best_path["current_arrival_turn"]
            })
            number_of_drons -= drones_to_send
            best_path["current_arrival_turn"] += 1
            best_path["sart_turn"] += 1
        return list_of_batches
