import pygame
import random
import sys
import time

screen_width = 400
screen_height = 800
grid_height = 20
grid_width = 10
cell_size = int(screen_width / grid_width)
fps = 60
fall_delta_time = 0.5 #in seconds
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 195, 0)
purple = (255, 0, 255)

colours = [red, green, blue, orange, purple]

blocks = [
    [
        ['00000',
         '00000',
         '00000',
         '11110',
         '00000'],
        ['00000',
         '00100',
         '00100',
         '00100',
         '00100']
    ]
]

#initialize pygame
pygame.init()

#set up game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

def game_grid(surf):
    #draws playing grid
    surf.fill(black)

    #draws vertical grid lines
    for ix in range(grid_width + 1):
        xpos = ix * cell_size
        pygame.draw.line(surf, (50, 50, 50), (xpos, 0), (xpos, screen_height))

    #draws horizontal grid lines
    for iy in range(grid_height + 1):
        ypos = iy * cell_size
        pygame.draw.line(surf, (50, 50, 50), (0, ypos), (screen_width, ypos))


def shape_to_cells(shape_5x5, px, py):
    #turns cells within grid into coordinates
    coords = []
    for r_i, row in enumerate(shape_5x5):
        for c_i, ch in enumerate(row):
            if ch == '1':
                gx = px + c_i
                gy = py + r_i
                coords.append((gx, gy))
    return coords

def draw_block(surf, block):
    #draws piece by filling in cells within grid
    block_cells = shape_to_cells(
        block['shape'][block['rotation']],
        block['x'],
        block['y']
    )
    for (cx, cy) in block_cells:
        if 0 <= cx < grid_width and 0 <= cy < grid_height:
            rect = pygame.Rect(cx * cell_size, cy * cell_size, cell_size, cell_size)
            pygame.draw.rect(surf, block['colour'], rect)

def check_wall_collision(block):
    #check if piece is within grid
    pcs = shape_to_cells(block['shape'][block['rotation']], block['x'], block['y'])
    for gx, gy in pcs:
        if gx < 0 or gx >= grid_width:
            return False
    return True

def generate_block():
    #randomise shape and colour
    block_shape = random.choice(blocks)
    block_colour = random.choice(colours)
    start_x = grid_width // 2 - 2
    start_y = 0
    return {
        'shape': block_shape,
        'rotation': 0,
        'x': start_x,
        'y': start_y,
        'colour': block_colour
    }


def main():
    current_time = time.time()
    last_fall_time = current_time
    current_block = generate_block()

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                #moves the block left when left arrow pressed
                if event.key == pygame.K_LEFT:
                    current_block['x'] -= 1
                    if not check_wall_collision(current_block):
                        current_block['x'] += 1

                elif event.key == pygame.K_RIGHT:
                #moves the block right when right arrow pressed    
                    current_block['x'] += 1
                    if not check_wall_collision(current_block):
                        current_block['x'] -= 1

                elif event.key == pygame.K_SPACE:
                    current_block = generate_block()

        #moves the block down every half a second
        current_time = time.time()
        if current_time >= last_fall_time + fall_delta_time:
            current_block['y'] += 1
            last_fall_time = current_time
            
        #state of game updated so game is redrawn
        game_grid(screen)
        draw_block(screen, current_block)

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()