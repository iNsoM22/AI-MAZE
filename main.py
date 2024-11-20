from scripts.maze_generator import generator
from scripts.visualizer import MazeVisualizer
from scripts.solver import MazeSolver
from scripts.utils import (
    euclidean_distance,
    explorer,
    manhattan_distance,
    combine)
from config import MAZE_SIZE, SCREEN_SIZE

maze = generator(rows=MAZE_SIZE[0], cols=MAZE_SIZE[1], include_end=True)
visualizer = MazeVisualizer(
    dimensions=MAZE_SIZE, screen_size=SCREEN_SIZE, fps_adjustment=True)
visualizer.set_maze(maze)


def mixer(profile): return combine(profile,
                                   [euclidean_distance, explorer,
                                       manhattan_distance],
                                   [0.3, 0.15, 0.55])


solver = MazeSolver(
    maze, fitness_function=mixer, maximize_fitness=True)


visualizer.draw_solution(solver, path_offset=0.2)


print("Maze Conquered:", solver.maze_conquered)

if __name__ == "__main__":
    print("Starting the Program")
    print("-"*10)
