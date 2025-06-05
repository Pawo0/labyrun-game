"""
This module contains the logic utilized to generate a random maze using the Kruskal's algorithm.
"""

import json
import os
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


class MazeGenerator:
    """This class contains the logic to generate a random maze using Kruskal's algorithm."""

    @staticmethod
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

        if width % 4 != 3 or height % 4 != 3:
            raise ValueError("Maze dimensions must be equal to a multiple of 4 - 1.")

        maze = [[1 for _ in range(width)] for _ in range(height)]
        cells = [
            (row, col) for row in range(1, height, 2) for col in range(1, width, 2)
        ]
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

    @staticmethod
    def create_map(width, height):
        """
        Create a 2-player maze map consisting of two mazes with the given dimensions.

        :param width: The width of the maze (must be an odd integer).
        :param height: The height of the maze (must be an odd integer).

        :returns: The generated map as a 2D array.
        """
        maze = MazeGenerator.generate_maze(width, height)

        maze_map = [row + [1] * 3 + row[::-1] for row in maze]

        maze_map[height // 2 - 1][width : width + 3] = [0] * 3
        maze_map[height // 2][width - 1 : width + 4] = [0] * 5
        maze_map[height // 2 + 1][width : width + 3] = [0] * 3

        # todo change the file format to txt
        maze_json = {"maze": maze_map}

        directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".maps",
        )
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, "map.json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(maze_json, file, indent=2)

        return maze
