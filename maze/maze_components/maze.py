# W pliku maze/maze_components/maze.py

import json
import random
import pygame.sprite

from .floor import Floor
from .wall import Wall
from .power_up import SpeedBoost, SlowDown  # dodaj import

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
                    self.walls.add(Wall(self.settings.wall_color, pos_x, pos_y, self.block_size))
                else:
                    self.floors.add(Floor(self.settings.floor_color, pos_x, pos_y, self.block_size))

    def generate_power_ups(self):
        """
        Generates random power-ups in the maze.
        """
        # Liczba modyfikatorów zależna od wielkości labiryntu
        num_power_ups = max(1, (self.settings.maze_width * self.settings.maze_height) // 25)

        # Lista dostępnych modyfikatorów
        power_up_types = [SpeedBoost, SlowDown]

        # Podział dostępnych pozycji na dwie grupy
        player1_positions = []
        player2_positions = []

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                # jesli srodek labiryntu, to nie dodajemy modyfikatora
                center_x = len(row) // 2
                center_y = len(self.maze) // 2

                if (center_x - 2 <= x <= center_x + 2) and (center_y - 2 <= y <= center_y + 2):
                    continue

                # jesli pole jest puste (0), to dodajemy je jako potencjalną pozycję modyfikatora
                if cell == 0:
                    pos_x = self.offset_x + x * self.block_size
                    pos_y = self.offset_y + y * self.block_size

                    # gracze na starcie sa w dolnych rogach labiryntu
                    player1_pos = self.get_lower_left()
                    player2_pos = self.get_lower_right()

                    # Dodajemy pozycje do odpowiednich grup na podstawie odległości
                    if not ((pos_x, pos_y) == player1_pos or (pos_x, pos_y) == player2_pos):
                        distance_to_player1 = abs(pos_x - player1_pos[0]) + abs(pos_y - player1_pos[1])
                        distance_to_player2 = abs(pos_x - player2_pos[0]) + abs(pos_y - player2_pos[1])

                        if distance_to_player1 < distance_to_player2:
                            player1_positions.append((pos_x, pos_y))
                        else:
                            player2_positions.append((pos_x, pos_y))

        # Losowanie pozycji dla obu graczy
        selected_positions = []
        if player1_positions:
            selected_positions += random.sample(player1_positions, min(num_power_ups // 2, len(player1_positions)))
        if player2_positions:
            selected_positions += random.sample(player2_positions, min(num_power_ups // 2, len(player2_positions)))

        # Tworzenie modyfikatorów
        for pos in selected_positions:
            power_up_class = random.choice(power_up_types)
            power_up = power_up_class(self.main, pos[0], pos[1], self.block_size)
            self.power_ups.add(power_up)

    def check_collision(self, rect):
        """
        Checks for collisions with walls in the maze.
        """
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = rect
        return pygame.sprite.spritecollide(temp_sprite, self.walls, False)

    def check_power_up_collision(self, player):
        """
        Checks if player collided with any power-up and applies its effect.
        """
        collided_power_ups = pygame.sprite.spritecollide(player, self.power_ups, False)
        for power_up in collided_power_ups:
            if power_up.active:
                power_up.apply_effect(player)
                # Możemy dodać efekt dźwiękowy
                # pygame.mixer.Sound('assets/power_up.wav').play()

    def reset_player_speed(self, player_number):
        """
        Resetuje prędkość gracza po upływie czasu działania modyfikatora.
        """
        if player_number == 1:
            self.main.player1.reset_speed()
        else:
            self.main.player2.reset_speed()

    def draw(self):
        """
        Draws the maze on the screen.
        """
        self.walls.draw(self.screen)
        self.floors.draw(self.screen)
        
        # Rysujemy aktywne modyfikatory
        for power_up in self.power_ups:
            if power_up.active:
                power_up.draw(self.screen)

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