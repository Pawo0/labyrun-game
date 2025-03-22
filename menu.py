from button import Button


class Menu:
    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.items = ["Start", "Settings", "Quit"]
        self.ys = [self.screen.get_height() // 2 - 100, self.screen.get_height() // 2,
                   self.screen.get_height() // 2 + 100]
        self.x = self.screen.get_width() // 2
        self.selected = 0

    def draw(self):
        for i, item in enumerate(self.items):
            active = False
            if i == self.selected:
                active = True
            Button(self.main, item, self.x, self.ys[i], active).draw()
