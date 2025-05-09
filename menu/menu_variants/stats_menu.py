"""
This module contains the StatsMenu class.
"""

import pygame

from menu.menu_elements import Button


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
        """
        Draw the statistics screen.
        """
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
