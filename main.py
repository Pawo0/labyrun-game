"""
LabyRun is a 2D maze game where two players race through a maze to reach the treasure.
Authors: Paweł Czajczyk, Jakub Psarski
"""

import pygame

from entities import Player
from game_engine import Engine, GameState
from maze_components import Maze
from maze_generation import create_map
from menu import GameOverMenu, MainMenu, MazeSize, SettingsMenu
from util import Settings


class LabyRunGame:
    """
    Main class for the game.
    """

    def __init__(self):

        # inicjalizacja pygame
        pygame.init()

        # ustawienia okna
        self.screen = pygame.display.set_mode()
        self.settings = Settings(self)

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        # generacja mapy labiryntu
        self.maze = None
        self.generate_maze()

        # inicjalizacja graczy
        self.player1 = Player(self, 1)
        self.player2 = Player(self, 2)

        # inicjalizacja menu
        self.game_state = GameState(self)
        self.menu = MainMenu(self)
        self.gameover_menu = GameOverMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.maze_size_menu = MazeSize(self)

        # ustawienia silnika
        self.engine = Engine(self)

    def generate_maze(self):
        """
        Generates the maze.
        """
        create_map(self.settings.maze_width, self.settings.maze_height)
        self.maze = Maze(self, "maps/map.json")
        self.settings.calculate_initial_positions()

    def run(self):
        """
        Runs the game.
        """
        self.engine.run()


if __name__ == "__main__":
    game = LabyRunGame()
    game.run()
