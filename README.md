# Maze Solver Project for Design & Analysis of Algorithms (H) course

## Members

| Name | Student ID |
|------|------------|
| Siti Zahra Ananda Kurniawan | 5025231037 |
| Tarisha Falah Basuki | 5025231043 |
| Putriani Pirma A. Sagala | 5025231045 |

## Description

The Maze Solver is an engaging visual tool that lets players experiment with and learn about four fundamental pathfinding algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), A Star (A*), and Bidirectional Search Algorithms. Designed as a grid-based puzzle, the application allows users to create mazes and observe how each algorithm navigates them in real time.

## Features

1. Grid Initialization
   When the program starts, it opens a Pygame window and initializes a grid based on the width and height from “config.py”. Each grid cell represents a possible position an agent can move to.
   - Empty cells (white): free to move
   - Wall (black): obstacle, cannot be passed
   - Start cell (green): user-defined starting point
   - End cell (red): user-defined goal

2. User Interaction / Setup Phase
   Before running an algorithm, the user can set up the grid by:
   - Clicking to place the start point (green).
   - Clicking to place the end point (red).
   - Clicking or dragging to add/remove walls (black) to shape the maze.
   
   This allows users to create layouts and test algorithm behaviour in different scenarios.

3. Algorithm Selection
   Once the setup is complete, the user can press a key to run a specific pathfinding algorithm:

   | Key | Algorithm |
   |-----|-----------|
   | B | BFS (Breadth-First Search) |
   | D | DFS (Depth-First Search) |
   | A | A* Search |
   | I | Bidirectional Search |

   The selected algorithm will then begin searching for a path from the start to the end point in real-time.

4. Search Visualization
   As the algorithm runs, the grid updates to show the search process:
   - Yellow cells: frontier – cells currently being considered
   - Gray cells: cells already been visited
   - Blue cells: final path found by the algorithm
   
   A message bar at the bottom displays the algorithm name, path length (if found), and search duration. This helps users analyze:
   - How the algorithm explores the grid.
   - How efficiently it finds the path.
   - Which areas are searched and revisited.

5. Reset Option
   At any time, pressing R will reset the entire board, allowing users to start over with a new setup.

6. Result Output
   After the algorithm finishes:
   - If a path is found, it is drawn in blue, and the path length and time taken are displayed.
   - If no path exists, a message is shown indicating that no solution is possible with the current setup.
   - The real-time feedback and performance metrics enable users to compare the effectiveness and efficiency of different search strategies.

## Sample Result

![image](https://github.com/user-attachments/assets/5f07b13b-94da-4225-8313-c3afd8f35941)

![image](https://github.com/user-attachments/assets/df3f2452-077e-413d-95af-fb8fedbde10a)

![image](https://github.com/user-attachments/assets/5c248f46-0b82-4fb0-9738-2e7e854ea2f6)


