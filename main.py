"""
Main game loop. Run with: python main.py

Controls:
- Arrow keys / WASD: move
- R: restart with a new maze
- Q / ESC: quit
"""

import sys
import random
import pygame

from config import (
    MAZE_ROWS, MAZE_COLS, CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
    FPS, PLAYER_MOVE_DELAY, GHOST_MOVE_DELAY, NUM_GHOSTS,
    COLOR_BG, COLOR_WALL, COLOR_PELLET, COLOR_PLAYER, COLOR_GHOSTS,
    COLOR_TEXT, COLOR_PANEL, WALL, PATH,
)
from maze_generator import generate_maze, get_all_path_cells
from entities import Player, Ghost


def spawn_far_from(player_pos, path_cells, min_distance=10):
    """Select a path cell that is at least min_distance (Manhattan) away from the player."""
    pr, pc = player_pos
    candidates = [
        (r, c) for (r, c) in path_cells
        if abs(r - pr) + abs(c - pc) >= min_distance
    ]
    if not candidates:
        candidates = path_cells
    return random.choice(candidates)


def new_game():
    """Initialize all state for a fresh game."""
    grid = generate_maze()
    path_cells = get_all_path_cells(grid)

    # Player spawns at the top-left corridor (always PATH since DFS starts at (1,1))
    player = Player(1, 1)

    # Pellets on every path cell except the player's starting position
    pellets = set(path_cells) - {(player.row, player.col)}

    # Ghosts spawn far from the player, each with a distinct color
    ghosts = []
    for i in range(NUM_GHOSTS):
        gr, gc = spawn_far_from((player.row, player.col), path_cells,
                                min_distance=8)
        ghosts.append(Ghost(gr, gc, COLOR_GHOSTS[i % len(COLOR_GHOSTS)]))

    return grid, player, ghosts, pellets


def draw_maze(screen, grid):
    """Render the maze walls."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == WALL:
                pygame.draw.rect(
                    screen, COLOR_WALL,
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )


def draw_pellets(screen, pellets):
    radius = max(2, CELL_SIZE // 8)
    for (r, c) in pellets:
        cx = c * CELL_SIZE + CELL_SIZE // 2
        cy = r * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, COLOR_PELLET, (cx, cy), radius)


def draw_player(screen, player):
    cx = player.col * CELL_SIZE + CELL_SIZE // 2
    cy = player.row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, COLOR_PLAYER, (cx, cy), CELL_SIZE // 2 - 2)


def draw_ghost(screen, ghost):
    cx = ghost.col * CELL_SIZE + CELL_SIZE // 2
    cy = ghost.row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 2
    # Classic ghost shape: circle on top + rectangle on the bottom half
    pygame.draw.circle(screen, ghost.color, (cx, cy - 2), radius)
    pygame.draw.rect(
        screen, ghost.color,
        (cx - radius, cy - 2, radius * 2, radius)
    )
    # Eyes
    eye_r = max(2, radius // 4)
    pygame.draw.circle(screen, (255, 255, 255), (cx - 4, cy - 4), eye_r)
    pygame.draw.circle(screen, (255, 255, 255), (cx + 4, cy - 4), eye_r)


def draw_panel(screen, font, score, pellets_left, status):
    """Bottom HUD panel showing score, remaining pellets, and game status."""
    panel_y = MAZE_ROWS * CELL_SIZE
    pygame.draw.rect(screen, COLOR_PANEL,
                     (0, panel_y, WINDOW_WIDTH, 60))

    score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
    pellets_text = font.render(f"Pellets: {pellets_left}", True, COLOR_TEXT)
    screen.blit(score_text, (10, panel_y + 8))
    screen.blit(pellets_text, (10, panel_y + 32))

    if status:
        status_text = font.render(status, True, COLOR_TEXT)
        rect = status_text.get_rect(
            center=(WINDOW_WIDTH // 2, panel_y + 30)
        )
        screen.blit(status_text, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("DAA Pac-Man — BFS + DFS Maze")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    grid, player, ghosts, pellets = new_game()

    player_timer = 0
    ghost_timer = 0
    status = ""  # "YOU WIN!" / "GAME OVER" / ""
    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    grid, player, ghosts, pellets = new_game()
                    status = ""
                    game_over = False
                    player_timer = ghost_timer = 0
                elif not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        player.request_move(-1, 0)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        player.request_move(1, 0)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        player.request_move(0, -1)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        player.request_move(0, 1)

        # Update game logic — only while the game is active
        if not game_over:
            player_timer += 1
            ghost_timer += 1

            if player_timer >= PLAYER_MOVE_DELAY:
                player.update(grid)
                player_timer = 0

                # Check if the player collected a pellet
                pos = (player.row, player.col)
                if pos in pellets:
                    pellets.remove(pos)
                    player.score += 10

                # Win condition: all pellets collected
                if not pellets:
                    status = "YOU WIN!  (R = restart)"
                    game_over = True

            if ghost_timer >= GHOST_MOVE_DELAY and not game_over:
                for ghost in ghosts:
                    ghost.update(grid, player.row, player.col)
                    if ghost.caught(player.row, player.col):
                        status = "GAME OVER  (R = restart)"
                        game_over = True
                        break
                ghost_timer = 0

        # Render
        screen.fill(COLOR_BG)
        draw_maze(screen, grid)
        draw_pellets(screen, pellets)
        draw_player(screen, player)
        for ghost in ghosts:
            draw_ghost(screen, ghost)
        draw_panel(screen, font, player.score, len(pellets), status)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
