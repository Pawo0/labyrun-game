"""
This script provides a visual representation of the maze generation process.
"""
import random

import pygame


CELL_SIZE = 20
MAZE_WIDTH = 51
MAZE_HEIGHT = 51

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)


pygame.init()
screen = pygame.display.set_mode((MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))


class FindUnion:
    """
    A class that implements the Disjoint Set Union data structure with path compression and union
    by rank optimizations.
    """
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, item):
        """
        Find the root of the set that contains the given item.
        Applies path compression to flatten the structure for faster future queries.

        :param item: The element to find.

        :returns parent: The root of the set containing 'item'.
        """
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, set1, set2):
        """
        Merge the sets containing 'set1' and 'set2'.
        Uses union by rank to keep the tree shallow.

        :param set1: An element in the first set.
        :param set2: An element in the second set.

        :returns: None
        """
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1


def draw_maze(maze):
    """
    Draws the maze on the screen.
    """
    screen.fill(BLACK)
    for r in range(MAZE_HEIGHT):
        for c in range(MAZE_WIDTH):
            if not maze[r][c]:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    pygame.display.flip()


def generate_maze():
    """
    Generate a maze with given dimensions.

    :param width: The width of the maze (must be an odd integer).

    :param height: The height of the maze (must be an odd integer).

    :returns maze: The generated maze as a 2D array.
    
        1 -> wall
    
        0 -> corridor

    :raises keyError: Raises a keyError exception if the given dimensions do not meet the criteria.
    """
    maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    cells = [(r, c) for r in range(1, MAZE_HEIGHT, 2) for c in range(1, MAZE_WIDTH, 2)]
    walls = []

    for r, c in cells:
        maze[r][c] = 0

    uf = FindUnion(cells)

    for r, c in cells:
        if r + 2 < MAZE_HEIGHT:
            walls.append(((r + 1, c), (r, c), (r + 2, c)))
        if c + 2 < MAZE_WIDTH:
            walls.append(((r, c + 1), (r, c), (r, c + 2)))

    random.shuffle(walls)

    draw_maze(maze)

    for wall, cell1, cell2 in walls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []

        if uf.find(cell1) != uf.find(cell2):
            r, c = wall
            maze[r][c] = 0
            uf.union(cell1, cell2)
            draw_maze(maze)

    return maze


generate_maze()


if __name__ == "__main__":
    RUNNING = True
    while RUNNING:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                RUNNING = False

    pygame.quit()
