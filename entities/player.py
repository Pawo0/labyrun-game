import pygame


class Player(pygame.sprite.Sprite):  # Dziedziczenie po pygame.sprite.Sprite
    """
    This class represents the player in the game.
    It handles position, movement, and draws the player on the screen.
    """

    def __init__(self, main, player_no=1):
        super().__init__()  # Wywołanie konstruktora klasy nadrzędnej
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

        self.rect = None  # Dodajemy atrybut rect
        self.image = None  # Dodajemy atrybut image wymagany przez sprite

        self.player_number = player_no

        self.reset()

    def set_name(self, name):
        """
        Sets the player's name.
        """
        self.player_name = name

    def reset_speed(self):
        """
        Resetuje prędkość gracza do wartości domyślnej.
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

        self.x = self.pos[0]
        self.y = self.pos[1]

        # Inicjalizacja image i rect
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.reset_speed()

    def update(self):
        """
        Updates the player's position based on the current movement state.
        """
        new_x = self.x
        new_y = self.y

        # Obliczanie nowej pozycji na podstawie wciśniętych klawiszy
        if self.movements["up"]:
            new_y = self.y - self.speed if self.y - self.speed > 0 else 0
        if self.movements["down"]:
            new_y = min(self.y + self.speed, self.screen.get_height() - self.height)
        if self.movements["left"]:
            new_x = self.x - self.speed if self.x - self.speed > 0 else 0
        if self.movements["right"]:
            new_x = min(self.x + self.speed, self.screen.get_width() - self.width)

        # Obsługa kolizji w poziomie (X)
        if new_x != self.x:
            # Sprawdzanie czy wystąpiła kolizja dla docelowej pozycji X
            tmp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_x):
                # Jeśli kolizja, znajdź maksymalną pozycję bez kolizji
                target_x = new_x
                start_x = self.x

                # Binary search dla znalezienia maksymalnej pozycji bez kolizji
                while abs(target_x - start_x) > 1:
                    mid_x = (target_x + start_x) // 2
                    mid_rect = pygame.Rect(mid_x, self.y, self.width, self.height)

                    if self.main.maze.check_collision(mid_rect):
                        target_x = mid_x
                    else:
                        start_x = mid_x

                new_x = start_x

            self.x = new_x
            self.rect.x = new_x

        # Obsługa kolizji w pionie (Y)
        if new_y != self.y:
            # Sprawdzanie czy wystąpiła kolizja dla docelowej pozycji Y
            tmp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_y):
                # Jeśli kolizja, znajdź maksymalną pozycję bez kolizji
                target_y = new_y
                start_y = self.y

                # Binary search dla znalezienia maksymalnej pozycji bez kolizji
                while abs(target_y - start_y) > 1:
                    mid_y = (target_y + start_y) // 2
                    mid_rect = pygame.Rect(self.x, mid_y, self.width, self.height)

                    if self.main.maze.check_collision(mid_rect):
                        target_y = mid_y
                    else:
                        start_y = mid_y

                new_y = start_y

            self.y = new_y
            self.rect.y = new_y

        self.draw()

    def draw(self):
        """
        Draws the player on the screen.
        """
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))
