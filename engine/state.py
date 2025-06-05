"""
This module contains the GameState class.
"""


class GameState:
    """
    This class provides the current state of the game.
    """

    def __init__(self, main):
        self.winner = None
        self.loser = None
        self.main = main

        self.state = "main_menu" # Default state is main_menu
        self.settings_state = "main" # Default state is main

    def game_won(self, winner, loser):
        """
        Sets the game state to game over.
        """
        self.state = "game_over"  # Set state to game_over
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
        self.state = "set_names"  # Set state to set_names

    def run_game(self):
        """
        Sets the game state to running.
        """
        self.state = "running"  # Set state to running

        self.winner = None
        self.main.generate_maze()
        self.main.player1.reset()  # Reinitialize player1
        self.main.player2.reset()  # Reinitialize player2

        self.main.stats_manager.start_game_timer()

    def open_stats_menu(self):
        """
        Sets the game state to stats menu.
        """
        self.state = "stats_menu"

    def main_menu(self):
        """
        Sets the game state to main menu.
        """
        self.state = "main_menu"  # Set state to main_menu
        self.winner = None

    def open_settings_menu(self):
        """
        Sets the game state to settings.
        """
        self.state = "settings_menu"  # Set state to settings

    def get_current_state(self):
        """
        Returns the current game state.
        """
        return self.state

    def open_settings(self):
        """
        Sets the game state to settings.
        """
        self.settings_state = "main"

    def open_game_settings(self):
        """
        Sets the game state to maze size settings.
        """
        self.settings_state = "game"

    def open_powerup_settings(self):
        """
        Sets the game state to game settings.
        """
        self.settings_state = "power_ups"

    def open_event_settings(self):
        """
        Sets the game state to event settings.
        """
        self.settings_state = "events"

    def get_current_settings_state(self):
        """
        Returns the current settings state.
        """
        return self.settings_state
