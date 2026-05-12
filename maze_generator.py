"""
Maze generation using the DFS (Recursive Backtracking) algorithm.

Core idea:
1. Start from a cell and mark it as visited.
2. Randomly look for unvisited neighbors at a distance of 2 cells
   (the cell in between them is the wall to knock down).
3. If a neighbor is found, carve through the wall and recurse into it.
4. If no unvisited neighbors remain, backtrack.

Time complexity: O(N) where N = number of cells, since each cell is visited
exactly once.

The result is a "perfect maze" — there is exactly one path between any two
points. For better gameplay, we optionally remove a few extra internal walls
to introduce loops, making ghost AI less predictable and giving the player
more route choices.
"""

import random
from config import MAZE_ROWS, MAZE_COLS, WALL, PATH


def generate_maze(rows=MAZE_ROWS, cols=MAZE_COLS, extra_openings=8, seed=None):
    """
    Generate a maze and return it as a 2D grid (list of lists).
    grid[r][c] = WALL (1) or PATH (0).

    Args:
        rows, cols:       Maze dimensions in cells (forced odd if even).
        extra_openings:   Number of extra walls to remove to create loops.
        seed:             Random seed for reproducibility (used in benchmarks).
    """
    if seed is not None:
        random.seed(seed)

    # Dimensions must be odd for the generator to work correctly
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    # Initialize all cells as walls
    grid = [[WALL for _ in range(cols)] for _ in range(rows)]

    # Iterative DFS using an explicit stack — avoids Python's recursion limit
    # on large mazes (default limit is ~1000 frames).
    start_r, start_c = 1, 1
    grid[start_r][start_c] = PATH
    stack = [(start_r, start_c)]

    # Step size is 2: the cell between current and neighbor is the wall to carve
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        r, c = stack[-1]

        # Collect unvisited neighbors (still WALL, within inner bounds)
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 < nr < rows - 1 and 0 < nc < cols - 1 and grid[nr][nc] == WALL:
                neighbors.append((nr, nc, dr, dc))

        if neighbors:
            # Pick a random neighbor and carve through the wall between them
            nr, nc, dr, dc = random.choice(neighbors)
            wall_r, wall_c = r + dr // 2, c + dc // 2
            grid[wall_r][wall_c] = PATH
            grid[nr][nc] = PATH
            stack.append((nr, nc))
        else:
            # No unvisited neighbors — backtrack
            stack.pop()

    # Extra openings: randomly remove internal walls to create loops.
    # Without this, the maze is "perfect" and ghost paths are trivially unique.
    openings_done = 0
    attempts = 0
    while openings_done < extra_openings and attempts < extra_openings * 20:
        attempts += 1
        r = random.randint(1, rows - 2)
        c = random.randint(1, cols - 2)
        if grid[r][c] == WALL:
            # Only remove walls that connect two corridors (not corner walls).
            # Check that both sides (left-right OR top-bottom) are PATH.
            if (grid[r - 1][c] == PATH and grid[r + 1][c] == PATH) or \
               (grid[r][c - 1] == PATH and grid[r][c + 1] == PATH):
                grid[r][c] = PATH
                openings_done += 1

    return grid


def get_all_path_cells(grid):
    """Return a list of all cells that are PATH. Used for pellet placement and spawning."""
    cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == PATH:
                cells.append((r, c))
    return cells


if __name__ == "__main__":
    # Quick visual test: print the maze to the terminal
    maze = generate_maze(seed=42)
    for row in maze:
        print("".join("█" if cell == WALL else " " for cell in row))
