import json
import math
import random

import pygame.sprite

from powerups import (Enlarge, Freeze, ReverseControls, SlowDown, SpeedBoost,
                      Teleport)


class Maze:
    """
    This class is responsible for loading and rendering the maze.
    """

    def __init__(self, main, maze_json):
        self.screen = main.screen
        self.settings = main.settings
        self.block_size = self.settings.block_size
        self.main = main  # Zapisujemy referencję do main

        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # Nowa grupa dla modyfikatorów

        self.maze = []
        self.load_maze(maze_json)

        self.maze_width = len(self.maze[0]) * self.block_size
        self.maze_height = len(self.maze) * self.block_size
        self.offset_x = (self.screen.get_width() - self.maze_width) // 2
        self.offset_y = (self.screen.get_height() - self.maze_height) // 2

        # Tworzenie powierzchni dla mgły wojny
        self.fog_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA
        )
        # Zasięg widoczności w blokach
        self.fog_radius = 4 * self.block_size

        self.create_sprites()
        self.generate_power_ups()  # Generowanie modyfikatorów

    def load_maze(self, maze_json):
        """
        Loads the maze from a JSON file.
        """
        with open(maze_json, "r", encoding="utf-8") as file:
            self.maze = json.load(file)["maze"]

    def create_sprites(self):
        """
        Creates wall and floor sprites based on the maze data.
        """
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                pos_x = self.offset_x + x * self.block_size
                pos_y = self.offset_y + y * self.block_size
                if cell == 1:
                    self.walls.add(
                        Wall(self.settings.wall_color, pos_x, pos_y, self.block_size)
                    )
                else:
                    self.floors.add(
                        Floor(self.settings.floor_color, pos_x, pos_y, self.block_size)
                    )

    def generate_power_ups(self):
        """
        Generates random power-ups in the maze.
        """
        # Jeśli power-upy są wyłączone, nie generujemy ich
        if (
            not hasattr(self.settings, "power_ups_enabled")
            or not self.settings.power_ups_enabled
        ):
            return

        # Liczba modyfikatorów zależna od wielkości labiryntu
        num_power_ups = max(
            1, (self.settings.maze_width * self.settings.maze_height) // 25
        )

        # Lista dostępnych modyfikatorów
        power_up_types = []
        if (
            hasattr(self.settings, "speed_boost_enabled")
            and self.settings.speed_boost_enabled
        ):
            power_up_types.append(SpeedBoost)
        if (
            hasattr(self.settings, "slow_down_enabled")
            and self.settings.slow_down_enabled
        ):
            power_up_types.append(SlowDown)
        if hasattr(self.settings, "enlarge_enabled") and self.settings.enlarge_enabled:
            power_up_types.append(Enlarge)
        if (
            hasattr(self.settings, "teleport_enabled")
            and self.settings.teleport_enabled
        ):
            power_up_types.append(Teleport)
        if hasattr(self.settings, "freeze_enabled") and self.settings.freeze_enabled:
            power_up_types.append(Freeze)
        if (
            hasattr(self.settings, "reverse_controls_enabled")
            and self.settings.reverse_controls_enabled
        ):
            power_up_types.append(ReverseControls)

        if not power_up_types:
            return
        # Podział dostępnych pozycji na dwie grupy
        player1_positions = []
        player2_positions = []

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                # jesli srodek labiryntu, to nie dodajemy modyfikatora
                center_x = len(row) // 2
                center_y = len(self.maze) // 2

                if (center_x - 2 <= x <= center_x + 2) and (
                    center_y - 2 <= y <= center_y + 2
                ):
                    continue

                # jesli pole jest puste (0), to dodajemy je jako potencjalną pozycję modyfikatora
                if cell == 0:
                    pos_x = self.offset_x + x * self.block_size
                    pos_y = self.offset_y + y * self.block_size

                    # Pobierz pozycje startowe graczy
                    player1_pos = self.main.settings.player1_initial_position
                    player2_pos = self.main.settings.player2_initial_position

                    # Dodajemy pozycje do odpowiednich grup na podstawie odległości
                    if not (
                        (pos_x, pos_y) == player1_pos or (pos_x, pos_y) == player2_pos
                    ):
                        distance_to_player1 = abs(pos_x - player1_pos[0]) + abs(
                            pos_y - player1_pos[1]
                        )
                        distance_to_player2 = abs(pos_x - player2_pos[0]) + abs(
                            pos_y - player2_pos[1]
                        )

                        if distance_to_player1 < distance_to_player2:
                            player1_positions.append((pos_x, pos_y))
                        else:
                            player2_positions.append((pos_x, pos_y))

        # Losowanie pozycji dla obu graczy
        selected_positions = []
        p1_count = min(num_power_ups // 2, len(player1_positions))
        p2_count = min(num_power_ups // 2, len(player2_positions))

        if player1_positions and p1_count > 0:
            selected_positions += random.sample(player1_positions, p1_count)
        if player2_positions and p2_count > 0:
            selected_positions += random.sample(player2_positions, p2_count)

        # Tworzenie modyfikatorów
        for pos in selected_positions:
            power_up_class = random.choice(power_up_types)
            power_up = power_up_class(self.main, pos[0], pos[1], self.block_size)
            self.power_ups.add(power_up)

    def check_collision(self, rect):
        """
        Sprawdza kolizje ze ścianami labiryntu.
        """
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = rect
        collisions = pygame.sprite.spritecollide(temp_sprite, self.walls, False)

        return collisions

    def check_power_up_collision(self, player):
        """
        Checks if player collided with any power-up and applies its effect.
        """
        # Jeśli power-upy są wyłączone, nie sprawdzamy kolizji
        if (
            not hasattr(self.settings, "power_ups_enabled")
            or not self.settings.power_ups_enabled
        ):
            return

        collided_power_ups = pygame.sprite.spritecollide(player, self.power_ups, False)
        for power_up in collided_power_ups:
            if power_up.active:
                power_up.apply_effect(player)

    def reset_player_speed(self, player_number):
        """
        Resetuje prędkość gracza po upływie czasu działania modyfikatora.
        """
        if player_number == 1:
            self.main.player1.reset_speed()
        else:
            self.main.player2.reset_speed()

    def update_fog_of_war(self):
        """
        Aktualizuje mgłę wojny na podstawie pozycji graczy.
        """
        # Czyścimy powierzchnię mgły
        self.fog_surface.fill((0, 0, 0))  # Półprzezroczysta czarna mgła

        # Odkrywamy obszar wokół graczy
        if hasattr(self.main, "player1") and hasattr(self.main, "player2"):
            for player in [self.main.player1, self.main.player2]:
                # Centrum gracza
                center_x = int(player.x + player.width // 2)
                center_y = int(player.y + player.height // 2)

                # Rysujemy tylko jeden przezroczysty krąg zamiast gradientu
                pygame.draw.circle(
                    self.fog_surface,
                    (0, 0, 0, 0),
                    (center_x, center_y),
                    self.fog_radius,
                )

    def _create_visibility_gradient(self, center_pos):
        """
        Tworzy gradient widoczności wokół danego punktu.
        """
        # Konwersja do int przed użyciem w range()
        start_x = max(0, int(center_pos[0] - self.fog_radius))
        end_x = min(self.screen.get_width(), int(center_pos[0] + self.fog_radius) + 1)
        start_y = max(0, int(center_pos[1] - self.fog_radius))
        end_y = min(self.screen.get_height(), int(center_pos[1] + self.fog_radius) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                # Obliczanie odległości od centrum
                dist = math.sqrt((x - center_pos[0]) ** 2 + (y - center_pos[1]) ** 2)

                # Sprawdzamy czy punkt jest w zasięgu mgły
                if dist <= self.fog_radius:
                    # Obliczamy przezroczystość mgły (im dalej od centrum, tym bardziej nieprzezroczysta)
                    alpha = int((dist / self.fog_radius) * 200)

                    # Pobieramy aktualny kolor piksela
                    current_alpha = self.fog_surface.get_at((x, y))[3]

                    # Ustawiamy nową przezroczystość, biorąc mniejszą z dwóch wartości
                    new_alpha = min(current_alpha, alpha)

                    # Ustawiamy nowy kolor piksela
                    self.fog_surface.set_at((x, y), (0, 0, 0, new_alpha))

    def draw(self):
        """
        Draws the maze on the screen.
        """
        self.walls.draw(self.screen)
        self.floors.draw(self.screen)

        # Rysujemy aktywne modyfikatory jeśli są włączone
        if (
            hasattr(self.settings, "power_ups_enabled")
            and self.settings.power_ups_enabled
        ):
            for power_up in self.power_ups:
                if power_up.active:
                    power_up.draw(self.screen)

        # Aktualizujemy i rysujemy mgłę wojny, jeśli gra jest w trakcie i opcja włączona
        if (
            self.main.game_state.state == "running"
            and hasattr(self.settings, "fog_of_war_enabled")
            and self.settings.fog_of_war_enabled
        ):
            self.update_fog_of_war()
            self.screen.blit(self.fog_surface, (0, 0))

    def get_lower_left(self):
        """
        Returns the lower left corner of the maze.
        """
        return self.offset_x, self.offset_y + self.maze_height

    def get_lower_right(self):
        """
        Returns the lower right corner of the maze.
        """
        return self.offset_x + self.maze_width, self.offset_y + self.maze_height


class Floor(pygame.sprite.Sprite):
    """
    This class represents floors in the maze.
    """

    def __init__(self, color, x, y, block_size):
        super().__init__()

        self.image = pygame.Surface([block_size, block_size])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Wall(pygame.sprite.Sprite):
    """
    This class represents walls in the maze.
    """

    def __init__(self, color, x, y, block_size):
        super().__init__()

        self.image = pygame.Surface([block_size, block_size])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
