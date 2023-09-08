# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 9/8/23
# Description: John Conway's Game of Life, sourced from https://www.geeksforgeeks.org/conways-game-life-python-implementation/, https://conwaylife.com/wiki/Main_Page, and https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# Used PyGame to implement a GUI for general control - PyGame documentation: https://www.pygame.org/docs/

# Follows the standard B3/S23 rule system:
# If a cell is ON and has fewer than two neighbors that are ON, it turns OFF
# If a cell is ON and has either two or three neighbors that are ON, it remains ON.
# If a cell is ON and has more than three neighbors that are ON, it turns OFF.
# If a cell is OFF and has exactly three neighbors that are ON, it turns ON.


# --------------- Imports and Constants ---------------


import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
ON_COLOR = (255, 255, 255)  # white
OFF_COLOR = (0, 0, 0)  # black

# --------------- Create Display, Initialize Game Grid ---------------


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)


# --------------- Game Logic ---------------


def update_grid():
    """
    Updates grid according to B3/S23 rules of Conway's Game of Life.
    """
    global grid
    new_grid = grid.copy()

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            total = np.sum(grid[max(i - 1, 0):min(i + 2, GRID_WIDTH), max(j - 1, 0):min(j + 2, GRID_HEIGHT)]) - grid[
                i, j]

            if grid[i, j] == 1:
                if total < 2 or total > 3:
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1

    grid[:] = new_grid[:]


def draw_grid():
    """
    Renders the grid based on the update.
    """
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            # if [i, j] contains a living cell, we want white - if not, black
            color = ON_COLOR if grid[i, j] else OFF_COLOR
            pygame.draw.rect(screen, color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def create_initial_cluster():
    """
    Beginning glider cluster for life to stem from.
    """
    global grid
    center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

    # Create a glider pattern
    glider = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]

    for i in range(5):
        for j in range(5):
            grid[center_x + i, center_y + j] = glider[i][j]


# --------------- Driver Code ---------------


def main():
    global grid
    clock = pygame.time.Clock()
    running = True
    paused = False

    create_initial_cluster()  # Set up the initial cluster
    expansion_depth = 1  # Adjust the expansion depth as needed

    glider_x, glider_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not paused:
            if expansion_depth > 0:
                expansion_depth -= 1
            else:
                # Add a random offset to the glider's position
                glider_x += np.random.randint(-1, 2)
                glider_y += np.random.randint(-1, 2)

            screen.fill(OFF_COLOR)
            draw_grid()

            # Update the glider's position
            grid[glider_x:glider_x + 3, glider_y:glider_y + 3] = grid[glider_x:glider_x + 3, glider_y:glider_y + 3][
                                                                 ::-1, ::-1]

            update_grid()

            pygame.display.flip()
            clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
