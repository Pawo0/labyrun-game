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
            self.main.player1: [pygame.K_w, pygame.K_d, pygame.K_a, pygame.K_s],
            self.main.player2: [
                pygame.K_UP,
                pygame.K_RIGHT,
                pygame.K_LEFT,
                pygame.K_DOWN,
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
            reversed_controls = player.reversed_controls

            if event.type in key_actions:
                action_value = key_actions[event.type]
                if reversed_controls:
                    keys = keys[::-1]
                direction_map = {
                    keys[0]: "up",
                    keys[1]: "right",
                    keys[2]: "left",
                    keys[3]: "down",
                }

                if event.key in direction_map:
                    player.movements[direction_map[event.key]] = action_value

    def _handle_settings_events(self, event):
        """
        Handles events in the settings menu.
        """
        settings_state = self.main.game_state.settings_state

        match settings_state:
            case "main":
                self.main.settings_menu.handle_events(event)
            case "game":
                self.main.game_menu.handle_events(event)
            case "power_ups":
                self.main.powerup_menu.handle_events(event)
            case "events":
                self.main.event_menu.handle_events(event)
            case _:
                pass

    def _draw_running_state(self):
        self.main.maze.draw()
        self.main.player1.update()
        self.main.player2.update()

    def _draw_settings_state(self):
        """
        Draws the settings menu.
        """
        settings_state = self.main.game_state.settings_state

        match settings_state:
            case "main":
                self.main.settings_menu.draw()
            case "game":
                self.main.game_menu.draw()
            case "power_ups":
                self.main.powerup_menu.draw()
            case "events":
                self.main.event_menu.draw()
