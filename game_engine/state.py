"""
This module contains the GameState class.
"""


class GameState:
    """
    This class manages the current state of the game.
    """

    def __init__(self, main):
        self.winner = None
        self.main = main

        # Here we define all possible states of the game for easier management
        # something like enum // for future improvements
        # todo : przyjrzec sie temu, oraz sprawdzanie eventow dla poszczegolnych stanow mozna wyodrebnic
        self.states = {
            "main_menu": "main_menu",
            "running": "running",
            "game_over": "game_over",
            "settings_menu": "settings_menu",
        }

        self.state = self.states["main_menu"]  # Default state is main_menu

    def game_won(self, winner):
        """
        Sets the game state to game over.
        """
        self.state = self.states["game_over"]  # Set state to game_over
        self.winner = winner


    def run_game(self):
        """
        Sets the game state to running.
        """
        self.state = self.states["running"]  # Set state to running

        self.winner = None
        self.main.player1.reset(self.main.player1_initial_position)
        self.main.player2.reset(self.main.player2_initial_position)
        self.main.generate_maze()

    def main_menu(self):
        """
        Sets the game state to main menu.
        """
        self.state = self.states["main_menu"]  # Set state to main_menu
        self.winner = None

    def open_settings_menu(self):
        """
        Sets the game state to settings.
        """
        self.state = self.states["settings_menu"]  # Set state to settings

    def get_current_state(self):
        """
        Returns the current game state.
        """
        return self.state
