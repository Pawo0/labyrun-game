"""
This module contains the GameState class.
"""


class GameState:
    """
    This class manages the current state of the game.
    """
    def __init__(self):
        self.running = False
        self.game_over = False

    def game_won(self):
        """
        Sets the game state to game over.
        """
        self.running = False
        self.game_over = True

    def run_game(self):
        """
        Sets the game state to running.
        """
        self.running = True

    def is_running(self):
        """
        Returns the current game state.
        """
        return self.running

    def is_game_over(self):
        """
        Returns the current game state.
        """
        return self.game_over
