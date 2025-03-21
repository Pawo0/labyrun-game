import json


class Maze:
    def __init__(self, main, maze_json):
        self.screen = main.screen
        self.settings = main.settings
        self.block_size = self.settings.block_size

        self.maze = []
        self.load_maze(maze_json)

        self.offset_x = (self.screen.get_width() - len(self.maze[0]) * self.block_size) // 2
        self.offset_y = (self.screen.get_height() - len(self.maze) * self.block_size) // 2

    def load_maze(self, maze_json):
        with open(maze_json, "r") as file:
            self.maze = json.load(file)["maze"]

    def draw(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.screen.fill("blue", (
                        self.offset_x + x * self.block_size, self.offset_y + y * self.block_size, self.block_size,
                        self.block_size))
                else:
                    self.screen.fill("green", (
                        self.offset_x + x * self.block_size, self.offset_y + y * self.block_size, self.block_size,
                        self.block_size))
