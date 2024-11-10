from scripts.maze import Maze
import numpy as np
import time
import pickle
import os

SEED = 42

np.random.seed(SEED)


def generator(rows, cols, save_maze=False, save_path=None, include_end=False):
    start = time.time()
    maze = Maze((rows, cols))
    end = time.time()

    time_elapsed = end - start

    print(f"{rows}x{cols} Maze generated in {str(time_elapsed)}s.")
    if include_end:
        maze.routes.append((rows-1, cols-1, rows-1, cols))

    if save_maze:
        assert save_path != None
        with open(save_path, 'wb') as f:
            pickle.dump(maze, f)

        print(f"Generated Maze is saved in {save_path}")
    return maze


def loader(path: str):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            saved_maze = pickle.load(f)

        return saved_maze
    else:
        print(f"Path {path} does not exist")
