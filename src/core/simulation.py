from src.core.pathfinderr import pathfinderr
from src.core.graph import Graph


class Dron:
    def __init__(self, dron_id: int, path: list[str]):
        self.id_dron = dron_id
        self.path = path

    def location(self, current_turn: int):
        print(f"dron_id = {self.id_dron} now in {self.path[current_turn + 1]}")



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
        turn = 1
        dron_count = 1
        while dron_count < numberof_drons:
            for row in list_of_batches:
                if row["start_turn"] == turn:
                    for _ in range(row["drones_in_this_batch"]):
                        dron = Dron(dron_id=dron_count, path=row["path"])
                        dron_count += 1
                        list_of_drons.append(dron)
                else:
                    break
            turn += 1
        i = 1
        while i < turn:
            for dron in list_of_drons:
                dron.location(i)


