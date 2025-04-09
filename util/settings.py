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
    def __init__(self):
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080

        # Player settings
        self.player_speed = 5
        self.player_width = 15
        self.player_height = 15

        # Maze settings
        self.block_size = 35

    def get_screen_size(self):
        """
        Returns the width and height of the screen
        """
        return self.screen_width, self.screen_height

    def set_screen_size(self, width, height):
        """
        Sets the width and height of the screen
        """
        self.screen_width = width
        self.screen_height = height
