"""
This module contains the GameStateManager class for handling different game states.
"""

import pygame


class GameStateManager:
    """This class manages the different game states and their respective handlers."""

    def __init__(self, main):
        self.main = main

        self.states = {
            "running": {
                "handle_events": self._handle_running_events,
                "draw": self._draw_running_state,
            },
            "main_menu": {
                "handle_events": self.main.menu.handle_events,
                "draw": self.main.menu.draw,
            },
            "set_names": {
                "handle_events": self.main.set_name_menu.handle_events,
                "draw": self.main.set_name_menu.draw,
            },
            "stats_menu": {
                "handle_events": self.main.stats_menu.handle_events,
                "draw": self.main.stats_menu.draw,
            },
            "game_over": {
                "handle_events": self.main.gameover_menu.handle_events,
                "draw": self.main.gameover_menu.draw,
            },
            "settings_menu": {
                "handle_events": self._handle_settings_events,
                "draw": self._draw_settings_state,
            },
        }

        self.player_keys = {
            self.main.player1: [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
            self.main.player2: [
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT,
            ],
        }

    def handle_event(self, event):
        """Handle event for the current state"""
        current_state = self.main.game_state.get_current_state()
        state = self.states.get(current_state)
        if state and "handle_events" in state:
            state["handle_events"](event)

    def draw_current_state(self):
        """Draw the current state"""
        current_state = self.main.game_state.get_current_state()
        state = self.states.get(current_state)
        if state and "draw" in state:
            state["draw"]()

    def _handle_running_events(self, event):
        for player, keys in self.player_keys.items():
            key_actions = {pygame.KEYDOWN: True, pygame.KEYUP: False}

            if event.type in key_actions:
                action_value = key_actions[event.type]
                direction_map = {
                    keys[0]: "up",
                    keys[1]: "down",
                    keys[2]: "left",
                    keys[3]: "right",
                }

                if event.key in direction_map:
                    player.movements[direction_map[event.key]] = action_value

    def _handle_settings_events(self, event):
        settings_state = self.main.game_state.get_current_settings_state()
        if settings_state == "main":
            self.main.settings_menu.handle_events(event)
        elif settings_state == "maze_size":
            self.main.maze_size_menu.handle_events(event)

    def _draw_running_state(self):
        self.main.maze.draw()
        self.main.player1.update()
        self.main.player2.update()
        self.main.engine.check_win_condition()

    def _draw_settings_state(self):
        settings_state = self.main.game_state.get_current_settings_state()
        if settings_state == "main":
            self.main.settings_menu.draw()
        elif settings_state == "maze_size":
            self.main.maze_size_menu.draw()
