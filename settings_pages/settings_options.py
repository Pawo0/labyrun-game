import pygame
from .button import Button


class SettingsOptions:
    """
    Klasa wyświetlająca opcje ustawień z możliwością wyboru wartości dla każdej opcji.
    """

    def __init__(self, main, title, options_names, options_values):
        """
        Inicjalizacja strony z opcjami ustawień.

        :param main: Główny obiekt gry
        :param title: Tytuł strony ustawień
        :param options_names: Lista nazw ustawień
        :param options_values: Lista list możliwych wartości dla każdej opcji
        """
        self.main = main
        self.screen = main.screen
        self.title = title
        self.options_names = options_names
        self.options_values = options_values
        self.current_values = [0] * len(options_names)  # Indeksy wybranych wartości

        # Ustawienia tekstu
        self.font = pygame.font.SysFont('arialblack', 40)
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
        self.back_y = self.option_start_y + (len(options_names) + 1) * self.option_spacing


        self.back_button = Button(
            self.main,
            self.back_text,
            self.back_x,
            self.back_y,
            False
        )

    def handle_events(self, event):
        """
        Obsługa zdarzeń dla strony ustawień.
        """
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
            elif event.key == pygame.K_RIGHT and self.selected < len(self.options_names):
                # Zmiana wartości opcji w prawo
                self.current_values[self.selected] = (
                                                             self.current_values[self.selected] + 1
                                                     ) % len(self.options_values[self.selected])
                self._apply_setting(self.selected)
            elif event.key == pygame.K_RETURN:
                # Jeśli wybrano "Back"
                if self.selected == len(self.options_names):
                    self.main.game_state.open_settings()

        # todo obslugo eventow myszki

    def _apply_setting(self, index):
        """
        Aplikuje wybrane ustawienie do gry.
        """
        # Ta metoda powinna być nadpisana przez klasy pochodne
        pass

    def draw(self):
        """
        Rysuje stronę ustawień na ekranie.
        """
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
                pygame.draw.polygon(self.screen, option_color, [
                    (self.value_x - 60, option_y + 30),
                    (self.value_x - 40, option_y + 15),
                    (self.value_x - 40, option_y + 45)
                ])

                # Prawa strzałka
                pygame.draw.polygon(self.screen, option_color, [
                    (self.value_x + 60, option_y + 30),
                    (self.value_x + 40, option_y + 15),
                    (self.value_x + 40, option_y + 45)
                ])

        # Rysuj przycisk "Back"
        if self.selected == len(self.options_names):
            self.back_button.active = True
        else:
            self.back_button.active = False
        self.back_button.draw()