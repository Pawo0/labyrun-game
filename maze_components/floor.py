"""
This module defines the Floor class.
"""

import pygame.sprite


class Floor(pygame.sprite.Sprite):
    """
    This class represents floors in the maze.
    """

    def __init__(self, x, y, block_size):
        super().__init__()

        self.image = pygame.Surface([block_size, block_size])
        self.image.fill((52, 202, 234))
        self.rect = self.image.get_rect(topleft=(x, y))
