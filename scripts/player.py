from .maze import Maze
from config import *
import random
from collections import deque


class Player:
    MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, maze: Maze, generation: int, inherited_path: list = []):
        self.maze = maze
        self.generation = generation
        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.path = []
        self.position = STARTING_POINT
        self.fitness = 0
        self.canwalk = True
        self.winner = False
        self.inheritance = deque(inherited_path)

    def __str__(self):
        return f"{STARTING_POINT} Fitness: {self.fitness}"

    def _inside(self, x, y):
        """Check if the Player is inside the Maze bounds"""
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height

    def _next_move(self, move, pos=None) -> tuple:
        """Returns the next position based on current position and move"""
        x, y = self.position if pos is None else pos
        dx, dy = move
        dx += x
        dy += y
        return (dx, dy)

    def _is_move_valid(self, move):
        """Check if a move is allowed or not"""
        new_position = self._next_move(move)
        is_inside = self._inside(*new_position)
        is_not_reverse = new_position not in self.path

        is_not_wall = any(
            (door[0], door[1]) == self.position and (door[2], door[3]) == move
            for door in self.maze.doors
        )

        return is_inside and is_not_reverse and is_not_wall

    def _onestep(self):
        moved = False
        if len(self.inheritance):
            inherited_move = self.inheritance.popleft()

            if self._is_move_valid(inherited_move):
                self.position = inherited_move
                self.path.append(self.position)
                moved = True

        if not moved:
            valid_moves = list(
                filter(lambda x: self._is_move_valid(x), self.MOVES))

            if len(valid_moves) == 0:
                print("NOw NO Moves Left")
                self.canwalk = False
                return

            move = random.choice(valid_moves)
            move_to = self._next_move(move)
            self.position = move_to
            self.path.append(move_to)

        if self.position == END_POINT:
            self.canwalk = False
            self.winner = True

    def play(self):
        """Initiate player's movement sequence"""
        if self.canwalk:
            self._onestep()

    def mutate(self):
        """Mutate part of the inherited path for diversity"""
        for _ in range(int(len(self.inheritance) * MUTATION_RATE)):
            mutation_point = random.randint(5, len(self.inheritance) - 1)
            random_move = random.choice(self.MOVES)
            position = self.inheritance[mutation_point - 1]
            mutated_position = self._next_move(random_move, position)
            self.inheritance[mutation_point] = mutated_position

    def update_fitness(self, value):
        self.fitness = value

    def map_from_to(x, a, b, c, d):
        return (x-a)/(b-a)*(d-c)+c
