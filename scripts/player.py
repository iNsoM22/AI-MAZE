from .maze import Maze
from config import *
import random
from collections import deque


class Player:
    MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, maze: Maze, generation: int, inherited_path: list = []):
        self.maze = maze
        self.generation = generation
        self.color = (random.randrange(0, 255), random.randrange(
            0, 255), random.randrange(0, 255))
        self.path = []
        self.position = STARTING_POINT
        self.fitness = 0
        self.canwalk = True
        self.winner = False
        self.inheritance = deque(inherited_path)

    def __str__(self):
        return str(STARTING_POINT)+" Fitness: "+str(self.fitness)

    def _inside(self, x, y):
        """Checks if the Player is inside the Maze

        Args:
            y (int): Current Y Position of the Agent
            x (int): Current X Position of the Agent

        Returns:
            bool: returns True if the player is in valid position
        """
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height

    def _next_move(self, move) -> tuple[int, int]:
        """Returns the next move of the Player"""
        x, y = self.position
        dx, dy = move
        return x + dx, y + dy

    def _is_move_valid(self, move):
        """Check if a move is allowed or not"""
        new_position = self._next_move(move)
        is_inside = self._inside(*new_position)
        is_not_reverse = new_position not in self.path

        is_not_wall = False
        for door in self.maze.doors:
            if (door[0] == self.position[0] and door[1] == self.position[1] and door[2] == new_position[0] and door[3] == new_position[1]):
                is_not_wall = True

        return is_inside and is_not_reverse and is_not_wall

    def _onestep(self):
        if len(self.inheritance) > 0:
            inherited_move = self.inheritance.popleft()

            if self._is_move_valid(inherited_move):
                self.position = inherited_move
                self.path.append(self.position)

            else:
                self.canwalk = False

        else:
            valid_moves = [
                move for move in self.MOVES if self._is_move_valid(move)
            ]

            if len(valid_moves) == 0:
                self.canwalk = False
                return

            move_to = self._next_move(random.choice(valid_moves))
            self.position = move_to
            self.path.append(move_to)

        if self.position == END_POINT:
            self.canwalk = False
            self.winner = True

    def play(self):
        """Start the Sequence of Player Moves"""
        if self.canwalk:
            self._onestep()

    def mutate(self):
        for _ in range(int(len(self.inheritance) * MUTATION_RATE)):
            if len(self.path) > 2:
                mutation_point = random.randint(2, len(self.inheritance) - 1)
                random_move = random.choice(self.MOVES)
                if self._is_move_valid(random_move):
                    self.inheritance[mutation_point] = self._next_move(
                        random_move)

    def update_fitness(self, value: float):
        if value >= 0:
            self.fitness = value
