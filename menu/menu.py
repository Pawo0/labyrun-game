"""
This module contains the Menu class.
"""

import pygame

from .button import Button


# todo change comments to english
class Menu:
    """
    Base class for game menus.
    """

    def __init__(self, main, title, items):
        self.main = main
        self.screen = main.screen
        self.items = items
        # zaczynamy stawiac przyciski statyczne 225 pikseli od srodka ekranu
        self.ys = [self.screen.get_height() // 2 - 225]

        button_start_y = (
            self.screen.get_height() // 2 - 100
        )  # kazdy przycisk 100 pikseli nizej
        button_spacing = 100
        for i in range(len(items)):
            self.ys.append(button_start_y + i * button_spacing)

        self.x = self.screen.get_width() // 2
        self.selected = 0
        self.buttons = [
            Button(self.main, item, self.x, self.ys[i + 1], i == 0)
            for i, item in enumerate(self.items)
        ]
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont("arialblack", 40)
        self.title = title
        self.text_width, self.text_height = self.font.size(title)
        self.text_color = (255, 255, 255)

    def _button_pressed(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

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

    def draw(self):
        """
        Draws the menu on the screen.
        """
        text_render = self.font.render(self.title, True, self.text_color)
        self.screen.blit(text_render, (self.x - self.text_width // 2, self.ys[0]))

        for i, button in enumerate(self.buttons):
            button.active = i == self.selected
            button.draw()
