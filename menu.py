from button import Button
import pygame


class Menu:
    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.items = ["Start", "Settings", "Quit"]
        self.ys = [self.screen.get_height() // 2 - 100, self.screen.get_height() // 2,
                   self.screen.get_height() // 2 + 100]
        self.x = self.screen.get_width() // 2
        self.selected = 0
        self.buttons = [Button(self.main, item, self.x, self.ys[i], i == 0) for i, item in enumerate(self.items)]

    def draw(self):
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

