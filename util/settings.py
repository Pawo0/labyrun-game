"""
This module contains the Settings class.
"""


class Settings:
    """
    This class manages game settings:
    - Screen size
    - Maze block size
    - Player size
    - Player speed
    """

    def __init__(self, main):
        self.main = main
        # default maze size
        self.maze_width = 31
        self.maze_height = 31

        # set screen size
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()

        # players colors
        self.player1_color = (255, 0, 255)
        self.player2_color = (255, 0, 255)

        # labyrinth colors
        self.wall_color = (0, 0, 0)
        self.floor_color = (210, 210, 210)
        self.invis_wall_color = (208, 208, 208)
        self.shortcut_color = (190, 190, 190)

        # scale the maze size to fit the screen
        self.block_size = None
        self.player_width = None
        self.player_height = None
        self.player_speed = None
        self.default_speed = None
        self._calculate_block_size()

        # Oblicz bezpośrednio pozycje początkowe graczy (bez zależności od maze)
        self.player1_initial_position = self._calculate_player1_position()
        self.player2_initial_position = self._calculate_player2_position()

        # Ustawienie mgły wojny
        self.fog_of_war_enabled = False

        # Ustawienie power-upów
        self.power_up_duration = 5000

        self.power_ups_enabled = True  # Domyślnie włączone
        self.speed_boost_enabled = True
        self.slow_down_enabled = True
        self.enlarge_enabled = True
        self.teleport_enabled = False
        self.freeze_enabled = True
        self.reverse_controls_enabled = True
        self.freeze_color = (173, 216, 230)
        self.reverse_controls_color = (255, 0, 0)
        self.freeze_and_reverse_colors = (255, 105, 180)

        # Event system settings
        self.events_enabled = False
        self.event_min_interval = 3000  # Minimum time between events (3 seconds)
        self.event_max_interval = 8000  # Maximum time between events (8 seconds)

        # Individual event settings
        self.shortcutreveal_enabled = True  # Shortcut Reveal event
        self.teleportation_enabled = True  # Teleportation event
        self.fatigue_enabled = True  # Fatigue event
        self.invisiblewalls_enabled = True  # Invisible Walls event

    def _calculate_block_size(self):
        """
        Calculates the block size based on the screen size and maze dimensions.
        """
        self.block_size = min(
            self.screen_width // (self.maze_width * 2 + 3),
            self.screen_height // self.maze_height,
        )

        self.player_width = self.block_size // 2
        self.player_height = self.block_size // 2

        self.player_speed = self.block_size // 8
        self.default_speed = self.player_speed

    def _calculate_player1_position(self):
        """
        Calculates the starting position of player 1 (bottom left corner of the maze).
        """
        # Oblicz pozycję labiryntu
        maze_width = (
            self.maze_width * 2 + 3
        )  # Szerokość po uwzględnieniu odbicia i łącznika
        maze_height = self.maze_height

        offset_x = (self.screen_width - maze_width * self.block_size) // 2
        offset_y = (self.screen_height - maze_height * self.block_size) // 2

        # Lewy dolny róg (dodaj 1.5 bloku od lewej, odejmij 2 bloki od dołu)
        left_x = offset_x + 1.5 * self.block_size - self.player_width // 2
        left_y = (
            offset_y
            + maze_height * self.block_size
            - 2 * self.block_size
            + self.player_height // 2
        )

        return (left_x, left_y)

    def _calculate_player2_position(self):
        """
        Oblicza pozycję startową gracza 2 (prawy dolny róg labiryntu).
        """
        # Oblicz pozycję labiryntu
        maze_width = (
            self.maze_width * 2 + 3
        )  # Szerokość po uwzględnieniu odbicia i łącznika
        maze_height = self.maze_height

        offset_x = (self.screen_width - maze_width * self.block_size) // 2
        offset_y = (self.screen_height - maze_height * self.block_size) // 2

        # Prawy dolny róg (odejmij 2 bloki od prawej, odejmij 2 bloki od dołu)
        right_x = (
            offset_x
            + maze_width * self.block_size
            - 2 * self.block_size
            + self.player_width // 2
        )
        right_y = (
            offset_y
            + maze_height * self.block_size
            - 2 * self.block_size
            + self.player_height // 2
        )

        return (right_x, right_y)

    def calculate_initial_positions(self):
        """
        Aktualizuje pozycje początkowe graczy (np. po zmianie rozmiaru labiryntu).
        """
        self.player1_initial_position = self._calculate_player1_position()
        self.player2_initial_position = self._calculate_player2_position()

    def set_maze_size(self, width, height):
        """
        Sets the maze size.
        """
        self.maze_width = width
        self.maze_height = height
        self._calculate_block_size()
        self.calculate_initial_positions()

        if hasattr(self.main, "engine"):
            self.main.engine.update_win_zone()

        if hasattr(self.main, "player1") and hasattr(self.main, "player2"):
            self.main.player1.reset()
            self.main.player2.reset()
