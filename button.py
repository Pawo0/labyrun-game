import pygame


class Button:
    def __init__(self, main, text, x, y, active):
        self.main = main
        self.screen = main.screen
        self.text = text
        self.active = active
        self.font = pygame.font.SysFont('arialblack', 40)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.outline_color = (255, 255, 255)
        self.outline_color_active = (255, 0, 0)
        self.width, self.height = self.font.size(self.text)
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.outline_color_active, (self.x - 5, self.y - 5, self.width + 10, self.height + 10))
        else:
            pygame.draw.rect(self.screen, self.outline_color, (self.x - 5, self.y - 5, self.width + 10, self.height + 10))
        pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height))
        text_render = self.font.render(self.text, True, self.text_color)
        self.screen.blit(text_render, (self.x, self.y))
