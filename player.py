import pygame


class Player:
    def __init__(self, main, x, y, color="white"):
        self.main = main
        self.settings = main.settings
        self.screen = main.screen

        self.x = x
        self.y = y

        self.speed = self.settings.player_speed
        self.width = self.settings.player_width
        self.height = self.settings.player_height
        self.color = color
        self.movings = {"up": False, "down": False, "left": False, "right": False}

    def update(self):
        new_x = self.x
        new_y = self.y

        if self.movings["up"]:
            new_y = self.y - self.speed if self.y - self.speed > 0 else 0
        if self.movings["down"]:
            new_y = self.y + self.speed \
                if self.y + self.speed < self.screen.get_height() - self.height \
                else self.screen.get_height() - self.height
        if self.movings["left"]:
            new_x = self.x - self.speed if self.x - self.speed > 0 else 0
        if self.movings["right"]:
            new_x = self.x + self.speed \
                if self.x + self.speed < self.screen.get_width() - self.width \
                else self.screen.get_width() - self.width
        tmp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
        tmp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
        if not self.main.maze.check_collision(tmp_rect_x):
            self.x = new_x
        if not self.main.maze.check_collision(tmp_rect_y):
            self.y = new_y
        # self.x = new_x
        # self.y = new_y

        self.draw()

    def draw(self):
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))
