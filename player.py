class Player:
    def __init__(self, main, x, y, color="white"):
        self.main = main
        self.settings = main.settings
        self.screen = main.screen

        self.x = x
        self.y = y

        self.speed = self.settings.player_speed
        self.width = self.settings.player_width
        self.height = self.settings.player_height
        self.color = color
        self.movings = {"up": False, "down": False, "left": False, "right": False}

    def update(self):
        if self.movings["up"]:
            self.y = self.y - self.speed if self.y - self.speed > 0 else 0
        if self.movings["down"]:
            self.y = self.y + self.speed \
                if self.y + self.speed < self.screen.get_height() - self.height \
                else self.screen.get_height() - self.height
        if self.movings["left"]:
            self.x = self.x - self.speed if self.x - self.speed > 0 else 0
        if self.movings["right"]:
            self.x = self.x + self.speed \
                if self.x + self.speed < self.screen.get_width() - self.width \
                else self.screen.get_width() - self.width
        self.draw()

        print(self.x, self.y)

    def draw(self):
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))
