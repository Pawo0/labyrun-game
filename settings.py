class Settings:
    def __init__(self):
        """ Constructor """
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720

        # Player settings
        self.player_speed = 5
        self.player_width = 15
        self.player_height = 15

        # Maze settings
        self.block_size = 35

    def get_screen_size(self):
        """ Get width and height of the screen """
        return self.screen_width, self.screen_height

    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
