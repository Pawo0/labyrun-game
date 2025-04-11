"""
This module contains the GameState class.
"""


class GameState:
    """
    This class manages the current state of the game.
    """
    def __init__(self, main):
        self.running = False
        self.game_over = False
        self.winner = None
        self.main = main

    def game_won(self, winner):
        """
        Sets the game state to game over.
        """
        self.running = False
        self.game_over = True
        self.winner = winner

    def run_game(self):
        """
        Sets the game state to running.
        """
        self.running = True
        self.game_over = False
        self.winner = None
        self.main.player1.reset(self.main.player1_initial_position)
        self.main.player2.reset(self.main.player2_initial_position)

    def main_menu(self):
        """
        Sets the game state to main menu.
        """
        self.running = False
        self.game_over = False
        self.winner = None

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
