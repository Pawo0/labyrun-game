from menu.settings_pages.settings_options import SettingsOptions


class GameSettingsPage(SettingsOptions):
    """
    Strona ustawień gry.
    """

    def __init__(self, main):
        options_names = ["Fog of War", "Power-ups"]
        options_values = [
            ["On", "Off"],  # Opcje mgły wojny
            ["On", "Off"]   # Opcje power-upów
        ]

        super().__init__(main, "Ustawienia gry", options_names, options_values)

        # Ustawiamy aktualne wartości
        self.current_values[0] = 0 if main.settings.fog_of_war_enabled else 1
        self.current_values[1] = 0 if main.settings.power_ups_enabled else 1

    def _apply_setting(self, index):
        """
        Aplikuje wybrane ustawienie do gry.
        """
        if index == 0:  # Mgła wojny
            self.main.settings.fog_of_war_enabled = (self.current_values[0] == 0)
        elif index == 1:  # Power-upy
            self.main.settings.power_ups_enabled = (self.current_values[1] == 0)