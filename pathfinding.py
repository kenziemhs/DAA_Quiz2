"""
Pathfinding using the BFS (Breadth-First Search) algorithm.

Why BFS instead of DFS / Dijkstra / A*?
- In a grid maze, every move has the same cost (= 1 step).
- BFS is guaranteed to return the SHORTEST PATH in an unweighted graph.
- DFS can return a valid path but is often non-optimal (takes long detours).
- Dijkstra is designed for weighted graphs — it reduces to BFS when all
  edge weights are equal, so using it here adds overhead for no benefit.
- A* is faster in practice thanks to its heuristic, but requires more complex
  implementation. For a 21x21 maze (441 cells), BFS completes in < 0.2 ms —
  well within a single 60 FPS frame budget.

How it works:
1. Add the start cell to the queue.
2. Dequeue the front cell; explore all unvisited neighbors.
3. For each neighbor, record its parent (the cell it was reached from).
4. When the goal is found, walk back through parents to reconstruct the path.

Time complexity:  O(V + E), which on a grid = O(rows * cols).
Space complexity: O(V) for the visited set and parent dict.
"""

from collections import deque
from config import WALL


def bfs_shortest_path(grid, start, goal):
    """
    Find the shortest path from start to goal in the grid.

    Args:
        grid:  2D list — WALL=1 / PATH=0
        start: (row, col) tuple
        goal:  (row, col) tuple

    Returns:
        List of (row, col) from start (inclusive) to goal (inclusive).
        Returns [] if no path exists.
    """
    if start == goal:
        return [start]

    rows, cols = len(grid), len(grid[0])

    # Queue of cells to explore. deque gives O(1) popleft (vs O(n) for list).
    queue = deque([start])

    # parent[cell] = the cell this one was reached from.
    # Also acts as a visited set — if a key exists, the cell has been visited.
    parent = {start: None}

    # Four cardinal directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    found = False
    while queue:
        r, c = queue.popleft()

        if (r, c) == goal:
            found = True
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check: within bounds, not a wall, not yet visited
            if 0 <= nr < rows and 0 <= nc < cols \
                    and grid[nr][nc] != WALL \
                    and (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    if not found:
        return []

    # Reconstruct path by tracing parent pointers from goal back to start
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def bfs_with_stats(grid, start, goal):
    """
    BFS variant that also returns runtime statistics — used for evaluation/benchmarking.

    Returns:
        dict with keys: path, path_length, nodes_explored, runtime_seconds
    """
    import time
    t0 = time.perf_counter()

    if start == goal:
        return {"path": [start], "path_length": 0,
                "nodes_explored": 1, "runtime_seconds": 0.0}

    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    parent = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    found = False
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            found = True
            break
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols \
                    and grid[nr][nc] != WALL \
                    and (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    runtime = time.perf_counter() - t0

    if not found:
        return {"path": [], "path_length": -1,
                "nodes_explored": len(parent), "runtime_seconds": runtime}

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return {
        "path": path,
        "path_length": len(path) - 1,   # number of steps, not number of cells
        "nodes_explored": len(parent),  # total cells visited by BFS
        "runtime_seconds": runtime,
    }
