class GameState:
    def __init__(self):
        self.running = False

    def game_over(self):
        self.running = False

    def run_game(self):
        self.running = True

    def is_running(self):
        return self.running
