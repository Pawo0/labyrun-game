"""This module defines the PowerUpManager class, which manages active power-ups in the game."""

import pygame


class PowerUpManager:
    """
    This class manages active power-ups in the game.
    """

    def __init__(self, main):
        self.main = main
        self.active_powerups = {}  # Dictionary containing active power-ups

    def register_powerup(self, powerup_type, player_num, powerup_instance):
        """
        Register an active power-up for a given player.
        """
        key = (powerup_type, player_num)
        self.active_powerups[key] = powerup_instance

    def handle_event(self, event):
        """
        Handle events related to power-ups.
        """
        # Handle events for resetting player speed
        if event.type == pygame.USEREVENT + 1:  # player 1
            key = ("speed", 1)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(1)
                del self.active_powerups[key]
        elif event.type == pygame.USEREVENT + 2:  # player 2
            key = ("speed", 2)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(2)
                del self.active_powerups[key]

        # Handle events for restoring size
        elif event.type == pygame.USEREVENT + 21:  # player 1
            key = ("enlarge", 1)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(1)
                del self.active_powerups[key]
        elif event.type == pygame.USEREVENT + 22:  # player 2
            key = ("enlarge", 2)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(2)
                del self.active_powerups[key]

        # Handle events for unfreezing players
        elif event.type == pygame.USEREVENT + 31:  # player 1
            key = ("freeze", 1)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(1)
                del self.active_powerups[key]
        elif event.type == pygame.USEREVENT + 32:  # player 2
            key = ("freeze", 2)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(2)
                del self.active_powerups[key]

        # Handle events for reversing controls
        elif event.type == pygame.USEREVENT + 41:  # player 1
            key = ("reverse_controls", 1)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(1)
                del self.active_powerups[key]
        elif event.type == pygame.USEREVENT + 42:  # player 2
            key = ("reverse_controls", 2)
            if key in self.active_powerups:
                self.active_powerups[key].remove_effect(2)
                del self.active_powerups[key]
