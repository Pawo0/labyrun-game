"""
This module contains the GameOverMenu class.
"""
import pygame

from .button import Button


class GameOverMenu:
    """
    This class handles the game over menu.
    """
    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.items = ["Play Again", "Main Menu", "Quit"]
        self.ys = [self.screen.get_height() // 2 - 225,
                   self.screen.get_height() // 2 - 100,
                   self.screen.get_height() // 2,
                   self.screen.get_height() // 2 + 100]
        self.x = self.screen.get_width() // 2
        self.selected = 0
        self.buttons = [Button(self.main, item, self.x, self.ys[i + 1], i == 0)
                        for i, item in enumerate(self.items)]
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont('arialblack', 40)
        self.text_width, self.text_height = self.font.size(
            f"{"Player 1" if self.main.game_state.winner == 1 else "Player 2"} Wins!"
        )
        self.text_color = (255, 255, 255)


    def draw(self):
        """
        Draws the menu on the screen.
        """
        text_render = self.font.render(
            f"{"Player 1" if self.main.game_state.winner == 1 else "Player 2"} Wins!",
            True,
            self.text_color
        )
        self.screen.blit(text_render, (self.x - self.text_width // 2, self.ys[0]))

        for i, button in enumerate(self.buttons):
            button.active = i == self.selected
            button.draw()

    def _button_pressed(self):
        if self.selected == 0:
            self.main.game_state.run_game()
        elif self.selected == 1:
            self.main.game_state.main_menu()
        elif self.selected == 2:
            pygame.quit()

    def handle_events(self, event):
        """
        Handles events for the menu.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                self._button_pressed()

        elif event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button.is_hovered(event.pos):
                    self.selected = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    self._button_pressed()
                    break
