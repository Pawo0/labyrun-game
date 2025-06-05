"""This module contains classes for different power-ups in the game."""

import random

import pygame


class PowerUp(pygame.sprite.Sprite):
    """
    Base class for power-ups appearing on the map.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__()
        self.main = main
        # Set size to 60% of block_size
        self.size = int(block_size * 0.6)
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()

        # Center the power-up in the field
        self.rect.x = pos_x + (block_size - self.size) // 2
        self.rect.y = pos_y + (block_size - self.size) // 2

        self.block_size = block_size
        self.duration = self.main.settings.power_up_duration  # Effect duration in ms
        self.active = True

    def apply_effect(self, player):
        """
        Apply the power-up effect to the player.
        Method to be overridden by subclasses.
        """

    def remove_effect(self, player_num):
        """
        Remove the power-up effect from the player.
        Method to be overridden by subclasses.
        """

    def draw(self, screen):
        """
        Draw the power-up on the screen if it is active.
        """
        if self.active:
            screen.blit(self.image, self.rect)


class SpeedBoost(PowerUp):
    """
    Power-up that increases the player's speed.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((0, 255, 0))  # Green color for speed boost

        # Adjust coordinates for reduced size
        size = self.size  # This is now 60% of block_size
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
        Increases the player's speed for a specified time.
        """
        player.speed *= 1.5

        # Register the power-up with the manager
        self.main.powerup_manager.register_powerup("speed", player.player_number, self)

        # After a specified time, restore normal speed
        pygame.time.set_timer(pygame.USEREVENT + player.player_number, self.duration)
        self.active = False

    def remove_effect(self, player_num):
        """
        Restores the player's normal speed.
        """
        player = self.main.player1 if player_num == 1 else self.main.player2
        player.reset_speed()


class SlowDown(PowerUp):
    """
    Power-up that decreases the opponent's speed.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 0, 0))  # Red color for slow down

        # Adjust coordinates for reduced size
        size = self.size
        pygame.draw.circle(self.image, (0, 0, 0), (size // 2, size // 2), size // 3, 2)
        pygame.draw.line(
            self.image, (0, 0, 0), (size // 2, size // 5), (size // 2, 4 * size // 5), 3
        )

    def apply_effect(self, player):
        """
        Slows down the player's opponent.
        """
        # Find the opponent
        if player.player_number == 1:
            opponent = player.main.player2
            opponent_num = 2
        else:
            opponent = player.main.player1
            opponent_num = 1

        opponent.speed *= 0.5

        # Register the power-up with the manager
        self.main.powerup_manager.register_powerup("speed", opponent_num, self)

        # After a specified time, restore normal speed
        pygame.time.set_timer(pygame.USEREVENT + opponent_num, self.duration)
        self.active = False

    def remove_effect(self, player_num):
        """
        Restores the player's normal speed.
        """
        player = self.main.player1 if player_num == 1 else self.main.player2
        player.reset_speed()


class Enlarge(PowerUp):
    """
    Power-up that enlarges the player's opponent to exactly the size of a block.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 165, 0))  # Orange color

        size = self.size
        # Draw arrows pointing outward
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
        Enlarges the player's opponent to exactly the size of a block.
        """
        # Find the opponent
        if player.player_number == 1:
            opponent = self.main.player2
            opponent_num = 2
        else:
            opponent = self.main.player1
            opponent_num = 1

        # Save the original dimensions
        original_width = opponent.width
        original_height = opponent.height
        block_size = self.main.settings.block_size

        # Save the original center position of the player
        center_x = opponent.x + original_width / 2
        center_y = opponent.y + original_height / 2

        # Set the new size exactly to the size of a block
        new_width = int(block_size * 0.99)
        new_height = int(block_size * 0.99)

        # Calculate the new position of the player to keep it centered
        new_x = int(center_x - new_width / 2)
        new_y = int(center_y - new_height / 2)

        # set the new dimensions
        opponent.width = new_width
        opponent.height = new_height
        opponent.x = new_x
        opponent.y = new_y

        # Update the image and collision rectangle
        opponent.update_image()
        opponent.push_out_of_wall()

        # Register the power-up with the manager
        self.main.powerup_manager.register_powerup("enlarge", opponent_num, self)

        # Set a timer to restore the normal size
        pygame.time.set_timer(
            pygame.USEREVENT + 20 + opponent_num, self.duration, loops=1
        )

        # Deactivate the power-up
        self.active = False

    def remove_effect(self, player_num):
        """
        Restores the player's normal size.
        """
        player = self.main.player1 if player_num == 1 else self.main.player2

        original_width = self.main.settings.player_width
        original_height = self.main.settings.player_height

        # Save the player's center
        center_x = player.x + player.width / 2
        center_y = player.y + player.height / 2

        # Restore the original size
        player.width = original_width
        player.height = original_height

        # Update the position, keeping the center
        player.x = int(center_x - original_width / 2)
        player.y = int(center_y - original_height / 2)

        player.update_image()


class Teleport(PowerUp):
    """
    Power-up that teleports the player randomly to an available location.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((148, 0, 211))  # Purple color for teleport

        size = self.size
        # Draw a spiral
        for i in range(0, size, 2):
            radius = i // 2
            pos = (size // 2, size // 2)
            pygame.draw.circle(self.image, (255, 255, 255), pos, radius, 1)

    def apply_effect(self, player):
        """
        Teleports the player to a random location in the maze, except for the winning zone.
        """
        # Get all available floors
        available_floors = []

        # Get winning zones
        mid_x = self.main.settings.screen_width // 2
        safe_margin = self.main.settings.block_size * 2

        for floor in self.main.maze.floors:
            rect = pygame.Rect(floor.rect.x, floor.rect.y, player.width, player.height)

            # Check if the floor is outside the winning zone and does not collide with walls
            is_in_win_zone = (
                player.player_number == 1 and floor.rect.x > mid_x - safe_margin
            ) or (player.player_number == 2 and floor.rect.x < mid_x + safe_margin)

            if not is_in_win_zone and not self.main.maze.check_collision(rect):
                available_floors.append(floor)

        if available_floors:
            # Randomly select a floor
            new_floor = random.choice(available_floors)
            player.x = new_floor.rect.x
            player.y = new_floor.rect.y
            player.rect.x = player.x
            player.rect.y = player.y

        self.active = False


class Freeze(PowerUp):
    """
    Power-up that freezes the opponent for a short time.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((173, 216, 230))  # Light blue color for ice

        size = self.size
        # Draw a snowflake
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
        Freezes the player's opponent for a specified time.
        """
        # Find the opponent
        if player.player_number == 1:
            opponent = self.main.player2
            opponent_num = 2
        else:
            opponent = self.main.player1
            opponent_num = 1

        opponent.frozen = True
        opponent.old_speed = (
            opponent.speed
            if opponent.speed is not None
            else opponent.settings.player_speed
        )
        opponent.speed = 0

        # Register the power-up with the manager
        self.main.powerup_manager.register_powerup("freeze", opponent_num, self)

        # Set a timer for unfreezing
        pygame.time.set_timer(
            pygame.USEREVENT + 30 + opponent_num, self.duration, loops=1
        )
        self.active = False

    def remove_effect(self, player_num):
        """
        Unfreezes the player.
        """
        player = self.main.player1 if player_num == 1 else self.main.player2
        player.frozen = False

        if hasattr(player, "old_speed") and player.old_speed is not None:
            player.speed = player.old_speed
        else:
            player.reset_speed()


class ReverseControls(PowerUp):
    """
    Power-up that reverses the controls of the player's opponent.
    """

    def __init__(self, main, pos_x, pos_y, block_size):
        super().__init__(main, pos_x, pos_y, block_size)
        self.image.fill((255, 215, 0))  # Gold color for reverse controls

        size = self.size
        # Draw arrows indicating opposite directions
        pygame.draw.line(
            self.image, (0, 0, 0), (size // 4, size // 4), (size // 4, 3 * size // 4), 2
        )
        pygame.draw.line(
            self.image, (0, 0, 0), (size // 4, size // 4), (size // 8, size // 3), 2
        )
        pygame.draw.line(
            self.image, (0, 0, 0), (size // 4, size // 4), (3 * size // 8, size // 3), 2
        )

        pygame.draw.line(
            self.image,
            (0, 0, 0),
            (3 * size // 4, 3 * size // 4),
            (3 * size // 4, size // 4),
            2,
        )
        pygame.draw.line(
            self.image,
            (0, 0, 0),
            (3 * size // 4, 3 * size // 4),
            (5 * size // 8, 2 * size // 3),
            2,
        )
        pygame.draw.line(
            self.image,
            (0, 0, 0),
            (3 * size // 4, 3 * size // 4),
            (7 * size // 8, 2 * size // 3),
            2,
        )

        # Save the opponent on whom the effect will work
        self.affected_player = None

    def apply_effect(self, player):
        """
        Reverses the controls of the player's opponent for a specified time.
        """
        # Find the opponent
        if player.player_number == 1:
            self.affected_player = player.main.player2
            opponent_num = 2
        else:
            self.affected_player = player.main.player1
            opponent_num = 1

        # Reverse the controls
        self.affected_player.reversed_controls = True

        # Register the power-up with the manager
        self.main.powerup_manager.register_powerup(
            "reverse_controls", opponent_num, self
        )

        # Add a timer to restore normal controls
        pygame.time.set_timer(
            pygame.USEREVENT + 40 + opponent_num, self.duration, loops=1
        )

        self.active = False

    def remove_effect(self, player_num):
        """
        Removes the reversed control effect from the player.
        """
        if player_num == 1:
            player = self.main.player1
        else:
            player = self.main.player2
        player.reversed_controls = False
