import random


class Maze:
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

    def __init__(self, dimensions) -> None:
        self.dimensions = dimensions
        self.doors = []
        self.creator()

    def creator(self):
        # First Create a 2D Array with all elements as False/Zero
        visited = [[0 for _ in range(self.dimensions[1])]
                   for _ in range(self.dimensions[0])]
        choices = [self.UP, self.LEFT, self.DOWN, self.RIGHT]

        # Now Use the DFS Algorithm to iterate and create a Maze
        stack = [(-1, -1, 0, 0)]

        while len(stack) > 0:

            px, py, x, y = stack.pop()

            if not visited[x][y]:
                if px != -1 and py != -1:
                    self.doors.append(
                        (min(px, x), min(py, y), max(px, x), max(py, y)))

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
                            if y < self.dimensions[1] - 1 and not visited[x][y + 1]:
                                stack.append((x, y, x, y + 1))

                        case self.RIGHT:
                            if x < self.dimensions[0] - 1 and not visited[x + 1][y]:
                                stack.append((x, y, x + 1, y))
