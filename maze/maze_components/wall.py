"""
This module defines the Wall class.
"""

import pygame.sprite


class Wall(pygame.sprite.Sprite):
    """
    This class represents walls in the maze.
    """

    def __init__(self, color, x, y, block_size):
        super().__init__()

        self.image = pygame.Surface([block_size, block_size])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
