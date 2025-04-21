"""
This module contains the Player class.
"""
import pygame


class Player:
    """
    This class represents the player in the game. 
    It handles position, movement, and draws the player on the screen.
    """

    def __init__(self, main, player=1):
        self.main = main
        self.settings = main.settings
        self.screen = main.screen

        self.speed = self.settings.player_speed
        self.width = self.settings.player_width
        self.height = self.settings.player_height
        self.movements = {"up": False, "down": False, "left": False, "right": False}

        # depending on the player, set the color and initial position
        self.player = player
        if player == 1:
            self.color = self.settings.player1_color
            self.pos = self.settings.player1_initial_position
        elif player == 2:
            self.color = self.settings.player2_color
            self.pos = self.settings.player2_initial_position
        else:
            raise ValueError("Player must be 1 or 2")

        self.x = self.pos[0]
        self.y = self.pos[1]

    def update(self):
        """
        Updates the player's position based on the current movement state.
        """
        new_x = self.x
        new_y = self.y

        if self.movements["up"]:
            new_y = self.y - self.speed if self.y - self.speed > 0 else 0
        if self.movements["down"]:
            new_y = self.y + self.speed \
                if self.y + self.speed < self.screen.get_height() - self.height \
                else self.screen.get_height() - self.height
        if self.movements["left"]:
            new_x = self.x - self.speed if self.x - self.speed > 0 else 0
        if self.movements["right"]:
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
        """
        Draws the player on the screen.
        """
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))
