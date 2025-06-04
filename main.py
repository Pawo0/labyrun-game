"""
LabyRun is a 2D maze game where two players race through a maze to reach the treasure.
Authors: Paweł Czajczyk, Jakub Psarski
"""

import pygame

from engine import Engine, EventManager, GameState
from entities import Player
from maze import Maze, MazeGenerator
from menu import (EventMenu, GameMenu, GameOverMenu, MainMenu, MazeSize,
                  SetNames, SettingsMenu, StatsMenu)
from stats import StatsManager
from util import Settings


class LabyRunGame:
    """
    Main class for the game.
    """

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode()
        self.settings = Settings(self)

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        self.maze = None
        self.generate_maze()

        self.player1 = Player(self, 1)
        self.player2 = Player(self, 2)

        self.game_state = GameState(self)
        self.menu = MainMenu(self)
        self.gameover_menu = GameOverMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.maze_size_menu = MazeSize(self)
        self.set_name_menu = SetNames(self)
        self.stats_menu = StatsMenu(self)
        self.game_menu = GameMenu(self)
        self.event_menu = EventMenu(self)

        self.engine = Engine(self)
        self.event_manager = EventManager(self)
        self.stats_manager = StatsManager(".data/player_stats.json")

    def generate_maze(self):
        """
        Generates the maze.
        """
        MazeGenerator.create_map(self.settings.maze_width, self.settings.maze_height)
        self.maze = Maze(self, ".maps/map.json")
        self.settings.calculate_initial_positions()

    def run(self):
        """
        Runs the game.
        """
        self.engine.run()


if __name__ == "__main__":
    game = LabyRunGame()
    game.run()
