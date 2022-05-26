import pygame
import sys
import random

W_WIDTH, W_HEIGHT = [820, 820]
WINDOW_SIZE = [W_WIDTH, W_HEIGHT]
SCALE = 12

CELL_WIDTH = SCALE
CELL_OFFSET = 1

fps = 7                         # Change this to change the speed of the game.
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

rows = W_WIDTH // SCALE

collumns = W_HEIGHT // SCALE

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("The Game Of Life")


grid = [[0 for x in range(rows)] for y in range(collumns)]


def conway():
    updated = [[0 for x in range(rows)] for y in range(collumns)]
    global grid
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
    grid = updated


def get_neighbor(grid, x, y):
    total = 0
    for n in range(-1, 2):
        for m in range(-1, 2):
            x_edge = (x + n + rows) % rows
            y_edge = (y + m + collumns) % collumns

            total += grid[x_edge][y_edge]
    total -= grid[x][y]
    return total


saved_grid = []


def main():
    global grid
    global saved_grid
    run = True
    game = False

    while run:
        clock.tick(fps)
        screen.fill(BLACK)
        if game:
            conway()

        for event in pygame.event.get():
            saved = False

            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            # Controls
            # Mouse button to add or remove a cell.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (CELL_WIDTH + CELL_OFFSET)
                row = pos[1] // (CELL_WIDTH + CELL_OFFSET)

                grid[row][column] = 1 if grid[row][column] == 0 else 0

            # End to reset the matrix.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:                       
                    grid = [[0 for x in range(rows)] for y in range(collumns)]
                    game = False

                elif event.key == pygame.K_r:
                    grid = [[(random.randint(0, 1)) for x in range(rows)]
                            for y in range(collumns)]
                 """
                 if event.key == pygame.K_s and not saved:
                     saved = True
                     saved_grid = grid[:]
                 elif event.key == pygame.K_s and saved:
                     saved = False
                     grid = saved_grid
                     print(grid)
                """
                # Enter to start and pause.
                if event.key == pygame.K_RETURN and not game:     
                    game = True
                    pygame.display.set_caption("The Game Of Life (Running)")
                elif event.key == pygame.K_RETURN and game:
                    game = False
                    pygame.display.set_caption("The Game Of Life (Paused)")

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
