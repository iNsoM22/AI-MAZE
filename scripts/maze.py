import random


class Maze:
    UP: int = 1
    LEFT: int = 2
    DOWN: int = 3
    RIGHT: int = 4

    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.height, self.width = dimensions
        self.doors: list = []   # Stores the Doors Connection of the MAZE
        self.routes: list = []  # Stores the Doors Connection of the MAZE
        self.creator()

    def creator(self) -> None:
        # First Create a 2D Array with all elements as False/Zero
        visited = [[0 for _ in range(self.width)] for _ in range(self.height)]
        choices = [self.UP, self.LEFT, self.DOWN, self.RIGHT]

        # Use DFS algorithm to create the maze
        stack = [(-1, -1, 0, 0)]

        while len(stack) > 0:
            px, py, x, y = stack.pop()

            if not visited[x][y]:
                if px != -1 and py != -1:
                    self.doors.append(
                        (min(px, x), min(py, y), max(px, x), max(py, y)))
                    # Save route for actual path
                    self.routes.append((px, py, x, y))

                # Mark the Position as Visited
                # Then Select a new position to move to
                visited[x][y] = 1
                random.shuffle(choices)

                for move in choices:
                    match move:
                        case self.UP:
                            if y > 0 and not visited[x][y - 1]:
                                stack.append((x, y, x, y - 1))

                        case self.LEFT:
                            if x > 0 and not visited[x - 1][y]:
                                stack.append((x, y, x - 1, y))

                        case self.DOWN:
                            if y < self.width - 1 and not visited[x][y + 1]:
                                stack.append((x, y, x, y + 1))

                        case self.RIGHT:
                            if x < self.height - 1 and not visited[x + 1][y]:
                                stack.append((x, y, x + 1, y))

    def display_doors(self):
        """Display all the doors in the maze"""
        for door in self.doors:
            print(
                f"Door from ({door[0]}, {door[1]}) to ({door[2]}, {door[3]})")

    def display_routes(self):
        """Display the actual routes (path) created during DFS"""
        for route in self.routes:
            print(
                f"Route from ({route[0]}, {route[1]}) to ({route[2]}, {route[3]})")
