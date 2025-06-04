"""
This module contains the GameState class.
"""

from menu import GameSettingsPage


class GameState:
    """
    This class provides the current state of the game.
    """

    def __init__(self, main):
        self.winner = None
        self.loser = None
        self.main = main

        # Here we define all possible states of the game for easier management
        # something like enum // for future improvements
        # TODO : przyjrzec sie temu, sprawdzanie eventow dla poszczegolnych stanow mozna wyodrebnic
        self.states = {
            "main_menu": "main_menu",
            "set_names": "set_names",
            "running": "running",
            "game_over": "game_over",
            "settings_menu": "settings_menu",
            "stats_menu": "stats_menu",
        }

        self.state = self.states["main_menu"]  # Default state is main_menu

        # state settingsów
        self.settings_states = {
            "main": "main",
            "maze_size": "maze_size",
            "power_ups": "power_ups",
            "player_controllers": "player_controllers",
        }
        self.settings_state = self.settings_states["main"]  # Default state is main

    def game_won(self, winner, loser):
        """
        Sets the game state to game over.
        """
        self.state = self.states["game_over"]  # Set state to game_over
        self.winner = winner
        self.loser = loser

        self.main.stats_manager.record_game_result(
            winner_name=self.winner.player_name,
            loser_name=self.loser.player_name,
            maze_width=self.main.settings.maze_width,
            maze_height=self.main.settings.maze_height,
        )

    def set_names(self):
        """
        Sets the game state to set names.
        """
        self.state = self.states["set_names"]  # Set state to set_names

    def run_game(self):
        """
        Sets the game state to running.
        """
        self.state = self.states["running"]  # Set state to running

        self.winner = None
        self.main.generate_maze()
        self.main.player1.reset()  # Reinitialize player1
        self.main.player2.reset()  # Reinitialize player2

        self.main.stats_manager.start_game_timer()

    def open_game_settings(self):
        """
        Otwiera stronę ustawień gry.
        """

        self.state = "settings_menu"
        self.settings_state = "game"
        self.main.current_menu = GameSettingsPage(self.main)

    def open_stats_menu(self):
        """
        Sets the game state to stats menu.
        """
        self.state = self.states["stats_menu"]

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

    #     state settingsow
    # TODO: do wyodregnienia w przyszlosci pewnie
    def open_settings(self):
        """
        Sets the game state to settings.
        """
        self.settings_state = self.settings_states["main"]

    def open_maze_size(self):
        """
        Sets the game state to maze size settings.
        """
        self.settings_state = self.settings_states["maze_size"]

    def get_current_settings_state(self):
        """
        Returns the current settings state.
        """
        return self.settings_state
