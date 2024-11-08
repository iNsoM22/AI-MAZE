from scripts.maze_generator import generator
from scripts.visualizer import MazeVisualizer

MAZE_SIZE = (20, 20)  # (Rows, Cols)
SCREEN_SIZE = (800, 800)
maze = generator(rows=MAZE_SIZE[0], cols=MAZE_SIZE[1])
visualizer = MazeVisualizer(dimensions=MAZE_SIZE, screen_size=SCREEN_SIZE)

visualizer.draw_maze(maze)
