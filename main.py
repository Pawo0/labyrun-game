"""
LabyRun is a 2D maze game where two players race through a maze to reach the treasure.
Authors: Paweł Czajczyk, Jakub Psarski
"""
import pygame

from maze_components import Maze
from maze_generation import create_map
from menu import Menu
from entities import Player
from util import GameState, Settings


class LabyRunGame:
    """
    Main class for the game.
    """
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode()
        self.settings.set_screen_size(self.screen.get_width(), self.screen.get_height())
        self.settings.calculate_block_size()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        create_map(self.settings.maze_width, self.settings.maze_height)

        self.maze = Maze(self, "maps/map.json")

        left_x, left_y, right_x, right_y = self._calculate_initial_positions()

        self.player1 = Player(self, right_x, right_y, "red")
        self.player2 = Player(self, left_x, left_y)

        self.game_state = GameState()
        self.menu = Menu(self)

    def _calculate_initial_positions(self):
        """
        Calculates the initial positions of the players.
        """
        left = self.maze.get_lower_left()
        right = self.maze.get_lower_right()
        block_size = self.settings.block_size
        player_size = self.settings.player_width

        left_x = left[0] + 1.5 * block_size - player_size // 2
        left_y = left[1] - 2 * block_size + player_size // 2
        right_x = right[0] - 2 * block_size + player_size // 2
        right_y = right[1] - 2 * block_size + player_size // 2

        return left_x, left_y, right_x, right_y

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
            self.menu.handle_events(event)

            # Player movements
            if self.game_state.is_running():
                # Player 1
                self._player_movements(self.player1, event,
                                       [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
                                       )
                # Player 2
                self._player_movements(self.player2, event,
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
            self.screen.fill((0, 0, 0))
            if self.game_state.is_running():
                self.maze.draw()
                self.player1.update()
                self.player2.update()
            else:
                self.menu.draw()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = LabyRunGame()
    game.run()
