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

        self.alpha = 255  # Przezroczystość gracza
        self.frozen = False  # Stan zamrożenia
        self.old_speed = None  # Przechowuje prędkość przed zamrożeniem

        self.player_number = player_no

        self.reset()

    def update_image(self):
        """
        Aktualizuje obraz gracza po zmianie rozmiaru
        """
        # Tworzy nową powierzchnię o aktualnych wymiarach
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Rysuje gracza z odpowiednim kolorem
        self.image.fill(self.color)

        # Ustawia przezroczystość
        self.image.set_alpha(self.alpha)

        # Aktualizuje rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.push_out_of_wall()

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

    def push_out_of_wall(self):
        """
        Wypycha gracza ze ściany, jeśli się w niej znajduje, na najbliższe wolne pole.
        """
        # Sprawdzamy, czy gracz koliduje ze ścianą
        if self.main.maze.check_collision(self.rect):
            # Lista kierunków do sprawdzenia (prawo, lewo, dół, góra, prawo-dół, prawo-góra, lewo-dół, lewo-góra)
            directions = [
                (1, 0), (-1, 0), (0, 1), (0, -1),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]

            # Maksymalna odległość przeszukiwania (np. połowa bloku)
            max_distance = self.main.settings.block_size // 2

            # Szukamy najbliższego wolnego miejsca
            best_distance = float('inf')
            best_position = (self.x, self.y)

            for distance in range(1, max_distance + 1):
                for dx, dy in directions:
                    new_x = self.x + dx * distance
                    new_y = self.y + dy * distance

                    # Sprawdzamy, czy nowa pozycja mieści się na ekranie
                    if (new_x < 0 or new_x + self.width > self.screen.get_width() or
                            new_y < 0 or new_y + self.height > self.screen.get_height()):
                        continue

                    # Sprawdzamy, czy na nowej pozycji nie ma kolizji
                    test_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                    if not self.main.maze.check_collision(test_rect):
                        # Obliczamy odległość od oryginalnej pozycji
                        dist = abs(new_x - self.x) + abs(new_y - self.y)
                        if dist < best_distance:
                            best_distance = dist
                            best_position = (new_x, new_y)

            # Ustawiamy gracza na znalezionej pozycji
            if best_distance < float('inf'):
                self.x, self.y = best_position
                self.rect.x, self.rect.y = best_position
                self.update_image()

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
            tmp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_x):
                # Jeśli wykryto kolizję, znajdź najbliższą dozwoloną pozycję
                step = 1 if new_x > self.x else -1
                test_x = self.x
                while test_x != new_x:
                    test_x += step
                    test_rect = pygame.Rect(test_x, self.y, self.width, self.height)
                    if self.main.maze.check_collision(test_rect):
                        new_x = test_x - step
                        break

        # Aktualizacja pozycji X
        self.x = new_x
        self.rect.x = new_x

        # Obsługa kolizji w pionie (Y)
        if new_y != self.y:
            tmp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            if self.main.maze.check_collision(tmp_rect_y):
                # Jeśli wykryto kolizję, znajdź najbliższą dozwoloną pozycję
                step = 1 if new_y > self.y else -1
                test_y = self.y
                while test_y != new_y:
                    test_y += step
                    test_rect = pygame.Rect(self.x, test_y, self.width, self.height)
                    if self.main.maze.check_collision(test_rect):
                        new_y = test_y - step
                        break

        # Aktualizacja pozycji Y
        self.y = new_y
        self.rect.y = new_y


        self.push_out_of_wall()

        self.draw()

    def draw(self):
        """
        Draws the player on the screen.
        """
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))
