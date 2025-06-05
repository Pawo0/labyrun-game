"""This module defines the Player class, which represents a player in the game."""
import pygame


class Player(pygame.sprite.Sprite):
    """
    This class represents the player in the game.
    It handles position, movement, and draws the player on the screen.
    """

    def __init__(self, main, player_no=1):
        super().__init__()
        self.main = main
        self.settings = main.settings
        self.screen = main.screen
        self.player_no = player_no
        self.player_name = f"Player {player_no}"

        self.speed = None
        self.width = None
        self.height = None
        self.movements = None
        self.color = None
        self.pos = None
        self.x = None
        self.y = None

        self.rect = None  # Adding the rect attribute
        self.image = None  # Adding the image attribute required by sprite

        self.alpha = 255  # Player transparency
        self.frozen = False  # Frozen state
        self.old_speed = None  # Stores speed before freezing
        self.reversed_controls = False

        self.player_number = player_no

        self.reset()

    def update_image(self):
        """
        Updates the player's image after resizing.
        """
        # Creates a new surface with the current dimensions
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draws the player with the appropriate color
        self.image.fill(self.color)

        # Sets the transparency
        self.image.set_alpha(self.alpha)

        # Updates the rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def handle_key_event(self, event, key_up, key_right, key_left, key_down):
        """
        Handles keyboard events for this player.
        """
        key_actions = {pygame.KEYDOWN: True, pygame.KEYUP: False}

        if event.type in key_actions:
            action_value = key_actions[event.type]

            # Mapping keys to directions considering reversed controls
            if self.reversed_controls:
                # Reversed control - swap keys
                key_up, key_down = key_down, key_up
                key_left, key_right = key_right, key_left

            # Check which key was pressed/released and update movements
            if event.key == key_up:
                self.movements["up"] = action_value
            elif event.key == key_right:
                self.movements["right"] = action_value
            elif event.key == key_left:
                self.movements["left"] = action_value
            elif event.key == key_down:
                self.movements["down"] = action_value

    def set_name(self, name):
        """
        Sets the player's name.
        """
        self.player_name = name

    def reset_speed(self):
        """
        Resets the player's speed to the default value.
        """
        self.speed = self.settings.player_speed

    def reset(self):
        """
        Resets the player's position and movement state.
        """
        self.speed = self.settings.player_speed
        self.width = self.settings.player_width
        self.height = self.settings.player_height
        self.movements = {"up": False, "down": False, "left": False, "right": False}

        # depending on the player, set the color and initial position
        if self.player_no == 1:
            self.color = self.settings.player1_color
            self.pos = self.settings.player1_initial_position
        elif self.player_no == 2:
            self.color = self.settings.player2_color
            self.pos = self.settings.player2_initial_position
        else:
            raise ValueError("Player must be 1 or 2")

        self.original_color = self.color  # Save the original color
        self.x = self.pos[0]
        self.y = self.pos[1]

        # Initialize image and rect
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.reset_speed()

    def push_out_of_wall(self):
        """
        Pushes the player out of the wall if they are in it, to the nearest free space.
        """
        # Check if the player collides with the wall
        if self.main.maze.check_collision(self.rect):
            # List of directions to check (right, left, down, up, right-down, right-up, left-down, left-up)
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]

            # Maximum search distance (e.g. half a block)
            max_distance = self.main.settings.block_size // 2

            # Find the nearest free space
            best_distance = float("inf")
            best_position = (self.x, self.y)

            for distance in range(1, max_distance + 1):
                for dx, dy in directions:
                    new_x = self.x + dx * distance
                    new_y = self.y + dy * distance

                    # Check if the new position is within the screen bounds
                    if (
                        new_x < 0
                        or new_x + self.width > self.screen.get_width()
                        or new_y < 0
                        or new_y + self.height > self.screen.get_height()
                    ):
                        continue

                    # Check if there is no collision at the new position
                    test_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                    if not self.main.maze.check_collision(test_rect):
                        # Calculate the distance from the original position
                        dist = abs(new_x - self.x) + abs(new_y - self.y)
                        if dist < best_distance:
                            best_distance = dist
                            best_position = (new_x, new_y)

            # Set the player to the found position
            if best_distance < float("inf"):
                self.x, self.y = best_position
                self.rect.x, self.rect.y = best_position
                self.update_image()

    def update(self):
        """
        Updates the player's position based on the current movement state.
        """
        # If the player is frozen, do not update the position
        if self.frozen:
            self.draw()
            return

        # Check if speed is not None
        if self.speed is None:
            self.speed = self.settings.player_speed

        new_x = self.x
        new_y = self.y

        # Calculate the new position based on the pressed keys
        if self.movements["up"]:
            new_y = self.y - self.speed if self.y - self.speed > 0 else 0
        if self.movements["down"]:
            new_y = min(self.y + self.speed, self.screen.get_height() - self.height)
        if self.movements["left"]:
            new_x = self.x - self.speed if self.x - self.speed > 0 else 0
        if self.movements["right"]:
            new_x = min(self.x + self.speed, self.screen.get_width() - self.width)

        # Handle collisions in the horizontal direction (X)
        if new_x != self.x:
            tmp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_x):
                # If a collision is detected, find the nearest allowed position
                step = 1 if new_x > self.x else -1
                test_x = self.x
                while test_x != new_x:
                    test_x += step
                    test_rect = pygame.Rect(test_x, self.y, self.width, self.height)
                    if self.main.maze.check_collision(test_rect):
                        new_x = test_x - step
                        break

        # Update X position
        self.x = new_x
        self.rect.x = new_x

        # Handle collisions in the vertical direction (Y)
        if new_y != self.y:
            tmp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_y):
                # If a collision is detected, find the nearest allowed position
                step = 1 if new_y > self.y else -1
                test_y = self.y
                while test_y != new_y:
                    test_y += step
                    test_rect = pygame.Rect(self.x, test_y, self.width, self.height)
                    if self.main.maze.check_collision(test_rect):
                        new_y = test_y - step
                        break

        # Update Y position
        self.y = new_y
        self.rect.y = new_y

        self.draw()

    def draw(self):
        """
        Draws the player on the screen.
        """
        curr_color = self.color
        if self.frozen and self.reversed_controls:
            curr_color = self.settings.freeze_and_reverse_colors
        elif self.frozen:
            curr_color = self.settings.freeze_color
        elif self.reversed_controls:
            curr_color = self.settings.reverse_controls_color

        self.screen.fill(curr_color, (self.x, self.y, self.width, self.height))
