"""
This module contains the GameOverMenu class.
"""

import sys

import pygame

from .menu import Menu


class GameOverMenu(Menu):
    """
    This class handles the game over menu.
    """

    def __init__(self, main):
        items = ["Play Again", "Main Menu", "Quit"]
        super().__init__(main, "Game Over", items)  # placeholder for title

    def _button_pressed(self):
        """
        Handle button press based on selection.
        """
        if self.selected == 0:
            self.main.game_state.run_game()
        elif self.selected == 1:
            self.main.game_state.main_menu()
        elif self.selected == 2:
            pygame.quit()
            sys.exit()

    def draw(self):
        """
        Draws the menu on the screen, with dynamically updated winner text.
        """
        self.title = (
            f"{self.main.game_state.winner.player_name} Wins!"
        )
        self.text_width, self.text_height = self.font.size(self.title)
        super().draw()
