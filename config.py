"""
Global constants for the game.
Edit values here to change maze size, colors, speeds, etc.
"""

# Maze dimensions in cells. Must be odd so the DFS generator works correctly
# (cells at odd coordinates are corridors; even coordinates are walls).
MAZE_COLS = 21
MAZE_ROWS = 21

# Size of one cell in pixels
CELL_SIZE = 28

# Window dimensions
WINDOW_WIDTH = MAZE_COLS * CELL_SIZE
WINDOW_HEIGHT = MAZE_ROWS * CELL_SIZE + 60  # +60 for the score panel

# Frame rate and movement speeds
FPS = 60
PLAYER_MOVE_DELAY = 8      # frames between each player move
GHOST_MOVE_DELAY = 14      # frames between each ghost move (slower than player)
BFS_RECOMPUTE_INTERVAL = 14  # frames between BFS path recomputes for ghosts

# Number of ghosts
NUM_GHOSTS = 2

# Colors (R, G, B)
COLOR_BG = (10, 10, 30)
COLOR_WALL = (30, 60, 200)
COLOR_PATH = (10, 10, 30)
COLOR_PELLET = (255, 220, 100)
COLOR_PLAYER = (255, 230, 0)
COLOR_GHOSTS = [
    (255, 80, 80),    # red
    (255, 150, 220),  # pink
    (100, 220, 255),  # cyan
]
COLOR_TEXT = (240, 240, 240)
COLOR_PANEL = (20, 20, 50)

# Cell type constants
WALL = 1
PATH = 0
