from .maze import Maze
from .player import *
from collections import deque
from typing import Callable
import random
from time import sleep


class MazeSolver:
    def __init__(self, maze: Maze, fitness_function: Callable, maximize_fitness: bool = False):
        self.population: deque[list[Player]] = deque([])
        self.curr_gen_best_players: list[Player] = []
        self.maze_conquered: bool = False
        self.best_player: Player = None

        self.maze = maze
        self.curr_generation = 0
        self.fitness_function = fitness_function
        self.maximize_fitness = maximize_fitness
        self.moving_players: list = []

    def simulate(self):
        while self.curr_generation < GENERATIONS:
            self.step()

    def step(self):
        if self.curr_generation == 0:
            self.initialize_population()

        if self.curr_generation < GENERATIONS and not self._are_players_moving():
            self._selection()
            print("Current Generation:", self.curr_generation)
            if self.best_player:
                print("Best Player Fitness:", self.best_player.fitness)
            print("-" * 10)
            sleep(1)
            self._produce_offsprings()

    def _are_players_moving(self):
        population = self.population[-1]
        for idx in self.moving_players:
            player = population[idx]
            player.play()
            if not player.canwalk:
                self.moving_players.remove(idx)
        return len(self.moving_players) > 0

    def initialize_population(self):
        population = self._population_generator(initial=True)
        self.population.append(population)
        self.curr_generation += 1

    def _selection(self):
        """Selects the top half of the current players based on fitness."""
        self._generate_fitness()
        select = POPULATION_SIZE // 2
        top_players = sorted(
            [*self.population[-1]], key=lambda x: x.fitness, reverse=self.maximize_fitness
        )
        self.curr_gen_best_players = top_players[:select]
        if self.curr_gen_best_players:
            current_best = self.curr_gen_best_players[0]
            if not self.best_player or current_best.fitness > self.best_player.fitness:
                self.best_player = current_best

    def _generate_fitness(self):
        """Updates the Fitness of each player in the current generation."""
        for player in self.population[-1]:
            f_value = self.fitness_function(player)
            player.update_fitness(f_value)

            if player.winner:
                self.maze_conquered = True

    def _crossover(self, partner1: Player, partner2: Player):
        """Perform crossover between two players to create a child."""
        dominating_partner = max(partner1, partner2, key=lambda x: x.fitness)

        index = int(0.7 * len(dominating_partner.path))
        genes_1 = partner1.path[:index]
        genes_2 = partner2.path[-index:]
        inherited_path = list(genes_1 + genes_2)

        child = Player(self.maze, self.curr_generation + 1, inherited_path)
        return child

    def _population_generator(self, initial=False) -> list[Player]:
        population = []
        self.moving_players.clear()
        for _ in range(POPULATION_SIZE):
            if not initial:
                parentA = random.choice(
                    [*self.curr_gen_best_players, self.best_player])
                parentB = random.choice(
                    [*self.curr_gen_best_players, self.best_player])
                child = self._crossover(parentA, parentB)
                if child:
                    child.mutate()
            else:
                child = Player(self.maze, generation=self.curr_generation + 1)

            if child:
                population.append(child)
        self.moving_players.extend([*range(len(population))])
        return population

    def _produce_offsprings(self):
        """Produce Next Generation based on the selected candidates."""
        new_generation = self._population_generator()
        self.population.append(new_generation)

        if len(self.population) > 2:
            self.population.popleft()

        self.curr_generation += 1
        self.curr_gen_best_players.clear()
