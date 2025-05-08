"""
This module contains the TextInput class.
"""

import pygame

from .menu_element import MenuElement


class TextInput(MenuElement):
    """
    This class creates a text input field.
    """

    def __init__(self, main, text, x, y, active):
        super().__init__(main, text, x, y, active)
        self.width = 300
        self.height = 50
        self.max_length = 15
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        """
        Handle keyboard events for text input.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            self.active = self.rect.collidepoint(event.pos)
            return self.active

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
            return True
        return False

    def draw(self):
        """
        Draw the text input field.
        """
        # Draw the input box background
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        # Draw border with appropriate color
        border_color = self.outline_color_active if self.active else self.outline_color
        pygame.draw.rect(self.screen, border_color, self.rect, 2)

        # Render and display the text
        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text vertically and align left with some padding
        text_pos = (
            self.x + 10,
            self.y + (self.height - text_surface.get_height()) // 2,
        )
        self.screen.blit(text_surface, text_pos)

    def get_text(self):
        """
        Get the current input text.
        """
        return self.text
