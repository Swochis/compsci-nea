# write a simple pygame program that
# 1. opens a window
# 2. divides the window into a grid of 20x10 squares
# 3. fill all squares with black
# 4. animates a square block falling down the grid from top to bottom.
# 5. when the square reaches the bottom, it should restart from the top at a random horizontal position.
# 6. the colour of the single falling block must change each time the block starts at the top of the grid.
# 7. The colour chosen must be the colour at the head of a list of random colours.
# 8. In the top-left of the game grid, draw a row of 4 blocks which shows the next 4 colours in the colour list.
# 9. allow the user to move the block left or right using the arrow keys.
# 10. the block should move down one square every 500 milliseconds.
# 11. if the user presses Quit or closes the window, the program should exit.
import pygame
import random
import sys
import time
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT
import itertools
import collections
# Constants
GRID_COLS = 20
GRID_ROWS = 50
WINDOW_WIDTH = GRID_COLS * 10
WINDOW_HEIGHT = GRID_ROWS * 10
SQUARE_SIZE = WINDOW_WIDTH // GRID_COLS
FALL_INTERVAL = 0.1  # seconds
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Falling Block Game')
clock = pygame.time.Clock()
# Function to generate a list of random colors
def generate_random_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    return colors
# Game variables
color_list = collections.deque(generate_random_colors(100))
current_color = color_list.popleft()
next_colors = list(itertools.islice(color_list, 4))
block_x = random.randint(0, GRID_COLS - 1)
block_y = 0
last_fall_time = time.time()
# Function to draw the grid and blocks
def draw_grid():
    screen.fill((0, 0, 0))  # Fill background with black
    # Draw falling block
    pygame.draw.rect(screen, current_color, (block_x * SQUARE_SIZE, block_y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw next colors
    for i, color in enumerate(next_colors[::-1]):
        pygame.draw.rect(screen, color, (i * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.flip()
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and block_x > 0:
                block_x -= 1
            elif event.key == K_RIGHT and block_x < GRID_COLS - 1:
                block_x += 1
    # Handle block falling
    current_time = time.time()
    if current_time - last_fall_time >= FALL_INTERVAL:
        block_y += 1
        last_fall_time = current_time
        if block_y >= GRID_ROWS:
            # Reset block position and color
            block_y = 0
            block_x = random.randint(0, GRID_COLS - 1)
            current_color = next_colors.pop(0)
            next_colors.append(color_list.popleft())
    draw_grid()
    clock.tick(60)  # Limit to 60 FPS