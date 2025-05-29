import pygame
from pygame.locals import *
import sys
import numpy as np
from config import config
from bfs import bfs
from dfs import dfs
from a_star import a_star
from bidirectional import bidirectional_search

# Constants
CELL_SIZE = 20
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
GRAY, YELLOW = (200, 200, 200), (255, 255, 0)

BUTTON_HEIGHT = 30
BUTTON_WIDTH = 180
BUTTON_MARGIN_X = 20
BUTTON_MARGIN_Y = 10

def draw_text(screen, font, message, width, y_pos):
    screen.fill(WHITE, (0, y_pos, width, 30))
    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (10, y_pos + 5))

def draw_grid(screen, grid, width, height):
    screen.fill(WHITE)
    for x in range(width):
        for y in range(height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            value = grid[x, y]
            if value == 0:
                color = WHITE
            elif value == 1:
                color = BLACK
            elif value == 2:
                color = GREEN
            elif value == 3:
                color = RED
            elif value == 4:
                color = BLUE
            elif value == 5:
                color = GRAY
            elif value == 6:
                color = YELLOW
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def create_button_rect(col, row, base_y, total_width, center=False):
    if center:
        x = (total_width - BUTTON_WIDTH) // 2
    else:
        x = col * (BUTTON_WIDTH + BUTTON_MARGIN_X) + 10
    y = base_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN_Y)
    return pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_buttons(screen, font, buttons):
    for label, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = font.render(label, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        

def drawer():
    pygame.init()
    board_w, board_h = config['board']['w'], config['board']['h']
    width, height = board_w * CELL_SIZE, board_h * CELL_SIZE

    # UI layout
    padding_for_text = 30
    button_rows = 3
    padding_for_buttons = button_rows * (BUTTON_HEIGHT + BUTTON_MARGIN_Y)
    extra_ui_height = padding_for_text + padding_for_buttons

    screen = pygame.display.set_mode((width, height + extra_ui_height))
    pygame.display.set_caption("Pathfinding Visualizer")
    font = pygame.font.SysFont(None, 24)

    grid = np.zeros((board_w, board_h))
    start, end = None, None
    walls = set()
    placing_start, placing_end, placing_walls = True, False, False
    status_message = ""

    base_button_y = height + padding_for_text
    buttons = {
        "Run BFS": create_button_rect(0, 0, base_button_y, width),
        "Run DFS": create_button_rect(1, 0, base_button_y, width),
        "Run A*": create_button_rect(0, 1, base_button_y, width),
        "Run Bi-Search": create_button_rect(1, 1, base_button_y, width),
        "Edit Start/End Point": create_button_rect(0, 2, base_button_y, width),
        "Remove All Walls": create_button_rect(1, 2, base_button_y, width),
    }


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                grid_click = event.pos[1] < height

                if grid_click and 0 <= x < board_w and 0 <= y < board_h:
                    if placing_start:
                        if start: grid[start[0], start[1]] = 0
                        start = (x, y)
                        grid[x, y] = 2
                        placing_start, placing_end = False, True
                    elif placing_end:
                        if end: grid[end[0], end[1]] = 0
                        end = (x, y)
                        grid[x, y] = 3
                        placing_end, placing_walls = False, True
                    elif placing_walls and (x, y) != start and (x, y) != end:
                        grid[x, y] = 0 if grid[x, y] == 1 else 1
                        if grid[x, y] == 1: walls.add((x, y))
                        else: walls.discard((x, y))

                for label, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if label == "Run BFS" and start and end:
                            status_message = "Running BFS..."
                            draw_text(screen, font, status_message, width, height)
                            pygame.display.flip()
                            status_message = bfs(screen, grid, start, end, walls, CELL_SIZE, font)
                        elif label == "Run DFS" and start and end:
                            status_message = "Running DFS..."
                            draw_text(screen, font, status_message, width, height)
                            pygame.display.flip()
                            status_message = dfs(screen, grid, start, end, walls, CELL_SIZE, font)
                        elif label == "Run A*" and start and end:
                            status_message = "Running A*..."
                            draw_text(screen, font, status_message, width, height)
                            pygame.display.flip()
                            status_message = a_star(screen, grid, start, end, walls, CELL_SIZE, font)
                        elif label == "Run Bi-Search" and start and end:
                            status_message = "Running Bidirectional Search..."
                            draw_text(screen, font, status_message, width, height)
                            pygame.display.flip()
                            status_message = bidirectional_search(screen, grid, start, end, walls, CELL_SIZE, font)
                        elif label == "Edit Start/End":
                            placing_start, placing_end = True, False
                            if start:
                                grid[start[0], start[1]] = 0
                            if end:
                                grid[end[0], end[1]] = 0
                            start, end = None, None
                            status_message = "Place start point (green)"
                        elif label == "Remove All Walls":
                            for wall_x, wall_y in walls:
                                if grid[wall_x, wall_y] == 1:
                                    grid[wall_x, wall_y] = 0
                            walls.clear()
                            status_message = "All walls removed"


            if event.type == MOUSEMOTION and placing_walls and event.buttons[0]:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= x < board_w and 0 <= y < board_h and (x, y) != start and (x, y) != end:
                    grid[x, y] = 1
                    walls.add((x, y))

            if event.type == KEYDOWN:
                if event.key == K_r:
                    grid.fill(0)
                    start, end, walls = None, None, set()
                    placing_start, placing_end, placing_walls = True, False, False
                    status_message = "Place start point (green)"
                elif event.key == K_b and start and end:
                    status_message = "Running BFS..."
                    draw_text(screen, font, status_message, width, height)
                    pygame.display.flip()
                    status_message = bfs(screen, grid, start, end, walls, CELL_SIZE, font)
                elif event.key == K_d and start and end:
                    status_message = "Running DFS..."
                    draw_text(screen, font, status_message, width, height)
                    pygame.display.flip()
                    status_message = dfs(screen, grid, start, end, walls, CELL_SIZE, font)
                elif event.key == K_a and start and end:
                    status_message = "Running A*..."
                    draw_text(screen, font, status_message, width, height)
                    pygame.display.flip()
                    status_message = a_star(screen, grid, start, end, walls, CELL_SIZE, font)
                elif event.key == K_i and start and end:
                    status_message = "Running Bidirectional Search..."
                    draw_text(screen, font, status_message, width, height)
                    pygame.display.flip()
                    status_message = bidirectional_search(screen, grid, start, end, walls, CELL_SIZE, font)

        draw_grid(screen, grid, board_w, board_h)
        draw_buttons(screen, font, buttons)
        draw_text(screen, font, status_message or (
            "Place start point (green)" if placing_start else
            "Place end point (red)" if placing_end else
            "Place walls (black) - Press B/D/A/I to run algorithm"
        ), width, height)
        pygame.display.flip()

if __name__ == "__main__":
    drawer()
