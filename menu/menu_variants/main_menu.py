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
        items = ["Start", "Settings", "Quit"]
        super().__init__(main, "LabyRun", items)

    def _button_pressed(self):
        """
        Handle button press based on selection.
        """
        if self.selected == 0:
            self.main.game_state.run_game()
        elif self.selected == 1:
            self.main.game_state.open_settings_menu()
        elif self.selected == 2:
            pygame.quit()
            sys.exit()
