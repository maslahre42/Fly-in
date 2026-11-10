*This project has been created as part of the 42 curriculum by malshare.*

# Fly-in: Drone Traffic Simulation

Fly-in is a turn-based drone simulation and pathfinding project. Given a map of hubs and connections with capacity limits, the program finds safe flight plans to move all drones from the start hub to the end hub in the smallest number of turns.

---

## Table of Contents

1. [Description](#description)
2. [Instructions](#instructions)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Simulation](#running-the-simulation)
   - [Interactive Visualizer](#interactive-visualizer)
   - [Debugging](#debugging)
   - [Linting and Type Checking](#linting-and-type-checking)
   - [Cleaning Up](#cleaning-up)
3. [Algorithm Explanation](#algorithm-explanation)
   - [Network Structure](#network-structure)
   - [Dual-Solver Strategy](#dual-solver-strategy)
   - [Special Zone Types](#special-zone-types)
   - [Updating Remaining Capacities](#updating-remaining-capacities)
   - [Turn Scheduling](#turn-scheduling)
   - [Safety Rules](#safety-rules)
4. [Visual Representation](#visual-representation)
   - [Features and Controls](#features-and-controls)
   - [Color Scheme](#color-scheme)
5. [Example Input and Expected Output](#example-input-and-expected-output)
   - [Sample Map File](#sample-map-file)
   - [Simulation Output](#simulation-output)
   - [Turn-by-Turn Breakdown](#turn-by-turn-breakdown)
6. [Benchmark and Test Results](#benchmark-and-test-results)
7. [Resources and AI Usage](#resources-and-ai-usage)

---

## Description

Fly-in models a drone flight network using a graph that runs turn by turn:

- **Hubs (Nodes)**: Locations with $(x, y)$ coordinates and a limit on how many drones can be there at the same time (`max_drones`).
- **Connections (Edges)**: Two-way flight links between hubs with a limit on how many drones can use the link at the same time (`max_capacity`).
- **Drones**: Units with unique IDs ($D1, D2, \dots, DN$) that travel from `start_hub` to `end_hub`.
- **Zone Types**:
  - `start_hub` & `end_hub`: Unlimited capacity. Any number of drones can start or arrive at the same time.
  - `priority`: Priority hub with a set drone capacity. Paths through these zones are preferred first.
  - `normal`: Standard hub with a set drone capacity.
  - `restricted`: Restricted hub that takes **2 turns** to enter and pass (1 turn waiting on the connection before moving into the hub).
  - `blocked`: Closed zone. Drones can never enter or fly through it.

The main goal is to send as many drones as possible through the network in the fewest turns without breaking any hub or connection capacity limits.

---

## Instructions

### Prerequisites

- **Python**: Version 3.10 or higher.
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `python3 -m venv` / `pip`.
- **Make**: GNU `make`.

### Installation

Clone the repository and install the required packages:

```bash
git clone <repository_url> Fly-in
cd Fly-in
make install
```

Or run `uv` directly:

```bash
uv sync
```

### Running the Simulation

Run the simulation on any valid map file:

```bash
# Using Python directly
python3 main.py maps/basic/01_linear_path.txt

# Or using uv run
uv run main.py maps/challenger/01_the_impossible_dream.txt

# Or using the Makefile (defaults to the challenger map)
make run MAP=maps/advanced/01_maze_nightmare.txt
```

### Interactive Visualizer

Open the Pygame window by adding the `--gui` flag:

```bash
python3 main.py maps/challenger/01_the_impossible_dream.txt --gui

# Or using the Makefile
make run MAP=maps/challenger/01_the_impossible_dream.txt ARGS=--gui
```

### Debugging

Run the program with Python's built-in debugger (`pdb`):

```bash
make debug MAP=maps/basic/01_linear_path.txt
```

### Linting and Type Checking

Check code style (PEP 8) and type hints:

```bash
# Standard checks (Flake8 and mypy)
make lint

# Strict type checking
make lint-strict
```

### Cleaning Up

Remove cache files and the virtual environment (`__pycache__`, `.pyc`, `.mypy_cache`, `.pytest_cache`, `.venv`):

```bash
make clean
```

---

## Algorithm Explanation

### Network Structure

The graph is built from validated data models:
- `Hub`: Stores the hub name, coordinates, zone type (`ZoneType`), maximum drone capacity, and optional display color.
- `Connection`: Stores pairs of connected hubs and the link capacity.
- `Graph`: Holds the adjacency lists, neighbor lookups, and link capacities.

```text
+-----------+            Capacity: C             +-----------+
|  Hub A    | <================================> |  Hub B    |
| (Cap: Ma) |           (Two-way Link)           | (Cap: Mb) |
+-----------+                                    +-----------+
```

### Dual-Solver Strategy

Different maps have different layouts. Some maps have tight link limits, while others have priority or restricted zones. Because of this, Fly-in runs two pathfinding solvers and picks the better plan:

1. **Solver 1 (`Pathfinder_1` - Multi-Queue Priority BFS)**:
   - Uses 3 separate queues: `priority`, `normal`, and `restricted`.
   - Explores `priority` hubs first, then `normal` hubs, and finally `restricted` hubs.
   - Helps drones find fast paths early when priority zones are present.

2. **Solver 2 (`Pathfinder` - Standard BFS)**:
   - Uses a standard shortest-path BFS across the graph.
   - Focuses on finding the shortest hops and maximizing path capacity.

Both solvers collect a full set of usable paths. The simulation tests both plans and chooses the one that finishes in the **fewest total turns**.

### Special Zone Types

1. **Blocked Zones (`ZoneType.blocked`)**:
   - The pathfinder skips any neighbor marked as `blocked` while searching.
   - Drones will never enter a blocked zone.

2. **Restricted Zones (`ZoneType.restricted`)**:
   - Moving into a restricted hub adds 1 extra turn to the path cost:
     $$\text{Transit Cost} = \text{link steps} + \text{number of restricted hubs on the path}$$
   - The `Dron` class adds an intermediate link step (`hub-next_hub`) before the restricted hub, so the drone spends 1 turn on the connection before moving into the hub.

### Updating Remaining Capacities

Each time a valid path $P = (h_0, h_1, \dots, h_k)$ is found:
1. We find the bottleneck capacity $B$ (the smallest capacity along the path):
   $$B = \min \Big( \min_{i} \text{LinkCap}(h_i, h_{i+1}), \min_{i \in (1..k-1)} \text{NodeCap}(h_i) \Big)$$
2. We subtract $B$ from the remaining capacity of every connection $(h_i, h_{i+1})$ and $(h_{i+1}, h_i)$ along the path.
3. We subtract $B$ from the remaining capacity of each middle hub $h_i$ (excluding `start_hub` and `end_hub`).
4. BFS repeats until no more paths with $B > 0$ exist from `start_hub` to `end_hub`.

### Turn Scheduling

Once all paths, their turn costs ($C_p$), and their bottlenecks ($B_p$) are found:
- The scheduler tracks when drones on each path would finish:
  $$\text{Arrival Turn} = \text{Start Turn} + C_p - 1$$
- In each round, it picks the path with the earliest arrival turn.
- Up to $B_p$ drones are sent on that path starting at `start_turn`.
- That path's `start_turn` and next arrival turn then increase by 1, and this repeats until every drone is scheduled.

### Safety Rules

The simulation guarantees four main rules:
1. **Connection Limit**: On any turn $t$, the number of drones using a connection $(u, v)$ never goes above its `max_capacity`.
2. **Hub Limit**: On any turn $t$, the number of drones inside hub $u$ never goes above its `max_drones`.
3. **Restricted Zone Rule**: Drones always spend 1 wait turn on the connection before entering a restricted zone, matching the 2-turn movement rule.
4. **Every Drone Arrives**: Every drone leaves `start_hub` and reaches `end_hub` on its scheduled turn.

---

## Visual Representation

Fly-in includes an interactive Pygame window that draws the map and shows where the drones move on each turn.

### Features and Controls

- **Automatic Layout Scaling**: Scales the map coordinates $(x, y)$ so the whole network fits nicely inside the window.
- **Drone Grouping**: When several drones are at the same hub or connection, it displays the count (e.g., `x3`) instead of overlapping labels. Single drones show their ID (e.g., `D1`).
- **Turn Counter**: Shows the current turn and total turns at the top-left corner.
- **Keyboard Controls**:
  - `RIGHT ARROW`: Go forward 1 turn.
  - `LEFT ARROW`: Go back 1 turn.
  - `Window Close` button: Close the visualizer.

### Color Scheme

| Zone Type | Color | Meaning |
| :--- | :--- | :--- |
| **Start Hub** | Green (`#2ECC71`) | Starting point for all drones |
| **End Hub** | Red (`#E74C3C`) | Final destination hub |
| **Restricted Hub** | Yellow (`#F1C40F`) | Slow zone (takes 2 turns to enter) |
| **Normal Hub** | Blue (`#4682B4`) | Standard transit hub |
| **Connections** | Gray (`#646464`) | Two-way links between hubs |
| **Custom Colors** | Map Hex/Name Color | Uses `color=...` from the map file if valid |

---

## Example Input and Expected Output

### Sample Map File

```text
nb_drones: 4
start_hub: Alpha [0, 0]
end_hub: Omega [4, 0]
hub: Beta [2, 1] max_drones: 2
hub: Gamma [2, -1] max_drones: 1
connection: Alpha - Beta max_capacity: 2
connection: Beta - Omega max_capacity: 2
connection: Alpha - Gamma max_capacity: 1
connection: Gamma - Omega max_capacity: 1
```

### Simulation Output

```text
D1-Beta D2-Beta D3-Gamma
D1-Omega D2-Omega D3-Omega D4-Beta
D4-Omega
```

### Turn-by-Turn Breakdown

- **Turn 1**:
  - Drones $D1$ and $D2$ move to `Beta` (using the full capacity of 2 on `Alpha - Beta`).
  - Drone $D3$ moves to `Gamma` (using the capacity of 1 on `Alpha - Gamma`).
- **Turn 2**:
  - Drones $D1$ and $D2$ arrive at `Omega` from `Beta`.
  - Drone $D3$ arrives at `Omega` from `Gamma`.
  - Drone $D4$ leaves `Alpha` and enters `Beta`.
- **Turn 3**:
  - Drone $D4$ arrives at `Omega`. All 4 drones reach the goal in 3 turns.

---

## Benchmark and Test Results

Fly-in has been tested on all 10 project maps and meets or beats every target turn limit:

| Category | Map Name | Drones | Target Turns | Achieved Turns | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Basic** | `01_linear_path.txt` | 3 | $\le 6$ | **4** | Pass |
| **Basic** | `02_simple_fork.txt` | 4 | $\le 6$ | **5** | Pass |
| **Basic** | `03_basic_capacity.txt` | 6 | $\le 8$ | **6** | Pass |
| **Advanced** | `01_maze_nightmare.txt` | 10 | $\le 45$ | **14** | Pass |
| **Advanced** | `02_capacity_hell.txt` | 15 | $\le 60$ | **18** | Pass |
| **Advanced** | `03_ultimate_challenge.txt` | 20 | $\le 35$ | **26** | Pass |
| **Special** | `01_dead_end_trap.txt` | 5 | $\le 15$ | **8** | Pass |
| **Special** | `02_circular_loop.txt` | 8 | $\le 20$ | **11** | Pass |
| **Special** | `03_priority_puzzle.txt` | 6 | $\le 12$ | **7** | Pass |
| **Challenger** | `01_the_impossible_dream.txt` | 50 | $\le 45$ | **43** | **pass** |

---

## Resources and AI Usage

### References

1. **Network Flow and Shortest Paths**:
   - Edmonds, J., & Karp, R. M. (1972). *Theoretical improvements in algorithmic efficiency for network flow problems*.
   - Ford, L. R., & Fulkerson, D. R. (1956). *Maximal flow through a network*.
2. **Quickest Flow Problems**:
   - Burkard, R. E., Dlaska, K., & Klinz, B. (1993). *The quickest flow problem*. ZOR - Methods and Models of Operations Research.
3. **Python Standards and Libraries**:
   - [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
   - [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
   - [Pygame Documentation](https://www.pygame.org/docs/)

### AI Usage Disclosure

- **How AI was used**:
  - Created the initial structure and skeleton for `README.md`.
  - Reviewed and added PEP 257 docstrings across the codebase.
