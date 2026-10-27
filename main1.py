from src.core.graph import Graph
from src.parser import Parser
from src.core.simulation import Simulation
from src.core.pathfinderr import Pathfinderr
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
    max_turn_needed = simulation.simulation_try(nb_drones)
    viz = Visualizer(graph)
    viz.run()

if __name__ == "__main__":
    main()
