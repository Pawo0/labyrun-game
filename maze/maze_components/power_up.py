# W nowym pliku maze/maze_components/power_up.py
import pygame
import random


class PowerUp(pygame.sprite.Sprite):
    """
    Klasa bazowa dla modyfikatorów pojawiających się na mapie.
    """

    def __init__(self,main, pos_x, pos_y, block_size):
        super().__init__()
        self.main = main
        self.image = pygame.Surface((block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.block_size = block_size
        self.duration = self.main.settings.power_up_duration  # Czas trwania efektu w ms
        self.active = True

    def apply_effect(self, player):
        """
        Aplikuje efekt modyfikatora na gracza.
        Metoda do nadpisania przez klasy potomne.
        """
        pass

    def draw(self, screen):
        """
        Rysuje modyfikator na ekranie, jeśli jest aktywny.
        """
        if self.active:
            screen.blit(self.image, self.rect)


class SpeedBoost(PowerUp):
    """
    Modyfikator zwiększający prędkość gracza.
    """

    def __init__(self,main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((0, 255, 0))  # Zielony kolor dla przyspieszenia
        # Możesz też załadować obrazek zamiast jednolitego koloru
        # self.image = pygame.image.load('assets/speed_boost.png')
        # self.image = pygame.transform.scale(self.image, (block_size, block_size))

        # Rysujemy symbol błyskawicy
        pygame.draw.polygon(self.image, (255, 255, 0), [
            (block_size // 4, block_size // 4),
            (block_size // 2, block_size // 2),
            (block_size // 4, block_size // 2),
            (3 * block_size // 4, 3 * block_size // 4),
            (3 * block_size // 4, block_size // 2),
            (block_size // 2, block_size // 2),
        ])

    def apply_effect(self, player):
        """
        Zwiększa prędkość gracza na określony czas.
        """
        player.speed *= 1.5
        # Po określonym czasie przywracamy normalną prędkość
        pygame.time.set_timer(pygame.USEREVENT + player.player_number, self.duration)
        self.active = False


class SlowDown(PowerUp):
    """
    Modyfikator zmniejszający prędkość przeciwnika.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 0, 0))  # Czerwony kolor dla spowolnienia

        # Rysujemy symbol spowolnienia
        pygame.draw.circle(self.image, (0, 0, 0),
                           (block_size // 2, block_size // 2),
                           block_size // 3, 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (block_size // 2, block_size // 5),
                         (block_size // 2, 4 * block_size // 5), 3)

    def apply_effect(self, player):
        """
        Spowalnia przeciwnika gracza.
        """
        # Znajdujemy przeciwnika
        if player.player_number == 1:
            opponent = player.main.player2
        else:
            opponent = player.main.player1

        opponent.speed *= 0.5
        # Po określonym czasie przywracamy normalną prędkość
        pygame.time.set_timer(pygame.USEREVENT + opponent.player_number, self.duration)
        self.active = False

# Można dodać więcej typów modyfikatorów