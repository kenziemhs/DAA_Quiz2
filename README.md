# DAA Pac-Man — BFS + DFS

Group project untuk EF234405 Design & Analysis of Algorithms (Quiz 2).

A Pac-Man-style maze game written in Python with Pygame. Implements two algorithms from the course:

- **DFS (Recursive Backtracking)** — generates a random maze each game, guaranteeing solvability.
- **BFS (Breadth-First Search)** — drives the ghost AI; ghosts compute the shortest path to the player on a recurring tick.

## Setup

```bash
pip install -r requirements.txt
```

## Run the game

```bash
python main.py
```

**Controls:**
- Arrow keys or WASD — move
- R — restart with a new maze
- ESC or Q — quit

## Run the benchmarks (for the report)

```bash
python evaluation.py
```

Produces `results_maze_generation.csv` and `results_bfs_pathfinding.csv` — open in Excel/Google Sheets to make plots for the Evaluation section.

## File structure

| File | Purpose |
|------|---------|
| `main.py` | Game loop, rendering, input |
| `maze_generator.py` | **DFS** algorithm — generates the maze |
| `pathfinding.py` | **BFS** algorithm — computes shortest paths |
| `entities.py` | `Player` and `Ghost` classes |
| `config.py` | All constants (sizes, colors, speeds) — tweak here |
| `evaluation.py` | Benchmark script for the report |

## Algorithms

### DFS maze generation
Iterative DFS with a stack. Starts at cell `(1,1)`, picks a random unvisited neighbor at distance 2, knocks down the wall between them, and recurses. When stuck, backtracks. Time complexity **O(N)** where N = number of cells (each cell visited once). After generation, a few internal walls are randomly removed to create loops, which makes the ghost AI more interesting.

### BFS ghost AI
Standard BFS from ghost position to player position. Uses a `deque` for the queue and a `parent` dict that doubles as the visited set. Reconstructs the path by walking back through parents. Time complexity **O(V + E)**; on a grid that's **O(rows × cols)**. Re-computed every `BFS_RECOMPUTE_INTERVAL` frames rather than every frame to save CPU without making the ghosts noticeably "dumber".

## Team

[Kenzie Maheswara - 5025241001]
[Palpal Yalmialam T. - 5025241002]
[Rayen Yeriel M. - 5025241262]
