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
        self.main = main
        # default maze size
        self.maze_width = 15
        self.maze_height = 15

        # set screen size
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()

        # players colors
        self.player1_color = "red"
        self.player2_color = "white"

        # set initial player positions
        self.player1_initial_position = None
        self.player2_initial_position = None

        # scale the maze size to fit the screen
        self.block_size = None
        self.player_width = None
        self.player_height = None
        self.player_speed = None
        self._calculate_block_size()

    def _calculate_block_size(self):
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

    def calculate_initial_positions(self):
        """
        Calculates the initial positions of the players.
        """
        left = self.main.maze.get_lower_left()
        right = self.main.maze.get_lower_right()
        block_size = self.block_size
        player_size = self.player_width

        left_x = left[0] + 1.5 * block_size - player_size // 2
        left_y = left[1] - 2 * block_size + player_size // 2
        right_x = right[0] - 2 * block_size + player_size // 2
        right_y = right[1] - 2 * block_size + player_size // 2

        self.player1_initial_position = (left_x, left_y)
        self.player2_initial_position = (right_x, right_y)

    def set_maze_size(self, width, height):
        """
        Sets the maze size.
        """
        self.maze_width = width
        self.maze_height = height
        self._calculate_block_size()
        self.calculate_initial_positions()
