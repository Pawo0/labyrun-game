# W nowym pliku maze/maze_components/power_up.py
import random

import pygame


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
        pygame.draw.polygon(
            self.image,
            (255, 255, 0),
            [
                (size // 4, size // 4),
                (size // 2, size // 2),
                (size // 4, size // 2),
                (3 * size // 4, 3 * size // 4),
                (3 * size // 4, size // 2),
                (size // 2, size // 2),
            ],
        )

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
        pygame.draw.circle(self.image, (0, 0, 0), (size // 2, size // 2), size // 3, 2)
        pygame.draw.line(
            self.image, (0, 0, 0), (size // 2, size // 5), (size // 2, 4 * size // 5), 3
        )

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


class Enlarge(PowerUp):
    """
    Modyfikator zwiększający rozmiar przeciwnika gracza dokładnie do rozmiaru bloku.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 165, 0))  # Pomarańczowy kolor

        size = self.size
        # Rysujemy strzałki na zewnątrz
        pygame.draw.polygon(
            self.image,
            (0, 0, 0),
            [
                (size // 2, size // 4),
                (size // 4, size // 2),
                (size // 2, size * 3 // 4),
                (size * 3 // 4, size // 2),
            ],
        )

    def apply_effect(self, player):
        """
        Zwiększa rozmiar przeciwnika gracza dokładnie do rozmiaru bloku.
        """
        # Znajdujemy przeciwnika
        if player.player_number == 1:
            opponent = self.main.player2
        else:
            opponent = self.main.player1

        # Zapisujemy oryginalne wymiary
        original_width = opponent.width
        original_height = opponent.height
        block_size = self.main.settings.block_size

        # Zapisujemy oryginalne położenie środka gracza
        center_x = opponent.x + original_width / 2
        center_y = opponent.y + original_height / 2

        # Ustawiamy nowy rozmiar dokładnie na rozmiar bloku
        new_width = int(block_size * 0.99)
        new_height = int(block_size * 0.99)

        # Obliczamy nowe położenie gracza, aby pozostał wyśrodkowany
        new_x = int(center_x - new_width / 2)
        new_y = int(center_y - new_height / 2)

        # ustawiamy nowe wymiary
        opponent.width = new_width
        opponent.height = new_height
        opponent.x = new_x
        opponent.y = new_y

        # Aktualizujemy obrazek i prostokąt kolizji
        opponent.update_image()
        opponent.push_out_of_wall()

        # Ustawiamy timer na przywrócenie normalnego rozmiaru
        player_num = 2 if player.player_number == 1 else 1
        pygame.time.set_timer(
            pygame.USEREVENT + 20 + player_num, self.duration, loops=1
        )

        # Niezależnie od wyniku sprawdzenia kolizji, dezaktywujemy power-up
        self.active = False


class Teleport(PowerUp):
    """
    Modyfikator teleportujący gracza losowo w dostępne miejsce.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((148, 0, 211))  # Fioletowy kolor dla teleportu

        size = self.size
        # Rysujemy spiralę
        for i in range(0, size, 2):
            radius = i // 2
            pos = (size // 2, size // 2)
            pygame.draw.circle(self.image, (255, 255, 255), pos, radius, 1)

    def apply_effect(self, player):
        """
        Teleportuje gracza w losowe miejsce w labiryncie, z wyjątkiem strefy wygranej.
        """
        # Pobieramy wszystkie dostępne podłogi
        available_floors = []

        # Pobieranie stref wygranej
        left_zone, right_zone = self.main.engine.win_zone
        mid_x = self.main.settings.screen_width // 2
        safe_margin = self.main.settings.block_size * 2

        for floor in self.main.maze.floors:
            rect = pygame.Rect(floor.rect.x, floor.rect.y, player.width, player.height)

            # Sprawdzanie czy podłoga jest poza strefą wygranej i nie koliduje ze ścianami
            is_in_win_zone = (
                player.player_number == 1 and floor.rect.x > mid_x - safe_margin
            ) or (player.player_number == 2 and floor.rect.x < mid_x + safe_margin)

            if not is_in_win_zone and not self.main.maze.check_collision(rect):
                available_floors.append(floor)

        if available_floors:
            # Losujemy podłogę
            new_floor = random.choice(available_floors)
            player.x = new_floor.rect.x
            player.y = new_floor.rect.y
            player.rect.x = player.x
            player.rect.y = player.y

        self.active = False


class Freeze(PowerUp):
    """
    Modyfikator zamrażający przeciwnika na chwilę.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((173, 216, 230))  # Jasnoniebieski kolor dla lodu

        size = self.size
        # Rysujemy płatek śniegu
        pygame.draw.line(
            self.image, (255, 255, 255), (size // 2, 0), (size // 2, size), 2
        )
        pygame.draw.line(
            self.image, (255, 255, 255), (0, size // 2), (size, size // 2), 2
        )
        pygame.draw.line(
            self.image,
            (255, 255, 255),
            (size // 4, size // 4),
            (3 * size // 4, 3 * size // 4),
            2,
        )
        pygame.draw.line(
            self.image,
            (255, 255, 255),
            (size // 4, 3 * size // 4),
            (3 * size // 4, size // 4),
            2,
        )

    def apply_effect(self, player):
        """
        Zamraża przeciwnika gracza na określony czas.
        """
        # Znajdujemy przeciwnika
        if player.player_number == 1:
            opponent = player.main.player2
        else:
            opponent = player.main.player1

        opponent.frozen = True
        opponent.old_speed = (
            opponent.speed
            if opponent.speed is not None
            else opponent.settings.player_speed
        )
        opponent.speed = 0

        # Ustawiam timer na odmrożenie
        player_num = 2 if player.player_no == 1 else 1
        pygame.time.set_timer(
            pygame.USEREVENT + 30 + player_num, self.duration, loops=1
        )
        self.active = False


class ReverseControls(PowerUp):
    """
    Modyfikator odwracający sterowanie przeciwnika gracza.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 215, 0))  # Złoty kolor dla odwrócenia sterowania

        size = self.size
        # Rysujemy strzałki wskazujące przeciwne kierunki
        pygame.draw.line(self.image, (0, 0, 0),
                         (size // 4, size // 4), (size // 4, 3 * size // 4), 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (size // 4, size // 4), (size // 8, size // 3), 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (size // 4, size // 4), (3 * size // 8, size // 3), 2)

        pygame.draw.line(self.image, (0, 0, 0),
                         (3 * size // 4, 3 * size // 4), (3 * size // 4, size // 4), 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (3 * size // 4, 3 * size // 4), (5 * size // 8, 2 * size // 3), 2)
        pygame.draw.line(self.image, (0, 0, 0),
                         (3 * size // 4, 3 * size // 4), (7 * size // 8, 2 * size // 3), 2)

    def apply_effect(self, player):
        """
        Odwraca sterowanie przeciwnika gracza na określony czas.
        """
        # Znajdujemy przeciwnika
        if player.player_number == 1:
            opponent = player.main.player2
        else:
            opponent = player.main.player1

        # Odwracamy sterowanie
        opponent.reversed_controls = True

        # Dodajemy timer do przywrócenia normalnego sterowania
        player_num = 2 if player.player_number == 1 else 1
        pygame.time.set_timer(pygame.USEREVENT + 40 + player_num, self.duration, loops=1)

        self.active = False