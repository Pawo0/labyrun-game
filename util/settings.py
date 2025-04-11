"""
This module contains the Settings class.
"""


class Settings:
    """
    This class manages game settings:
    - Screen size
    - Maze block size
    - Player size
    - Player speed
    """
    def __init__(self, width, height):
        # Maze settings
        self.maze_width = 19
        self.maze_height = 19

        self.screen_width = width
        self.screen_height = height

        self.block_size = min(
            self.screen_width // (self.maze_width * 2 + 3),
            self.screen_height // self.maze_height
        )

        self.player_width = self.block_size // 2
        self.player_height = self.block_size // 2

        self.player_speed = self.block_size // 8
