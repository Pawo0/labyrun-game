"""
This module provides the Maze class and related components for loading, rendering,
and managing the maze, including fog of war and power-ups.
"""

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
        self.main = main  # Save a reference to main

        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # New group for power-ups

        self.maze = []
        self.load_maze(maze_json)

        self.maze_width = len(self.maze[0]) * self.block_size
        self.maze_height = len(self.maze) * self.block_size
        self.offset_x = (self.screen.get_width() - self.maze_width) // 2
        self.offset_y = (self.screen.get_height() - self.maze_height) // 2

        # Creating surface for the fog of war
        self.fog_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA
        )
        # Visibility range in blocks
        self.fog_radius = 4 * self.block_size

        self.create_sprites()
        self.generate_power_ups()  # Generate power-ups

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
        # If power-ups are disabled, do not generate them
        if (
            not hasattr(self.settings, "power_ups_enabled")
            or not self.settings.power_ups_enabled
        ):
            return

        # Number of power-ups depends on maze size
        num_power_ups = max(
            1, (self.settings.maze_width * self.settings.maze_height) // 25
        )

        # List of available power-ups
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
        # Divide available positions into two groups
        player1_positions = []
        player2_positions = []

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                # if center of the maze, do not add a modifier
                center_x = len(row) // 2
                center_y = len(self.maze) // 2

                if (center_x - 2 <= x <= center_x + 2) and (
                    center_y - 2 <= y <= center_y + 2
                ):
                    continue

                # if the field is empty (0), add it as a potential modifier position
                if cell == 0:
                    pos_x = self.offset_x + x * self.block_size
                    pos_y = self.offset_y + y * self.block_size

                    # Get the starting positions of the players
                    player1_pos = self.main.settings.player1_initial_position
                    player2_pos = self.main.settings.player2_initial_position

                    # Add positions to the appropriate group based on distance
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

        # Randomly select positions for both players
        selected_positions = []
        p1_count = min(num_power_ups // 2, len(player1_positions))
        p2_count = min(num_power_ups // 2, len(player2_positions))

        if player1_positions and p1_count > 0:
            selected_positions += random.sample(player1_positions, p1_count)
        if player2_positions and p2_count > 0:
            selected_positions += random.sample(player2_positions, p2_count)

        # Create power-ups
        for pos in selected_positions:
            power_up_class = random.choice(power_up_types)
            power_up = power_up_class(self.main, pos[0], pos[1], self.block_size)
            self.power_ups.add(power_up)

    def check_collision(self, rect):
        """
        Checks collisions with the maze walls.
        """
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = rect
        collisions = pygame.sprite.spritecollide(temp_sprite, self.walls, False)

        return collisions

    def check_power_up_collision(self, player):
        """
        Checks if player collided with any power-up and applies its effect.
        """
        # If power-ups are disabled, do not check collisions
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
        Resets player speed after the power-up effect duration.
        """
        if player_number == 1:
            self.main.player1.reset_speed()
        else:
            self.main.player2.reset_speed()

    def update_fog_of_war(self):
        """
        Updates the fog of war based on player positions.
        """
        # Clear the fog surface
        self.fog_surface.fill((0, 0, 0))  # Semi-transparent black fog

        # Reveal the area around players
        if hasattr(self.main, "player1") and hasattr(self.main, "player2"):
            for player in [self.main.player1, self.main.player2]:
                # Player center
                center_x = int(player.x + player.width // 2)
                center_y = int(player.y + player.height // 2)

                # Draw only one transparent circle instead of a gradient
                pygame.draw.circle(
                    self.fog_surface,
                    (0, 0, 0, 0),
                    (center_x, center_y),
                    self.fog_radius,
                )

    def _create_visibility_gradient(self, center_pos):
        """
        Creates a visibility gradient around a given point.
        """
        # Convert to int before using in range()
        start_x = max(0, int(center_pos[0] - self.fog_radius))
        end_x = min(self.screen.get_width(), int(center_pos[0] + self.fog_radius) + 1)
        start_y = max(0, int(center_pos[1] - self.fog_radius))
        end_y = min(self.screen.get_height(), int(center_pos[1] + self.fog_radius) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                # Calculate distance from the center
                dist = math.sqrt((x - center_pos[0]) ** 2 + (y - center_pos[1]) ** 2)

                # Check if the point is within the fog range
                if dist <= self.fog_radius:
                    # Calculate fog transparency (the further from the center, the more opaque)
                    alpha = int((dist / self.fog_radius) * 200)

                    # Get the current pixel color
                    current_alpha = self.fog_surface.get_at((x, y))[3]

                    # Set the new transparency, taking the lesser of the two values
                    new_alpha = min(current_alpha, alpha)

                    # Set the new pixel color
                    self.fog_surface.set_at((x, y), (0, 0, 0, new_alpha))

    def draw(self):
        """
        Draws the maze on the screen.
        """
        self.walls.draw(self.screen)
        self.floors.draw(self.screen)

        # Draw active modifiers if enabled
        if (
            hasattr(self.settings, "power_ups_enabled")
            and self.settings.power_ups_enabled
        ):
            for power_up in self.power_ups:
                if power_up.active:
                    power_up.draw(self.screen)

        # Update and draw the fog of war if the game is running and the option is enabled
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
