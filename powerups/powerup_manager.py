import pygame


class PowerUpManager:
    """
    Klasa zarządzająca aktywne power-upy w grze.
    """

    def __init__(self, main):
        self.main = main
        self.active_powerups = {}  # Słownik zawierający aktywne power-upy

    def register_powerup(self, powerup_type, player_num, powerup_instance):
        """
        Rejestruje aktywny power-up dla danego gracza.
        """
        key = (powerup_type, player_num)
        self.active_powerups[key] = powerup_instance

    def handle_event(self, event):
        """
        Obsługuje zdarzenia związane z power-upami.
        """
        # Obsługa zdarzeń resetowania prędkości graczy
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

        # Obsługa zdarzeń dla przywracania rozmiaru
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

        # Obsługa zdarzeń dla odmrażania graczy
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

        # Obsługa zdarzeń dla odwróconego sterowania
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
