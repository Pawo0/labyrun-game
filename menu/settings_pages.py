# TODO: add docstrings, change comments to english
"""This module contains classes for different settings pages in the game."""
import pygame

from menu.menu_elements import Button, TextInput


class SettingsOptions:
    """Klasa bazowa dla stron ustawień w grze."""

    def __init__(self, main, title, options_names, options_values):
        """Inicjalizacja strony z opcjami ustawień."""
        self.main = main
        self.screen = main.screen
        self.title = title
        self.options_names = options_names
        self.options_values = options_values
        self.current_values = [0] * len(options_names)  # Indeksy wybranych wartości

        # Ustawienia tekstu
        self.font = pygame.font.SysFont("arialblack", 40)
        self.text_color = (255, 255, 255)
        self.active_color = (255, 0, 0)
        self.background_color = (0, 0, 0)

        # Pozycja tytułu
        self.title_width, self.title_height = self.font.size(title)
        self.title_x = self.screen.get_width() // 2 - self.title_width // 2
        self.title_y = self.screen.get_height() // 2 - 225

        # Pozycje opcji
        self.option_spacing = 100
        self.option_start_y = self.screen.get_height() // 2 - 100
        self.option_x = self.screen.get_width() // 2 - 150
        self.value_x = self.screen.get_width() // 2 + 150

        # Aktualnie wybrana opcja
        self.selected = 0

        # Przycisk powrotu
        self.back_text = "Back"
        self.back_width, self.back_height = self.font.size(self.back_text)
        self.back_x = self.screen.get_width() // 2
        self.back_y = (
            self.option_start_y + (len(options_names) + 1) * self.option_spacing
        )

        self.back_button = Button(
            self.main, self.back_text, self.back_x, self.back_y, False
        )

    def handle_events(self, event):
        """Obsługa zdarzeń dla strony ustawień."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % (len(self.options_names) + 1)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % (len(self.options_names) + 1)
            elif event.key == pygame.K_LEFT and self.selected < len(self.options_names):
                # Zmiana wartości opcji w lewo
                self.current_values[self.selected] = (
                    self.current_values[self.selected] - 1
                ) % len(self.options_values[self.selected])
                self._apply_setting(self.selected)
            elif event.key == pygame.K_RIGHT and self.selected < len(
                self.options_names
            ):
                # Zmiana wartości opcji w prawo
                self.current_values[self.selected] = (
                    self.current_values[self.selected] + 1
                ) % len(self.options_values[self.selected])
                self._apply_setting(self.selected)
            elif event.key == pygame.K_RETURN:
                # Jeśli wybrano "Back"
                if self.selected == len(self.options_names):
                    self.main.game_state.open_settings()

        # TODO: obslugo eventow myszki

    def _apply_setting(self, index):
        """Aplikuje wybrane ustawienie do gry."""
        # Ta metoda powinna być nadpisana przez klasy pochodne
        raise NotImplementedError("This method should be overridden by subclasses.")

    def draw(self):
        """Rysuje stronę ustawień na ekranie."""
        # Rysuj tytuł
        title_render = self.font.render(self.title, True, self.text_color)
        self.screen.blit(title_render, (self.title_x, self.title_y))

        # Rysuj opcje i ich wartości
        for i, option_name in enumerate(self.options_names):
            option_y = self.option_start_y + i * self.option_spacing

            # Nazwa opcji
            option_color = self.active_color if i == self.selected else self.text_color
            option_render = self.font.render(option_name, True, option_color)
            self.screen.blit(option_render, (self.option_x, option_y))

            # Wartość opcji
            current_value = self.options_values[i][self.current_values[i]]
            value_render = self.font.render(str(current_value), True, option_color)
            value_width = value_render.get_width()
            self.screen.blit(value_render, (self.value_x - value_width // 2, option_y))

            # Rysuj strzałki
            if i == self.selected:
                # Lewa strzałka
                pygame.draw.polygon(
                    self.screen,
                    option_color,
                    [
                        (self.value_x - 60, option_y + 30),
                        (self.value_x - 40, option_y + 15),
                        (self.value_x - 40, option_y + 45),
                    ],
                )

                # Prawa strzałka
                pygame.draw.polygon(
                    self.screen,
                    option_color,
                    [
                        (self.value_x + 60, option_y + 30),
                        (self.value_x + 40, option_y + 15),
                        (self.value_x + 40, option_y + 45),
                    ],
                )

        # Rysuj przycisk "Back"
        if self.selected == len(self.options_names):
            self.back_button.active = True
        else:
            self.back_button.active = False
        self.back_button.draw()


class MazeSize(SettingsOptions):
    """Strona ustawień rozmiaru labiryntu."""

    def __init__(self, main):
        # Definiowanie opcji dla rozmiaru labiryntu
        options_names = ["Width", "Height"]
        options_values = [
            [7, 11, 15, 23, 31, 79],  # możliwe szerokości
            [7, 11, 15, 23, 31, 79],  # możliwe wysokości
        ]

        # Znajdź aktualne wartości w options_values
        current_width = main.settings.maze_width
        current_height = main.settings.maze_height

        super().__init__(main, "Maze Size Settings", options_names, options_values)

        # Ustaw aktualne indeksy dla wartości
        for i, value in enumerate(options_values[0]):
            if value == current_width:
                self.current_values[0] = i
                break

        for i, value in enumerate(options_values[1]):
            if value == current_height:
                self.current_values[1] = i
                break

    def _apply_setting(self, index):
        """Aplikuje wybrane ustawienie rozmiaru labiryntu."""
        width = self.options_values[0][self.current_values[0]]
        height = self.options_values[1][self.current_values[1]]
        self.main.settings.set_maze_size(width, height)


class GameSettingsPage(SettingsOptions):
    """Strona ustawień gry."""

    def __init__(self, main):
        options_names = ["Fog of War", "Power-ups"]
        options_values = [
            ["On", "Off"],  # Opcje mgły wojny
            ["On", "Off"],  # Opcje power-upów
        ]

        super().__init__(main, "Ustawienia gry", options_names, options_values)

        # Ustawiamy aktualne wartości
        self.current_values[0] = 0 if main.settings.fog_of_war_enabled else 1
        self.current_values[1] = 0 if main.settings.power_ups_enabled else 1

    def _apply_setting(self, index):
        """Aplikuje wybrane ustawienie do gry."""
        if index == 0:  # Mgła wojny
            self.main.settings.fog_of_war_enabled = self.current_values[0] == 0
        elif index == 1:  # Power-upy
            self.main.settings.power_ups_enabled = self.current_values[1] == 0


class SetNames:
    """This class handles the player name input menu."""

    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.font = pygame.font.SysFont("arialblack", 40)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2

        self.title_pos = (
            center_x - self.font.size("Set Player Names")[0] // 2,
            screen_height // 6,
        )

        vertical_center = screen_height // 2
        vertical_spacing = 120

        p1_y = vertical_center - vertical_spacing
        p2_y = vertical_center + 20

        label_x = center_x - 300
        input_x = center_x + 130

        self.p1_input = TextInput(main, "", input_x, p1_y, True)
        self.p2_input = TextInput(main, "", input_x, p2_y, False)
        self.play_button = Button(
            main, "Play!", center_x, p2_y + vertical_spacing, True
        )

        self.labels = [
            ("Set Player Names", self.title_pos),
            (
                "Player 1:",
                (
                    label_x - self.font.size("Player 1:")[0] // 2,
                    p1_y - self.font.size("Player 1:")[1] // 2,
                ),
            ),
            (
                "Player 2:",
                (
                    label_x - self.font.size("Player 2:")[0] // 2,
                    p2_y - self.font.size("Player 2:")[1] // 2,
                ),
            ),
        ]

        self.active_input = 1

    def handle_events(self, event):
        """Handle events for the name input screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.is_clicked(event.pos):
                self._play()
            if self.p1_input.handle_event(event):
                self.active_input = 1
                self.p2_input.active = False
            elif self.p2_input.handle_event(event):
                self.active_input = 2
                self.p1_input.active = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.active_input = 1
                self.p1_input.active = True
                self.p2_input.active = False
            elif event.key == pygame.K_DOWN:
                self.active_input = 2
                self.p1_input.active = False
                self.p2_input.active = True
            elif event.key == pygame.K_TAB:
                self.active_input = 2 if self.active_input == 1 else 1
                self.p1_input.active = not self.p1_input.active
                self.p2_input.active = not self.p2_input.active
            elif event.key == pygame.K_RETURN:
                self._play()
            else:
                if self.active_input == 1:
                    self.p1_input.handle_event(event)
                elif self.active_input == 2:
                    self.p2_input.handle_event(event)

    def _play(self):
        p1_name = self.p1_input.get_text() or "Player 1"
        p2_name = self.p2_input.get_text() or "Player 2"
        self.main.player1.set_name(p1_name)
        self.main.player2.set_name(p2_name)
        self.main.game_state.run_game()

    def draw(self):
        """Draw the name input menu screen."""

        for text, pos in self.labels:
            self.screen.blit(self.font.render(text, True, (255, 255, 255)), pos)

        self.p1_input.draw()
        self.p2_input.draw()
        self.play_button.draw()
