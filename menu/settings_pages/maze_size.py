# todo add docstrings, change comments to english
from .settings_options import SettingsOptions


class MazeSize(SettingsOptions):
    def __init__(self, main):
        # Definiowanie opcji dla rozmiaru labiryntu
        options_names = ["Width", "Height"]
        options_values = [
            [7, 11, 15, 23, 31],  # możliwe szerokości
            [7, 11, 15, 23, 31],  # możliwe wysokości
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
        """
        Aplikuje wybrane ustawienie rozmiaru labiryntu.
        """
        width = self.options_values[0][self.current_values[0]]
        height = self.options_values[1][self.current_values[1]]
        self.main.settings.set_maze_size(width, height)
