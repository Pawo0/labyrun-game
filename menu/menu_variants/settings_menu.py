from .menu_base import Menu


class SettingsMenu(Menu):
    def __init__(self, main):
        items = ["Game Settings", "Player Controllers", "Labyrun Size", "Back"]
        super().__init__(main, "Settings", items)
        self.main = main
        self.selected = 0

    def _button_pressed(self):
        """
        Handle button press based on selection.
        """
        if self.selected == 0:
            self.main.game_state.open_game_settings()
        elif self.selected == 1:
            pass  # Kontrolery graczy
        elif self.selected == 2:
            self.main.game_state.open_maze_size()
        elif self.selected == 3:
            self.main.game_state.main_menu()