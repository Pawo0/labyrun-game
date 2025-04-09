"""
This module generates a 2-player maze map by creating two mazes of the same dimensions.
"""
import json

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

    maze_map[height // 2 - 1][width:width+3] = [0] * 3
    maze_map[height // 2][width-1:width+4] = [0] * 5
    maze_map[height // 2 + 1][width:width+3] = [0] * 3

    maze_json = {
        "maze": maze_map
    }

    with open("maps/map.json", "w", encoding="utf-8") as file:
        json.dump(maze_json, file, indent=2)
