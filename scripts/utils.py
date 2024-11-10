from config import END_POINT, MAZE_SIZE
from scripts.player import Player
from typing import Callable


def manhattan_distance(agent: Player) -> float:
    distance = abs(
        agent.position[0] - END_POINT[0]) + abs(agent.position[1] - END_POINT[1])
    return distance


def euclidean_distance(agent: Player) -> float:
    x = (agent.position[0] - END_POINT[0])**2
    y = (agent.position[1] - END_POINT[1])**2
    return (x + y)**0.5


def explorer(agent: Player) -> float:
    exploration_score = (MAZE_SIZE[0] * MAZE_SIZE[1]) - len(agent.path)
    return exploration_score


def combine(agent: Player, fitness_functions: list[Callable], weights: list):
    f_value = 0
    for func, weight in zip(fitness_functions, weights):
        f_value = f_value + func(agent)*weight
    return f_value
