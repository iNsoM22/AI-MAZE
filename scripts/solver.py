from .maze import Maze
from .player import *
from collections import deque


class MazeSolver:

    def __init__(self, maze: Maze):
        self.population: deque[list[Player]] = deque([])
        self.curr_gen_best_players: list[Player] = []
        self.maze_conquered: bool = False
        self.best_player: Player = None
        self.conquerers: list[Player] = []

        self.maze = maze
        self.curr_generation = 0

    def simulate(self):
        while self.curr_generation < GENERATIONS:
            self.step()

    def step(self):
        if self.curr_generation == 0:
            self.initialize_population()
            self.curr_generation += 1

        if self.curr_generation < GENERATIONS and not self._are_players_moving():
            print("Current Generation:", self.curr_generation)
            self._produce_offsprings()

    def _are_players_moving(self):
        not_stuck = []
        for player in self.population[-1]:
            player.play()
            not_stuck.append(player.canwalk)
        return any(not_stuck)

    def initialize_population(self):
        population = self._population_generator(initial=True)
        self.population.append(population)

    def _euclidean_distance(self, agent_position: tuple[int, int]):
        x = (agent_position[0] - END_POINT[0])**2
        y = (agent_position[1] - END_POINT[1])**2
        return 1/(x + y)**0.5

    def _selection(self):
        """Selects the top half of the current players based on fitness."""
        self._generate_fitness()
        select = POPULATION_SIZE // 2
        top_players = sorted(self.population[-1], key=lambda x: x.fitness)
        self.curr_gen_best_players = top_players[:select]
        self.best_player = self.curr_gen_best_players[0]

    def _generate_fitness(self):
        """Updates the Fitness of each player in the current generation"""
        # Iterate over the players of latest generation
        for player in self.population[-1]:
            player_position = player.position
            distance = self._euclidean_distance(player_position)
            player.update_fitness(distance)

            if player.winner:
                self.maze_conquered = True
                self.conquerers.append(player)

    def _crossover(self, partner1, partner2):
        """Perform crossover between two players to create a child."""
        if not isinstance(partner1, Player) or not isinstance(partner2, Player):
            return None

        dominating_partner = max(partner1, partner2, key=lambda x: x.fitness)
        submissive_partner = min(partner1, partner2, key=lambda x: x.fitness)

        genes_1 = int(0.7 * len(dominating_partner.path))
        genes_2 = len(submissive_partner.path) - genes_1
        inherited_path = dominating_partner.path[:genes_1] + \
            submissive_partner.path[-genes_2:]

        child = Player(self.maze, self.curr_generation + 1, inherited_path)

        return child

    def _population_generator(self, initial=False):
        population = []
        for _ in range(POPULATION_SIZE):

            if not initial and len(self.curr_gen_best_players):
                partner1, partner2 = random.choices(
                    [*self.curr_gen_best_players, self.best_player], k=2)
                child = self._crossover(partner1, partner2)

                if child:
                    child.mutate()

            else:
                child = Player(self.maze, generation=self.curr_generation+1)

            population.append(child)

        return population

    def _produce_offsprings(self):
        """Produce Next Generation based on the selected candidates"""
        self._selection()
        new_generation = self._population_generator()
        self.curr_generation += 1
        self.curr_gen_best_players = []
        self.best_player = None
        self.population.append(new_generation)
        if len(self.population) >= 2:
            self.population.popleft()
