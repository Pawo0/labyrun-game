"""
This module generates a 2-player maze map by creating two mazes of the same dimensions.
"""

import json
import os

from .maze_gen import generate_maze


def create_map(width, height):
    """
    Create a 2-player maze map consisting of two mazes with the given dimensions.

    :param width: The width of the maze (must be an odd integer).
    :param height: The height of the maze (must be an odd integer).

    :returns: The generated map as a 2D array.
    """
    maze = generate_maze(width, height)

    maze_map = [row + [1] * 3 + row[::-1] for row in maze]

    maze_map[height // 2 - 1][width : width + 3] = [0] * 3
    maze_map[height // 2][width - 1 : width + 4] = [0] * 5
    maze_map[height // 2 + 1][width : width + 3] = [0] * 3

    # todo change the file format to txt
    maze_json = {"maze": maze_map}

    directory = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "maps",
    )
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "map.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(maze_json, file, indent=2)

    return maze
