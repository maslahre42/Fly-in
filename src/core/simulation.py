from src.core.graph import Graph
from src.model.ZoneType import ZoneType


class Dron:
    def __init__(self, dron_id: int, path: list[str], start_turn: int, graph: Graph) -> None:
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

    def simulation_try(self, numberof_drons: int):
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
