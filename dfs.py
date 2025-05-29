import numpy as np
import pygame
import time
from config import config

def is_valid(mat, visited, row, col):
    M, N = mat.shape
    return 0 <= row < M and 0 <= col < N and mat[row][col] != 1 and not visited[row][col]

def draw_cell(screen, grid, x, y, cell_size, color):
    if grid[x, y] not in (2, 3):  # Don’t overwrite start or end
        grid[x, y] = color
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    if color == 4:
        pygame.draw.rect(screen, (0, 0, 255), rect)  # Path
    elif color == 5:
        pygame.draw.rect(screen, (200, 200, 200), rect)  # Visited
    elif color == 6:
        pygame.draw.rect(screen, (255, 255, 0), rect)  # Frontier
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    pygame.display.flip()
    time.sleep(0.01)

def dfs(screen, grid, start, end, walls, cell_size, font):
    start_x, start_y = start
    end_x, end_y = end
    mat = np.zeros([config['board']['w'], config['board']['h']])
    for i in walls:
        mat[i] = 1

    M, N = mat.shape
    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]
    stack = [(start_x, start_y)]
    visited = [[False for _ in range(N)] for __ in range(M)]
    visited[start_x][start_y] = True
    came_from = {}
    found = False

    start_time = time.time()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "DFS: Interrupted"

        current_x, current_y = stack.pop()
        if (current_x, current_y) == (end_x, end_y):
            found = True
            break

        for k in range(4):
            new_x, new_y = current_x + row[k], current_y + col[k]
            if is_valid(mat, visited, new_x, new_y):
                visited[new_x][new_y] = True
                came_from[(new_x, new_y)] = (current_x, current_y)
                draw_cell(screen, grid, new_x, new_y, cell_size, 6)
                stack.append((new_x, new_y))
                draw_cell(screen, grid, new_x, new_y, cell_size, 5)

    end_time = time.time()
    duration = end_time - start_time

    if found:
        path_length = 0
        current = end
        while current != start:
            if current != end:
                draw_cell(screen, grid, current[0], current[1], cell_size, 4)
            current = came_from[current]
            path_length += 1
        return f"DFS: Path found! Length: {path_length} | Time: {duration:.2f} s"
    else:
        return f"DFS: No path found | Time: {duration:.2f} s"
