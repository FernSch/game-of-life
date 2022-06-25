import time
import pygame
import numpy as np

color_bg = (10,10,10)
color_grid = (40,40,40)
color_die = (170,170,170)
color_alive = (255,255,255)

def update(screen, cells, size, step_over=False):
    #step_over would be executing game rules
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    

    #calculate game rule
    for row, col in np.ndindex(cells.shape):

        #calculate number of alive cells surronding each cell
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = color_bg if cells[row, col] == 0 else color_alive

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if step_over:
                    color = color_die
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if step_over:
                    color = color_alive
        else:
            if alive == 3:
                updated_cells[row, col] = 1

                if step_over:
                    color = color_alive
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    cells = np.zeros((60,80))
    
    screen.fill(color_grid)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(color_grid) 

        if running:
            cells = update(screen, cells, 10, step_over = True)
            pygame.display.update()
    
        time.sleep(.001)
