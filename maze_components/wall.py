import pygame.sprite


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, block_size):
        super().__init__()

        self.image = pygame.Surface([block_size, block_size])
        self.image.fill((245, 52, 177))
        self.rect = self.image.get_rect(topleft=(x, y))
