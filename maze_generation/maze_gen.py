"""
This module contains the logic utilized to generate a random maze using the Kruskal's algorithm.
"""
import random


class FindUnion:
    """
    This class implements the Disjoint Set Union data structure with path compression and union
    by rank optimizations.
    """
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, item):
        """
        Finds the root of the set that contains the given item.
        Applies path compression to flatten the structure for faster future queries.

        :param item: The element to find.

        :returns parent: The root of the set containing 'item'.
        """
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, set1, set2):
        """
        Merges the sets containing 'set1' and 'set2'.
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


def generate_maze(width: int, height: int):
    """
    Generates a maze with given dimensions.

    :param width: The width of the maze (must be an odd integer).

    :param height: The height of the maze (must be an odd integer).

    :returns maze: The generated maze as a 2D array.
    
        1 -> wall
    
        0 -> corridor

    :raises keyError: Raises a keyError exception if the given dimensions do not meet the criteria.
    """

    if not (isinstance(width, int) and isinstance(height, int)):
        raise ValueError("Maze dimensions must be integers.")

    if width < 0 or height < 0:
        raise ValueError("Maze dimensions must be positive.")

    if width % 2 == 0 or height % 2 == 0:
        raise ValueError("Maze dimensions must be odd.")

    maze = [[1 for _ in range(width)] for _ in range(height)]
    cells = [(row, col) for row in range(1, height, 2) for col in range(1, width, 2)]
    walls = []

    for row, col in cells:
        maze[row][col] = 0

    fu = FindUnion(cells)

    for row, col in cells:
        if row + 2 < height:
            walls.append(((row + 1, col), (row, col), (row + 2, col)))
        if col + 2 < width:
            walls.append(((row, col + 1), (row, col), (row, col + 2)))

    random.shuffle(walls)

    for wall, cell1, cell2 in walls:
        if fu.find(cell1) != fu.find(cell2):
            row, col = wall
            maze[row][col] = 0
            fu.union(cell1, cell2)

    return maze


def print_maze(maze):
    """
    Prints the generated maze.
    """
    for row in maze:
        print("".join("  " if cell else "# " for cell in row))


# Test
if __name__ == "__main__":
    w, h = 51, 51
    m = generate_maze(w, h)
    print_maze(m)
