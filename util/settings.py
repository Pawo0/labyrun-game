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

    def __init__(self, main):
        # default maze size
        self.maze_width = 7
        self.maze_height = 7

        # set screen size
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()

        # scale the maze size to fit the screen
        self.block_size = None
        self.player_width = None
        self.player_height = None
        self.player_speed = None
        self.calculate_block_size()



    def calculate_block_size(self):
        """
        Calculates the block size based on the screen size and maze dimensions.
        """
        self.block_size = min(
            self.screen_width // (self.maze_width * 2 + 3),
            self.screen_height // self.maze_height
        )

        self.player_width = self.block_size // 2
        self.player_height = self.block_size // 2

        self.player_speed = self.block_size // 8

    def set_maze_size(self, width, height):
        """
        Sets the maze size.
        """
        self.maze_width = width
        self.maze_height = height
        self.calculate_block_size()
