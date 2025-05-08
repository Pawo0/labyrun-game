# todo add docstrings
from .menu_base import Menu


class SettingsMenu(Menu):
    def __init__(self, main):
        items = ["Player controllers", "Enable Power-ups", "Labyrun size", "Back"]
        super().__init__(main, "Settings", items)
        self.main = main
        self.selected = 0

    def _button_pressed(self):
        """
        Handle button press based on selection.
        """
        if self.selected == 0:
            pass
        elif self.selected == 1:
            pass
        elif self.selected == 2:
            self.main.game_state.open_maze_size()
        elif self.selected == 3:
            self.main.game_state.main_menu()
