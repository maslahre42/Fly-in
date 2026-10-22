from src.core.graph import Graph
from src.core.Dron import Dron


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
                "current_arrival_turn": p["cost_turns"]
            }
            for idx, p in enumerate(self.all_paths)
        ]
        if not path_trackers:
            raise ValueError("No valid path found from start to goal.")
        while number_of_drons > 0:
            path_trackers.sort(key=lambda x: x["current_arrival_turn"])
            best_path = path_trackers[0]
            drones_to_send = min(best_path["throughput"], number_of_drons)
            list_of_batches.append({
                "path_id": best_path["path_id"],
                "start_turn": best_path["start_turn"],
                "path": best_path["path"],
                "drones_in_this_batch": drones_to_send,
                "arrival_turn": best_path["current_arrival_turn"]
            })
            number_of_drons -= drones_to_send
            best_path["current_arrival_turn"] += 1
            best_path["start_turn"] += 1
        list_of_batches.sort(key=lambda x: (x["start_turn"], x["path_id"]))
        return list_of_batches

    def simulation_try(self, numberof_drons: int) -> int:
        list_of_batches = self._assign_drones_to_paths(numberof_drons)
        list_of_drons: list[Dron] = []
        dron_count = 1
        max_turn_needed = 0
        for row in list_of_batches:
            for _ in range(row["drones_in_this_batch"]):
                dron = Dron(
                    dron_id=dron_count,
                    path=row["path"],
                    start_turn=row["start_turn"],
                    graph=self.graph)
                list_of_drons.append(dron)
                dron_count += 1
                if row["arrival_turn"] > max_turn_needed:
                    max_turn_needed = row["arrival_turn"]
        for current_turn in range(1, max_turn_needed + 1):
            turn_moves = []
            for dron in list_of_drons:
                loc = dron.location(current_turn)
                if loc:
                    turn_moves.append(loc)
            if turn_moves:
                print(" ".join(turn_moves))
        return max_turn_needed
