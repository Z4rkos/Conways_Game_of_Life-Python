import pygame
import sys
import random

# Change this to adjust window size.
W_WIDTH, W_HEIGHT = [820, 820]
WINDOW_SIZE = [W_WIDTH, W_HEIGHT]

# Change this to adjust the size of the squares.
SCALE = 12
CELL_WIDTH = SCALE
CELL_OFFSET = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Change this to change the speed of the game.
fps = 7
clock = pygame.time.Clock()

rows = W_WIDTH // SCALE
collumns = W_HEIGHT // SCALE


pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("The Game Of Life")


def conway(grid):
    updated = [[0 for x in range(rows)] for y in range(collumns)]

    for x in range(rows):
        for y in range(collumns):

            state = grid[x][y]
            neighbors = get_neighbor(grid, x, y)

            if neighbors == 3 and state == 0:
                updated[x][y] = 1
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                updated[x][y] = 0
            else:
                updated[x][y] = state

    return updated


def get_neighbor(grid, x, y):
    total = 0
    for n in range(-1, 2):
        for m in range(-1, 2):

            x_edge = (x + n + rows) % rows
            y_edge = (y + m + collumns) % collumns

            total += grid[x_edge][y_edge]
    total -= grid[x][y]
    return total


def main():
    run = True
    game = False

    grid = [[0 for x in range(rows)] for y in range(collumns)]

    while run:
        clock.tick(fps)

        # This fills in the backround with black to get the grid pattern.
        screen.fill(BLACK)

        if game:
            grid = conway(grid)

        for event in pygame.event.get():
            saved = False

            if event.type == pygame.QUIT:
                run = False
                sys.exit()

                
            ### Controls ###

            # Mouse button to add or remove a cell.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (CELL_WIDTH + CELL_OFFSET)
                row = pos[1] // (CELL_WIDTH + CELL_OFFSET)

                grid[row][column] = 1 if grid[row][column] == 0 else 0

            elif event.type == pygame.KEYDOWN:

                # End to reset the matrix.
                if event.key == pygame.K_END:
                    grid = [[0 for x in range(rows)] for y in range(collumns)]
                    game = False
                    pygame.display.set_caption("The Game Of Life (Paused)")

                # r to randomize the grid.
                elif event.key == pygame.K_r:
                    grid = [[(random.randint(0, 1)) for x in range(rows)]
                            for y in range(collumns)]

                # Enter to start and pause.
                if event.key == pygame.K_RETURN and not game:
                    game = True
                    pygame.display.set_caption("The Game Of Life (Running)")
                elif event.key == pygame.K_RETURN and game:
                    game = False
                    pygame.display.set_caption("The Game Of Life (Paused)")

        # This renders the grid.
        for row in range(rows):
            for column in range(collumns):
                color = BLACK if grid[row][column] == 1 else WHITE

                pygame.draw.rect(screen,
                                 color,
                                 [(CELL_OFFSET + CELL_WIDTH) * column + CELL_OFFSET,
                                  (CELL_OFFSET + CELL_WIDTH) * row + CELL_OFFSET,
                                  CELL_WIDTH,
                                  CELL_WIDTH])

        pygame.display.update()


if __name__ == '__main__':
    main()

pygame.quit()
