"""
This module contains the Menu class.
"""
import pygame

from .button import Button


class MainMenu:
    """
    This class handles the main menu of the game.
    """
    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.items = ["Start", "Settings", "Quit"]
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
        self.text_width, self.text_height = self.font.size("LabyRun")
        self.text_color = (255, 255, 255)

    def draw(self):
        """
        Draws the menu on the screen.
        """
        text_render = self.font.render("LabyRun", True, self.text_color)
        self.screen.blit(text_render, (self.x - self.text_width // 2, self.ys[0]))

        for i, button in enumerate(self.buttons):
            button.active = i == self.selected
            button.draw()

    def _button_pressed(self):
        if self.selected == 0:
            self.main.game_state.run_game()
        elif self.selected == 1:
            pass
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
