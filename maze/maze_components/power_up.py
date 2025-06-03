# W nowym pliku maze/maze_components/power_up.py
import pygame
import random


class PowerUp(pygame.sprite.Sprite):
    """
    Klasa bazowa dla modyfikatorów pojawiających się na mapie.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__()
        self.main = main
        # Ustawiamy rozmiar na 60% block_size
        self.size = int(block_size * 0.6)
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()

        # Centrujemy modyfikator w polu
        self.rect.x = pos_x + (block_size - self.size) // 2
        self.rect.y = pos_y + (block_size - self.size) // 2

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

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((0, 255, 0))  # Zielony kolor dla przyspieszenia

        # Dostosowujemy koordynaty do zmniejszonego rozmiaru
        size = self.size  # To jest teraz 60% block_size
        pygame.draw.polygon(self.image, (255, 255, 0), [
            (size // 4, size // 4),
            (size // 2, size // 2),
            (size // 4, size // 2),
            (3 * size // 4, 3 * size // 4),
            (3 * size // 4, size // 2),
            (size // 2, size // 2),
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

        # Dostosowujemy koordynaty do zmniejszonego rozmiaru
        size = self.size
        pygame.draw.circle(self.image, (0, 0, 0),
                           (size // 2, size // 2),
                           size // 3, 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (size // 2, size // 5),
                         (size // 2, 4 * size // 5), 3)

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