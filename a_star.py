import numpy as np
import pygame
import time
from queue import PriorityQueue
from config import config

def is_valid(mat, row, col):
    M, N = mat.shape
    return 0 <= row < M and 0 <= col < N and mat[row][col] != 1

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

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

def a_star(screen, grid, start, end, walls, cell_size, font):
    mat = np.zeros([config['board']['w'], config['board']['h']])
    for w in walls:
        mat[w] = 1

    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]

    q = PriorityQueue()
    count = 0
    q.put((0, count, start))
    came_from = {}
    g_score = {(x, y): float('inf') for x in range(mat.shape[0]) for y in range(mat.shape[1])}
    g_score[start] = 0
    f_score = {(x, y): float('inf') for x in range(mat.shape[0]) for y in range(mat.shape[1])}
    f_score[start] = manhattan_distance(*start, *end)

    q_hash = {start}
    found = False

    start_time = time.time()

    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "A*: Interrupted"

        current = q.get()[2]
        q_hash.remove(current)

        if current == end:
            found = True
            break

        for k in range(4):
            neighbor = (current[0] + row[k], current[1] + col[k])
            if is_valid(mat, *neighbor):
                temp_g = g_score[current] + 1
                if temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + manhattan_distance(*neighbor, *end)
                    if neighbor not in q_hash:
                        count += 1
                        q_hash.add(neighbor)
                        q.put((f_score[neighbor], count, neighbor))
                        draw_cell(screen, grid, neighbor[0], neighbor[1], cell_size, 6)
                        draw_cell(screen, grid, neighbor[0], neighbor[1], cell_size, 5)

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
        return f"A*: Path found! Length: {path_length} | Time: {duration:.2f} s"
    else:
        return f"A*: No path found | Time: {duration:.2f} s"
