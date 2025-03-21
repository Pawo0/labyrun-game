class Player:
    def __init__(self, main, x, y):
        self.main = main
        self.screen = main.screen
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 50
        self.height = 50
        self.color = (255, 255, 255)
        self.movings = {"up": False, "down": False, "left": False, "right": False}

    def update(self):
        if self.movings["up"]:
            self.y -= self.speed
        if self.movings["down"]:
            self.y += self.speed
        if self.movings["left"]:
            self.x -= self.speed
        if self.movings["right"]:
            self.x += self.speed
        self.draw()

    def draw(self):
        self.screen.fill(self.color, (self.x, self.y, self.width, self.height))