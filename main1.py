from src.core.graph import Graph
from src.parser import Parser
from src.core.simulation import Simulation
from src.core.pathfinderr import Pathfinderr
from src.core.pathfinder import Pathfinder
from ui.Visualiser import Visualizer

import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_map_file>")
        sys.exit(1)

    map_filepath = sys.argv[1]
    perser1 = Parser()
    try:
        list_of_nodes, list_of_conection, nb_drones = perser1.parse(
            map_filepath)
    except Exception as e:
        print(f"Error parsing the map: {e}")
        sys.exit(1)
    graph = Graph(list_of_nodes, list_of_conection)

    path_finder = Pathfinderr(graph)
    all_found_paths = path_finder.get_all_paths()
    simulation = Simulation(graph, all_found_paths)
    max_turn_needed, drones = simulation.simulation_try(nb_drones)
    path_finde = Pathfinder(graph)
    all_found_paths_2 = path_finde.get_all_paths()
    simulation_2 = Simulation(graph, all_found_paths_2)
    max_turn_neededd, droness = simulation_2.simulation_try(nb_drones)
    if max_turn_neededd < max_turn_needed:
        drones = droness
        max_turn_needed = max_turn_neededd
    simulation.print_turns(drones, max_turn_needed)
    viz = Visualizer(graph, drones, max_turn_needed)
    viz.run()


if __name__ == "__main__":
    main()
