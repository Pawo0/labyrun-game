"""
This module contains the Engine class
"""

import sys

import pygame

from .state_manager import GameStateManager


class Engine:
    """This class manages the main loop and game events."""

    def __init__(self, main):
        self.main = main
        self.win_zone = self._calculate_win_zone()
        self.state_manager = GameStateManager(main)

    def check_win_condition(self):
        """Checks if any player has won the game."""
        left_zone, right_zone = self.win_zone
        if self.main.player1.x > left_zone:
            self.main.game_state.game_won(self.main.player1, self.main.player2)
        if self.main.player2.x < right_zone:
            self.main.game_state.game_won(self.main.player2, self.main.player1)

    def update_win_zone(self):
        """Updates the win zone based on the current screen size."""
        self.win_zone = self._calculate_win_zone()

    def run(self):
        """Main loop of the game."""
        while True:
            self._check_events()

            self.main.screen.fill((0, 0, 0))

            self.state_manager.draw_current_state()

            pygame.display.flip()
            self.main.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

            self.state_manager.handle_event(event)

    def _calculate_win_zone(self):
        mid = self.main.settings.screen_width // 2
        block_size = self.main.settings.block_size

        return (
            mid - block_size * 1.5 - self.main.settings.player_width // 2,
            mid + block_size * 1.5 - self.main.settings.player_width // 2,
        )
