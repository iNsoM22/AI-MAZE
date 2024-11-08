import pygame
from .maze import Maze
from pygame.locals import *


class MazeVisualizer:
    def __init__(self, dimensions=(20, 20), screen_size=(800, 800), margin=100):
        pygame.init()

        self._dimensions = dimensions
        self._screen_size = screen_size
        self._margin = margin
        self._bgcolor = (100, 78, 32)
        self._white = (255, 255, 255)
        self._maze = None

        self._screen = pygame.display.set_mode(self._screen_size)
        self._clock = pygame.time.Clock()
        self._running = True

        self._cell_size = min((self._screen_size[0] - 2 * self._margin) // self._dimensions[0],
                              (self._screen_size[1] - 2 * self._margin) // self._dimensions[1])

        self.start = None
        self.end = None
        self._bx, self._by = ((self._screen_size[0] - self._cell_size * self._dimensions[0]) // 2,
                              (self._screen_size[1] - self._cell_size * self._dimensions[1]) // 2)

    def draw_maze(self, maze: Maze):
        """Display the _maze using Pygame."""
        if maze is None:
            return

        self._maze = maze
        while self._running:
            self._screen.fill(self._bgcolor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._draw_maze_walls()

            pygame.display.update()
            self._clock.tick(60)

        pygame.quit()

    def _draw_maze_walls(self):
        for x in range(self._dimensions[0]):
            for y in range(self._dimensions[1]):
                if not (x - 1, y, x, y) in self._maze.doors and not (x + y == 0):
                    pygame.draw.line(self._screen, self._white,
                                     (self._bx + x * self._cell_size,
                                      self._by + y * self._cell_size),
                                     (self._bx + x * self._cell_size, self._by + (y + 1) * self._cell_size))
                if not (x, y, x + 1, y) in self._maze.doors:
                    pygame.draw.line(self._screen, self._white,
                                     (self._bx + (x + 1) * self._cell_size,
                                      self._by + y * self._cell_size),
                                     (self._bx + (x + 1) * self._cell_size, self._by + (y + 1) * self._cell_size))
                if not (x, y - 1, x, y) in self._maze.doors:
                    pygame.draw.line(self._screen, self._white,
                                     (self._bx + x * self._cell_size,
                                      self._by + y * self._cell_size),
                                     (self._bx + (x + 1) * self._cell_size, self._by + y * self._cell_size))
                if not (x, y, x, y + 1) in self._maze.doors and not (x + y == self._dimensions[0] + self._dimensions[1] - 2):
                    pygame.draw.line(self._screen, self._white,
                                     (self._bx + x * self._cell_size,
                                      self._by + (y + 1) * self._cell_size),
                                     (self._bx + (x + 1) * self._cell_size, self._by + (y + 1) * self._cell_size))
