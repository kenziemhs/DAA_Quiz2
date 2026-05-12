"""
Entity classes: Player (Pac-Man) and Ghost.

The Player is controlled by keyboard input.
Ghosts are driven by BFS — every N frames, compute the shortest path to the
player and advance one step along it.
"""

from pathfinding import bfs_shortest_path
from config import WALL, BFS_RECOMPUTE_INTERVAL


class Player:
    """Pac-Man character, controlled by the keyboard."""

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.score = 0
        # Currently active movement direction (dr, dc). (0, 0) = stationary.
        self.direction = (0, 0)
        # Next direction requested by the player (applied when the move is valid)
        self.requested_direction = (0, 0)

    def request_move(self, dr, dc):
        """Record a direction request from the player. Applied on the next valid frame."""
        self.requested_direction = (dr, dc)

    def update(self, grid):
        """Attempt to move. Prefer the newly requested direction if it is valid."""
        rows, cols = len(grid), len(grid[0])

        def can_move(dr, dc):
            nr, nc = self.row + dr, self.col + dc
            return 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != WALL

        # Try the requested direction first
        if self.requested_direction != (0, 0) and can_move(*self.requested_direction):
            self.direction = self.requested_direction

        # Move in the current active direction if possible
        if can_move(*self.direction):
            self.row += self.direction[0]
            self.col += self.direction[1]
        else:
            # Hit a wall — stop moving
            self.direction = (0, 0)


class Ghost:
    """
    Ghost enemy that chases the player using BFS.

    Optimization: BFS is only recomputed every BFS_RECOMPUTE_INTERVAL frames
    rather than every frame. This saves CPU without making the ghost noticeably
    slower, since the player also moves only every PLAYER_MOVE_DELAY frames.
    """

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.path = []           # the currently planned route to the player
        self.frames_since_bfs = 0

    def update(self, grid, player_row, player_col):
        """
        Recompute the BFS path if necessary, then advance one step along it.
        """
        self.frames_since_bfs += 1

        # Recompute if: (a) interval has elapsed, (b) path is exhausted, or
        # (c) the player has moved away from where the current path leads.
        need_recompute = (
            self.frames_since_bfs >= BFS_RECOMPUTE_INTERVAL
            or len(self.path) < 2
            or (self.path and self.path[-1] != (player_row, player_col))
        )

        if need_recompute:
            self.path = bfs_shortest_path(
                grid, (self.row, self.col), (player_row, player_col)
            )
            self.frames_since_bfs = 0

        # Advance one step: path[0] is current position, path[1] is next cell
        if len(self.path) >= 2:
            self.row, self.col = self.path[1]
            self.path = self.path[1:]

    def caught(self, player_row, player_col):
        return self.row == player_row and self.col == player_col
