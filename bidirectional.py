import numpy as np
import pygame
import time
from collections import deque
from config import config

def is_valid(mat, visited, row, col):
    M, N = mat.shape
    return 0 <= row < M and 0 <= col < N and mat[row][col] != 1 and not visited[row][col]

def draw_cell(screen, grid, x, y, cell_size, color):
    if grid[x, y] not in (2, 3):  # Don't overwrite start or end
        grid[x, y] = color
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    if color == 4:
        pygame.draw.rect(screen, (0, 0, 255), rect)  # Final path
    elif color == 5:
        pygame.draw.rect(screen, (200, 200, 200), rect)  # Visited
    elif color == 6:
        pygame.draw.rect(screen, (255, 255, 0), rect)  # Frontier
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    pygame.display.flip()
    time.sleep(0.01)

def bidirectional_search(screen, grid, start, end, walls, cell_size, font):
    start_x, start_y = start
    end_x, end_y = end
    mat = np.zeros([config['board']['w'], config['board']['h']])
    for i in walls:
        mat[i] = 1

    M, N = mat.shape
    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]

    visited_start = [[False for _ in range(N)] for __ in range(M)]
    visited_end = [[False for _ in range(N)] for __ in range(M)]

    came_from_start = {}
    came_from_end = {}

    queue_start = deque([(start_x, start_y)])
    queue_end = deque([(end_x, end_y)])
    visited_start[start_x][start_y] = True
    visited_end[end_x][end_y] = True

    meet_point = None

    start_time = time.time()

    while queue_start and queue_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Bidirectional: Interrupted"

        # Expand from start
        if queue_start:
            current = queue_start.popleft()
            for k in range(4):
                nx, ny = current[0] + row[k], current[1] + col[k]
                if is_valid(mat, visited_start, nx, ny):
                    visited_start[nx][ny] = True
                    came_from_start[(nx, ny)] = current
                    draw_cell(screen, grid, nx, ny, cell_size, 6)
                    queue_start.append((nx, ny))
                    draw_cell(screen, grid, nx, ny, cell_size, 5)
                    if visited_end[nx][ny]:
                        meet_point = (nx, ny)
                        break
            if meet_point:
                break

        # Expand from end
        if queue_end:
            current = queue_end.popleft()
            for k in range(4):
                nx, ny = current[0] + row[k], current[1] + col[k]
                if is_valid(mat, visited_end, nx, ny):
                    visited_end[nx][ny] = True
                    came_from_end[(nx, ny)] = current
                    draw_cell(screen, grid, nx, ny, cell_size, 6)
                    queue_end.append((nx, ny))
                    draw_cell(screen, grid, nx, ny, cell_size, 5)
                    if visited_start[nx][ny]:
                        meet_point = (nx, ny)
                        break
            if meet_point:
                break

    end_time = time.time()
    duration = end_time - start_time

    if meet_point:
        # Build path from start to meet_point
        path_length = 0
        current = meet_point
        while current != start:
            draw_cell(screen, grid, current[0], current[1], cell_size, 4)
            current = came_from_start[current]
            path_length += 1
        current = meet_point
        while current != end:
            current = came_from_end[current]
            if current != end:
                draw_cell(screen, grid, current[0], current[1], cell_size, 4)
            path_length += 1
        return f"Bidirectional: Path found! Length: {path_length} | Time: {duration:.2f} second"
    else:
        return f"Bidirectional: No path found | Time: {duration:.2f} second"
