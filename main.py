"""Main entry point for Fly-in drone simulation and visualization."""
import sys
from src.core.graph import Graph
from src.parser import Parser
from src.core.simulation import Simulation
from src.core.pathfinder_1 import Pathfinder_1
from src.core.pathfinder import Pathfinder
from ui.Visualiser import Visualizer


def main() -> None:
    """Parse CLI arguments, run multi-solver simulation, and handle output."""
    run_visualizer = "--gui" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(args) != 1:
        print("Usage: python main.py <path_to_map_file> [--visualize]")
        sys.exit(1)

    map_filepath = args[0]
    parser = Parser()
    try:
        nodes, connections, nb_drones = parser.parse(map_filepath)
        graph = Graph(nodes, connections)
        path_finder_1 = Pathfinder_1(graph)
        paths_1 = path_finder_1.get_all_paths()
        sim_1 = Simulation(graph, paths_1)
        turns_1, drones_1 = sim_1.simulation_try(nb_drones)
        path_finder_2 = Pathfinder(graph)
        paths_2 = path_finder_2.get_all_paths()
        sim_2 = Simulation(graph, paths_2)
        turns_2, drones_2 = sim_2.simulation_try(nb_drones)

        if turns_2 < turns_1:
            best_simulation = sim_2
            best_drones = drones_2
            best_turns = turns_2
        else:
            best_simulation = sim_1
            best_drones = drones_1
            best_turns = turns_1

        best_simulation.print_turns(best_drones, best_turns)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if run_visualizer:
        viz = Visualizer(graph, best_drones, best_turns)
        viz.run()


if __name__ == "__main__":
    main()
