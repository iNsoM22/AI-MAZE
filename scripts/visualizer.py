import pygame
from .maze import Maze
from pygame.locals import *
import random
import time
from config import POPULATION_SIZE, MAX_PENALITY


class MazeVisualizer:
    def __init__(self, dimensions=(20, 20), screen_size=(800, 800), margin=70, fps=30, fps_adjustment=False, lines_width: int = 1):
        pygame.init()

        self._dimensions = dimensions
        self._screen_size = screen_size
        self._margin = margin
        self._fps = fps
        self.fps_adjustment = fps_adjustment
        self._bgcolor = (100, 78, 32)
        self._white = (255, 255, 255)
        self._maze = None

        self._screen = pygame.display.set_mode(self._screen_size)
        self._clock = pygame.time.Clock()
        self._running = True
        self.font = pygame.font.Font(None, 36)
        self._maze_line_width = lines_width
        self.bg_image = pygame.image.load("resources/BG.jpg")

        self._cell_size = min(
            (self._screen_size[0] - 2 * self._margin) // self._dimensions[0],
            (self._screen_size[1] - 2 * self._margin) // self._dimensions[1]
        )

        self._center_offset_x = (
            self._screen_size[0] - self._dimensions[0] * self._cell_size) // 2
        self._center_offset_y = (
            self._screen_size[1] - self._dimensions[1] * self._cell_size) // 2

    def draw_maze(self):
        """Display the maze and walls using Pygame."""
        while self._running:
            self._screen.fill(self._bgcolor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._draw_maze_walls()
            pygame.display.update()
            self._clock.tick(self._fps)

        pygame.quit()

    def _build_generation_history(self, solver, offset: float):
        """Build or update history of all players' paths across generations."""
        self._generation_history = {}
        self.current_generation = solver.curr_generation
        for player_idx in range(POPULATION_SIZE):
            profile = {
                "color": self._generate_random_color(),
                "offset": player_idx * offset,
                # Start from (0, 0) or any valid start position
                "path": [(0, 0)],
            }

            self._generation_history[player_idx] = profile

    def draw_solution(self, solver, path_offset: float = 0.7):
        """Visualize each player's path from the current generation using solver's step method."""
        self._build_generation_history(solver, path_offset)

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if self.fps_adjustment:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self._fps += 5
                        elif event.key == pygame.K_DOWN:
                            self._fps = max(1, self._fps - 5)

            self._screen.blit(self.bg_image, (0, 0))
            gen_text = self.font.render(
                f"Generation Count: {self.current_generation}", True, self._white)

            self._screen.blit(gen_text, (self._center_offset_x, 30))
            self._draw_maze_walls()
            pygame.display.update()

            solver.step()

            if solver.curr_generation != self.current_generation:
                del self._generation_history
                self._build_generation_history(solver, path_offset)
                self.clear_paths()

            population = solver.population[-1]
            for idx in self._generation_history.keys():
                player = population[idx]
                player_profile = self._generation_history.get(idx, None)
                if player_profile:
                    self._draw_players(player_profile, player)

            pygame.display.update()
            self._clock.tick(self._fps)

        pygame.quit()

    def set_maze(self, maze: Maze):
        """Set the maze to visualize."""
        if maze is None:
            return
        self._maze = maze

    def _generate_random_color(self):
        """Generate a random color for visualizing player paths."""
        return random.randint(20, 255), random.randint(20, 255), random.randint(20, 255)

    def _draw_maze_walls(self):
        """Draw the walls and doors of the maze."""
        for x in range(self._dimensions[0]):
            for y in range(self._dimensions[1]):
                if not (x - 1, y, x, y) in self._maze.doors and not (x + y == 0):
                    pygame.draw.line(self._screen, self._white,
                                     (self._center_offset_x + x * self._cell_size,
                                      self._center_offset_y + y * self._cell_size),
                                     (self._center_offset_x + x * self._cell_size, self._center_offset_y + (y + 1) * self._cell_size), self._maze_line_width)
                if not (x, y, x + 1, y) in self._maze.doors:
                    pygame.draw.line(self._screen, self._white,
                                     (self._center_offset_x + (x + 1) * self._cell_size,
                                      self._center_offset_y + y * self._cell_size),
                                     (self._center_offset_x + (x + 1) * self._cell_size, self._center_offset_y + (y + 1) * self._cell_size), self._maze_line_width)
                if not (x, y - 1, x, y) in self._maze.doors:
                    pygame.draw.line(self._screen, self._white,
                                     (self._center_offset_x + x * self._cell_size,
                                      self._center_offset_y + y * self._cell_size),
                                     (self._center_offset_x + (x + 1) * self._cell_size, self._center_offset_y + y * self._cell_size), self._maze_line_width)
                if not (x, y, x, y + 1) in self._maze.doors and not (x + y == self._dimensions[0] + self._dimensions[1] - 2):
                    pygame.draw.line(self._screen, self._white,
                                     (self._center_offset_x + x * self._cell_size,
                                      self._center_offset_y + (y + 1) * self._cell_size),
                                     (self._center_offset_x + (x + 1) * self._cell_size, self._center_offset_y + (y + 1) * self._cell_size), self._maze_line_width)

    def _draw_players(self, profile, player):
        """Draw a player's path in the maze with offset for visual separation."""
        offset = profile.get(
            "offset")  # Offset to separate players' paths visually
        color = profile.get("color")  # Color of the player's path
        path = profile.get("path")  # Player's path

        if player.fitness <= MAX_PENALITY or not player.canwalk:
            color = (255, 0, 0)
            profile["color"] = color

        if player.winner:
            color = (0, 255, 20)
            profile["color"] = color

        if player.position not in path:
            path.append(player.position)

        # Draw each segment of the player's path
        for i in range(len(path) - 1):
            start_x = path[i][0]*self._cell_size + self._cell_size // 2.5
            start_y = path[i][1]*self._cell_size + self._cell_size // 2.5
            end_x = path[i + 1][0]*self._cell_size + self._cell_size // 2.5
            end_y = path[i + 1][1]*self._cell_size + self._cell_size // 2.5

            start_x += offset + self._center_offset_x
            start_y += offset + self._center_offset_y
            end_x += offset + self._center_offset_x
            end_y += offset + self._center_offset_y

            # Draw the line segment of the path
            pygame.draw.line(self._screen, color,
                             (start_x, start_y), (end_x, end_y), 5)

    def clear_paths(self):
        """Clear all player paths to prepare for the next generation visualization."""
        self._screen.blit(self.bg_image, (0, 0))
        self._draw_maze_walls()
        pygame.display.update()
        self._clock.tick(self._fps)
