import pygame
from player import Player


class LabyRunGame:
    def __init__(self):
        """ Constructor """
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("LabyRun")

        self.player = Player(self, 100, 100)

    def _check_events(self):
        """ Check events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Check keydown events """
        if event.key == pygame.K_ESCAPE:
            return False
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.movings["up"] = True
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.movings["down"] = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.movings["left"] = True
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.movings["right"] = True

    def _check_keyup_events(self, event):
        """ Check keyup events """
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.player.movings["up"] = False
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.movings["down"] = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.movings["left"] = False
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.movings["right"] = False

    def run(self):
        """ Main loop """
        running = True
        while running:
            self._check_events()
            self.screen.fill("black")
            self.player.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = LabyRunGame()
    game.run()
