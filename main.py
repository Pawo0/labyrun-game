import pygame
from player import Player
from settings import Settings
from maze_components import Maze
from game_state import GameState
from menu import Menu

class LabyRunGame:
    def __init__(self):
        """ Constructor """
        pygame.init()
        self.settings = Settings()

        width, height = self.settings.get_screen_size()
        self.screen = pygame.display.set_mode((width, height))
        self.settings.set_screen_size(self.screen.get_width(), self.screen.get_height())

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        self.maze = Maze(self, "maps/map1.json")

        self.player1 = Player(self, 930, 55, "red")
        self.player2 = Player(self, 335, 655)

        self.game_state = GameState()
        self.menu = Menu(self)

    def _check_events(self):
        """ Check events """
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
        """ Player movements """
        if event.type == pygame.KEYDOWN:
            if event.key == keys[0]:
                player.movings["up"] = True
            if event.key == keys[1]:
                player.movings["down"] = True
            if event.key == keys[2]:
                player.movings["left"] = True
            if event.key == keys[3]:
                player.movings["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == keys[0]:
                player.movings["up"] = False
            if event.key == keys[1]:
                player.movings["down"] = False
            if event.key == keys[2]:
                player.movings["left"] = False
            if event.key == keys[3]:
                player.movings["right"] = False

    def run(self):
        """ Main loop """
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
