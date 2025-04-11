"""
This module contains the Engine class
"""
import pygame


class Engine:
    """
    This class manages the main loop and game events.
    """
    def __init__(self, main):
        self.main = main

    def _check_events(self):
        """
        Checks game events.
        """
        for event in pygame.event.get():
            # Game events
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            # Menu events
            self.main.menu.handle_events(event)

            # Player movements
            if self.main.game_state.is_running():
                # Player 1
                self._player_movements(self.main.player1, event,
                                       [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
                                       )
                # Player 2
                self._player_movements(self.main.player2, event,
                                       [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
                                       )


    def _player_movements(self, player, event, keys):
        """
        Handles player movements.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == keys[0]:
                player.movements["up"] = True
            if event.key == keys[1]:
                player.movements["down"] = True
            if event.key == keys[2]:
                player.movements["left"] = True
            if event.key == keys[3]:
                player.movements["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == keys[0]:
                player.movements["up"] = False
            if event.key == keys[1]:
                player.movements["down"] = False
            if event.key == keys[2]:
                player.movements["left"] = False
            if event.key == keys[3]:
                player.movements["right"] = False


    def run(self):
        """
        Main loop of the game.
        """
        while True:
            self._check_events()
            self.main.screen.fill((0, 0, 0))
            if self.main.game_state.is_running():
                self.main.maze.draw()
                self.main.player1.update()
                self.main.player2.update()
            elif not self.main.game_state.is_game_over():
                self.main.menu.draw()
            else:
                print("Game Over")
            pygame.display.flip()
            self.main.clock.tick(60)
