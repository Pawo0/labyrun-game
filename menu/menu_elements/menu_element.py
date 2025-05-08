"""
This module contains the MenuElement class.
"""

import pygame


class MenuElement:
    """
    Base class for all menu elements.
    """

    def __init__(self, main, text, x, y, active):
        self.main = main
        self.screen = main.screen
        self.text = text
        self.active = active
        self.font = pygame.font.SysFont("arialblack", 40)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.outline_color = (255, 255, 255)
        self.outline_color_active = (255, 0, 0)

    def draw(self):
        """
        Draws the element on the screen.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def is_hovered(self, mouse_pos):
        """
        Checks if the mouse is hovering over the element.
        """
        return self.rect.collidepoint(mouse_pos)
