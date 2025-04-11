"""
LabyRun is a 2D maze game where two players race through a maze to reach the treasure.
Authors: Paweł Czajczyk, Jakub Psarski
"""
import pygame

from maze_components import Maze
from maze_generation import create_map
from menu import Menu, GameOverMenu
from entities import Player
from util import Settings
from game_engine import Engine, GameState


class LabyRunGame:
    """
    Main class for the game.
    """
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode()
        self.settings = Settings(self.screen.get_width(), self.screen.get_height())

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        create_map(self.settings.maze_width, self.settings.maze_height)

        self.maze = Maze(self, "maps/map.json")

        self.player1_initial_position, self.player2_initial_position = \
            self._calculate_initial_positions()

        self.player1 = Player(self, self.player1_initial_position, "red")
        self.player2 = Player(self, self.player2_initial_position)

        self.game_state = GameState(self)
        self.menu = Menu(self)
        self.gameover_menu = GameOverMenu(self)
        self.engine = Engine(self)

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

        return (left_x, left_y), (right_x, right_y)

    def run(self):
        """
        Run the game.
        """
        self.engine.run()


if __name__ == "__main__":
    game = LabyRunGame()
    game.run()
