"""
This module contains the Button class.
"""

import pygame

from menu.menu_elements.menu_element import MenuElement


class Button(MenuElement):
    """
    This class creates buttons in the game menu.
    """

    def __init__(self, main, text, x, y, active):
        super().__init__(main, text, x, y, active)
        self.width, self.height = self.font.size(self.text)
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """
        Draws the button on the screen.
        """
        if self.active:
            pygame.draw.rect(
                self.screen,
                self.outline_color_active,
                (self.x - 5, self.y - 5, self.width + 10, self.height + 10),
            )
        else:
            pygame.draw.rect(
                self.screen,
                self.outline_color,
                (self.x - 5, self.y - 5, self.width + 10, self.height + 10),
            )
        pygame.draw.rect(
            self.screen,
            self.background_color,
            (self.x, self.y, self.width, self.height),
        )
        text_render = self.font.render(self.text, True, self.text_color)
        self.screen.blit(text_render, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        """
        Checks if the button is clicked.
        """
        return self.rect.collidepoint(mouse_pos)
