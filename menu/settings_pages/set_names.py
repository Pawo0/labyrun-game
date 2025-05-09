"""
This module contains the SetNames class for player name input.
"""

import pygame

from menu.menu_elements import Button, TextInput


class SetNames:
    """
    This class handles the player name input menu.
    """

    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.font = pygame.font.SysFont("arialblack", 40)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2

        self.title_pos = (
            center_x - self.font.size("Set Player Names")[0] // 2,
            screen_height // 6,
        )

        vertical_center = screen_height // 2
        vertical_spacing = 120

        p1_y = vertical_center - vertical_spacing
        p2_y = vertical_center + 20

        label_x = center_x - 300
        input_x = center_x + 130

        self.p1_input = TextInput(main, "", input_x, p1_y, True)
        self.p2_input = TextInput(main, "", input_x, p2_y, False)
        self.play_button = Button(
            main, "Play!", center_x, p2_y + vertical_spacing, True
        )

        self.labels = [
            ("Set Player Names", self.title_pos),
            (
                "Player 1:",
                (
                    label_x - self.font.size("Player 1:")[0] // 2,
                    p1_y - self.font.size("Player 1:")[1] // 2,
                ),
            ),
            (
                "Player 2:",
                (
                    label_x - self.font.size("Player 2:")[0] // 2,
                    p2_y - self.font.size("Player 2:")[1] // 2,
                ),
            ),
        ]

        self.active_input = 1

    def handle_events(self, event):
        """
        Handle events for the name input screen.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.is_clicked(event.pos):
                self._play()
            if self.p1_input.handle_event(event):
                self.active_input = 1
                self.p2_input.active = False
            elif self.p2_input.handle_event(event):
                self.active_input = 2
                self.p1_input.active = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.active_input = 1
                self.p1_input.active = True
                self.p2_input.active = False
            elif event.key == pygame.K_DOWN:
                self.active_input = 2
                self.p1_input.active = False
                self.p2_input.active = True
            elif event.key == pygame.K_TAB:
                self.active_input = 2 if self.active_input == 1 else 1
                self.p1_input.active = not self.p1_input.active
                self.p2_input.active = not self.p2_input.active
            elif event.key == pygame.K_RETURN:
                self._play()
            else:
                if self.active_input == 1:
                    self.p1_input.handle_event(event)
                elif self.active_input == 2:
                    self.p2_input.handle_event(event)

    def _play(self):
        p1_name = self.p1_input.get_text() or "Player 1"
        p2_name = self.p2_input.get_text() or "Player 2"
        self.main.player1.set_name(p1_name)
        self.main.player2.set_name(p2_name)
        self.main.game_state.run_game()

    def draw(self):
        """
        Draw the name input menu screen.
        """

        for text, pos in self.labels:
            self.screen.blit(self.font.render(text, True, (255, 255, 255)), pos)

        self.p1_input.draw()
        self.p2_input.draw()
        self.play_button.draw()
