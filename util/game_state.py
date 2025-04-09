"""
This module contains the GameState class.
"""


class GameState:
    """
    This class manages the current state of the game.
    """
    def __init__(self):
        self.running = False

    def game_over(self):
        """
        Sets the game state to game over.
        """
        self.running = False

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
