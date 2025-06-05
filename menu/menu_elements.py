"""
This module contains the MenuElement class.
"""

import pygame


class MenuElement:
    """Base class for all menu elements."""

    def __init__(self, main, text, active):
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
        """Draw the element on the screen."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def is_hovered(self, mouse_pos):
        """Check if the mouse is hovering over the element."""
        return self.rect.collidepoint(mouse_pos)


class Button(MenuElement):
    """This class creates buttons in the game menu."""

    def __init__(self, main, text, x, y, active):
        super().__init__(main, text, active)
        self.width, self.height = self.font.size(self.text)
        self.width += 20
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """Draw the button on the screen."""
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
        self.screen.blit(text_render, (self.x + 10, self.y))

    def is_clicked(self, mouse_pos):
        """Check if the button is clicked."""
        return self.rect.collidepoint(mouse_pos)


class TextInput(MenuElement):
    """This class creates a text input field."""

    def __init__(self, main, text, x, y, active):
        super().__init__(main, text, active)
        self.width = 620
        self.height = 50
        self.max_length = 15
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        """Handle keyboard and mouse events for text input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        """Draw the text input field."""
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        border_color = self.outline_color_active if self.active else self.outline_color
        pygame.draw.rect(self.screen, border_color, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text vertically and align left with some padding
        text_pos = (
            self.x + 10,
            self.y + (self.height - text_surface.get_height()) // 2,
        )
        self.screen.blit(text_surface, text_pos)

    def get_text(self):
        """Get the current input text."""
        return self.text
