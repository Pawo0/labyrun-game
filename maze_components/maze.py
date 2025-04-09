"""
This module contains the Maze class.
"""
import json

import pygame.sprite

from .floor import Floor
from .wall import Wall


class Maze:
    """
    This class is responsible for loading and rendering the maze.
    """
    def __init__(self, main, maze_json):
        self.screen = main.screen
        self.settings = main.settings
        self.block_size = self.settings.block_size

        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()

        self.maze = []
        self.load_maze(maze_json)

        # self.offset_x = (self.screen.get_width() - len(self.maze[0]) * self.block_size) // 2
        # self.offset_y = (self.screen.get_height() - len(self.maze) * self.block_size) // 2

        self.maze_width = len(self.maze[0]) * self.block_size
        self.offset_x = (self.screen.get_width() - self.maze_width) // 2
        self.offset_y = (self.screen.get_height() - self.maze_width) // 2

        self.create_sprites()

    def load_maze(self, maze_json, mirrored=False):
        """
        Loads the maze from a JSON file.
        """
        with open(maze_json, "r", encoding="utf-8") as file:
            self.maze = json.load(file)["maze"]
        if mirrored:
            self.maze = [row[::-1] for row in self.maze]

    def create_sprites(self):
        """
        Creates wall and floor sprites based on the maze data.
        """
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                pos_x = self.offset_x + x * self.block_size
                pos_y = self.offset_y + y * self.block_size
                if cell == 1:
                    self.walls.add(Wall(pos_x, pos_y, self.block_size))
                else:
                    self.floors.add(Floor(pos_x, pos_y, self.block_size))

    def check_collision(self, rect):
        """
        Checks for collisions with walls in the maze.
        """
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = rect
        return pygame.sprite.spritecollide(temp_sprite, self.walls, False)

    def draw(self):
        """
        Draws the maze on the screen.
        """
        self.walls.draw(self.screen)
        self.floors.draw(self.screen)
