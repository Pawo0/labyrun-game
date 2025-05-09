"""
This module contains the MainMenu class.
"""

import sys

import pygame

from .menu_base import Menu


class MainMenu(Menu):
    """
    This class handles the main menu of the game.
    """

    def __init__(self, main):
        items = ["Start", "Leaderboard", "Settings", "Quit"]
        super().__init__(main, "LabyRun", items)

    def _button_pressed(self):
        """
        Handle button press based on selection.
        """
        match self.selected:
            case 0:
                self.main.game_state.set_names()
            case 1:
                self.main.game_state.open_stats_menu()
            case 2:
                self.main.game_state.open_settings_menu()
            case 3:
                pygame.quit()
                sys.exit()
