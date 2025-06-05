"""This module contains classes for different types of menus."""

import sys

import pygame

from menu.menu_elements import Button


class Menu:
    """Base class for game menus."""

    def __init__(self, main, title, items):
        self.main = main
        self.screen = main.screen
        self.items = items
        # zaczynamy stawiac przyciski statyczne 225 pikseli od srodka ekranu
        self.ys = [self.screen.get_height() // 2 - 225]

        button_start_y = (
            self.screen.get_height() // 2 - 100
        )  # kazdy przycisk 100 pikseli nizej
        button_spacing = 100
        for i in range(len(items)):
            self.ys.append(button_start_y + i * button_spacing)

        self.x = self.screen.get_width() // 2
        self.selected = 0
        self.buttons = [
            Button(self.main, item, self.x, self.ys[i + 1], i == 0)
            for i, item in enumerate(self.items)
        ]
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont("arialblack", 40)
        self.title = title
        self.text_width, self.text_height = self.font.size(title)
        self.text_color = (255, 255, 255)

    def _button_pressed(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def handle_events(self, event):
        """Handles events for the menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                self._button_pressed()

        elif event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button.is_hovered(event.pos):
                    self.selected = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    self._button_pressed()
                    break

    def draw(self):
        """Draws the menu on the screen."""
        text_render = self.font.render(self.title, True, self.text_color)
        self.screen.blit(text_render, (self.x - self.text_width // 2, self.ys[0]))

        for i, button in enumerate(self.buttons):
            button.active = i == self.selected
            button.draw()


class MainMenu(Menu):
    """This class handles the main menu of the game."""

    def __init__(self, main):
        items = ["Start", "Leaderboard", "Settings", "Quit"]
        super().__init__(main, "LabyRun", items)

    def _button_pressed(self):
        """Handle button press based on selection."""
        match self.selected:
            case 0:
                self.main.game_state.set_names()
            case 1:
                self.main.game_state.open_stats_menu()
            case 2:
                self.main.game_state.open_settings_menu()
            case 3:
                pygame.quit()
                sys.exit()


class SettingsMenu(Menu):
    """This class handles the settings menu of the game."""

    def __init__(self, main):
        items = ["Game Settings", "Powerup Settings", "Event Settings", "Back"]
        super().__init__(main, "Settings", items)
        self.main = main
        self.selected = 0

    def _button_pressed(self):
        """Handle button press based on selection."""
        if self.selected == 0:
            self.main.game_state.open_game_settings()
        elif self.selected == 1:
            self.main.game_state.open_powerup_settings()
        elif self.selected == 2:
            self.main.game_state.open_event_settings()
        elif self.selected == 3:
            self.main.game_state.main_menu()


class StatsMenu:
    """This class handles the statistics menu."""

    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.font = pygame.font.SysFont("arialblack", 40)
        self.small_font = pygame.font.SysFont("arialblack", 24)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.title = "Leaderboard"
        self.title_width, self.title_height = self.font.size(self.title)
        self.title_x = screen_width // 2 - self.title_width // 2
        self.title_y = screen_height // 6

        self.back_button = Button(
            main, "Back", screen_width // 2, screen_height - 100, True
        )

    def handle_events(self, event):
        """Handle events for the statistics screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos):
                self.main.game_state.main_menu()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.main.game_state.main_menu()

    def draw(self):
        """Draw the statistics screen."""
        title_render = self.font.render(self.title, True, self.text_color)
        self.screen.blit(title_render, (self.title_x, self.title_y))

        leaderboard = self.main.stats_manager.get_leaderboard()

        headers = ["Player", "Wins", "Games", "Win Rate", "Avg Time"]
        col_widths = [200, 100, 100, 150, 150]
        total_table_width = sum(col_widths)

        table_start_x = (self.screen.get_width() - total_table_width) // 2

        start_y = self.title_y + self.title_height + 50
        row_height = 40

        for i, header in enumerate(headers):
            x = table_start_x + sum(col_widths[:i])
            header_surface = self.small_font.render(header, True, self.text_color)
            # Center text in its column
            x_centered = x + (col_widths[i] - header_surface.get_width()) // 2
            self.screen.blit(header_surface, (x_centered, start_y))

        for i, player in enumerate(leaderboard[:10]):  # Show top 10
            y = start_y + (i + 1) * row_height

            row_data = [
                player["player_name"],
                str(player["wins"]),
                str(player["total_games"]),
                f"{player['win_rate']:.1%}" if player["total_games"] > 0 else "0.0%",
                f"{player['avg_time']:.1f}s" if player["avg_time"] else "N/A",
            ]

            for j, data in enumerate(row_data):
                x = table_start_x + sum(col_widths[:j])
                data_surface = self.small_font.render(data, True, self.text_color)

                if j == 0:
                    x_pos = x + 10
                else:
                    x_pos = x + (col_widths[j] - data_surface.get_width()) // 2

                self.screen.blit(data_surface, (x_pos, y))

        self.back_button.draw()


class GameOverMenu(Menu):
    """This class handles the game over menu."""

    def __init__(self, main):
        items = ["Play Again", "Main Menu", "Quit"]
        super().__init__(main, "Game Over", items)  # placeholder for title

    def _button_pressed(self):
        """Handle button press based on selection."""
        if self.selected == 0:
            self.main.game_state.run_game()
        elif self.selected == 1:
            self.main.game_state.main_menu()
        elif self.selected == 2:
            pygame.quit()
            sys.exit()

    def draw(self):
        """Draws the menu on the screen, with dynamically updated winner text."""
        self.title = f"{self.main.game_state.winner.player_name} Wins!"
        self.text_width, self.text_height = self.font.size(self.title)
        super().draw()
