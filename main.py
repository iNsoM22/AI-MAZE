from scripts.maze_generator import generator
from scripts.visualizer import MazeVisualizer
from scripts.solver import MazeSolver

MAZE_SIZE = (20, 20)  # (Rows, Cols)
SCREEN_SIZE = (800, 800)
maze = generator(rows=MAZE_SIZE[0], cols=MAZE_SIZE[1])
visualizer = MazeVisualizer(dimensions=MAZE_SIZE, screen_size=SCREEN_SIZE)
visualizer.set_maze(maze)

solver = MazeSolver(maze)

visualizer.draw_solution(solver, path_offset=0.9)

print("Maze Conquered:", solver.maze_conquered)
print("Maze Conquerers:", solver.conquerers)
